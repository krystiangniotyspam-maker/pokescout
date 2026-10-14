"""Uczciwy test przewidywań na prawdziwej historii cen.

1. `build_panel` – dla każdej daty decyzji (co 2 tygodnie) liczy cechy każdej karty WYŁĄCZNIE
   z danych do tej daty, dodaje cechy przekrojowe (karta vs podobne karty, vs ten sam Pokémon,
   trend całego setu) i zwrot w przód po 3/6/12 miesiącach.
2. `walk_forward` – model uczony tylko na przykładach, których wynik był już znany w dniu
   decyzji (data + horyzont ≤ dzień decyzji). Żadnej wiedzy z przyszłości.
3. `evaluate_scores` – dla każdego sygnału: IC (korelacja rang oceny ze zwrotem, liczona osobno
   w każdej dacie), zwrot top-K ponad medianę rynku, odsetek trafień.

Zwrot liczymy jako log(cena za h mies. / cena dziś) minus mediana wszystkich kart w tej dacie
(„zwrot ponad rynek”), żeby ocenić wybór kart, a nie to, czy cały rynek rósł.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .buzz import BUZZ_FEATURES
from .features import _days, _weekly, features_from_weekly
from .scoring import CardMeta, Config, score_trough
from .tiers import TIER_SCORE, pokemon_key, pokemon_tier, rarity_weight

HORIZONS = (3, 6, 12)
FEATURES = [
    "drawdown", "range_pos_180", "slope_30", "slope_60", "slope_90", "slope_180", "vol_ratio",
    "weeks_since_low", "above_low", "sealed_slope_90", "age_months", "logp", "tier_score",
    "rarity_w", "special", "history_complete", "rv_z", "poke_pop", "set_trend_90", "set_rel",
    *BUZZ_FEATURES,
]


def _robust_z(x: pd.Series) -> pd.Series:
    med = x.median()
    mad = (x - med).abs().median() * 1.4826
    return (x - med) / (mad if mad > 0 else np.nan)


def build_panel(prices: dict[str, pd.Series], metas: dict[str, CardMeta], sealed: dict[str, pd.Series],
                step_days: int = 14, min_price: float = 5.0, min_history_days: int = 182,
                start: pd.Timestamp | None = None, buzz: pd.DataFrame | None = None) -> pd.DataFrame:
    weekly = {cid: _weekly(s) for cid, s in prices.items()}
    arrays = {cid: (_days(w.index), w.to_numpy(dtype=float)) for cid, w in weekly.items() if len(w)}
    sealed_arr = {k: (_days(w.index), w.to_numpy(dtype=float))
                  for k, w in ((k, _weekly(v)) for k, v in sealed.items()) if len(w)}
    first = min(a[0][0] for a in arrays.values())
    last = max(a[0][-1] for a in arrays.values())
    first, last = pd.Timestamp(first, unit="D"), pd.Timestamp(last, unit="D")
    start = max(start or first, first + pd.Timedelta(days=min_history_days))
    # niedziele = końce tygodni, więc tygodniowa mediana z dnia decyzji nie zawiera przyszłości
    dates = pd.date_range(start, last, freq=f"{max(1, step_days // 7)}W-SUN")

    static = {cid: dict(tier=pokemon_tier(m.name), rarity_w=rarity_weight(m.rarity, m.name),
                        poke=pokemon_key(m.name), special=float(m.set_type == "special"))
              for cid, m in metas.items()}
    cfg = Config()
    rows = []
    for d in dates:
        dd = int(np.datetime64(d.date(), "D").astype(np.int64))
        for cid, (t, v) in arrays.items():
            m = metas.get(cid)
            if m is None or m.set_type == "promo" or t[0] > dd - 56:
                continue
            k = np.searchsorted(t, dd, side="right")
            if k == 0 or t[k - 1] < dd - 21:  # karta zniknęła z notowań
                continue
            st_ = sealed_arr.get(m.set_id)
            sk = np.searchsorted(st_[0], dd, side="right") if st_ else 0
            f = features_from_weekly(cid, t[:k], v[:k], m.release_date, d,
                                     st_[0][:sk] if st_ else None, st_[1][:sk] if st_ else None)
            if f is None or f.price_now < min_price or f.age_months < 2:
                continue
            st = static[cid]
            rule = score_trough(f, m, cfg)
            row = dict(f.to_dict(), date=d, set_id=m.set_id, set_name=m.set_name, name=m.name, poke=st["poke"],
                       tier=st["tier"], tier_score=TIER_SCORE[st["tier"]], rarity_w=st["rarity_w"],
                       special=st["special"], logp=np.log(f.price_now),
                       rule_a=rule.components["raw_score"], rule_a_pass=rule.passed_gates)
            for h in HORIZONS:
                ed = int(np.datetime64((d + pd.DateOffset(months=h)).date(), "D").astype(np.int64))
                j = np.searchsorted(t, ed, side="right")
                p = v[j - 1] if j > 0 and t[j - 1] > ed - 21 and t[j - 1] > dd else np.nan
                row[f"fwd_{h}"] = np.log(p / f.price_now) if p > 0 else np.nan
            rows.append(row)
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["history_complete"] = df["history_complete"].astype(float)
    df["era"] = (pd.to_datetime(df["date"]) - pd.to_timedelta(df["age_months"] * 30.44, unit="D")).dt.year // 2
    df["rbucket"] = (df["rarity_w"] * 4).round()

    g = df.groupby(["date", "tier", "rbucket", "era"])["logp"]
    df["rv_z"] = g.transform(lambda x: _robust_z(x) if len(x) >= 5 else pd.Series(np.nan, index=x.index))
    # popularność Pokémona z danych: mediana log-ceny jego POZOSTAŁYCH kart (IR+) w tej dacie
    hi = df[df.rarity_w >= 0.75]
    pop = hi.groupby(["date", "poke"])["logp"].agg(["sum", "count"])
    j = df.join(pop, on=["date", "poke"])
    own = np.where(df.rarity_w >= 0.75, df.logp, 0.0)
    n_other = j["count"].fillna(0) - (df.rarity_w >= 0.75)
    df["poke_pop"] = np.where(n_other > 0, (j["sum"].fillna(0) - own) / n_other.where(n_other > 0), np.nan)
    df["poke_pop"] = df["poke_pop"] - df.groupby("date")["logp"].transform("median")
    df["set_trend_90"] = df.groupby(["date", "set_id"])["slope_90"].transform("median")
    df["set_rel"] = df["logp"] - df.groupby(["date", "set_id"])["logp"].transform("median")
    if buzz is not None and len(buzz):
        df = df.merge(buzz, on=["date", "poke"], how="left")
        covered = df["date"] >= buzz["date"].min() + pd.Timedelta(weeks=8)
        for c in BUZZ_FEATURES:  # Pokémon bez wzmianek w okresie z danymi = 0, nie brak danych
            df.loc[covered & df[c].isna(), c] = 0.0 if c != "buzz_growth" else np.log(1.0)
    else:
        for c in BUZZ_FEATURES:
            df[c] = np.nan
    for h in HORIZONS:
        df[f"ex_{h}"] = df[f"fwd_{h}"] - df.groupby("date")[f"fwd_{h}"].transform("median")
    return df.reset_index(drop=True)


# Ocena C – suma rang sygnałów, które na historii 2024–2026 przewidywały zwrot ponad rynek:
# popularność Pokémona z danych, wiek setu, karta tańsza niż podobne, dno trzymane od tygodni.
# Bez dopasowanych wag (mniejsze ryzyko przeuczenia niż model), wszystko liczone w dniu decyzji.
COMBO = {"poke_pop": 1, "age_months": 1, "rv_z": -1, "weeks_since_low": 1}


def combo_score(panel: pd.DataFrame) -> pd.Series:
    by_date = panel.groupby("date")
    return sum(sign * (by_date[c].rank(pct=True).fillna(0.5) - 0.5) for c, sign in COMBO.items())


def walk_forward(panel: pd.DataFrame, horizon: int, min_train_dates: int = 6, model: str = "gbm") -> pd.Series:
    """Ocena modelu dla każdej daty, uczonego tylko na wynikach znanych w tej dacie."""
    from sklearn.ensemble import HistGradientBoostingRegressor
    from sklearn.linear_model import Ridge

    y_col = f"ex_{horizon}"
    out = pd.Series(np.nan, index=panel.index)
    dates = sorted(panel["date"].unique())
    for d in dates:
        known = panel["date"] + pd.DateOffset(months=horizon) <= d
        train = panel[known & panel[y_col].notna()]
        if train["date"].nunique() < min_train_dates:
            continue
        test = panel["date"] == d
        X, Xt = train[FEATURES], panel.loc[test, FEATURES]
        y = train[y_col].clip(-1.5, 1.5)  # pojedyncze skoki x5 nie mogą dominować nauki
        if model == "gbm":
            m = HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=250,
                                              min_samples_leaf=100, l2_regularization=1.0, random_state=0)
            m.fit(X, y)
            out[test] = m.predict(Xt)
        else:  # ridge na rangach cech (odporny na wartości skrajne, braki = środek)
            def ranks(df_):
                return df_.groupby(panel.loc[df_.index, "date"]).rank(pct=True).fillna(0.5) - 0.5
            m = Ridge(alpha=10.0).fit(ranks(X), y)
            out[test] = m.predict(ranks(Xt))
    return out


def fit_latest(panel: pd.DataFrame, horizon: int = 6):
    """Model uczony na wszystkich znanych wynikach – do bieżącego rankingu."""
    from sklearn.ensemble import HistGradientBoostingRegressor

    y_col = f"ex_{horizon}"
    train = panel[panel[y_col].notna()]
    m = HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=250,
                                      min_samples_leaf=100, l2_regularization=1.0, random_state=0)
    m.fit(train[FEATURES], train[y_col].clip(-1.5, 1.5))
    return m


def evaluate_scores(panel: pd.DataFrame, scores: dict[str, pd.Series], horizon: int,
                    top_k: int = 20, step_days: int = 14) -> pd.DataFrame:
    """Tabela: IC, t-stat IC, zwrot top-K ponad rynek, odsetek trafień, liczba dat.

    Daty decyzji co 2 tygodnie przy horyzoncie 6 mies. dają nakładające się okresy, więc
    zwykły t-stat jest zawyżony; ic_t_adj koryguje go do liczby niezależnych okresów."""
    y_col = f"ex_{horizon}"
    rows = []
    for name, s in scores.items():
        df = panel.assign(_s=s)[["date", "_s", y_col]].dropna()
        ics, tops, hits = [], [], []
        for _, g in df.groupby("date"):
            if len(g) < max(30, top_k):
                continue
            ics.append(g["_s"].corr(g[y_col], method="spearman"))
            t = g.nlargest(top_k, "_s")
            tops.append(t[y_col].mean())
            hits.append((t[y_col] > 0).mean())
        if not ics:
            continue
        ics = np.array(ics)
        rows.append(dict(
            signal=name, dates=len(ics), ic=ics.mean(),
            ic_t_adj=(ics.mean() / (ics.std(ddof=1) + 1e-12) * np.sqrt(len(ics))
                      * np.sqrt(min(1.0, step_days / (horizon * 30.44)))) if len(ics) > 1 else np.nan,
            top_excess=np.expm1(np.mean(tops)), top_hit_rate=np.mean(hits),
        ))
    return pd.DataFrame(rows).sort_values("ic", ascending=False).reset_index(drop=True)
