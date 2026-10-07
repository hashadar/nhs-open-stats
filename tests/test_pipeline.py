import json
from pathlib import Path

import polars as pl
import pytest

from nhs_stats import cli, pipeline
from nhs_stats.paths import DataPaths
from nhs_stats.quality import QualityGateError


def test_end_to_end_writes_silver_report_and_lineage(fixture_csv: Path, paths: DataPaths) -> None:
    pipeline.ingest_file(fixture_csv, "2026-03", paths)
    result = pipeline.build("2026-03", paths)

    silver = pl.read_parquet(result.silver_path)
    assert silver.height == 6
    assert silver["quality_tier"].unique().to_list() == ["official"]
    assert "TOTAL" not in silver["org_code"].to_list()

    report = json.loads(result.report_path.read_text())
    assert report["passed"] is True
    assert report["contract"] == "ae_monthly_silver@1"

    runs = [json.loads(line) for line in paths.lineage_log.read_text().splitlines()]
    assert runs[-1]["result"] == "success"
    assert {o["layer"] for o in runs[-1]["outputs"]} == {"silver"}
    assert runs[-1]["inputs"][0]["sha256"] == silver["source_sha256"][0]


def test_silver_accumulates_months(fixture_csv: Path, paths: DataPaths, tmp_path: Path) -> None:
    pipeline.ingest_file(fixture_csv, "2026-03", paths)
    pipeline.build("2026-03", paths)
    april = tmp_path / "april.csv"
    april.write_text(fixture_csv.read_text().replace("MARCH-2026", "APRIL-2026"))
    pipeline.ingest_file(april, "2026-04", paths)
    pipeline.build("2026-04", paths)
    months = {
        p.parent.name.removeprefix("reporting_month=")
        for p in paths.root.glob("silver/ae_monthly/reporting_month=*/data.parquet")
    }
    assert months == {"2026-03", "2026-04"}


def test_quality_failure_blocks_silver_and_is_recorded(
    fixture_csv: Path, paths: DataPaths, tmp_path: Path
) -> None:
    lines = fixture_csv.read_text().splitlines()
    lines.append(lines[2].replace("TST01", "TST01"))
    bad = tmp_path / "dup.csv"
    bad.write_text("\n".join(lines) + "\n")
    pipeline.ingest_file(bad, "2026-03", paths)

    with pytest.raises(QualityGateError):
        pipeline.build("2026-03", paths)

    assert not paths.silver_file("ae_monthly", "2026-03").exists()
    report = json.loads(paths.quality_report("ae_monthly", "2026-03").read_text())
    assert report["passed"] is False
    last = json.loads(paths.lineage_log.read_text().splitlines()[-1])
    assert last["result"] == "failed"


def test_cli_fetch_and_build(
    fixture_csv: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data = str(tmp_path / "cli-data")
    assert (
        cli.main(["--data-dir", data, "fetch", "--month", "2026-03", "--file", str(fixture_csv)])
        == 0
    )
    assert cli.main(["--data-dir", data, "build", "--month", "2026-03"]) == 0
    out = capsys.readouterr().out
    assert "silver:" in out
    assert "gold:" not in out
