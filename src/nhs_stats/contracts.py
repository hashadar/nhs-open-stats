"""Data contracts: YAML column definitions validated against polars frames."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import polars as pl
import yaml

from nhs_stats.resources import contracts_dir

_DTYPES: dict[str, pl.DataType | type[pl.DataType]] = {
    "String": pl.String,
    "Int64": pl.Int64,
    "Float64": pl.Float64,
    "Date": pl.Date,
    "Datetime": pl.Datetime("us", "UTC"),
    "Boolean": pl.Boolean,
}


@dataclass(frozen=True)
class Column:
    name: str
    dtype: str
    description: str = ""
    nullable: bool = True
    pattern: str | None = None
    min: float | None = None


@dataclass(frozen=True)
class Contract:
    name: str
    version: int
    description: str
    columns: tuple[Column, ...]
    primary_key: tuple[str, ...] = field(default_factory=tuple)

    @property
    def column_names(self) -> list[str]:
        return [c.name for c in self.columns]

    def polars_schema(self) -> dict[str, pl.DataType | type[pl.DataType]]:
        return {c.name: _DTYPES[c.dtype] for c in self.columns}


@dataclass(frozen=True)
class Violation:
    column: str | None
    message: str


def load_contract(name: str, directory: Path | None = None) -> Contract:
    path = (directory or contracts_dir()) / f"{name}.yaml"
    raw: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8"))
    columns = tuple(Column(**c) for c in raw["columns"])
    unknown = {c.dtype for c in columns} - set(_DTYPES)
    if unknown:
        raise ValueError(f"Contract {name} uses unsupported dtypes: {sorted(unknown)}")
    return Contract(
        name=raw["name"],
        version=int(raw["version"]),
        description=raw.get("description", ""),
        columns=columns,
        primary_key=tuple(raw.get("primary_key", ())),
    )


def validate(df: pl.DataFrame, contract: Contract) -> list[Violation]:
    """Return every contract violation; an empty list means the frame conforms."""
    violations: list[Violation] = []
    expected = contract.polars_schema()

    missing = [n for n in expected if n not in df.columns]
    extra = [n for n in df.columns if n not in expected]
    violations += [Violation(n, "column missing") for n in missing]
    violations += [Violation(n, "column not in contract") for n in extra]

    for column in contract.columns:
        if column.name not in df.columns:
            continue
        series = df[column.name]
        if series.dtype != expected[column.name]:
            violations.append(
                Violation(column.name, f"dtype {series.dtype}, expected {column.dtype}")
            )
            continue
        if not column.nullable and series.null_count() > 0:
            violations.append(Violation(column.name, f"{series.null_count()} null values"))
        if column.pattern is not None:
            bad = series.drop_nulls().filter(~series.drop_nulls().str.contains(column.pattern))
            if len(bad) > 0:
                sample = bad.head(3).to_list()
                violations.append(
                    Violation(column.name, f"{len(bad)} values break /{column.pattern}/: {sample}")
                )
        if column.min is not None:
            below = int((series.drop_nulls() < column.min).sum())
            if below > 0:
                violations.append(Violation(column.name, f"{below} values below {column.min}"))

    if contract.primary_key and not missing:
        duplicates = df.select(contract.primary_key).is_duplicated().sum()
        if duplicates:
            violations.append(
                Violation(None, f"{duplicates} rows duplicate key {list(contract.primary_key)}")
            )
    return violations
