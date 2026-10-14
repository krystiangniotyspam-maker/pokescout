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

from pokescout.buzz import buzz_features, load_reddit  # noqa: E402
from pokescout.data import load_repo_history  # noqa: E402
from pokescout.tiers import pokemon_key  # noqa: E402
from pokescout.evaluate import (FEATURES, HORIZONS, build_panel, combo_score, evaluate_scores,  # noqa: E402
                                fit_latest, walk_forward)

REPORTS = ROOT / "reports"
TOP_K = 20
UP = "model: szansa na wzrost o 50%+"
MAIN = "ranking: szansa na +50% + model zwrotu"  # główny ranking: największy wzrost w perspektywie roku
MIN_INVEST = 20.0  # USD – ranking i kontrola na żywo tylko dla kart, na których koszty nie zjadają zysku


def fmt(df: pd.DataFrame) -> str:
    d = df.copy()
    for c in ("ic", "ic_t_adj"):
        d[c] = d[c].map(lambda x: f"{x:+.3f}" if c == "ic" else f"{x:+.1f}")
    d["top_excess"] = d["top_excess"].map(lambda x: f"{x:+.1%}")
    d["top_hit_rate"] = d["top_hit_rate"].map(lambda x: f"{x:.0%}")
    d["top_net"] = d["top_net"].map(lambda x: f"{x:+.1%}")
    return d.to_markdown(index=False)


def market_section(panel: pd.DataFrame) -> list[str]:
    """Kiedy kupować: tempo całego rynku (mediana trendów kart) a późniejszy zwrot mediany rynku."""
    idx = panel.groupby("date").agg(trend_90=("slope_90", "median"), trend_180=("slope_180", "median"),
                                    zwrot_3m=("fwd_3", "median"), zwrot_6m=("fwd_6", "median"))
    corr = idx.corr(method="spearman").loc[["trend_90", "trend_180"], ["zwrot_3m", "zwrot_6m"]]
    now = idx.iloc[-1]
    pct = lambda c: (idx[c] <= now[c]).mean()
    return ["## Rynek: kiedy kupować", "",
            "Trend rynku = mediana trendów cen wszystkich kart (%/mies.). Na historii szybki wzrost rynku "
            "zapowiadał słabsze kolejne miesiące, a spokojny lub spadający rynek – lepsze (korelacja rang poniżej; "
            "to tylko ok. 2 cykle, więc traktuj orientacyjnie).", "",
            corr.round(2).to_markdown(), "",
            f"Teraz ({idx.index[-1]:%Y-%m-%d}): trend 90 dni {now.trend_90:+.1%}/mies. "
            f"(wyżej niż w {pct('trend_90'):.0%} historii), trend 180 dni {now.trend_180:+.1%}/mies. "
            f"(wyżej niż w {pct('trend_180'):.0%} historii).", ""]


