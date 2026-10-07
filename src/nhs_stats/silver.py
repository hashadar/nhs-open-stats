"""Silver layer: typed, renamed, validated provider-month tables."""

from __future__ import annotations

import io
from datetime import date, datetime

import polars as pl

from nhs_stats.sources import ae_monthly as ae


class SchemaDriftError(ValueError):
    """The raw file no longer matches the layout this module understands."""


def read_raw(content: bytes) -> pl.DataFrame:
    return pl.read_csv(io.BytesIO(content), infer_schema=False, encoding="utf8-lossy")


def _to_count(column: str) -> pl.Expr:
    cleaned = pl.col(column).str.strip_chars().str.replace_all(",", "")
    return (
        pl.when(cleaned.is_in(["", "-", "*", "n/a"]))
        .then(None)
        .otherwise(cleaned)
        .cast(pl.Float64, strict=False)
        .cast(pl.Int64, strict=False)
        .alias(column)
    )


def clean_ae_monthly(
    raw: pl.DataFrame,
    *,
    month_label: str,
    quality_tier: str,
    status: str,
    source_sha256: str,
    ingested_at: datetime,
) -> tuple[pl.DataFrame, pl.DataFrame]:
    """Return (provider rows, England total row) in contract column order."""
    renamed = {h: ae.normalise_header(h) for h in raw.columns}
    unknown = [h for h, n in renamed.items() if n not in ae.COLUMN_MAP]
    absent = sorted(set(ae.COLUMN_MAP) - set(renamed.values()))
    if absent or unknown:
        raise SchemaDriftError(f"missing columns: {absent}; unexpected columns: {unknown}")

    df = raw.rename({h: ae.COLUMN_MAP[n] for h, n in renamed.items()})
    df = df.with_columns(
        pl.col("org_code").str.strip_chars().str.to_uppercase().replace("", None),
        pl.col("org_name").str.strip_chars(),
        pl.col("parent_org").str.strip_chars(),
        *(_to_count(c) for c in ae.COUNT_COLUMNS),
    )

    labels = {ae.parse_period_label(p) for p in df["period_label"].drop_nulls().to_list()}
    if labels != {month_label}:
        raise SchemaDriftError(f"period labels {sorted(map(str, labels))} != {month_label}")
    year, month = (int(part) for part in month_label.split("-"))

    df = df.with_columns(
        pl.lit(date(year, month, 1)).alias("reporting_month"),
        pl.lit(quality_tier).alias("quality_tier"),
        pl.lit(status).alias("status"),
        pl.lit(source_sha256).alias("source_sha256"),
        pl.lit(ingested_at).cast(pl.Datetime("us", "UTC")).alias("ingested_at"),
    )
    ordered = [
        "reporting_month",
        "org_code",
        "org_name",
        "parent_org",
        *ae.COUNT_COLUMNS,
        "quality_tier",
        "status",
        "source_sha256",
        "ingested_at",
    ]
    df = df.select(ordered)
    providers = df.filter(pl.col("org_code").is_not_null()).sort("org_code")
    england = df.filter(pl.col("org_code").is_null())
    return providers, england
