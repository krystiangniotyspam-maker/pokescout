"""Codzienny zrzut cen „łakomych” kart z pokemontcg.io.

Zapisuje:
  data/cards.csv                        – katalog kart (nadpisywany codziennie)
  data/prices/RRRR/MM/DD.csv            – ceny z danego dnia (jeden mały plik na dzień)

Ceny:
  tcg_market_usd – TCGplayer, cena rynkowa (aktualizowana codziennie)
  cm_trend_eur   – Cardmarket trend z pokemontcg.io (UWAGA: w 10.2026 nieaktualizowane od 11.2025,
                   zapisujemy razem z datą aktualizacji, żeby było widać, kiedy znów ruszy)

Klucz API opcjonalny (zmienna POKEMONTCG_API_KEY) – bez klucza limit to ok. 1000 zapytań/dzień,
a skrypt potrzebuje ok. 100–150.
"""
from __future__ import annotations

import datetime as dt
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

API = "https://api.pokemontcg.io/v2"
MIN_RELEASE = "2019/01/01"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

KEEP_RARITIES = {
    "illustration rare", "special illustration rare", "hyper rare", "ultra rare",
    "rare secret", "rare rainbow", "rare ultra", "trainer gallery rare holo",
    "shiny rare", "shiny ultra rare", "rare shiny gx", "rare shining", "double rare",
}

session = requests.Session()
if os.getenv("POKEMONTCG_API_KEY"):
    session.headers["X-Api-Key"] = os.environ["POKEMONTCG_API_KEY"]


def get(path: str, params: dict | None = None, tries: int = 5) -> dict:
    for i in range(tries):
        r = session.get(f"{API}/{path}", params=params, timeout=60)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(5 * (i + 1))
            continue
        r.raise_for_status()
    raise RuntimeError(f"Nie udało się pobrać {path} {params}")


def is_chase(card: dict, printed_total: int) -> bool:
    rarity = (card.get("rarity") or "").lower()
    if rarity in KEEP_RARITIES:
        return True
    num = card.get("number", "")
    return num.isdigit() and printed_total and int(num) > printed_total


def tcg_market(card: dict) -> tuple[float | None, float | None]:
    prices = (card.get("tcgplayer") or {}).get("prices") or {}
    for variant in ("holofoil", "normal", "reverseHolofoil", "1stEditionHolofoil"):
        if variant in prices:
            p = prices[variant]
            return p.get("market"), p.get("low")
    if prices:
        p = next(iter(prices.values()))
        return p.get("market"), p.get("low")
    return None, None


def main() -> int:
    today = dt.date.today()
    sets = get("sets", {"pageSize": 250, "orderBy": "releaseDate"})["data"]
    sets = [s for s in sets if s.get("releaseDate", "") >= MIN_RELEASE]
    print(f"Sety od {MIN_RELEASE}: {len(sets)}")

    cards_rows, price_rows = [], []
    for s in sets:
        page = 1
        while True:
            res = get("cards", {"q": f"set.id:{s['id']}", "pageSize": 250, "page": page,
                                "select": "id,name,number,rarity,artist,tcgplayer,cardmarket"})
            for c in res["data"]:
                if not is_chase(c, s.get("printedTotal") or 0):
                    continue
                market, low = tcg_market(c)
                cm = c.get("cardmarket") or {}
                cmp = cm.get("prices") or {}
                cards_rows.append(dict(
                    card_id=c["id"], name=c["name"], number=c.get("number"),
                    set_id=s["id"], set_name=s["name"], series=s.get("series"),
                    rarity=c.get("rarity"), artist=c.get("artist"),
                    release_date=s["releaseDate"].replace("/", "-"),
                ))
                price_rows.append(dict(
                    card_id=c["id"],
                    tcg_market_usd=market, tcg_low_usd=low,
                    cm_trend_eur=cmp.get("trendPrice"), cm_avg30_eur=cmp.get("avg30"),
                    cm_updated=cm.get("updatedAt"),
                ))
            if page * 250 >= res.get("totalCount", 0):
                break
            page += 1
        time.sleep(0.3)

    if not price_rows:
        print("Brak danych – coś poszło nie tak", file=sys.stderr)
        return 1

    DATA.mkdir(exist_ok=True)
    cards = pd.DataFrame(cards_rows).drop_duplicates("card_id")
    old = DATA / "cards.csv"
    if old.exists():  # zachowaj ręczne kolumny (set_type, reprint_announced, buzz)
        prev = pd.read_csv(old)
        manual = [c for c in ("card_id", "set_type", "reprint_announced", "buzz") if c in prev.columns]
        if len(manual) > 1:
            cards = cards.merge(prev[manual], on="card_id", how="left")
    cards.to_csv(old, index=False)

    out = DATA / "prices" / f"{today:%Y}" / f"{today:%m}" / f"{today:%d}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(price_rows).drop_duplicates("card_id").to_csv(out, index=False)
    print(f"Zapisano {len(price_rows)} kart → {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # komunikat jako adnotacja GitHub Actions – widać go bez otwierania logu
        import traceback
        tb = traceback.format_exc().strip().splitlines()
        print(f"::error title=collect_prices::{type(e).__name__}: {e} | {' / '.join(tb[-4:])}")
        raise