def track_live(panel: pd.DataFrame, rank: pd.DataFrame, reports: Path) -> list[str]:
    """Kontrola na żywo: zapisuje top-20 z każdego dnia rankingu i rozlicza je, gdy minie horyzont.

    Te wybory powstały bez znajomości przyszłości, więc to jedyny test, którego nie da się
    (nawet nieświadomie) dopasować do historii."""
    log_f = reports / "picks_log.csv"
    log = pd.read_csv(log_f, parse_dates=["date"], dtype={"card_id": str}) if log_f.exists() else pd.DataFrame()
    today = panel.date.max()
    if len(log):  # ponowny przebieg w tym samym tygodniu nadpisuje jego wybory
        log = log[log.date != today]
    top = rank.head(TOP_K).assign(date=today, rank=range(1, min(TOP_K, len(rank)) + 1))
    new = top[["date", "rank", "card_id", "name", "price_now", "score", "szansa_50", "model_6m", "combo"]]
    log = pd.concat([log, new], ignore_index=True) if len(log) else new
    log.to_csv(log_f, index=False)
    lines = ["## Kontrola na żywo", "",
             f"Każdy przebieg zapisuje top-{TOP_K} do `reports/picks_log.csv`; po 3 i 6 mies. liczymy, jak wypadły.", ""]
    rows = []
    p = panel.assign(card_id=panel.card_id.astype(str))
    for h in (3, 6):
        j = log.merge(p[["date", "card_id", f"ex_{h}", f"net_{h}"]], on=["date", "card_id"], how="left")
        done = j[j[f"ex_{h}"].notna()]
        for d, g in done.groupby("date"):
            rows.append(dict(data=f"{d:%Y-%m-%d}", horyzont=f"{h} mies.", kart=len(g),
                             ponad_rynek=f"{np.expm1(g[f'ex_{h}'].mean()):+.1%}",
                             pobilo_rynek=f"{(g[f'ex_{h}'] > 0).mean():.0%}",
                             netto=f"{g[f'net_{h}'].mean():+.1%}"))
    if rows:
        lines += [pd.DataFrame(rows).to_markdown(index=False), ""]
    else:
        lines += [f"Zapisane dni z wyborami: {log.date.nunique()}. Pierwsze wyniki po 3 mies. "
                  f"od {log.date.min():%Y-%m-%d}.", ""]
    return lines


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
    posts = load_reddit(a.data)
    buzz = buzz_features(posts, {pokemon_key(m.name) for m in metas.values()}) if len(posts) else None
    print(f"Posty z Reddita: {len(posts)}")
    low, *_ = load_repo_history(a.data, price_col="low")
    panel = build_panel(prices, metas, sealed, buzz=buzz, low_prices=low)
    print(f"Panel: {len(panel)} wierszy, {panel.date.nunique()} dat, {panel.card_id.nunique()} kart")
    reports.mkdir(exist_ok=True)

    lines = ["# PokeScout – test przewidywań na historii", "",
             f"Dane: {n_days} dni notowań, {len(metas)} kart w katalogu; panel {len(panel)} obserwacji "
             f"({panel.date.min():%Y-%m-%d} – {panel.date.max():%Y-%m-%d}, co 2 tygodnie).", "",
             "**Jak czytać:** IC = korelacja rang oceny ze zwrotem ponad rynek (0 = brak związku, "
             "0,05 = użyteczny sygnał w finansach, 0,1+ = mocny). `ic_t_adj` > 2 = raczej nie przypadek. "
             f"`top_excess` = średni zwrot {TOP_K} najwyżej ocenionych kart ponad medianę rynku, "
             "`top_hit_rate` = jaki odsetek z nich pobił rynek, `top_net` = ich średni zwrot netto po kosztach "
             "(prowizja 13% i wysyłka $1,5 w każdą stronę) – realny zysk, nie ponad rynek, "
             "`top_up50` = jaki odsetek z nich zdrożał o 50% lub więcej.", ""]

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
        # przy 12 mies. za mało dat, by uczyć na wynikach rocznych: modele uczone na 6 mies.
        # (bez zaglądania w przyszłość – walk_forward bierze tylko wyniki znane w dniu decyzji)
        mh = min(h, 6)
        scores["model: gradient boosting"] = walk_forward(panel, mh, model="gbm")
        scores["model: ridge na rangach"] = walk_forward(panel, mh, model="ridge")
        scores["model: gradient boosting, cel zysk netto"] = walk_forward(panel, mh, model="gbm", target="exn")
        rk = lambda x: x.groupby(panel.date).rank(pct=True)
        scores["łącznie: model + ocena C"] = rk(scores["model: gradient boosting"]) + rk(combo)
        scores[UP] = walk_forward(panel, mh, target="up50")
        scores[MAIN] = rk(scores[UP]) + rk(scores["model: gradient boosting"])
        res = evaluate_scores(panel, scores, h, top_k=TOP_K)
        res.to_csv(reports / f"evaluation_{h}m.csv", index=False)

        known = panel[panel[y].notna()]
        gated = known[known.rule_a_pass]
        lines += [f"## Horyzont {h} mies.", "",
                  f"Daty z wynikiem: {known.date.nunique()}. Karty, które przeszły bramki modułu A: "
                  f"{len(gated)} obserwacji, średni zwrot ponad rynek "
                  f"{np.expm1(gated[y].mean()) if len(gated) else float('nan'):+.1%}.", "",
                  fmt(res), ""]
        main_inv = [MAIN, UP, "łącznie: model + ocena C", "model: gradient boosting", "model: gradient boosting, cel zysk netto",
                    "ocena C: popularność + wiek + tania + dno", "reguły: moduł B1 (tania vs podobne)",
                    "reguły: moduł A (ocena bez bramek)"]
        inv = evaluate_scores(panel, {k: scores[k] for k in main_inv}, h, top_k=TOP_K, min_price=MIN_INVEST)
        lines += [f"Tylko karty od ${MIN_INVEST:.0f} (przy tańszych koszty zjadają zysk):", "", fmt(inv), ""]
        if True:  # czy sygnał działa w obu połowach okresu (inny stan rynku)
            dates = sorted(known.date.unique())
            mid = dates[len(dates) // 2]
            main = [MAIN, UP, "łącznie: model + ocena C", "ocena C: popularność + wiek + tania + dno", "reguły: moduł A (ocena bez bramek)",
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
    model_net = fit_latest(panel, 6, target="exn")
    model_up = fit_latest(panel, 6, target="up50")
    now = panel[panel.date == panel.date.max()].copy()
    now["model_6m"] = model.predict(now[FEATURES])
    now["model_net_6m"] = model_net.predict(now[FEATURES])
    now["szansa_50"] = model_up.predict_proba(now[FEATURES])[:, 1]
    inv = now[now.price_now >= MIN_INVEST]
    now["score"] = (inv["szansa_50"].rank(pct=True) + inv["model_6m"].rank(pct=True)) / 2
    cols = ["card_id", "name", "set_name", "price_now", "score", "szansa_50", "model_6m", "combo", "spread", "poke_pop",
            "rv_z", "weeks_since_low", "buzz_share", "model_net_6m"]
    rank = now[now.price_now >= MIN_INVEST].sort_values("score", ascending=False)[cols]
    rank.to_csv(reports / "ranking.csv", index=False)
    lines += ["## Bieżący ranking modelu (6 mies., karty od $20)", "",
              f"Stan na {panel.date.max():%Y-%m-%d}. Kolejność wg `score` (0–1, wyżej = lepiej) = średnia rang modelu "
              "szukającego kart, które zdrożeją o 50%+ (`szansa_50`), i modelu zwrotu (`model_6m`); "
              "w teście ta para najlepiej wybierała karty na rok (sekcja 12 mies.). `szansa_50` porządkuje karty, ale nie jest prawdziwym "
              "prawdopodobieństwem – faktyczny odsetek wzrostów o 50%+ zależy głównie od stanu całego rynku. "
              "`model_6m` = przewidywany log-zwrot ponad rynek w 6 mies. "
              "(0,20 ≈ +22%), `model_net_6m` = to samo po kosztach, "
              "`spread` = log(cena rynkowa / najniższa oferta). To lista do sprawdzenia, nie rekomendacja zakupu.", "",
              rank.drop(columns="card_id").head(25).to_markdown(index=False, floatfmt=".2f"), ""]
    lines += market_section(panel)
    lines += track_live(panel, rank, reports)
    (reports / "evaluation.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
