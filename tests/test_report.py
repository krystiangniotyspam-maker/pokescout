"""Raport pokazuje przedział rankingu i historię, bez niezwalidowanych prognoz (Issue #13)."""
import numpy as np
import pandas as pd

import evaluate as ev
import notify_discord as nd


def test_card_potential_uses_percentile_not_raw_score():
    # score = średnia dwóch rang: rozkład nie jest równomierny, więc surowy score źle trafia w przedziały
    rng = np.random.default_rng(0)
    a, b = rng.random(1000), rng.random(1000)
    cards = pd.DataFrame({"score": (pd.Series(a).rank(pct=True) + pd.Series(b).rank(pct=True)) / 2})
    out = ev.card_potential(cards, pd.DataFrame())
    assert (out.przedzial == "górne 5%").sum() == 50
    assert (out.przedzial == "5–10% od góry").sum() == 50
    assert (out.przedzial == "górne 50%").sum() == 0  # najniższy przedział to „50–100% od góry”


def test_potential_table_takes_weaker_half():
    dates = pd.date_range("2025-01-05", periods=10, freq="14D")
    rows = []
    for i, d in enumerate(dates):
        for k in range(200):
            ret = 0.5 if i < 5 else 0.1  # pierwsza połowa dat lepsza od drugiej
            rows.append(dict(date=d, fwd_12=np.log1p(ret), price_now=100.0, s=k))
    panel = pd.DataFrame(rows)
    t = ev.potential_table(panel, panel.s)
    assert np.allclose(t.mediana, 0.1)


def test_card_line_has_no_forecast_amounts():
    r = pd.Series(dict(card_id=1, name="Eevee - 188/167", set_name="SV: Twilight Masquerade", price_now=69.0,
                       przedzial="górne 5%", dlaczego="popularny Pokémon"))
    line = nd._card_line(1, r, {})
    assert "📊 ranking: górne 5%" in line
    assert "za rok" not in line and "→" not in line and "🌧️" not in line
