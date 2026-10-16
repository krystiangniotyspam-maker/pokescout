"""Log wyborów na żywo: tylko dopisywany, z wersją modelu i dniem cen (PROTOCOL.md, Issue #13)."""
from pathlib import Path

import pandas as pd

import evaluate as ev

ROOT = Path(__file__).resolve().parents[1]


def _fake(n=30):
    d = pd.Timestamp("2026-10-18")
    panel = pd.DataFrame({"date": [d] * n, "card_id": [str(i) for i in range(n)],
                          **{f"{k}_{h}": [float("nan")] * n for k in ("ex", "net") for h in (3, 6)}})
    rank = pd.DataFrame({"card_id": [str(i) for i in range(n)], "name": "x", "price_now": 50.0,
                         "score": 1.0, "szansa_50": 0.5, "model_6m": 0.1, "combo": 0.0})
    return panel, rank


def test_rerun_same_model_does_not_overwrite(tmp_path):
    panel, rank = _fake()
    ev.track_live(panel, rank, tmp_path, seen_at="2026-10-16", run_at="2026-10-16T10:00:00Z")
    rank2 = rank.iloc[::-1]  # inna kolejność, ale ta sama wersja modelu
    ev.track_live(panel, rank2, tmp_path, seen_at="2026-10-16", run_at="2026-10-16T12:00:00Z")
    log = pd.read_csv(tmp_path / "picks_log.csv", dtype={"card_id": str})
    assert len(log) == ev.TOP_K
    assert list(log.card_id) == [str(i) for i in range(ev.TOP_K)]


def test_new_model_appends_and_first_run_counts(tmp_path, monkeypatch):
    panel, rank = _fake()
    ev.track_live(panel, rank, tmp_path, seen_at="2026-10-16", run_at="2026-10-16T10:00:00Z")
    monkeypatch.setattr(ev, "model_sha", lambda: "inny")
    ev.track_live(panel, rank.iloc[::-1], tmp_path, seen_at="2026-10-16", run_at="2026-10-16T12:00:00Z")
    log = pd.read_csv(tmp_path / "picks_log.csv", parse_dates=["date"], dtype={"card_id": str})
    assert len(log) == 2 * ev.TOP_K
    first = ev.first_runs(log)
    assert len(first) == ev.TOP_K and (first.run_at == "2026-10-16T10:00:00Z").all()


def test_old_rows_without_run_at_count_as_first():
    log = pd.DataFrame({"date": ["2026-10-18"] * 4, "card_id": list("abcd"),
                        "run_at": [None, None, "2026-10-19T08:00:00Z", "2026-10-19T08:00:00Z"]})
    assert list(ev.first_runs(log).card_id) == ["a", "b"]


def test_observed_at_is_latest_price_file(tmp_path):
    for day in ("2026/10/14", "2026/10/16"):
        f = tmp_path / "prices" / f"{day}.csv.gz"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b"")
    assert ev.observed_at(tmp_path) == "2026-10-16"


def test_logged_picks_never_after_latest_snapshot():
    """Żaden zapisany sygnał nie może mieć dnia cen późniejszego niż najnowszy snapshot ani niż dzień przebiegu."""
    log_f = ROOT / "reports" / "picks_log.csv"
    if not log_f.exists():
        return
    log = pd.read_csv(log_f)
    if "observed_at" not in log:
        return
    seen = log.dropna(subset=["observed_at"])
    latest = ev.observed_at(ROOT / "data")
    assert (seen.observed_at <= latest).all()
    assert (seen.observed_at <= seen.run_at.str[:10]).all()
