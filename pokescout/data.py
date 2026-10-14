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
    "151", "celebrations", "crown zenith", "shining fates", "hidden fates",
    "paldean fates", "prismatic evolutions", "pokémon go", "pokemon go",
    "champion's path", "shrouded fable", "30th", "detective pikachu", "dragon majesty",
)


def guess_set_type(set_name: str) -> str:
    n = (set_name or "").lower()
    if "promo" in n:
        return "promo"
    if any(k in n for k in SPECIAL_SET_KEYWORDS):
        return "special"
    return "main"


def load_repo_history(data_dir: str | Path, price_col: str = "tcg_market_usd"):
    """Wczytuje data/cards.csv i wszystkie dzienne pliki data/prices/RRRR/MM/DD.csv."""
    data_dir = Path(data_dir)
    files = sorted((data_dir / "prices").glob("*/*/*.csv"))
    frames = []
    for f in files:
        y, m, d = f.parts[-3], f.parts[-2], f.stem
        df = pd.read_csv(f, usecols=["card_id", price_col])
        df["date"] = pd.Timestamp(f"{y}-{m}-{d}")
        frames.append(df)
    if not frames:
        return {}, {}, {}, 0
    p = pd.concat(frames).dropna(subset=[price_col])
    prices = {cid: g.set_index("date")[price_col].sort_index() for cid, g in p.groupby("card_id")}

    c = pd.read_csv(data_dir / "cards.csv", parse_dates=["release_date"])
    metas = {}
    for r in c.itertuples():
        if r.card_id not in prices:
            continue
        set_type = getattr(r, "set_type", None)
        buzz = getattr(r, "buzz", None)
        reprint = getattr(r, "reprint_announced", None)
        metas[r.card_id] = CardMeta(
            card_id=r.card_id, name=r.name, set_id=r.set_id, rarity=str(r.rarity),
            release_date=r.release_date,
            set_type=set_type if isinstance(set_type, str) and set_type else guess_set_type(r.set_name),
            reprint_announced=bool(reprint) if reprint is not None and not pd.isna(reprint) else False,
            buzz=None if buzz is None or pd.isna(buzz) else float(buzz),
        )
    return prices, metas, {}, len(files)
