"""Codzienny zrzut cen z tcgcsv.com (kopie cen TCGplayer, bez klucza API).

Zapisuje:
  data/catalog/sets.csv                 – sety od 2019 r. (group_id, nazwa, premiera, typ setu)
  data/catalog/cards.csv                – śledzone karty (rzadkie albo drogie); ręczne kolumny
                                          reprint_announced i buzz są zachowywane
  data/catalog/sealed.csv               – zamknięte produkty (booster box, bundle, ETB, paczka)
  data/prices/RRRR/MM/DD.csv.gz         – ceny z danego dnia: product_id, sub_type, market, low, mid

Cały przebieg to ok. 2 zapytania na set (ok. 300–400 zapytań, kilka minut).
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pokescout.data import guess_set_type  # noqa: E402
from pokescout.tcgcsv import Client, ext, is_tracked_card, sealed_kind  # noqa: E402

MIN_RELEASE = "2019-01-01"
DATA = ROOT / "data"
CATALOG = DATA / "catalog"
MANUAL_COLS = ("reprint_announced", "buzz")


def price_rows(prices: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(prices)
    if df.empty:
        return pd.DataFrame(columns=["product_id", "sub_type", "market", "low", "mid"])
    df = df.rename(columns={"productId": "product_id", "subTypeName": "sub_type",
                            "marketPrice": "market", "lowPrice": "low", "midPrice": "mid"})
    return df[["product_id", "sub_type", "market", "low", "mid"]]


def collect(client: Client, today: dt.date) -> int:
    groups = [g for g in client.groups() if (g.get("publishedOn") or "")[:10] >= MIN_RELEASE]
    print(f"Sety od {MIN_RELEASE}: {len(groups)}")

    sets, cards, sealed, prices, failed = [], [], [], [], []
    for g in groups:
        gid, gname = g["groupId"], g["name"]
        release = g["publishedOn"][:10]
        try:
            products = client.products(gid)
            pr = price_rows(client.prices(gid))
        except RuntimeError as e:
            failed.append(gname)
            print(f"::warning title=collect_prices::pominięto set {gname}: {e}")
            continue
        set_type = guess_set_type(gname)
        sets.append(dict(group_id=gid, set_name=gname, abbreviation=g.get("abbreviation"),
                         release_date=release, set_type=set_type,
                         supplemental=bool(g.get("isSupplemental"))))
        max_market = pr.groupby("product_id")["market"].max()
        keep: set[int] = set()
        for p in products:
            pid, e = p["productId"], ext(p)
            if "Number" in e or "Rarity" in e:
                if is_tracked_card(e.get("Rarity"), max_market.get(pid)):
                    keep.add(pid)
                    cards.append(dict(product_id=pid, name=p.get("name"), number=e.get("Number"),
                                      rarity=e.get("Rarity"), group_id=gid, set_name=gname,
                                      release_date=release, set_type=set_type))
            else:
                kind = sealed_kind(p.get("name"))
                if kind:
                    keep.add(pid)
                    sealed.append(dict(product_id=pid, name=p.get("name"), kind=kind,
                                       group_id=gid, set_name=gname, release_date=release))
        prices.append(pr[pr.product_id.isin(keep)])

    print(f"Sety pobrane: {len(sets)}/{len(groups)}; pominięte: {failed}")
    if not sets or len(failed) > len(groups) / 4:
        print("::error title=collect_prices::Za dużo nieudanych setów")
        return 1
    save_catalog(pd.DataFrame(sets), pd.DataFrame(cards), pd.DataFrame(sealed))
    out = save_prices(today, pd.concat(prices))
    print(f"Zapisano {len(cards)} kart i {len(sealed)} produktów sealed → {out}")
    return 0


def save_catalog(sets: pd.DataFrame, cards: pd.DataFrame, sealed: pd.DataFrame) -> None:
    CATALOG.mkdir(parents=True, exist_ok=True)
    cards = cards.drop_duplicates("product_id")
    old = CATALOG / "cards.csv"
    if old.exists():  # zachowaj ręczne kolumny
        prev = pd.read_csv(old)
        manual = [c for c in MANUAL_COLS if c in prev.columns]
        if manual:
            cards = cards.merge(prev[["product_id", *manual]], on="product_id", how="left")
    for c in MANUAL_COLS:
        if c not in cards.columns:
            cards[c] = pd.NA
    sets.to_csv(CATALOG / "sets.csv", index=False)
    cards.to_csv(old, index=False)
    sealed.drop_duplicates("product_id").to_csv(CATALOG / "sealed.csv", index=False)


def save_prices(day: dt.date, prices: pd.DataFrame) -> Path:
    out = DATA / "prices" / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}.csv.gz"
    out.parent.mkdir(parents=True, exist_ok=True)
    prices = prices.dropna(subset=["market", "low", "mid"], how="all")
    prices.sort_values(["product_id", "sub_type"]).to_csv(out, index=False, float_format="%.2f")
    return out


if __name__ == "__main__":
    try:
        sys.exit(collect(Client(), dt.date.today()))
    except Exception as e:  # komunikat jako adnotacja GitHub Actions – widać go bez otwierania logu
        import traceback
        tb = traceback.format_exc().strip().splitlines()
        print(f"::error title=collect_prices::{type(e).__name__}: {e} | {' / '.join(tb[-4:])}")
        raise
