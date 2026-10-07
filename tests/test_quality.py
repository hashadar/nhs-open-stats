from datetime import UTC, datetime
from pathlib import Path

import polars as pl

from nhs_stats import quality, silver
from nhs_stats.contracts import load_contract


def _frames(csv: Path) -> tuple[pl.DataFrame, pl.DataFrame]:
    return silver.clean_ae_monthly(
        silver.read_raw(csv.read_bytes()),
        month_label="2026-03",
        quality_tier="official",
        status="provisional",
        source_sha256="abc",
        ingested_at=datetime(2026, 4, 9, tzinfo=UTC),
    )


def test_fixture_passes_blocking_checks_and_warns_on_provider_count(fixture_csv: Path) -> None:
    providers, england = _frames(fixture_csv)
    results = quality.run_checks(providers, england, load_contract("ae_monthly_silver"), "2026-03")
    assert quality.failures(results) == []
    by_name = {r.name: r for r in results}
    assert by_name["england_reconciliation"].passed
    assert not by_name["plausible_provider_count"].passed


def test_over_4h_above_attendances_is_blocking(fixture_csv: Path) -> None:
    providers, england = _frames(fixture_csv)
    broken = providers.with_columns(
        pl.when(pl.col("org_code") == "TST01")
        .then(pl.col("attendances_type1") + 1)
        .otherwise(pl.col("over_4h_type1"))
        .alias("over_4h_type1")
    )
    results = quality.run_checks(broken, england, load_contract("ae_monthly_silver"), "2026-03")
    assert [r.name for r in quality.failures(results)] == ["over_4h_not_above_attendances"]


def test_reconciliation_flags_large_gap(fixture_csv: Path) -> None:
    providers, england = _frames(fixture_csv)
    skewed = england.with_columns(pl.col("attendances_type1") * 2)
    assert not quality.check_england_reconciliation(providers, skewed).passed
