"""Lightweight run lineage: one JSON line per pipeline run, OpenLineage-shaped."""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

from nhs_stats import __version__
from nhs_stats.paths import DataPaths


@dataclass
class Dataset:
    layer: str
    path: str
    sha256: str | None = None
    rows: int | None = None


@dataclass
class RunRecord:
    job: str
    started_at: str
    ended_at: str = ""
    result: str = "running"
    inputs: list[Dataset] = field(default_factory=list)
    outputs: list[Dataset] = field(default_factory=list)
    quality_report: str | None = None
    code_version: str = field(
        default_factory=lambda: f"{__version__}+{os.environ.get('NHS_STATS_GIT_SHA', 'unknown')}"
    )
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append(record: RunRecord, paths: DataPaths) -> None:
    paths.lineage_log.parent.mkdir(parents=True, exist_ok=True)
    with paths.lineage_log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(record)) + "\n")
