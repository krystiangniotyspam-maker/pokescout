"""Market/report date is the actual price observation, not future Sunday label."""
import json

import pandas as pd

import evaluate as ev


def test_market_json_uses_observed_at_not_future_week_label(tmp_path):
    panel = pd.DataFrame({
        "date": pd.to_datetime(["2026-09-20", "2026-10-04", "2026-10-18"]),
        "slope_90": [0.01, 0.02, 0.03],
        "slope_180": [0.0, 0.01, 0.04],
        "fwd_3": [0.2, 0.15, float("nan")],
        "fwd_6": [0.3, 0.1, float("nan")],
    })
    text = ev.market_section(panel, tmp_path, seen_at="2026-10-16")
    market = json.loads((tmp_path / "market.json").read_text())
    assert market["date"] == "2026-10-16"
    assert market["week_bucket_end"] == "2026-10-18"
    assert "ceny do 2026-10-16" in "\n".join(text)
