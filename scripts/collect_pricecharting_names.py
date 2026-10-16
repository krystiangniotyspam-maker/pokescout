"""Nazwy kart do historii cen z PriceCharting (data/history/pricecharting_monthly.csv.gz).

Plik z historią (zbiór z Kaggle, ceny miesięczne 12.2020–10.2024) ma tylko numery produktów PriceCharting.
Ten skrypt pobiera nazwy ze stron setów: jedna strona na angielski set, posortowana od najdroższych,
więc obejmuje karty, które nas interesują. Robi przerwę między zapytaniami.

    python scripts/collect_pricecharting_names.py            # zapis do data/history/pricecharting_names.csv
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "history"
BASE = "https://www.pricecharting.com"
USER_AGENT = "PokeScout/0.2 (+https://github.com/krystiangniotyspam-maker/pokescout)"
SKIP = re.compile(r"pokemon-(japanese|chinese|korean|german|french|italian|spanish|portuguese|dutch)", re.I)
ROW = re.compile(r"<tr[^>]*\bid=\"product-(\d+)\"(.*?)</tr>", re.S)
TITLE = re.compile(r"<a[^>]+href=\"/game/[^\"]+\"[^>]*>(.*?)</a>", re.S)


def get(session: requests.Session, url: str, tries: int = 4) -> str:
    for i in range(tries):
        r = session.get(url, timeout=60)
        if r.status_code == 200:
            return r.text
        time.sleep(10 * (i + 1))
    r.raise_for_status()
    return ""


def set_slugs(page: str) -> list[str]:
    slugs = sorted(set(re.findall(r"href=\"(?:https://www\.pricecharting\.com)?/console/(pokemon-[^\"?#]+)\"", page)))
    return [s for s in slugs if not SKIP.match(s)]


def parse_set(page: str, slug: str) -> list[dict]:
    rows = []
    for pid, body in ROW.findall(page):
        m = TITLE.search(body)
        if m:
            name = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
            rows.append({"pc_id": int(pid), "name": name, "pc_set": slug})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--delay", type=float, default=3.0)
    ap.add_argument("--debug", action="store_true", help="zapisz surowy HTML pierwszej strony setu")
    a = ap.parse_args()
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    slugs = set_slugs(get(s, f"{BASE}/category/pokemon-cards"))
    print(f"Sety angielskie: {len(slugs)}", flush=True)
    rows = []
    for i, slug in enumerate(slugs):
        try:
            page = get(s, f"{BASE}/console/{slug}?sort=highest-price")
        except requests.RequestException as e:
            print(f"::warning::{slug}: {e}")
            continue
        if a.debug and i == 0:
            (OUT / "debug_set.html").write_text(page)
        got = parse_set(page, slug)
        rows += got
        print(f"{slug}: {len(got)}", flush=True)
        time.sleep(a.delay)
    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).drop_duplicates("pc_id").to_csv(OUT / "pricecharting_names.csv", index=False)
    print(f"Zapisano {len(rows)} nazw")
    return 0 if rows else 1


if __name__ == "__main__":
    sys.exit(main())
