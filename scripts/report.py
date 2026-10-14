"""Raport: ocena kart na dziś + wysyłka na Discord.

Zmienne środowiskowe (GitHub Secrets):
  DISCORD_WEBHOOK_RAPORT – kanał z raportem (wymagany do wysyłki; bez niego raport tylko w logu)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pokescout import card_features, score_relative_value, score_trough  # noqa: E402
from pokescout.data import load_repo_history  # noqa: E402

MIN_DAYS_FOR_SCORING = 56  # algorytm potrzebuje min. 8 tygodni historii


def build_report() -> str:
    prices, metas, sealed, n_days = load_repo_history(ROOT / "data")
    if not n_days:
        return "PokeScout: brak danych – codzienne zbieranie jeszcze nie ruszyło."
    as_of = max(s.index.max() for s in prices.values())
    lines = [f"**PokeScout – {as_of:%Y-%m-%d}**",
             f"Śledzone karty: {len(metas)} · dni historii: {n_days}"]

    if n_days < MIN_DAYS_FOR_SCORING:
        lines.append(f"Zbieram dane – oceny ruszą po ok. {MIN_DAYS_FOR_SCORING} dniach "
                     f"(zostało {MIN_DAYS_FOR_SCORING - n_days}). Szybciej po wczytaniu historii z PokemonPriceTracker.")
        return "\n".join(lines)

    feats, res = [], []
    for cid, m in metas.items():
        f = card_features(cid, prices[cid], m.release_date, as_of, sealed.get(m.set_id))
        if f:
            feats.append(f)
            res.append(score_trough(f, m))
    top_a = sorted([r for r in res if r.passed_gates], key=lambda r: -r.score)[:10]
    top_b = score_relative_value(feats, metas)[:10]

    lines.append("\n__Dołki (moduł A)__")
    lines += [f"`{r.score:5.1f}` **{r.name}** – {r.reasons[0]}" for r in top_a] or ["brak kandydatów"]
    lines.append("\n__Niedoszacowane (moduł B1)__")
    lines += [f"`{r.score:5.1f}` **{r.name}** – {r.reasons[0]}" for r in top_b] or ["brak kandydatów"]
    lines.append("\n_Ceny: TCGplayer (USD). To lista do sprawdzenia, nie rekomendacja zakupu._")
    return "\n".join(lines)


def send_discord(text: str) -> None:
    url = os.getenv("DISCORD_WEBHOOK_RAPORT")
    if not url:
        print("Brak DISCORD_WEBHOOK_RAPORT – pomijam wysyłkę.")
        return
    chunks, buf = [], ""
    for line in text.splitlines():  # limit Discorda: 2000 znaków na wiadomość
        if len(buf) + len(line) + 1 > 1900:
            chunks.append(buf)
            buf = ""
        buf += line + "\n"
    chunks.append(buf)
    for ch in chunks:
        r = requests.post(url, json={"content": ch}, timeout=30)
        r.raise_for_status()


if __name__ == "__main__":
    report = build_report()
    print(report)
    if "--send" in sys.argv:
        send_discord(report)
