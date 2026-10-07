"""Bronze layer: immutable raw files with a provenance sidecar."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

import httpx

from nhs_stats.paths import DataPaths

USER_AGENT = "nhs-stats/0.1 (open data pipeline)"
TIMEOUT_SECONDS = 60.0


@dataclass(frozen=True)
class BronzeFile:
    source_id: str
    month_label: str
    path: Path
    sha256: str
    size_bytes: int
    fetched_at: str
    source_url: str
    status: str
    http_etag: str | None = None
    http_last_modified: str | None = None

    @property
    def meta_path(self) -> Path:
        return self.path.with_suffix(self.path.suffix + ".meta.json")


def _now() -> datetime:
    return datetime.now(UTC)


def fetch_bytes(url: str, client: httpx.Client | None = None) -> httpx.Response:
    owns_client = client is None
    http = client or httpx.Client(
        headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS, follow_redirects=True
    )
    try:
        response = http.get(url)
        response.raise_for_status()
        return response
    finally:
        if owns_client:
            http.close()


def store(
    content: bytes,
    *,
    paths: DataPaths,
    source_id: str,
    month_label: str,
    source_url: str,
    status: str,
    suffix: str = ".csv",
    headers: httpx.Headers | None = None,
    fetched_at: datetime | None = None,
) -> BronzeFile:
    """Write content once, named by hash; identical re-fetches are no-ops."""
    digest = hashlib.sha256(content).hexdigest()
    directory = paths.bronze_dir(source_id, month_label)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{source_id}_{month_label}_{digest[:12]}{suffix}"
    record = BronzeFile(
        source_id=source_id,
        month_label=month_label,
        path=target,
        sha256=digest,
        size_bytes=len(content),
        fetched_at=(fetched_at or _now()).isoformat(),
        source_url=source_url,
        status=status,
        http_etag=headers.get("etag") if headers else None,
        http_last_modified=headers.get("last-modified") if headers else None,
    )
    if target.exists():
        return load(target)
    target.write_bytes(content)
    payload = asdict(record) | {"path": paths.relative(target)}
    record.meta_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return record


def load(path: Path) -> BronzeFile:
    meta_path = path.with_suffix(path.suffix + ".meta.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return BronzeFile(**{**meta, "path": path})


def latest(paths: DataPaths, source_id: str, month_label: str) -> BronzeFile:
    """Most recently fetched bronze file for a month (revisions append, never replace)."""
    directory = paths.bronze_dir(source_id, month_label)
    candidates = [
        load(p.with_name(p.name.removesuffix(".meta.json"))) for p in directory.glob("*.meta.json")
    ]
    if not candidates:
        raise FileNotFoundError(f"No bronze file for {source_id} {month_label} in {directory}")
    return max(candidates, key=lambda b: b.fetched_at)
