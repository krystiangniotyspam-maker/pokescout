"""Ocena kart na wybrany dzień.

Użycie:
    python run.py --prices prices.csv --cards cards.csv --sealed sealed.csv --as-of 2026-10-14
"""
import argparse

import pandas as pd

from pokescout import card_features, score_relative_value, score_trough


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prices", required=True)
    ap.add_argument("--cards", required=True)
    ap.add_argument("--sealed")
    ap.add_argument("--as-of", default=pd.Timestamp.today().strftime("%Y-%m-%d"))
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--out", default="ranking.csv")
    a = ap.parse_args()

    from pokescout.data import load
    prices, metas, sealed = load(a.prices, a.cards, a.sealed)
    as_of = pd.Timestamp(a.as_of)

    feats, results = [], []
    for cid, m in metas.items():
        f = card_features(cid, prices[cid], m.release_date, as_of, sealed.get(m.set_id))
        if f is None:
            continue
        feats.append(f)
        results.append(score_trough(f, m))
    results += score_relative_value(feats, metas)

    rows = [dict(module=r.module, card_id=r.card_id, name=r.name, score=r.score,
                 passed=r.passed_gates, reasons=" | ".join(r.reasons)) for r in results]
    df = pd.DataFrame(rows).sort_values(["module", "score"], ascending=[True, False])
    df.to_csv(a.out, index=False)

    for mod, title in [("A", "DOŁKI (moduł A)"), ("B1", "NIEDOSZACOWANE (moduł B1)")]:
        print(f"\n=== {title} ===")
        top = df[(df.module == mod) & df.passed].head(a.top)
        if top.empty:
            print("brak kandydatów")
        for r in top.itertuples():
            print(f"{r.score:5.1f}  {r.name:<35} {r.reasons}")


if __name__ == "__main__":
    main()
