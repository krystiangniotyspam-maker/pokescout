"""Test przewidywań na historii z repo + bieżący ranking modelu.

    python scripts/evaluate.py            # raport w reports/evaluation.md i reports/ranking.csv

Porównuje: obecne reguły (moduł A i B1), pojedyncze cechy i model uczony (walk-forward).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pokescout.data import load_repo_history  # noqa: E402
from pokescout.evaluate import (FEATURES, HORIZONS, build_panel, combo_score, evaluate_scores,  # noqa: E402
                                fit_latest, walk_forward)

REPORTS = ROOT / "reports"
TOP_K = 20


def fmt(df: pd.DataFrame) -> str:
    d = df.copy()
    for c in ("ic", "ic_t_adj"):
        d[c] = d[c].map(lambda x: f"{x:+.3f}" if c == "ic" else f"{x:+.1f}")
    d["top_excess"] = d["top_excess"].map(lambda x: f"{x:+.1%}")
    d["top_hit_rate"] = d["top_hit_rate"].map(lambda x: f"{x:.0%}")
    return d.to_markdown(index=False)


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "data"))
    ap.add_argument("--reports", default=str(REPORTS))
    a = ap.parse_args()
    reports = Path(a.reports)
    prices, metas, sealed, n_days = load_repo_history(a.data)
    if not n_days:
        print("Brak danych w data/prices")
        return 1
    panel = build_panel(prices, metas, sealed)
    print(f"Panel: {len(panel)} wierszy, {panel.date.nunique()} dat, {panel.card_id.nunique()} kart")
    reports.mkdir(exist_ok=True)

    lines = ["# PokeScout – test przewidywań na historii", "",
             f"Dane: {n_days} dni notowań, {len(metas)} kart w katalogu; panel {len(panel)} obserwacji "
             f"({panel.date.min():%Y-%m-%d} – {panel.date.max():%Y-%m-%d}, co 2 tygodnie).", "",
             "**Jak czytać:** IC = korelacja rang oceny ze zwrotem ponad rynek (0 = brak związku, "
             "0,05 = użyteczny sygnał w finansach, 0,1+ = mocny). `ic_t_adj` > 2 = raczej nie przypadek. "
             f"`top_excess` = średni zwrot {TOP_K} najwyżej ocenionych kart ponad medianę rynku, "
             "`top_hit_rate` = jaki odsetek z nich pobił rynek.", ""]

    combo = combo_score(panel)
    panel["combo"] = combo
    for h in HORIZONS:
        y = f"ex_{h}"
        if panel[y].notna().sum() == 0:
            continue
        scores = {f"cecha: {c}": panel[c] for c in FEATURES}
        scores |= {f"cecha: −{c}": -panel[c] for c in ("drawdown", "rv_z", "slope_90", "range_pos_180")}
        scores["reguły: moduł A (ocena bez bramek)"] = panel["rule_a"]
        scores["reguły: moduł B1 (tania vs podobne)"] = -panel["rv_z"]
        scores["ocena C: popularność + wiek + tania + dno"] = combo
        scores["model: gradient boosting"] = walk_forward(panel, h, model="gbm")
        scores["model: ridge na rangach"] = walk_forward(panel, h, model="ridge")
        res = evaluate_scores(panel, scores, h, top_k=TOP_K)
        res.to_csv(reports / f"evaluation_{h}m.csv", index=False)

        known = panel[panel[y].notna()]
        gated = known[known.rule_a_pass]
        lines += [f"## Horyzont {h} mies.", "",
                  f"Daty z wynikiem: {known.date.nunique()}. Karty, które przeszły bramki modułu A: "
                  f"{len(gated)} obserwacji, średni zwrot ponad rynek "
                  f"{np.expm1(gated[y].mean()) if len(gated) else float('nan'):+.1%}.", "",
                  fmt(res), ""]
        if h <= 6:  # czy sygnał działa w obu połowach okresu (inny stan rynku)
            dates = sorted(known.date.unique())
            mid = dates[len(dates) // 2]
            main = ["ocena C: popularność + wiek + tania + dno", "reguły: moduł A (ocena bez bramek)",
                    "reguły: moduł B1 (tania vs podobne)", "cecha: weeks_since_low", "cecha: −drawdown",
                    "model: gradient boosting"]
            rows = []
            for label, part in (("1. połowa", panel.date < mid), ("2. połowa", panel.date >= mid)):
                r = evaluate_scores(panel[part], {k: scores[k][part] for k in main}, h, top_k=TOP_K)
                r.insert(0, "okres", f"{label} (od {panel[part].date.min():%Y-%m})")
                rows.append(r)
            lines += [f"Stabilność ({h} mies.): ten sam test osobno w pierwszej i drugiej połowie okresu.", "",
                      fmt(pd.concat(rows)), ""]

    model = fit_latest(panel, 6)
    now = panel[panel.date == panel.date.max()].copy()
    now["model_6m"] = model.predict(now[FEATURES])
    cols = ["name", "set_name", "price_now", "age_months", "poke_pop", "rv_z", "weeks_since_low",
            "combo", "model_6m", "rule_a_pass"]
    rank = now.sort_values("model_6m", ascending=False)[cols]
    rank.to_csv(reports / "ranking.csv", index=False)
    lines += ["## Bieżący ranking modelu (6 mies.)", "",
              f"Stan na {panel.date.max():%Y-%m-%d}. `model_6m` = przewidywany przez model log-zwrot ponad rynek "
              "w 6 mies. (0,30 ≈ +35%), `combo` = ocena C dla porównania (wyżej = lepiej). "
              "To lista do sprawdzenia, nie rekomendacja zakupu.", "",
              rank.head(25).to_markdown(index=False, floatfmt=".2f"), ""]
    (reports / "evaluation.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
