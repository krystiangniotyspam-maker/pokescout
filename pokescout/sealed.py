"""Produkty zamknięte (booster box, ETB, booster bundle, saszetka): test i ranking.

Na historii 2024–2026 produkty zamknięte zyskiwały mocniej niż karty, a lepiej od reszty wypadały:
  - ETB i booster bundle (zamiast boxów i pojedynczych saszetek),
  - produkty w wieku ok. 1,5 roku od premiery (świeże jeszcze tanieją, bardzo stare rosną wolniej),
  - droższe produkty z danego setu.
Ocena = suma rang tych trzech cech w danym dniu; bez dopasowanych wag.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

KINDS_UP = ("etb", "booster_bundle")
SWEET_AGE = 18.0  # miesięcy od premiery


def load_sealed_weekly(data_dir: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(ceny tygodniowe: data × product_id, katalog sealed)."""
    data_dir = Path(data_dir)
    cat = pd.read_csv(data_dir / "catalog" / "sealed.csv").set_index("product_id")
    rows = []
    for f in sorted((data_dir / "prices").glob("*/*/*.csv.gz")):
        d = pd.read_csv(f, usecols=["product_id", "market"])
        d = d[d.product_id.isin(cat.index)]
        d["date"] = pd.Timestamp(f"{f.parent.parent.name}-{f.parent.name}-{f.name[:2]}")
        rows.append(d)
    if not rows:
        return pd.DataFrame(), cat
    p = pd.concat(rows).groupby(["date", "product_id"]).market.max().unstack()
    return p.resample("W-SUN").last().ffill(limit=2), cat


def features_at(prices: pd.DataFrame, cat: pd.DataFrame, d: pd.Timestamp, min_price: float = 5.0) -> pd.DataFrame:
    now = prices.loc[d].dropna()
    now = now[now >= min_price]
    df = cat.loc[now.index, ["name", "kind", "set_name", "release_date"]].copy()
    df["price_now"] = now
    df["age_months"] = (d - pd.to_datetime(df.release_date)).dt.days / 30.44
    df = df[df.age_months >= 1]
    df["etb"] = df.kind.isin(KINDS_UP).astype(float)
    df["age_fit"] = -np.abs(np.log(df.age_months.clip(lower=1) / SWEET_AGE))
    df["score"] = (df.etb.rank(pct=True) + df.age_fit.rank(pct=True) + np.log(df.price_now).rank(pct=True)) / 3
    return df


def evaluate(prices: pd.DataFrame, cat: pd.DataFrame, horizons=(6, 12), top_k: int = 10,
             step: int = 2) -> pd.DataFrame:
    """Top-K wg oceny vs wszystkie produkty zamknięte; średni zwrot (bez kosztów) w horyzoncie."""
    rows = []
    for h in horizons:
        res = []
        for d in prices.index[::step]:
            e = d + pd.Timedelta(weeks=round(h * 52 / 12))
            if e > prices.index[-1]:
                break
            f = features_at(prices, cat, d)
            f["ret"] = prices.loc[e, f.index] / f.price_now - 1
            f = f.dropna(subset=["ret"])
            if len(f) < 3 * top_k:
                continue
            t = f.nlargest(top_k, "score")
            res.append(dict(top=t.ret.mean(), all=f.ret.mean(), loss=(t.ret < 0).mean(),
                            ic=f.score.corr(f.ret, method="spearman")))
        if not res:
            continue
        r = pd.DataFrame(res)
        half = len(r) // 2
        rows.append({"horyzont": f"{h} mies.", "dat": len(r), "ic": round(r.ic.mean(), 3),
                     f"top{top_k}": f"{r.top.mean():+.0%}", "wszystkie": f"{r['all'].mean():+.0%}",
                     f"top{top_k} ze stratą": f"{r.loss.mean():.0%}",
                     "top: 1. / 2. połowa": f"{r.top[:half].mean():+.0%} / {r.top[half:].mean():+.0%}"})
    return pd.DataFrame(rows)


def ranking(prices: pd.DataFrame, cat: pd.DataFrame, min_price: float = 20.0) -> pd.DataFrame:
    d = prices.index[-1]
    f = features_at(prices, cat, d, min_price=min_price)
    f = f.sort_values("score", ascending=False)
    return f.reset_index()[["product_id", "name", "kind", "set_name", "release_date", "age_months",
                            "price_now", "score"]]


def _norm(name: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", " ", str(name).lower().replace("pokémon", "pokemon")).strip()


def add_cardmarket(rank: pd.DataFrame, data_dir: str | Path) -> pd.DataFrame:
    """Dokleja cenę z Cardmarket (EUR, trend) po nazwie produktu, gdy nazwa jest taka sama."""
    cm = Path(data_dir) / "cardmarket"
    files = sorted((cm / "prices").glob("*.csv.gz"))
    if not files or not (cm / "products.csv.gz").exists():
        return rank
    prods = pd.read_csv(cm / "products.csv.gz")
    prods = prods[~prods.categoryName.str.contains("Single", na=False)]
    price = pd.read_csv(files[-1]).set_index("idProduct")["trend"]
    prods["eur"] = prods.idProduct.map(price)
    by_name = prods.dropna(subset=["eur"]).assign(k=lambda x: x.name.map(_norm)).drop_duplicates("k").set_index("k").eur
    return rank.assign(cardmarket_eur=rank.name.map(lambda n: by_name.get(_norm(n))))
