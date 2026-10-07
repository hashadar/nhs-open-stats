"""Filesystem layout for the bronze, silver and gold layers.

The same relative layout maps one-to-one onto S3 prefixes.
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

    def silver_glob(self, source_id: str) -> str:
        return str(self.root / "silver" / source_id / "reporting_month=*" / "data.parquet")

    def gold_file(self, table: str) -> Path:
        return self.root / "gold" / table / f"{table}.parquet"

    def quality_report(self, source_id: str, month_label: str) -> Path:
        return self.root / "quality" / source_id / f"{month_label}.json"

    @property
    def lineage_log(self) -> Path:
        return self.root / "lineage" / "runs.jsonl"

    def relative(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()
