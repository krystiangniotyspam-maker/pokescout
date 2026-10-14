"""Import historii cen tcgcsv (dzienne kopie cen TCGplayer od 2024-02-08).

Źródła (`--source`):
  github – publiczna kopia archiwum tcgcsv w wydaniach (Releases) repozytorium
           github.com/sodennis/cardarchive-tcgcsv: jedno wydanie na dzień, plik
           prices-3-pokemon.tar.xz z surowym JSON-em tcgcsv (domyślne; luki m.in. 2026-09-16 … 2026-10-04)
  tcgcsv – oryginalne archiwum tcgcsv.com; od 10.2026 tymczasowo wyłączone przez autora (403)

Gdy danego dnia brakuje, bierze najbliższy z kolejnych 3 dni.

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
import tarfile
import tempfile
from pathlib import Path

import pandas as pd
import py7zr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pokescout.tcgcsv import ARCHIVE_START, BASE, CATEGORY, Client  # noqa: E402
from scripts.collect_prices import CATALOG, DATA, price_rows, save_prices  # noqa: E402


GITHUB_MIRROR = "https://github.com/sodennis/cardarchive-tcgcsv/releases/download"


def archive_url(day: dt.date, source: str = "tcgcsv") -> str:
    if source == "github":
        return f"{GITHUB_MIRROR}/{day:%Y-%m-%d}/prices-{CATEGORY}-pokemon.tar.xz"
    return f"{BASE}/archive/tcgplayer/prices-{day:%Y-%m-%d}.ppmd.7z"


def _is_prices(name: str, groups: set[int]) -> bool:
    parts = [p for p in name.split("/") if p not in ("", ".")]  # RRRR-MM-DD/3/<groupId>/prices
    return (len(parts) == 4 and parts[1] == str(CATEGORY) and parts[3] == "prices"
            and parts[2].isdigit() and int(parts[2]) in groups)


def read_tar(path: Path, groups: set[int]) -> list[dict]:
    rows = []
    with tarfile.open(path, "r:*") as t:
        for m in t:
            if m.isfile() and _is_prices(m.name, groups):
                rows += json.loads(t.extractfile(m).read()).get("results", [])
    return rows


def read_archive(path: Path, groups: set[int], workdir: Path) -> list[dict]:
    """Ceny wszystkich produktów z wybranych setów z jednego archiwum."""
    with py7zr.SevenZipFile(path) as z:
        targets = []
        for n in z.getnames():
            if _is_prices(n, groups):
                targets.append(n)
        z.extract(path=workdir, targets=targets)
    rows = []
    for t in targets:
        f = workdir / t
        if f.is_file():
            rows += json.loads(f.read_text()).get("results", [])
    return rows


def backfill_day(client: Client, day: dt.date, groups: set[int], keep: set[int],
                 source: str = "tcgcsv") -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        arc = tmp / "archive"
        with client.get(archive_url(day, source), stream=True) as r, open(arc, "wb") as fh:
            for chunk in r.iter_content(1 << 20):
                fh.write(chunk)
        rows = read_tar(arc, groups) if source == "github" else read_archive(arc, groups, tmp / "x")
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
    ap.add_argument("--source", choices=["github", "tcgcsv"], default="github")
    a = ap.parse_args()

    cards = pd.read_csv(CATALOG / "cards.csv")
    sealed = pd.read_csv(CATALOG / "sealed.csv")
    groups = set(pd.read_csv(CATALOG / "sets.csv").group_id)
    keep = set(cards.product_id) | set(sealed.product_id)

    client = Client(pause=1.0, timeout=180, tries=3)
    day, end = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    done, skipped, failed = 0, 0, []
    while day <= end:
        out = DATA / "prices" / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}.csv.gz"
        if out.exists():
            skipped += 1
        else:
            err = None
            for shift in range(4):  # brak wydania z tego dnia → najbliższy kolejny
                d = day + dt.timedelta(days=shift)
                try:
                    n = backfill_day(client, d, groups, keep, a.source)
                    done += 1
                    err = None
                    print(f"{d}: {n} cen", flush=True)
                    break
                except Exception as e:
                    err = e
                    if "HTTP 403" in str(e):
                        print(f"::error title=backfill::archiwum niedostępne (403) – przerywam")
                        return 1
                    if "HTTP 404" not in str(e):
                        break
            if err is not None:
                failed.append(str(day))
                print(f"::warning title=backfill::{day}: {type(err).__name__}: {err}")
        day += dt.timedelta(days=a.every)
    print(f"Zaimportowane dni: {done}, już były: {skipped}, nieudane: {len(failed)} {failed}")
    return 0 if done or skipped else 1


if __name__ == "__main__":
    sys.exit(main())
