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
    history_complete: bool   # czy dane sięgają premiery (inaczej „szczyt” = maksimum od początku danych)

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
    w = _weekly(prices[prices.index <= as_of])
    sw = None
    if sealed_prices is not None and len(sealed_prices):
        sw = _weekly(sealed_prices[sealed_prices.index <= as_of])
    return features_from_weekly(card_id, _days(w.index), w.to_numpy(dtype=float), release_date, as_of,
                                None if sw is None else _days(sw.index),
                                None if sw is None else sw.to_numpy(dtype=float))


def _days(idx: pd.DatetimeIndex) -> np.ndarray:
    return idx.to_numpy(dtype="datetime64[D]").astype(np.int64)


def _slope(t: np.ndarray, v: np.ndarray, ref: int, days: int) -> float:
    m = t > ref - days
    if m.sum() < 3:
        return np.nan
    x, y = t[m].astype(float), np.log(v[m])
    x = x - x.mean()
    sxx = (x * x).sum()
    if sxx == 0:
        return np.nan
    k = (x * (y - y.mean())).sum() / sxx
    return float(np.exp(k * 30) - 1)


def _vol(t: np.ndarray, v: np.ndarray, ref: int, days: int) -> float:
    m = t > ref - days
    if m.sum() < 4:
        return np.nan
    return float(np.std(np.diff(np.log(v[m]))))


def features_from_weekly(
    card_id: str,
    t: np.ndarray,            # dni (int, od 1970-01-01) tygodniowych median, rosnąco, tylko dane do as_of
    v: np.ndarray,
    release_date: pd.Timestamp,
    as_of: pd.Timestamp,
    sealed_t: np.ndarray | None = None,
    sealed_v: np.ndarray | None = None,
) -> CardFeatures | None:
    """Szybka wersja liczenia cech na gotowych tablicach tygodniowych (używana w teście na historii)."""
    if len(v) < 8:
        return None
    ref = int(t[-1])
    rel = int(np.datetime64(release_date.date(), "D").astype(np.int64))
    price_now = float(v[-1])
    after = v[t >= rel + HYPE_SKIP_DAYS]
    peak = float(after.max()) if len(after) else float(v.max())

    m180 = t > ref - 180
    t180, v180 = t[m180], v[m180]
    lo, hi = float(v180.min()), float(v180.max())
    range_pos = (price_now - lo) / (hi - lo) if hi > lo else 0.5
    low_t = int(t180[np.argmin(v180)])

    v60, v180_ = _vol(t, v, ref, 60), _vol(t, v, ref, 180)
    vol_ratio = v60 / v180_ if v180_ and not np.isnan(v180_) and v180_ > 0 else np.nan

    sealed_slope = np.nan
    if sealed_t is not None and len(sealed_t):
        sealed_slope = _slope(sealed_t, sealed_v, ref, 90)

    return CardFeatures(
        card_id=card_id,
        as_of=as_of,
        price_now=price_now,
        age_months=(as_of - release_date).days / 30.44,
        peak_post_release=peak,
        drawdown=1 - price_now / peak if peak > 0 else 0.0,
        range_pos_180=range_pos,
        slope_30=_slope(t, v, ref, 30),
        slope_60=_slope(t, v, ref, 60),
        slope_90=_slope(t, v, ref, 90),
        slope_180=_slope(t, v, ref, 180),
        vol_ratio=vol_ratio,
        weeks_since_low=(ref - low_t) // 7,
        above_low=price_now / lo - 1 if lo > 0 else 0.0,
        sealed_slope_90=sealed_slope,
        weeks_of_data=len(v),
        history_complete=bool(t[0] <= rel + 45),
    )
