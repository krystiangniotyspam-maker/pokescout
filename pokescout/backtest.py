"""Test algorytmu na historii.

Co miesiąc (data decyzji) liczymy oceny tylko z danych do tej daty, wybieramy
top N kart i sprawdzamy, ile zyskały po `horizon_months`. Porównujemy to z
„bazą”: wszystkimi kartami o tej samej rzadkości/popularności dostępnymi
w tym samym momencie. Algorytm ma sens tylko wtedy, gdy wyraźnie bije bazę.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .features import card_features
from .scoring import CardMeta, Config, score_trough
from .tiers import pokemon_tier, rarity_weight


def _price_at(s: pd.Series, when: pd.Timestamp, window_days: int = 21) -> float:
    w = s[(s.index > when - pd.Timedelta(days=window_days)) & (s.index <= when)]
    return float(w.median()) if len(w) else np.nan


def run_backtest(
    prices: dict[str, pd.Series],
    metas: dict[str, CardMeta],
    sealed: dict[str, pd.Series],
    start: str,
    end: str,
    horizon_months: int = 24,
    top_n: int = 5,
    cfg: Config = Config(),
) -> tuple[pd.DataFrame, pd.DataFrame]:
    decisions = pd.date_range(start, end, freq="MS")
    picks_rows, summary_rows = [], []

    for d in decisions:
        exit_d = d + pd.DateOffset(months=horizon_months)
        scored = []
        for cid, m in metas.items():
            f = card_features(cid, prices[cid], m.release_date, d, sealed.get(m.set_id))
            if f is None:
                continue
            r = score_trough(f, m, cfg)
            p_exit = _price_at(prices[cid], exit_d)
            if np.isnan(p_exit):
                continue
            fwd = p_exit / f.price_now - 1
            base_ok = (pokemon_tier(m.name) <= cfg.max_tier
                       and rarity_weight(m.rarity, m.name) >= cfg.min_rarity_weight
                       and f.age_months >= 3)
            scored.append(dict(date=d, card_id=cid, name=m.name, score=r.score,
                               passed=r.passed_gates, fwd=fwd, base=base_ok))
        if not scored:
            continue
        df = pd.DataFrame(scored)
        picks = df[df.passed].nlargest(top_n, "score")
        base = df[df.base]
        if len(picks):
            picks_rows.append(picks)
        summary_rows.append(dict(
            date=d,
            n_picks=len(picks),
            picks_median_return=picks.fwd.median() if len(picks) else np.nan,
            base_median_return=base.fwd.median() if len(base) else np.nan,
            picks_hit_rate_2x=(picks.fwd >= 1.0).mean() if len(picks) else np.nan,
            base_hit_rate_2x=(base.fwd >= 1.0).mean() if len(base) else np.nan,
        ))

    picks_df = pd.concat(picks_rows) if picks_rows else pd.DataFrame()
    return picks_df, pd.DataFrame(summary_rows)
