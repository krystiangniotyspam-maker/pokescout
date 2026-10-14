"""Liczenie cech z historii cen.

Wszystkie funkcje przyjmują datę `as_of` i używają WYŁĄCZNIE danych do tej daty
(włącznie). Dzięki temu te same funkcje służą do bieżącej oceny i do testu
na historii bez „wiedzy z przyszłości”.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd

HYPE_SKIP_DAYS = 14  # pierwsze dni po premierze (przedsprzedaż, chaos cen) pomijamy przy szukaniu szczytu


def _weekly(series: pd.Series) -> pd.Series:
    """Mediana tygodniowa — tłumi pojedyncze dziwne transakcje."""
    s = series.dropna()
    s = s[s > 0]
    return s.resample("W").median().dropna()


def monthly_slope(series: pd.Series, days: int, as_of: pd.Timestamp) -> float:
    """Nachylenie log-ceny z ostatnich `days` dni, wyrażone jako % zmiany na miesiąc."""
    s = series[(series.index > as_of - pd.Timedelta(days=days)) & (series.index <= as_of)]
    if len(s) < 3:
        return np.nan
    x = (s.index - s.index[0]).days.to_numpy(dtype=float)
    y = np.log(s.to_numpy(dtype=float))
    if np.ptp(x) == 0:
        return np.nan
    k = np.polyfit(x, y, 1)[0]
    return float(np.exp(k * 30) - 1)


def volatility(series: pd.Series, days: int, as_of: pd.Timestamp) -> float:
    s = series[(series.index > as_of - pd.Timedelta(days=days)) & (series.index <= as_of)]
    if len(s) < 4:
        return np.nan
    r = np.diff(np.log(s.to_numpy(dtype=float)))
    return float(np.std(r))


@dataclass
class CardFeatures:
    card_id: str
    as_of: pd.Timestamp
    price_now: float
    age_months: float
    peak_post_release: float
    drawdown: float          # 0.45 = 45% poniżej szczytu po premierze
    range_pos_180: float     # 0 = przy minimum z 180 dni, 1 = przy maksimum
    slope_30: float          # % zmiany na miesiąc
    slope_60: float
    slope_90: float
    slope_180: float
    vol_ratio: float         # zmienność 60 dni / 180 dni (<1 = uspokojenie)
    weeks_since_low: int     # ile tygodni temu było minimum z 180 dni (0 = właśnie robi nowe dno)
    above_low: float         # o ile % cena jest powyżej minimum z 180 dni
    sealed_slope_90: float   # trend zamkniętych produktów z tego setu
    weeks_of_data: int

    def to_dict(self) -> dict:
        return asdict(self)


def card_features(
    card_id: str,
    prices: pd.Series,
    release_date: pd.Timestamp,
    as_of: pd.Timestamp,
    sealed_prices: pd.Series | None = None,
) -> CardFeatures | None:
    """Cechy jednej karty na dzień `as_of`. Zwraca None, gdy danych jest za mało."""
    prices = prices[prices.index <= as_of]
    w = _weekly(prices)
    if len(w) < 8:
        return None

    price_now = float(w.iloc[-1])
    after_hype = w[w.index >= release_date + pd.Timedelta(days=HYPE_SKIP_DAYS)]
    peak = float(after_hype.max()) if len(after_hype) else float(w.max())

    last_180 = w[w.index > as_of - pd.Timedelta(days=180)]
    lo, hi = float(last_180.min()), float(last_180.max())
    range_pos = (price_now - lo) / (hi - lo) if hi > lo else 0.5
    low_date = last_180.idxmin()
    weeks_since_low = int((w.index[-1] - low_date).days // 7)
    above_low = price_now / lo - 1 if lo > 0 else 0.0

    v60 = volatility(w, 60, as_of)
    v180 = volatility(w, 180, as_of)
    vol_ratio = v60 / v180 if v180 and not np.isnan(v180) and v180 > 0 else np.nan

    sealed_slope = np.nan
    if sealed_prices is not None and len(sealed_prices):
        sw = _weekly(sealed_prices[sealed_prices.index <= as_of])
        sealed_slope = monthly_slope(sw, 90, as_of)

    return CardFeatures(
        card_id=card_id,
        as_of=as_of,
        price_now=price_now,
        age_months=(as_of - release_date).days / 30.44,
        peak_post_release=peak,
        drawdown=1 - price_now / peak if peak > 0 else 0.0,
        range_pos_180=range_pos,
        slope_30=monthly_slope(w, 30, as_of),
        slope_60=monthly_slope(w, 60, as_of),
        slope_90=monthly_slope(w, 90, as_of),
        slope_180=monthly_slope(w, 180, as_of),
        vol_ratio=vol_ratio,
        weeks_since_low=weeks_since_low,
        above_low=above_low,
        sealed_slope_90=sealed_slope,
        weeks_of_data=len(w),
    )
