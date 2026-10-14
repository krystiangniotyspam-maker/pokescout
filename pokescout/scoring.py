"""Algorytm oceny kart.

Moduł A – „dołek po premierze”: popularne, rzadkie karty z setów po fazie hype'u,
których cena mocno spadła od szczytu i właśnie przestała spadać.

Moduł B – „niedoszacowane i okazje”:
  B1 wartość względna (karta tańsza niż podobne karty),
  B2 para kart (np. Espeon vs Umbreon z tego samego setu) – rozjazd proporcji,
  B3 sprawdzenie pojedynczej oferty (okazja czy podejrzana).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .features import CardFeatures, _weekly
from .tiers import TIER_SCORE, pokemon_tier, rarity_weight


def _clip01(x: float) -> float:
    if x is None or np.isnan(x):
        return np.nan
    return float(min(1.0, max(0.0, x)))


@dataclass
class Config:
    # --- bramki modułu A (karta musi je przejść, żeby w ogóle dostać ocenę)
    min_rarity_weight: float = 0.75     # Illustration Rare i wyżej
    max_tier: int = 2
    min_age_main: float = 9.0           # miesiące od premiery – zwykły set
    min_age_special: float = 15.0       # sety specjalne (151, Celebrations, 30th) zwykle wolniej dochodzą do dna
    max_age: float = 48.0
    min_drawdown: float = 0.35
    max_falling_slope: float = -0.03    # spadek szybszy niż 3%/mies. = nóż jeszcze leci
    # „potwierdzone dno”: od minimum minęło trochę czasu i cena się od niego odbiła.
    # Bez tego algorytm łapie karty, które tanieją powoli, ale bez końca (pułapka Celebrations).
    min_weeks_since_low: int = 6
    min_above_low: float = 0.05
    min_price: float = 8.0          # w walucie danych (TCGplayer: USD)
    # --- wagi składników oceny A
    w_quality: float = 0.25
    w_depth: float = 0.20
    w_stab: float = 0.20
    w_supply: float = 0.15
    w_calm: float = 0.10
    w_buzz: float = 0.10
    # --- moduł B1
    min_peer_group: int = 5
    z_threshold: float = -1.0


@dataclass
class CardMeta:
    card_id: str
    name: str
    set_id: str
    rarity: str
    release_date: pd.Timestamp
    set_type: str = "main"              # "main" | "special" | "promo"
    reprint_announced: bool = False     # ręczna flaga: zapowiedziany dodruk
    buzz: float | None = None           # 0–1 z analizy forów/YouTube; None = brak danych
    set_name: str = ""


@dataclass
class Result:
    card_id: str
    name: str
    module: str
    score: float
    passed_gates: bool
    reasons: list[str] = field(default_factory=list)
    components: dict = field(default_factory=dict)


# ---------------------------------------------------------------- moduł A

def _depth(dd: float) -> float:
    # najlepiej 50–80% pod szczytem; bardzo głęboki spadek (>85%) bywa sygnałem trwałego załamania
    if dd < 0.35:
        return 0.0
    if dd <= 0.75:
        return (dd - 0.35) / 0.40
    if dd <= 0.85:
        return 1.0
    return max(0.5, 1.0 - (dd - 0.85) * 3)


def _age_fit(age: float, set_type: str) -> float:
    lo, hi = (12, 30) if set_type == "main" else (18, 36)
    if lo <= age <= hi:
        return 1.0
    if lo - 3 <= age < lo or hi < age <= hi + 10:
        return 0.6
    return 0.3


def score_trough(f: CardFeatures, meta: CardMeta, cfg: Config = Config()) -> Result:
    tier = pokemon_tier(meta.name)
    rw = rarity_weight(meta.rarity, meta.name)
    reasons: list[str] = []
    gates: list[str] = []

    min_age = cfg.min_age_main if meta.set_type == "main" else cfg.min_age_special
    if rw < cfg.min_rarity_weight:
        gates.append("za niska rzadkość")
    if tier > cfg.max_tier:
        gates.append("mało popularny Pokémon")
    if meta.set_type == "promo":
        gates.append("karta promo (duży nakład)")
    if not (min_age <= f.age_months <= cfg.max_age):
        gates.append(f"wiek setu {f.age_months:.0f} mies. poza oknem {min_age:.0f}–{cfg.max_age:.0f}")
    if f.drawdown < cfg.min_drawdown:
        gates.append(f"tylko {f.drawdown:.0%} pod szczytem")
    if not np.isnan(f.slope_60) and f.slope_60 < cfg.max_falling_slope:
        gates.append(f"cena wciąż spada ({f.slope_60:+.0%}/mies.)")
    if f.weeks_since_low < cfg.min_weeks_since_low or f.above_low < cfg.min_above_low:
        gates.append(f"brak potwierdzonego dna (minimum {f.weeks_since_low} tyg. temu, "
                     f"cena {f.above_low:+.0%} nad nim)")
    if f.price_now < cfg.min_price:
        gates.append("za tania (mała płynność, wysyłka zjada zysk)")
    if meta.reprint_announced:
        gates.append("zapowiedziany dodruk")

    quality = 0.6 * TIER_SCORE[tier] + 0.4 * rw
    depth = _depth(f.drawdown)

    s60 = 0.5 if np.isnan(f.slope_60) else _clip01((f.slope_60 + 0.03) / 0.06)
    turn = 1.0 if (not np.isnan(f.slope_30) and not np.isnan(f.slope_90)
                   and f.slope_30 > f.slope_90 + 0.01) else 0.0
    # dno: im dłużej cena trzyma się nad minimum, tym pewniej (max przy 16 tyg.)
    bottom = _clip01(f.weeks_since_low / 16) * (1.0 if f.range_pos_180 < 0.6 else 0.6)
    stab = 0.4 * s60 + 0.3 * turn + 0.3 * bottom

    age_fit = _age_fit(f.age_months, meta.set_type)
    if np.isnan(f.sealed_slope_90):
        sealed_sig = 0.4
    else:
        div = f.sealed_slope_90 - (0 if np.isnan(f.slope_90) else f.slope_90)
        sealed_sig = _clip01(div / 0.08)
        if meta.set_type != "main":
            # w setach specjalnych sealed potrafi rosnąć, a karty dalej tanieć
            # (Celebrations: paczki x8, karty −64% od szczytu) – sygnał słabszy
            sealed_sig *= 0.5
    supply = 0.5 * age_fit + 0.5 * sealed_sig

    calm = 0.5 if np.isnan(f.vol_ratio) else _clip01((1.2 - f.vol_ratio) / 0.6)
    buzz = 0.5 if meta.buzz is None else _clip01(meta.buzz)

    score = 100 * (cfg.w_quality * quality + cfg.w_depth * depth + cfg.w_stab * stab
                   + cfg.w_supply * supply + cfg.w_calm * calm + cfg.w_buzz * buzz)

    reasons.append(f"{f.drawdown:.0%} poniżej szczytu po premierze ({f.peak_post_release:.2f} → {f.price_now:.2f})")
    if not np.isnan(f.slope_60):
        reasons.append(f"trend 60 dni: {f.slope_60:+.1%}/mies.")
    if turn:
        reasons.append("krótki trend lepszy niż długi – możliwy zwrot")
    if not np.isnan(f.sealed_slope_90) and sealed_sig > 0.5:
        reasons.append(f"zamknięte produkty z setu drożeją ({f.sealed_slope_90:+.1%}/mies.) – podaż wysycha")
    reasons.append(f"set ma {f.age_months:.0f} mies.; Pokémon tier {tier}; rzadkość: {meta.rarity}")

    return Result(
        card_id=meta.card_id, name=meta.name, module="A",
        score=round(score, 1) if not gates else 0.0,
        passed_gates=not gates,
        reasons=reasons if not gates else gates,
        components=dict(quality=quality, depth=depth, stab=stab, supply=supply,
                        calm=calm, buzz=buzz, raw_score=round(score, 1)),
    )


# ---------------------------------------------------------------- moduł B1

def _era(d: pd.Timestamp) -> str:
    y = d.year
    return f"{y - (y % 2)}-{y - (y % 2) + 1}"


def score_relative_value(
    feats: list[CardFeatures], metas: dict[str, CardMeta], cfg: Config = Config()
) -> list[Result]:
    """Karta wyraźnie tańsza niż podobne (ten sam tier, rzadkość i epoka)."""
    rows = []
    for f in feats:
        m = metas[f.card_id]
        rows.append(dict(
            card_id=f.card_id, name=m.name, tier=pokemon_tier(m.name),
            rarity=m.rarity.lower(), era=_era(m.release_date),
            logp=np.log(f.price_now), slope_60=f.slope_60, f=f, m=m,
        ))
    df = pd.DataFrame(rows)
    if df.empty:
        return []
    out: list[Result] = []
    for _, g in df.groupby(["tier", "rarity", "era"]):
        if len(g) < cfg.min_peer_group:
            continue
        med = g["logp"].median()
        mad = (g["logp"] - med).abs().median() * 1.4826 or 1e-9
        for _, r in g.iterrows():
            z = (r.logp - med) / mad
            if z > cfg.z_threshold:
                continue
            if not np.isnan(r.slope_60) and r.slope_60 < cfg.max_falling_slope:
                continue
            quality = 0.6 * TIER_SCORE[r.tier] + 0.4 * rarity_weight(r.rarity, r["name"])
            cheap = _clip01(-z / 2.5)
            stab = 0.5 if np.isnan(r.slope_60) else _clip01((r.slope_60 + 0.03) / 0.06)
            buzz = 0.5 if r.m.buzz is None else r.m.buzz
            score = 100 * (0.4 * cheap + 0.3 * quality + 0.2 * stab + 0.1 * buzz)
            out.append(Result(
                card_id=r.card_id, name=r["name"], module="B1", score=round(score, 1),
                passed_gates=True,
                reasons=[
                    f"cena {np.exp(r.logp):.2f} to {np.exp(r.logp - med):.0%} mediany grupy "
                    f"(tier {r.tier}, {r.rarity}, {r.era}, {len(g)} kart)",
                    f"odchylenie z = {z:.1f}",
                ],
                components=dict(z=z, cheap=cheap, quality=quality, stab=stab),
            ))
    return sorted(out, key=lambda x: -x.score)


# ---------------------------------------------------------------- moduł B2

def pair_signal(prices_a: pd.Series, prices_b: pd.Series, as_of: pd.Timestamp,
                lookback_days: int = 365, threshold: float = 0.25) -> dict | None:
    """Czy karta A jest teraz tańsza względem B niż zwykle?

    Przykład pary: Espeon i Umbreon z tego samego setu i tej samej rzadkości.
    """
    a = _weekly(prices_a[prices_a.index <= as_of])
    b = _weekly(prices_b[prices_b.index <= as_of])
    ratio = (a / b).dropna()
    hist = ratio[ratio.index > as_of - pd.Timedelta(days=lookback_days)]
    if len(hist) < 12:
        return None
    typical = float(hist.iloc[:-4].median())
    now = float(hist.iloc[-1])
    gap = now / typical - 1
    return dict(ratio_now=now, ratio_typical=typical, gap=gap, signal=gap <= -threshold)


# ---------------------------------------------------------------- moduł B3

def deal_check(listing_price: float, trend_price: float,
               seller_feedback: int | None = None, n_photos: int | None = None,
               shows_back: bool | None = None) -> dict:
    """Szybka ocena pojedynczej oferty (Allegro, OLX, Vinted…)."""
    ratio = listing_price / trend_price if trend_price else np.nan
    flags = []
    if ratio < 0.4:
        flags.append("cena < 40% rynku – typowe dla podróbek")
    if seller_feedback is not None and seller_feedback < 10:
        flags.append("sprzedawca z małą liczbą opinii")
    if n_photos is not None and n_photos < 2:
        flags.append("za mało zdjęć")
    if shows_back is False:
        flags.append("brak zdjęcia rewersu")

    if ratio < 0.4 or len(flags) >= 2:
        verdict = "podejrzane"
    elif ratio <= 0.75:
        verdict = "okazja"
    elif ratio <= 0.9:
        verdict = "lekko poniżej rynku"
    else:
        verdict = "cena rynkowa lub wyższa"
    return dict(ratio=ratio, verdict=verdict, flags=flags)
