"""Posty z subredditów o kartach Pokémon (archiwum Arctic Shift, bez klucza API).

Zapisuje tytuły i zaangażowanie postów do data/buzz/reddit/<subreddit>/RRRR-MM.csv.gz
(id, created_utc, title, score, num_comments), jeden plik na miesiąc. Kilka miesięcy pobiera
naraz (API oddaje po 100 postów). Przy kolejnym uruchomieniu pobiera tylko brakujące miesiące
oraz odświeża ostatni zapisany i bieżący, więc ten sam skrypt służy do importu historii
i do codziennej aktualizacji.

    python scripts/collect_reddit.py --start 2020-01-01

Starsze miesiące dociągają się stopniowo: krok ma limit czasu, a kolejne uruchomienia pobierają resztę.
"""
from __future__ import annotations

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "buzz" / "reddit"
API = "https://arctic-shift.photon-reddit.com/api/posts/search"
SUBREDDITS = ("PokemonTCG", "PokeInvesting", "pkmntcgcollections")
FIELDS = "id,created_utc,title,score,num_comments"
USER_AGENT = "PokeScout/0.2 (+https://github.com/krystiangniotyspam-maker/pokescout)"


def fetch(session: requests.Session, sub: str, after: int, before: int, tries: int = 5) -> list[dict]:
    params = dict(subreddit=sub, after=after, before=before, sort="asc", limit=100, fields=FIELDS)
    last = ""
    for i in range(tries):
        try:
            r = session.get(API, params=params, timeout=120)
            if r.status_code == 200:
                return r.json().get("data") or []
            last = f"HTTP {r.status_code}: {r.text[:200]}"
        except requests.RequestException as e:
            last = type(e).__name__
        time.sleep(5 * (i + 1))
    raise RuntimeError(f"Arctic Shift: r/{sub} po {after}: {last}")


def fetch_month(sub: str, month: pd.Period, session: requests.Session) -> pd.DataFrame:
    """Wszystkie posty z jednego miesiąca (API oddaje po 100, więc stronicujemy po czasie)."""
    after = int(month.start_time.timestamp())
    before = int((month.end_time + pd.Timedelta(seconds=1)).timestamp())
    rows, seen = [], set()
    while True:
        page = fetch(session, sub, after, before)
        page = [r for r in page if r["id"] not in seen]
        if not page:
            break
        rows += page
        seen.update(r["id"] for r in page)
        after = max(int(r["created_utc"]) for r in page)
    return pd.DataFrame(rows, columns=FIELDS.split(","))


def collect(subs: tuple[str, ...], start: str, workers: int = 4) -> int:
    """Pobiera brakujące miesiące; ostatni zapisany i bieżący miesiąc zawsze odświeża."""
    months = pd.period_range(start, pd.Timestamp.utcnow().tz_localize(None), freq="M")
    tasks = []
    for sub in subs:
        saved = sorted(f.name[:7] for f in (OUT / sub).glob("*.csv.gz"))
        for m in months:
            if str(m) in saved and str(m) != saved[-1] and m != months[-1]:
                continue
            tasks.append((sub, m))
    print(f"Do pobrania: {len(tasks)} miesięcy (subreddit × miesiąc)", flush=True)
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    total, failed = 0, []
    with ThreadPoolExecutor(workers) as ex:
        futures = {ex.submit(fetch_month, sub, m, session): (sub, m) for sub, m in tasks}
        for fut in as_completed(futures):
            sub, m = futures[fut]
            try:
                df = fut.result()
            except RuntimeError as e:
                failed.append(f"{sub} {m}")
                print(f"::warning title=collect_reddit::{e}")
                continue
            (OUT / sub).mkdir(parents=True, exist_ok=True)
            df.drop_duplicates("id").sort_values("created_utc").to_csv(OUT / sub / f"{m}.csv.gz", index=False)
            total += len(df)
            print(f"r/{sub} {m}: {len(df)} postów", flush=True)
    if failed:
        print(f"Nieudane: {failed}")
    return total if len(failed) < len(tasks) or not tasks else -1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2020-01-01")  # od boomu 2020–21: wskaźnik zainteresowania
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    n = collect(SUBREDDITS, a.start, a.workers)
    print(f"Zapisano {n} postów")
    return 0 if n >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
