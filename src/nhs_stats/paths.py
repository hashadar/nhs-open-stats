"""Filesystem layout for the bronze and silver layers.

The same relative layout maps one-to-one onto S3 prefixes. Gold (multi-year serving
tables) is deferred; see docs/architecture.md.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DATA_DIR_ENV = "NHS_STATS_DATA_DIR"


@dataclass(frozen=True)
class DataPaths:
    root: Path

    @classmethod
    def from_env(cls, override: Path | None = None) -> DataPaths:
        if override is not None:
            return cls(override)
        return cls(Path(os.environ.get(DATA_DIR_ENV, "data")))

    def bronze_dir(self, source_id: str, month_label: str) -> Path:
        return self.root / "bronze" / source_id / f"reporting_month={month_label}"

    def silver_file(self, source_id: str, month_label: str) -> Path:
        return self.root / "silver" / source_id / f"reporting_month={month_label}" / "data.parquet"

    def quality_report(self, source_id: str, month_label: str) -> Path:
        return self.root / "quality" / source_id / f"{month_label}.json"

    @property
    def lineage_log(self) -> Path:
        return self.root / "lineage" / "runs.jsonl"

    def relative(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()
