"""Reproducible provenance for PokeScout input snapshots and model runs (Issue #13, B.1).

A fingerprint identifies *all currently available files used as pipeline inputs*, not
just a date or a Git commit. The raw files must still be retained to reproduce a run.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

# Inputs to the current price/feature pipeline, Reddit signals and Cardmarket sealed ranking.
INPUT_DIRS = ("prices", "catalog", "buzz", "cardmarket")


def data_snapshot_hash(data_dir: str | Path) -> str:
    """SHA-256 over ordered relative paths and exact file bytes, not mutable mtimes.

    Stream contents instead of loading all daily/history CSVs into RAM.
    Adding/removing any input file changes the fingerprint.
    """
    root = Path(data_dir)
    files = sorted(
        (p for folder in INPUT_DIRS for p in (root / folder).rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(root).as_posix(),
    )
    if not files:
        raise FileNotFoundError(f"No PokeScout input files under {root}")

    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def code_commit_sha(repo_root: str | Path) -> str:
    """Best available source-code Git commit SHA for audit; never assume data is committed."""
    env_sha = os.environ.get("GITHUB_SHA", "")
    if env_sha:
        return env_sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, stderr=subprocess.DEVNULL,
            text=True, timeout=5,
        ).strip()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "unknown"
