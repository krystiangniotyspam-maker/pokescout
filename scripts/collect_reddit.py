"""Posty z subredditów o kartach Pokémon (archiwum Arctic Shift, bez klucza API).

Zapisuje tytuły i zaangażowanie postów do data/buzz/reddit/<subreddit>/RRRR-MM.csv.gz
(id, created_utc, title, score, num_comments). Przy kolejnym uruchomieniu dociąga tylko
posty nowsze niż ostatni zapisany, więc ten sam skrypt służy do importu historii
i do codziennej aktualizacji.

    python scripts/collect_reddit.py --start 2024-01-01
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "buzz" / "reddit"
API = "https://arctic-shift.photon-reddit.com/api/posts/search"
SUBREDDITS = ("PokemonTCG", "PokeInvesting", "pkmntcgcollections", "PokemonTCGDeals")
FIELDS = "id,created_utc,title,score,num_comments"
USER_AGENT = "PokeScout/0.2 (+https://github.com/krystiangniotyspam-maker/pokescout)"


def fetch(session: requests.Session, sub: str, after: int, tries: int = 5) -> list[dict]:
    params = dict(subreddit=sub, after=after, sort="asc", limit="auto", fields=FIELDS)
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


def last_saved(sub: str) -> int | None:
    files = sorted((OUT / sub).glob("*.csv.gz"))
    if not files:
        return None
    return int(pd.read_csv(files[-1], usecols=["created_utc"]).created_utc.max())


def save(sub: str, rows: list[dict]) -> None:
    df = pd.DataFrame(rows, columns=FIELDS.split(","))
    df["month"] = pd.to_datetime(df.created_utc, unit="s").dt.strftime("%Y-%m")
    (OUT / sub).mkdir(parents=True, exist_ok=True)
    for month, g in df.groupby("month"):
        f = OUT / sub / f"{month}.csv.gz"
        if f.exists():
            g = pd.concat([pd.read_csv(f), g])
        g = g.drop(columns="month").drop_duplicates("id").sort_values("created_utc")
        g.to_csv(f, index=False)


def collect(sub: str, start: str, session: requests.Session) -> int:
    after = last_saved(sub) or int(pd.Timestamp(start).timestamp())
    total, buf = 0, []
    while True:
        rows = fetch(session, sub, after)
        rows = [r for r in rows if int(r["created_utc"]) >= after]
        if not rows:
            break
        new_after = max(int(r["created_utc"]) for r in rows)
        buf += rows
        total += len(rows)
        if new_after == after:  # wszystkie posty z tą samą sekundą – przesuń się dalej
            new_after += 1
        after = new_after
        if len(buf) >= 20000:  # zapis co jakiś czas – przerwany import nie traci postępu
            save(sub, buf)
            buf = []
            print(f"r/{sub}: {total} postów, do {dt.datetime.utcfromtimestamp(after):%Y-%m-%d}", flush=True)
        time.sleep(1.0)
    if buf:
        save(sub, buf)
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2024-01-01")
    a = ap.parse_args()
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    failed = []
    for sub in SUBREDDITS:
        try:
            n = collect(sub, a.start, s)
            print(f"r/{sub}: pobrano {n} nowych postów", flush=True)
        except RuntimeError as e:
            failed.append(sub)
            print(f"::warning title=collect_reddit::{e}")
    return 1 if len(failed) == len(SUBREDDITS) else 0


if __name__ == "__main__":
    sys.exit(main())
