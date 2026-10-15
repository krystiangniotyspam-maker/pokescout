"""Ceny z Cardmarket (rynek europejski, EUR) – publiczne pliki eksportu, bez klucza API.

Raz w tygodniu zapisuje:
  data/cardmarket/products.csv.gz              – katalog Pokémonów (id, nazwa, kategoria, dodatek), nadpisywany
  data/cardmarket/prices/RRRR-MM-DD.csv.gz     – przewodnik cen: avg, low, trend, avg7, avg30 (+ wersje holo)
Zapisujemy tylko produkty z ceną trend od 1 EUR, żeby repo nie puchło. Z tych zrzutów powstaje
historia cen w EUR (dziś Cardmarket nie udostępnia historii za darmo).

    python scripts/collect_cardmarket.py
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "cardmarket"
BASE = "https://downloads.s3.cardmarket.com/productCatalog"
GAME = 6  # Pokémon
USER_AGENT = "PokeScout/0.2 (+https://github.com/krystiangniotyspam-maker/pokescout)"
PRICE_COLS = ["avg", "low", "trend", "avg7", "avg30", "trend-holo", "avg30-holo"]
MIN_TREND = 1.0


def get_json(session: requests.Session, path: str) -> dict:
    r = session.get(f"{BASE}/{path}", timeout=180)
    r.raise_for_status()
    return r.json()


def main() -> int:
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    guide = get_json(s, f"priceGuide/price_guide_{GAME}.json")
    prods = pd.concat([pd.DataFrame(get_json(s, f"productList/products_{kind}_{GAME}.json")["products"])
                       for kind in ("singles", "nonsingles")], ignore_index=True)
    day = pd.Timestamp(guide.get("createdAt", dt.date.today().isoformat())).date()

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prices").mkdir(exist_ok=True)
    prods = prods[["idProduct", "name", "idCategory", "categoryName", "idExpansion", "idMetacard"]]
    prods.to_csv(OUT / "products.csv.gz", index=False)

    pg = pd.DataFrame(guide["priceGuides"])
    pg = pg[["idProduct"] + [c for c in PRICE_COLS if c in pg.columns]]
    keep = (pg["trend"].fillna(0) >= MIN_TREND) | (pg.get("trend-holo", 0).fillna(0) >= MIN_TREND)
    pg = pg[keep]
    pg.to_csv(OUT / "prices" / f"{day}.csv.gz", index=False)
    print(f"Cardmarket {day}: {len(prods)} produktów w katalogu, {len(pg)} cen zapisanych")
    return 0


if __name__ == "__main__":
    sys.exit(main())
