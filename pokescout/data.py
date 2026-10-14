"""Wczytywanie danych w prostym, niezależnym od źródła formacie.

Pliki CSV (albo tabele DuckDB o tych samych kolumnach):

prices.csv  : card_id, date, price            (cena karty bez oceny, NM, jedna waluta)
cards.csv   : card_id, name, set_id, rarity, release_date, set_type, reprint_announced, buzz
sealed.csv  : set_id, date, price             (np. booster box / bundle / ETB danego setu)

Dzięki temu źródło danych (pokemontcg.io, PokemonPriceTracker, PriceCharting,
własne zrzuty Cardmarketu) można zmienić bez ruszania algorytmu.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .scoring import CardMeta


def load(prices_csv: str, cards_csv: str, sealed_csv: str | None = None):
    p = pd.read_csv(prices_csv, parse_dates=["date"])
    c = pd.read_csv(cards_csv, parse_dates=["release_date"])
    prices = {cid: g.set_index("date")["price"].sort_index() for cid, g in p.groupby("card_id")}
    metas = {}
    for r in c.itertuples():
        buzz = getattr(r, "buzz", None)
        metas[r.card_id] = CardMeta(
            card_id=r.card_id, name=r.name, set_id=r.set_id, rarity=r.rarity,
            release_date=r.release_date,
            set_type=getattr(r, "set_type", "main") or "main",
            reprint_announced=bool(getattr(r, "reprint_announced", False)),
            buzz=None if pd.isna(buzz) else float(buzz),
        )
    sealed = {}
    if sealed_csv:
        s = pd.read_csv(sealed_csv, parse_dates=["date"])
        sealed = {sid: g.set_index("date")["price"].sort_index() for sid, g in s.groupby("set_id")}
    return prices, metas, sealed


# ---------------------------------------------------------------- dane z repo (codzienne zrzuty)

# Sety specjalne – inny „zegar” dna i słabszy sygnał z zamkniętych produktów
SPECIAL_SET_KEYWORDS = (
    "151", "celebration", "crown zenith", "shining fates", "hidden fates",
    "paldean fates", "prismatic evolutions", "pokémon go", "pokemon go",
    "champion's path", "shrouded fable", "detective pikachu", "dragon majesty",
    "classic collection", "black bolt", "white flare", "ascended heroes",
)
# Produkty drukowane masowo albo spoza zwykłej dystrybucji
PROMO_KEYWORDS = ("promo", "mcdonald", "trick or trade", "battle academy", "first partner",
                  "deck exclusives", "league & championship", "prize pack", "jumbo",
                  "trading card game classic", "my first battle", "world championship")


def guess_set_type(set_name: str) -> str:
    n = (set_name or "").lower()
    if any(k in n for k in PROMO_KEYWORDS):
        return "promo"
    if any(k in n for k in SPECIAL_SET_KEYWORDS):
        return "special"
    return "main"


def _primary_series(g: pd.DataFrame, price_col: str) -> pd.Series:
    """Jedna seria na produkt: wersja (sub_type) z największą liczbą notowań, reverse holo na końcu."""
    counts = g.groupby("sub_type")[price_col].count()
    order = sorted(counts.index, key=lambda t: (-counts[t], "reverse" in str(t).lower()))
    s = g[g.sub_type == order[0]].set_index("date")[price_col]
    return s[~s.index.duplicated()].sort_index()


def load_repo_history(data_dir: str | Path, price_col: str = "market"):
    """Wczytuje katalog (data/catalog) i dzienne pliki data/prices/RRRR/MM/DD.csv.gz.

    Zwraca: prices {card_id: seria}, metas {card_id: CardMeta}, sealed {set_id: seria},
    liczba dni z danymi. card_id = productId z TCGplayer (jako tekst), set_id = groupId.
    """
    data_dir = Path(data_dir)
    files = sorted((data_dir / "prices").glob("*/*/*.csv.gz"))
    frames = []
    for f in files:
        y, m, d = f.parts[-3], f.parts[-2], f.name[:2]
        df = pd.read_csv(f, usecols=["product_id", "sub_type", price_col])
        df["date"] = pd.Timestamp(f"{y}-{m}-{d}")
        frames.append(df)
    if not frames:
        return {}, {}, {}, 0
    p = pd.concat(frames).dropna(subset=[price_col])
    p = p[p[price_col] > 0]
    series = {pid: _primary_series(g, price_col) for pid, g in p.groupby("product_id")}

    cat = data_dir / "catalog"
    c = pd.read_csv(cat / "cards.csv", parse_dates=["release_date"])
    prices, metas = {}, {}
    for r in c.itertuples():
        if r.product_id not in series:
            continue
        cid = str(r.product_id)
        prices[cid] = series[r.product_id]
        buzz = getattr(r, "buzz", None)
        reprint = getattr(r, "reprint_announced", None)
        metas[cid] = CardMeta(
            card_id=cid, name=r.name, set_id=str(r.group_id), rarity=str(r.rarity),
            release_date=r.release_date,
            set_type=guess_set_type(r.set_name),  # zawsze wg aktualnych reguł, nie z dnia zapisu katalogu
            reprint_announced=bool(reprint) if reprint is not None and not pd.isna(reprint) else False,
            buzz=None if buzz is None or pd.isna(buzz) else float(buzz),
            set_name=r.set_name,
        )

    sealed = {}
    sp = cat / "sealed.csv"
    if sp.exists():
        s = pd.read_csv(sp)
        rank = {"booster_box": 0, "booster_bundle": 1, "etb": 2, "booster_pack": 3}
        s = s[s.product_id.isin(series.keys())].copy()
        s["rank"] = s.kind.map(rank)
        s["n"] = s.product_id.map(lambda x: len(series[x]))
        for gid, g in s.sort_values(["rank", "n"], ascending=[True, False]).groupby("group_id"):
            sealed[str(gid)] = series[g.product_id.iloc[0]]
    return prices, metas, sealed, len(files)
