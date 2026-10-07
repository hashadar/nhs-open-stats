"""Data quality checks that run between silver cleaning and publication."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

import polars as pl

from nhs_stats.contracts import Contract, validate
from nhs_stats.sources.ae_monthly import ATTENDANCE_COLUMNS, COUNT_COLUMNS, OVER_4H_COLUMNS

Severity = Literal["error", "warning"]

MIN_PROVIDER_ROWS = 100
ENGLAND_TOLERANCE = 0.01


@dataclass(frozen=True)
class CheckResult:
    name: str
    severity: Severity
    passed: bool
    detail: str = ""


class QualityGateError(RuntimeError):
    def __init__(self, failures: list[CheckResult]) -> None:
        self.failures = failures
        super().__init__("; ".join(f"{f.name}: {f.detail}" for f in failures))


def _row_sum(columns: tuple[str, ...]) -> pl.Expr:
    return pl.sum_horizontal(*(pl.col(c) for c in columns))


def check_contract(df: pl.DataFrame, contract: Contract) -> CheckResult:
    violations = validate(df, contract)
    detail = "; ".join(f"{v.column or 'table'}: {v.message}" for v in violations[:10])
    return CheckResult("schema_contract", "error", not violations, detail)


def check_single_month(df: pl.DataFrame, expected_month: str) -> CheckResult:
    months = sorted({m.strftime("%Y-%m") for m in df["reporting_month"].unique().to_list()})
    return CheckResult(
        "single_expected_month",
        "error",
        months == [expected_month],
        f"found {months}, expected {expected_month}",
    )


def check_over_4h_not_above_attendances(df: pl.DataFrame) -> CheckResult:
    pairs = zip(ATTENDANCE_COLUMNS, OVER_4H_COLUMNS, strict=True)
    bad = df.filter(pl.any_horizontal(*(pl.col(o) > pl.col(a) for a, o in pairs)))
    return CheckResult(
        "over_4h_not_above_attendances",
        "error",
        bad.height == 0,
        f"{bad.height} providers, e.g. {bad['org_code'].head(3).to_list()}",
    )


def check_provider_count(df: pl.DataFrame) -> CheckResult:
    return CheckResult(
        "plausible_provider_count",
        "warning",
        df.height >= MIN_PROVIDER_ROWS,
        f"{df.height} providers, expected at least {MIN_PROVIDER_ROWS}",
    )


def check_null_rate(df: pl.DataFrame, threshold: float = 0.2) -> CheckResult:
    rates = {c: df[c].null_count() / max(df.height, 1) for c in COUNT_COLUMNS}
    high = {c: round(r, 3) for c, r in rates.items() if r > threshold}
    return CheckResult("count_null_rate", "warning", not high, f"above {threshold:.0%}: {high}")


def check_england_reconciliation(providers: pl.DataFrame, england: pl.DataFrame) -> CheckResult:
    """Provider totals should be close to the published England row."""
    if england.height != 1:
        return CheckResult(
            "england_reconciliation", "warning", False, f"{england.height} England rows found"
        )
    mismatches: dict[str, float] = {}
    for column in ("attendances_type1", "over_4h_type1", "emergency_admissions_type1"):
        published = england[column][0]
        summed = providers[column].sum()
        if published and abs(summed - published) / published > ENGLAND_TOLERANCE:
            mismatches[column] = round((summed - published) / published, 4)
    return CheckResult(
        "england_reconciliation",
        "warning",
        not mismatches,
        f"relative difference beyond {ENGLAND_TOLERANCE:.0%}: {mismatches}",
    )


def run_checks(
    providers: pl.DataFrame,
    england: pl.DataFrame,
    contract: Contract,
    expected_month: str,
) -> list[CheckResult]:
    checks: list[Callable[[], CheckResult]] = [
        lambda: check_contract(providers, contract),
        lambda: check_single_month(providers, expected_month),
        lambda: check_over_4h_not_above_attendances(providers),
        lambda: check_provider_count(providers),
        lambda: check_null_rate(providers),
        lambda: check_england_reconciliation(providers, england),
    ]
    return [check() for check in checks]


def failures(results: list[CheckResult]) -> list[CheckResult]:
    return [r for r in results if r.severity == "error" and not r.passed]


def write_report(results: list[CheckResult], path: Path, context: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        **context,
        "passed": not failures(results),
        "checks": [asdict(r) for r in results],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
