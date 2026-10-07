from pathlib import Path

import httpx

from nhs_stats import bronze, pipeline
from nhs_stats.paths import DataPaths


def _client(content: bytes) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=content, headers={"etag": '"v1"'})

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_fetch_stores_hashed_file_with_metadata(fixture_csv: Path, paths: DataPaths) -> None:
    content = fixture_csv.read_bytes()
    stored = pipeline.ingest_url(
        "https://example.invalid/ae.csv", "2026-03", paths, client=_client(content)
    )
    assert stored.path.read_bytes() == content
    assert stored.http_etag == '"v1"'
    assert stored.meta_path.exists()
    assert bronze.latest(paths, "ae_monthly", "2026-03").sha256 == stored.sha256


def test_identical_refetch_is_idempotent(fixture_csv: Path, paths: DataPaths) -> None:
    first = pipeline.ingest_file(fixture_csv, "2026-03", paths)
    second = pipeline.ingest_file(fixture_csv, "2026-03", paths)
    assert first.path == second.path
    assert len(list(first.path.parent.glob("*.csv"))) == 1


def test_revision_is_kept_and_latest_wins(
    fixture_csv: Path, paths: DataPaths, tmp_path: Path
) -> None:
    pipeline.ingest_file(fixture_csv, "2026-03", paths)
    revised = tmp_path / "revised.csv"
    revised.write_bytes(fixture_csv.read_bytes() + b"\n")
    second = pipeline.ingest_file(revised, "2026-03", paths, status="revised")
    assert len(list(second.path.parent.glob("*.csv"))) == 2
    assert bronze.latest(paths, "ae_monthly", "2026-03").status == "revised"
