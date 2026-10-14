"""Demo na DANYCH SYNTETYCZNYCH.

Sprawdza tylko, czy mechanika działa (cechy, bramki, ranking, test na historii).
Wyniki NIE są dowodem, że algorytm działa na prawdziwym rynku – to pokaże dopiero
test na prawdziwej historii cen.

Archetypy przebiegu ceny (mnożnik ceny z premiery w funkcji miesięcy):
  winner       – spadek po premierze, płaskie dno, potem kilkukrotny wzrost (jak „Moonbreon”)
  modest       – spadek, dno, umiarkowane odbicie
  flat         – spadek, potem długo w miejscu
  slow_decline – powolne, ciągłe tanienie (jak wiele kart z przedrukowanego setu specjalnego)
  freefall     – głęboki spadek bez dna
"""
import numpy as np
import pandas as pd

from pokescout import CardMeta, card_features, run_backtest, score_relative_value, score_trough

RNG = np.random.default_rng(7)
DATA_END = pd.Timestamp("2026-10-01")

KNOTS = {
    "winner":       [(0, 1.0), (0.5, 1.15), (8, 0.45), (16, 0.45), (40, 2.0), (62, 3.0)],
    "modest":       [(0, 1.0), (0.5, 1.1), (8, 0.55), (18, 0.55), (48, 0.9), (62, 1.0)],
    "flat":         [(0, 1.0), (0.5, 1.1), (8, 0.5), (62, 0.55)],
    "slow_decline": [(0, 1.0), (0.5, 1.1), (10, 0.5), (36, 0.3), (62, 0.24)],
    "freefall":     [(0, 1.0), (0.5, 1.05), (12, 0.2), (36, 0.08), (62, 0.06)],
}


def make_series(release: pd.Timestamp, base: float, archetype: str) -> pd.Series:
    days = pd.date_range(release, DATA_END, freq="D")
    months = (days - release).days / 30.44
    xs, ys = zip(*KNOTS[archetype])
    logm = np.interp(months, xs, np.log(ys))
    walk = np.cumsum(RNG.normal(0, 0.006, len(days)))
    walk -= pd.Series(walk).rolling(120, min_periods=1).mean().to_numpy()  # szum bez dryfu
    noise = RNG.normal(0, 0.03, len(days))
    return pd.Series(base * np.exp(logm + walk + noise), index=days)


def make_sealed(release: pd.Timestamp, start_m: float, rate: float) -> pd.Series:
    days = pd.date_range(release, DATA_END, freq="D")
    months = (days - release).days / 30.44
    lvl = np.where(months < start_m, 1.0, (1 + rate) ** (months - start_m))
    return pd.Series(150 * lvl * np.exp(RNG.normal(0, 0.02, len(days))), index=days)


SETS = {
    # set_id: (premiera, typ, start wzrostu sealed [mies.], tempo sealed/mies.)
    "EVS_demo": ("2021-08-27", "main", 10, 0.035),
    "CEL_demo": ("2021-10-08", "special", 14, 0.01),
    "PAL_demo": ("2023-06-09", "main", 12, 0.03),
    "OBF_demo": ("2023-08-11", "main", 99, 0.0),     # sealed bez wzrostu
}

