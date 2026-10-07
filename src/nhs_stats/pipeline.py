"""Orchestration for the A&E monthly slice: bronze -> quality gate -> silver."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import httpx

from nhs_stats import bronze, lineage, quality, silver
from nhs_stats.contracts import load_contract
from nhs_stats.paths import DataPaths
from nhs_stats.sources import ae_monthly as ae


@dataclass(frozen=True)
class BuildResult:
    silver_path: Path
    report_path: Path
    results: list[quality.CheckResult]


def ingest_url(
    url: str,
    month_label: str,
    paths: DataPaths,
    *,
    status: str = "provisional",
    client: httpx.Client | None = None,
) -> bronze.BronzeFile:
    response = bronze.fetch_bytes(url, client)
    return bronze.store(
        response.content,
        paths=paths,
        source_id=ae.SOURCE_ID,
        month_label=month_label,
        source_url=url,
        status=status,
        headers=response.headers,
    )


def ingest_file(
    file: Path, month_label: str, paths: DataPaths, *, status: str = "provisional"
) -> bronze.BronzeFile:
    return bronze.store(
        file.read_bytes(),
        paths=paths,
        source_id=ae.SOURCE_ID,
        month_label=month_label,
        source_url=file.resolve().as_uri(),
        status=status,
    )


def build(month_label: str, paths: DataPaths) -> BuildResult:
    """Clean the latest bronze file for a month, gate on quality, write silver."""
    run = lineage.RunRecord(job="ae_monthly.build", started_at=datetime.now(UTC).isoformat())
    source = bronze.latest(paths, ae.SOURCE_ID, month_label)
    run.inputs.append(
        lineage.Dataset("bronze", paths.relative(source.path), source.sha256, rows=None)
    )
    report_path = paths.quality_report(ae.SOURCE_ID, month_label)
    run.quality_report = paths.relative(report_path)

    try:
        providers, england = silver.clean_ae_monthly(
            silver.read_raw(source.path.read_bytes()),
            month_label=month_label,
            quality_tier=ae.QUALITY_TIER,
            status=source.status,
            source_sha256=source.sha256,
            ingested_at=datetime.fromisoformat(source.fetched_at),
        )
        contract = load_contract(ae.SILVER_CONTRACT)
        results = quality.run_checks(providers, england, contract, month_label)
        context = {
            "source": ae.SOURCE_ID,
            "reporting_month": month_label,
            "source_sha256": source.sha256,
            "contract": f"{contract.name}@{contract.version}",
        }
        quality.write_report(results, report_path, context)
        blocking = quality.failures(results)
        if blocking:
            raise quality.QualityGateError(blocking)

        silver_path = paths.silver_file(ae.SOURCE_ID, month_label)
        silver_path.parent.mkdir(parents=True, exist_ok=True)
        providers.write_parquet(silver_path, compression="zstd")
        run.outputs.append(
            lineage.Dataset(
                "silver",
                paths.relative(silver_path),
                lineage.file_sha256(silver_path),
                providers.height,
            )
        )
        run.result = "success"
        return BuildResult(silver_path, report_path, results)
    except Exception:
        run.result = "failed"
        raise
    finally:
        run.ended_at = datetime.now(UTC).isoformat()
        lineage.append(run, paths)
