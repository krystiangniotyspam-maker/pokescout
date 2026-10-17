"""Zabezpieczenie przed ponownym opublikowaniem wycofanych prognoz w artefaktach.

Issue #13, PR A.1: pliki na main to publikacja, nie tylko cache pipeline.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

LEGACY_COLUMNS = {
    "potencjal_rok",
    "potencjal_od",
    "potencjal_do",
    "potencjal_slaby",
    "szansa_50",
}


def test_public_rankings_do_not_publish_unvalidated_forecasts():
    for filename in ("ranking.csv", "ranking_tanie.csv"):
        with (REPORTS / filename).open(encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            assert reader.fieldnames is not None
            assert not LEGACY_COLUMNS.intersection(reader.fieldnames), filename
            assert "przedzial" in reader.fieldnames, filename
            for row in reader:
                assert row["przedzial"], filename


def test_published_report_contains_no_withdrawn_return_predictions():
    report = (REPORTS / "raport.md").read_text(encoding="utf-8")
    for forbidden in (
        "📈 **za rok",
        "🌧️ w słabym rynku",
        "Za 2–3 lata",
        "za rok ok.",
    ):
        assert forbidden not in report, forbidden


def test_original_picks_log_preserved_as_separate_audit_trail():
    """Sanity check: historical log remains separate from published ranking artifacts."""
    assert (REPORTS / "picks_log.csv").is_file()