CARDS = [
    # card_id, nazwa, set, rzadkość, cena startowa, archetyp
    ("evs-umb", "Umbreon VMAX", "EVS_demo", "Alternate Art", 300, "winner"),
    ("evs-ray", "Rayquaza VMAX", "EVS_demo", "Alternate Art", 200, "winner"),
    ("evs-syl", "Sylveon V", "EVS_demo", "Alternate Art", 90, "modest"),
    ("evs-esp", "Espeon V", "EVS_demo", "Alternate Art", 80, "modest"),
    ("evs-gla", "Glaceon V", "EVS_demo", "Alternate Art", 70, "modest"),
    ("evs-dra", "Dragonite V", "EVS_demo", "Alternate Art", 60, "flat"),
    ("evs-dur", "Duraludon V", "EVS_demo", "Alternate Art", 40, "freefall"),
    ("evs-tre", "Trevenant V", "EVS_demo", "Alternate Art", 25, "freefall"),
    ("cel-mew", "Mew", "CEL_demo", "Special Illustration Rare", 120, "slow_decline"),
    ("cel-pik", "Pikachu VMAX", "CEL_demo", "Special Illustration Rare", 60, "slow_decline"),
    ("cel-cha", "Charizard", "CEL_demo", "Classic Collection", 180, "flat"),
    ("cel-umb", "Umbreon", "CEL_demo", "Classic Collection", 50, "slow_decline"),
    ("cel-lug", "Lugia", "CEL_demo", "Classic Collection", 60, "slow_decline"),
    ("pal-kar", "Magikarp", "PAL_demo", "Illustration Rare", 60, "winner"),
    ("pal-ion", "Iono", "PAL_demo", "Special Illustration Rare", 120, "modest"),
    ("pal-gar", "Gardevoir ex", "PAL_demo", "Special Illustration Rare", 90, "modest"),
    ("pal-psy", "Psyduck", "PAL_demo", "Illustration Rare", 25, "flat"),
    ("pal-tin", "Tinkatink", "PAL_demo", "Illustration Rare", 15, "freefall"),
    ("pal-squ", "Squawkabilly ex", "PAL_demo", "Special Illustration Rare", 40, "freefall"),
    ("obf-cha", "Charizard ex", "OBF_demo", "Special Illustration Rare", 150, "modest"),
    ("obf-nin", "Ninetales", "OBF_demo", "Illustration Rare", 40, "flat"),
    ("obf-pal", "Palafin", "OBF_demo", "Illustration Rare", 15, "freefall"),
    ("obf-lec", "Lechonk", "OBF_demo", "Illustration Rare", 12, "flat"),
    ("obf-dar", "Darkrai", "OBF_demo", "Illustration Rare", 30, "slow_decline"),
    ("obf-pid", "Pidgeot ex", "OBF_demo", "Special Illustration Rare", 60, "slow_decline"),
]


def build():
    prices, metas, sealed = {}, {}, {}
    for sid, (rel, typ, sm, rate) in SETS.items():
        sealed[sid] = make_sealed(pd.Timestamp(rel), sm, rate)
    for cid, name, sid, rar, base, arch in CARDS:
        rel = pd.Timestamp(SETS[sid][0])
        prices[cid] = make_series(rel, base, arch)
        metas[cid] = CardMeta(cid, name, sid, rar, rel, set_type=SETS[sid][1])
    return prices, metas, sealed


def ranking(prices, metas, sealed, as_of):
    feats, res = [], []
    for cid, m in metas.items():
        f = card_features(cid, prices[cid], m.release_date, as_of, sealed.get(m.set_id))
        if f:
            feats.append(f)
            res.append(score_trough(f, m))
    return feats, res


if __name__ == "__main__":
    prices, metas, sealed = build()
    arche = {c[0]: c[5] for c in CARDS}

    for as_of in ["2022-09-01", "2024-09-01"]:
        print(f"\n=== Ranking modułu A na {as_of} ===")
        feats, res = ranking(prices, metas, sealed, pd.Timestamp(as_of))
        for r in sorted(res, key=lambda x: -x.score):
            if r.passed_gates:
                print(f"  {r.score:5.1f}  {r.name:<28} [{arche[r.card_id]}]  " + "; ".join(r.reasons[:2]))
        rejected = [r for r in res if not r.passed_gates]
        print(f"  odrzucone przez bramki: {len(rejected)}, np.:")
        for r in rejected[:4]:
            print(f"     - {r.name:<26} [{arche[r.card_id]}]: {r.reasons[0]}")

    print("\n=== Test na historii: decyzje co miesiąc 2022-03 … 2024-09, horyzont 24 mies., top 3 ===")
    picks, summary = run_backtest(prices, metas, sealed, "2022-03-01", "2024-09-01",
                                  horizon_months=24, top_n=3)
    s = summary.dropna(subset=["picks_median_return"])
    print(f"  miesięcy z wyborami: {len(s)} / {len(summary)}")
    print(f"  mediana zwrotu wybranych kart:   {s.picks_median_return.median():+.0%}")
    print(f"  mediana zwrotu bazy (IR+, tier≤2): {summary.base_median_return.median():+.0%}")
    print(f"  odsetek wyborów ≥2x: {s.picks_hit_rate_2x.mean():.0%}  vs baza: {summary.base_hit_rate_2x.mean():.0%}")
    picks["archetype"] = picks.card_id.map(arche)
    print("  jakie archetypy wybierał algorytm:")
    print(picks.archetype.value_counts().to_string().replace("\n", "\n    ").join(["    ", ""]))
