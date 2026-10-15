"""Szum w sieci: jak często i z jakim zaangażowaniem pisze się o danym Pokémonie.

Źródło: tytuły postów z subredditów o kartach (scripts/collect_reddit.py). Dla każdego tygodnia
liczymy wzmianki każdego Pokémona (klucz jak w tiers.pokemon_key) i z tego cechy na dzień decyzji,
wyłącznie z tygodni do tej daty:

  buzz_share   – udział Pokémona we wszystkich postach z ostatnich 4 tygodni (na 1000 postów)
  buzz_growth  – log(wzmianki z 4 tyg. / średnia 4-tygodniowa z ostatnich 26 tyg.) – nagły wzrost
  buzz_eng     – log(1 + suma punktów i komentarzy pod postami o nim z 4 tyg.) – zaangażowanie
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

BUZZ_FEATURES = ["buzz_share", "buzz_growth", "buzz_eng"]

# słowa, które są „kluczami” kart, ale w tytułach znaczą zwykle coś innego
STOP = {"professor", "boss", "energy", "rare", "pokemon", "card", "cards", "basic", "ultra", "full",
        "art", "great", "ball", "master", "team", "lost", "dark", "special", "the", "box", "pack",
        "trainer", "gallery", "classic", "collection", "promo", "gold", "shiny", "mega", "black",
        "white", "iron", "roaring", "walking", "scream", "great", "town", "city", "night", "super",
        "rod", "switch", "nest", "ultra", "prime", "radiant", "pal", "pad", "judge", "arven", "nemona"}
ALIASES = {"moonbreon": "umbreon", "zard": "charizard", "zards": "charizard", "pika": "pikachu",
           "magi": "magikarp", "eeveelution": "eevee", "eeveelutions": "eevee"}
WORD = re.compile(r"[a-zà-ž0-9][a-zà-ž0-9'\-]*")


def load_reddit(data_dir: str | Path) -> pd.DataFrame:
    files = sorted((Path(data_dir) / "buzz" / "reddit").glob("*/*.csv.gz"))
    if not files:
        return pd.DataFrame(columns=["id", "created_utc", "title", "score", "num_comments"])
    df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True).drop_duplicates("id")
    df["date"] = pd.to_datetime(df.created_utc, unit="s")
    return df


def weekly_mentions(posts: pd.DataFrame, keys: set[str]) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """Tygodniowe (W-SUN) wzmianki i zaangażowanie dla każdego klucza oraz liczba wszystkich postów."""
    keys = {k for k in keys if len(k) >= 3 and k not in STOP}
    eng = np.log1p(posts["score"].clip(lower=0).fillna(0) + posts["num_comments"].clip(lower=0).fillna(0))
    rows = []
    for title, e, d in zip(posts["title"].fillna("").str.lower(), eng, posts["date"]):
        found = set()
        for w in WORD.findall(title):
            w = ALIASES.get(w, w)
            if w.endswith("'s"):
                w = w[:-2]
            if w in keys:
                found.add(w)
        rows += [(d, k, e) for k in found]
    week = lambda s: s.dt.to_period("W-SUN").dt.end_time.dt.normalize()
    total = posts.groupby(week(posts["date"])).size()
    if not rows:
        empty = pd.DataFrame(index=total.index)
        return empty, empty, total
    m = pd.DataFrame(rows, columns=["date", "key", "eng"])
    m["week"] = week(m["date"])
    counts = m.pivot_table(index="week", columns="key", values="eng", aggfunc="size", fill_value=0)
    engs = m.pivot_table(index="week", columns="key", values="eng", aggfunc="sum", fill_value=0.0)
    idx = total.index.union(counts.index)
    return counts.reindex(idx, fill_value=0), engs.reindex(idx, fill_value=0.0), total.reindex(idx, fill_value=0)


def buzz_features(posts: pd.DataFrame, keys: set[str]) -> pd.DataFrame:
    """Tabela (date, poke) → cechy szumu; `date` to niedziela kończąca tydzień."""
    counts, engs, total = weekly_mentions(posts, keys)
    if counts.empty or not len(counts.columns):
        return pd.DataFrame(columns=["date", "poke", *BUZZ_FEATURES])
    c4 = counts.rolling(4, min_periods=1).sum()
    c26 = counts.rolling(26, min_periods=8).sum()
    t4 = total.rolling(4, min_periods=1).sum()
    share = c4.div(t4.replace(0, np.nan), axis=0) * 1000
    growth = np.log((c4 + 1) / (c26 * 4 / 26 + 1))
    eng = np.log1p(engs.rolling(4, min_periods=1).sum())
    out = pd.concat({"buzz_share": share.stack(), "buzz_growth": growth.stack(), "buzz_eng": eng.stack()}, axis=1)
    out.index.names = ["date", "poke"]
    return out.reset_index()


SET_ALIASES = {"scarlet & violet 151": [r"(?<![\d$.])151(?!\d)"], "prismatic evolutions": ["prismatic"],
               "evolving skies": ["evolving skies", r"\bevs\b"]}


def reprint_mentions(posts: pd.DataFrame, sets: pd.DataFrame, weeks: int = 8) -> pd.DataFrame:
    """Posty o dodrukach danego setu (tytuł z „reprint” i nazwą setu) z ostatnich `weeks` tygodni.

    Zwraca (date, set_id, reprint_posts); `date` to niedziela kończąca tydzień. Na historii karty z setów,
    o których dodrukach pisano 3+ razy w 8 tygodni, wypadały gorzej od rynku (6 mies. ok. −14%), ale model
    już je omijał, więc to informacja w rankingu, nie cecha modelu."""
    rp = posts[posts["title"].fillna("").str.contains("reprint", case=False)]
    if rp.empty:
        return pd.DataFrame(columns=["date", "set_id", "reprint_posts"])
    titles = rp["title"].str.lower()
    rows = []
    for gid, name in zip(sets["group_id"], sets["set_name"]):
        key = re.sub(r"^[A-Za-z0-9 ]+?:\s*", "", str(name)).lower().strip()
        kws = SET_ALIASES.get(key, [re.escape(key)] if len(key) >= 6 else [])
        if kws:
            rows += [(str(gid), d) for d in rp["date"][titles.str.contains("|".join(kws))]]
    if not rows:
        return pd.DataFrame(columns=["date", "set_id", "reprint_posts"])
    r = pd.DataFrame(rows, columns=["set_id", "d"])
    r["date"] = r["d"].dt.to_period("W-SUN").dt.end_time.dt.normalize()
    w = r.groupby(["date", "set_id"]).size().unstack()
    idx = pd.date_range(posts["date"].min().normalize(), posts["date"].max() + pd.Timedelta(days=7), freq="W-SUN")
    w = w.reindex(idx).fillna(0).rolling(weeks, min_periods=1).sum()
    out = w.stack().rename("reprint_posts").reset_index()
    out.columns = ["date", "set_id", "reprint_posts"]
    return out
