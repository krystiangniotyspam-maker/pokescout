"""Point-in-time audit trail for PokeScout picks, revisions and legacy rows (Issue #13, B.1)."""
from pathlib import Path

import pandas as pd
import pytest

import evaluate as ev
from pokescout.provenance import data_snapshot_hash

ROOT = Path(__file__).resolve().parents[1]
HASH_1 = "a" * 64
HASH_2 = "b" * 64


def _fake(n=30):
    # Friday observation/decision is assigned the following Sunday bucket.
    d = pd.Timestamp("2026-10-18")
    panel = pd.DataFrame({"date": [d] * n, "card_id": [str(i) for i in range(n)],
                          **{f"{k}_{h}": [float("nan")] * n for k in ("ex", "net") for h in (3, 6)}})
    rank = pd.DataFrame({"card_id": [str(i) for i in range(n)], "name": "x", "price_now": 50.0,
                         "score": 1.0, "szansa_50": 0.5, "model_6m": 0.1, "combo": 0.0})
    return panel, rank


def _track(panel, rank, folder, *, run_at="2026-10-16T10:00:00Z", snap=HASH_1, seen_at="2026-10-16"):
    return ev.track_live(panel, rank, folder, run_at=run_at, seen_at=seen_at,
                         snapshot_hash=snap, source_sha="testing-git-revision")


def _read(folder):
    return pd.read_csv(folder / "picks_log.csv", parse_dates=["date"], dtype={"card_id": str})


def test_rerun_same_model_and_snapshot_does_not_overwrite(tmp_path):
    panel, rank = _fake()
    _track(panel, rank, tmp_path)
    _track(panel, rank.iloc[::-1], tmp_path, run_at="2026-10-16T12:00:00Z")
    log = _read(tmp_path)
    assert len(log) == ev.TOP_K
    assert list(log.card_id) == [str(i) for i in range(ev.TOP_K)]


def test_new_model_appends_and_first_run_counts(tmp_path, monkeypatch):
    panel, rank = _fake()
    _track(panel, rank, tmp_path)
    monkeypatch.setattr(ev, "model_sha", lambda: "inny")
    _track(panel, rank.iloc[::-1], tmp_path, run_at="2026-10-16T12:00:00Z")
    log = _read(tmp_path)
    assert len(log) == 2 * ev.TOP_K
    first = ev.first_runs(log)
    assert len(first) == ev.TOP_K and (first.run_at == "2026-10-16T10:00:00Z").all()


def test_new_data_same_model_appends_revision_but_original_remains(tmp_path):
    panel, rank = _fake()
    _track(panel, rank, tmp_path)
    _track(panel, rank.iloc[::-1], tmp_path, snap=HASH_2, run_at="2026-10-16T12:00:00Z")
    log = _read(tmp_path)
    assert len(log) == ev.TOP_K * 2
    assert set(log.data_snapshot_hash) == {HASH_1, HASH_2}
    assert log.run_id.nunique() == 2
    assert log.model_sha.nunique() == 1
    assert log.week_bucket_end.nunique() == 1
    assert set(log.decision_at) == {"2026-10-16"}
    assert set(log.observed_at) == {"2026-10-16"}
    assert (log.date == pd.Timestamp("2026-10-18")).all()
    assert (log.market == "TCGplayer_USD").all()
    assert (log.variant == "unverified").all()
    assert log.instrument_id.str.startswith("tcgplayer:").all()
    original = ev.first_runs(log)
    assert list(original.card_id) == [str(i) for i in range(ev.TOP_K)]
    assert (original.data_snapshot_hash == HASH_1).all()


def test_second_observation_in_same_week_retains_first_forecast(tmp_path):
    panel, rank = _fake()
    _track(panel, rank, tmp_path)
    _track(panel, rank.iloc[::-1], tmp_path, run_at="2026-10-17T12:00:00Z",
           seen_at="2026-10-17", snap=HASH_2)
    log = _read(tmp_path)
    assert len(ev.first_runs(log)) == ev.TOP_K
    assert set(log.decision_at) == {"2026-10-16", "2026-10-17"}


def test_future_observation_rejected_before_writing(tmp_path):
    panel, rank = _fake()
    with pytest.raises(ValueError, match="observed_at"):
        _track(panel, rank, tmp_path, seen_at="2026-10-18")
    assert not (tmp_path / "picks_log.csv").exists()


def test_legacy_rows_are_preserved_as_primary(tmp_path):
    panel, rank = _fake()
    old = pd.DataFrame([{
        "date": "2026-10-18", "rank": 1, "card_id": "legacy", "name": "original",
        "price_now": 10, "score": 0.9, "szansa_50": 0.2,
        "model_6m": 0.01, "combo": 0.0,
    }])
    old.to_csv(tmp_path / "picks_log.csv", index=False)
    _track(panel, rank, tmp_path)
    log = _read(tmp_path)
    assert len(log) == ev.TOP_K + 1
    assert log.iloc[0].card_id == "legacy"
    assert pd.isna(log.iloc[0].get("decision_at"))
    assert list(ev.first_runs(log).card_id) == ["legacy"]


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


def test_hash_uses_file_contents_not_mtime(tmp_path):
    path = tmp_path / "prices" / "2026" / "10" / "16.csv.gz"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"price A")
    h1 = data_snapshot_hash(tmp_path)
    path.touch()
    assert data_snapshot_hash(tmp_path) == h1
    path.write_bytes(b"price B")
    assert data_snapshot_hash(tmp_path) != h1
    path.unlink()
    with pytest.raises(FileNotFoundError):
        data_snapshot_hash(tmp_path)


def test_hash_changes_when_reddit_or_catalog_files_change(tmp_path):
    price = tmp_path / "prices" / "p.csv.gz"
    price.parent.mkdir()
    price.write_bytes(b"one")
    initial = data_snapshot_hash(tmp_path)
    catalog = tmp_path / "catalog" / "cards.csv"
    catalog.parent.mkdir()
    catalog.write_text("two")
    assert data_snapshot_hash(tmp_path) != initial


def test_logged_picks_have_truthful_decision_at():
    """Old rows have no metadata; new rows must have actual decision_at <= run_at."""
    log_f = ROOT / "reports" / "picks_log.csv"
    if not log_f.exists():
        return
    log = pd.read_csv(log_f)
    if not {"observed_at", "decision_at", "run_at"}.issubset(log.columns):
        return
    new = log.dropna(subset=["observed_at", "decision_at", "run_at"])
    if new.empty:
        return
    latest = ev.observed_at(ROOT / "data")
    assert (new.observed_at <= latest).all()
    assert (new.observed_at <= new.decision_at).all()
    assert (new.decision_at <= new.run_at.str[:10]).all()
