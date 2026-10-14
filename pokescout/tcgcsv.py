"""Dane z tcgcsv.com – codzienne kopie cen TCGplayer (bez klucza API).

Endpointy (Pokémon = kategoria 3):
  https://tcgcsv.com/tcgplayer/3/groups                 – sety (groupId, name, publishedOn, isSupplemental)
  https://tcgcsv.com/tcgplayer/3/{groupId}/products     – produkty: karty (extendedData: Number, Rarity) i sealed
  https://tcgcsv.com/tcgplayer/3/{groupId}/prices       – ceny: productId, subTypeName, market/low/mid
  https://tcgcsv.com/archive/tcgplayer/prices-RRRR-MM-DD.ppmd.7z – archiwum cen z danego dnia (od 2024-02-08)

Zasady serwisu: rozpoznawalny User-Agent i krótka przerwa między zapytaniami.
"""
from __future__ import annotations

import re
import time

import requests

BASE = "https://tcgcsv.com"
CATEGORY = 3
ARCHIVE_START = "2024-02-08"
USER_AGENT = "PokeScout/0.2 (+https://github.com/krystiangniotyspam-maker/pokescout)"

# Rzadkości, które śledzimy zawsze (pozostałe karty tylko, gdy są drogie – patrz is_tracked_card)
CHASE_RARITIES = {
    "special illustration rare", "illustration rare", "hyper rare", "mega hyper rare",
    "ultra rare", "secret rare", "double rare", "shiny rare", "shiny ultra rare",
    "shiny holo rare", "radiant rare", "amazing rare", "prism rare", "classic collection",
    "black white rare", "ace spec rare", "rare shining", "trainer gallery rare holo",
}
MIN_PRICE_OTHER = 10.0  # USD – tańsze karty innych rzadkości pomijamy

SEALED_KINDS = [  # kolejność = priorytet przy wyborze „indeksu sealed” setu
    ("booster_box", re.compile(r"booster box(?! case)", re.I)),
    ("booster_bundle", re.compile(r"booster bundle(?! case)", re.I)),
    ("etb", re.compile(r"elite trainer box(?! case)", re.I)),
    ("booster_pack", re.compile(r"booster pack(?! art bundle)", re.I)),
]
SEALED_EXCLUDE = re.compile(r"case|display|code card|bundle of|set of|\[set|lot\b", re.I)


class Client:
    def __init__(self, pause: float = 0.25, timeout: float = 30, tries: int = 5):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = USER_AGENT
        self.pause, self.timeout, self.tries = pause, timeout, tries

    def get(self, url: str, stream: bool = False) -> requests.Response:
        last = ""
        for i in range(self.tries):
            try:
                r = self.s.get(url, timeout=self.timeout, stream=stream)
            except requests.RequestException as e:
                last = type(e).__name__
                time.sleep(3 * (i + 1))
                continue
            if r.status_code == 200:
                time.sleep(self.pause)
                return r
            last = f"HTTP {r.status_code}"
            if r.status_code == 404:
                break
            time.sleep(3 * (i + 1))
        raise RuntimeError(f"Nie udało się pobrać {url} ({last})")

    def results(self, path: str) -> list[dict]:
        return self.get(f"{BASE}/tcgplayer/{path}").json().get("results", [])

    def groups(self) -> list[dict]:
        return self.results(f"{CATEGORY}/groups")

    def products(self, group_id: int) -> list[dict]:
        return self.results(f"{CATEGORY}/{group_id}/products")

    def prices(self, group_id: int) -> list[dict]:
        return self.results(f"{CATEGORY}/{group_id}/prices")


def ext(product: dict) -> dict:
    return {e.get("name"): e.get("value") for e in product.get("extendedData") or []}


def sealed_kind(name: str) -> str | None:
    if SEALED_EXCLUDE.search(name or ""):
        return None
    for kind, rx in SEALED_KINDS:
        if rx.search(name or ""):
            return kind
    return None


def is_tracked_card(rarity: str, max_market: float | None) -> bool:
    r = (rarity or "").strip().lower()
    if r in CHASE_RARITIES:
        return True
    return max_market is not None and max_market >= MIN_PRICE_OTHER
