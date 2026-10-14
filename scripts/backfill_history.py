"""Import historii cen z archiwum tcgcsv.com (dzienne kopie od 2024-02-08).

Bierze co `--every` dni jedno archiwum, wyciąga z niego ceny Pokémonów (kategoria 3)
i zapisuje tylko produkty z katalogu (data/catalog/cards.csv i sealed.csv) w tym samym
formacie co codzienny zrzut: data/prices/RRRR/MM/DD.csv.gz. Dni, które już są, pomija.

Wymaga katalogu – najpierw uruchom scripts/collect_prices.py.

    python scripts/backfill_history.py --start 2024-02-08 --end 2026-10-13 --every 7
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd
import py7zr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pokescout.tcgcsv import ARCHIVE_START, BASE, CATEGORY, Client  # noqa: E402
from scripts.collect_prices import CATALOG, DATA, price_rows, save_prices  # noqa: E402


def archive_url(day: dt.date) -> str:
    return f"{BASE}/archive/tcgplayer/prices-{day:%Y-%m-%d}.ppmd.7z"


def read_archive(path: Path, groups: set[int], workdir: Path) -> list[dict]:
    """Ceny wszystkich produktów z wybranych setów z jednego archiwum."""
    with py7zr.SevenZipFile(path) as z:
        targets = []
        for n in z.getnames():
            parts = n.split("/")  # RRRR-MM-DD/3/<groupId>/prices
            if len(parts) == 4 and parts[1] == str(CATEGORY) and parts[3] == "prices" \
                    and parts[2].isdigit() and int(parts[2]) in groups:
                targets.append(n)
        z.extract(path=workdir, targets=targets)
    rows = []
    for t in targets:
        f = workdir / t
        if f.is_file():
            rows += json.loads(f.read_text()).get("results", [])
    return rows


def backfill_day(client: Client, day: dt.date, groups: set[int], keep: set[int]) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        arc = tmp / "a.7z"
        with client.get(archive_url(day), stream=True) as r, open(arc, "wb") as fh:
            for chunk in r.iter_content(1 << 20):
                fh.write(chunk)
        rows = read_archive(arc, groups, tmp / "x")
    pr = price_rows(rows)
    pr = pr[pr.product_id.isin(keep)]
    if pr.empty:
        raise RuntimeError("archiwum bez cen śledzonych produktów")
    save_prices(day, pr)
    return len(pr)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default=ARCHIVE_START)
    ap.add_argument("--end", default=(dt.date.today() - dt.timedelta(days=1)).isoformat())
    ap.add_argument("--every", type=int, default=7, help="co ile dni brać archiwum")
    a = ap.parse_args()

    cards = pd.read_csv(CATALOG / "cards.csv")
    sealed = pd.read_csv(CATALOG / "sealed.csv")
    groups = set(pd.read_csv(CATALOG / "sets.csv").group_id)
    keep = set(cards.product_id) | set(sealed.product_id)

    client = Client(pause=1.0, timeout=180)
    day, end = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    done, skipped, failed = 0, 0, []
    while day <= end:
        out = DATA / "prices" / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}.csv.gz"
        if out.exists():
            skipped += 1
        else:
            try:
                n = backfill_day(client, day, groups, keep)
                done += 1
                print(f"{day}: {n} cen")
            except Exception as e:  # brak archiwum z danego dnia itp. – idziemy dalej
                failed.append(str(day))
                print(f"::warning title=backfill::{day}: {type(e).__name__}: {e}")
        day += dt.timedelta(days=a.every)
    print(f"Zaimportowane dni: {done}, już były: {skipped}, nieudane: {len(failed)} {failed}")
    return 0 if done or skipped else 1


if __name__ == "__main__":
    sys.exit(main())
