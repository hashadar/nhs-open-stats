from datetime import UTC, date, datetime
from pathlib import Path

import polars as pl
import pytest

from nhs_stats import silver
from nhs_stats.contracts import load_contract, validate

INGESTED = datetime(2026, 4, 9, 9, 30, tzinfo=UTC)


def _clean(csv: Path) -> tuple[pl.DataFrame, pl.DataFrame]:
    return silver.clean_ae_monthly(
        silver.read_raw(csv.read_bytes()),
        month_label="2026-03",
        quality_tier="official",
        status="provisional",
        source_sha256="abc",
        ingested_at=INGESTED,
    )


def test_cleaning_separates_england_and_matches_contract(fixture_csv: Path) -> None:
    providers, england = _clean(fixture_csv)
    assert providers.height == 6
    assert england.height == 1
    assert providers["reporting_month"].unique().to_list() == [date(2026, 3, 1)]
    assert validate(providers, load_contract("ae_monthly_silver")) == []


def test_thousands_separators_and_suppression_handled(fixture_csv: Path) -> None:
    providers, _ = _clean(fixture_csv)
    row3 = providers.filter(pl.col("org_code") == "TST03")
    assert row3["attendances_type1"][0] > 999
    assert providers.filter(pl.col("org_code") == "TST04")["attendances_type2"][0] is None


def test_schema_drift_is_reported(fixture_csv: Path) -> None:
    raw = silver.read_raw(fixture_csv.read_bytes()).rename({"Org Name": "Organisation"})
    with pytest.raises(silver.SchemaDriftError, match="missing columns"):
        silver.clean_ae_monthly(
            raw,
            month_label="2026-03",
            quality_tier="official",
            status="final",
            source_sha256="x",
            ingested_at=INGESTED,
        )


def test_wrong_month_is_rejected(fixture_csv: Path) -> None:
    with pytest.raises(silver.SchemaDriftError, match="period labels"):
        silver.clean_ae_monthly(
            silver.read_raw(fixture_csv.read_bytes()),
            month_label="2026-04",
            quality_tier="official",
            status="final",
            source_sha256="x",
            ingested_at=INGESTED,
        )
