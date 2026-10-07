# Architecture overview

Goal: trusted, documented tables that dashboards can query directly. Data quality, assurance and lineage come
before breadth. Scope is NHS-published aggregate data only (see `DATA_LICENCE.md`). Status: first slice
(monthly A&E) runs locally through bronze to silver; AWS infrastructure is a validated skeleton.

Gold (multi-year, normalised serving tables) is intentionally deferred until silver covers enough history
and the time-series shape is clear.

```
 NHS England (CSV/XLSX)
        |  fetch (httpx) or local file
        v
 BRONZE  raw file + .meta.json (URL, time, SHA-256, status)        immutable, hash-named
        |  polars: rename, type, split national TOTAL row
        v
 QUALITY GATE  contract validation + checks  -->  data/quality/*.json   (errors block)
        |
        v
 SILVER  typed parquet per source and month                         quality_tier, status, source_sha256

 (later) GOLD  multi-year normalised time-series serving tables     Athena / any BI tool

 Every build appends a run record to data/lineage/runs.jsonl
```

## Components

| Path | Role |
|---|---|
| `src/nhs_stats/sources/` | Per-source layout knowledge (column map, period parsing) |
| `src/nhs_stats/bronze.py`, `silver.py` | Active medallion layers |
| `src/nhs_stats/contracts.py`, `contracts/*.yaml` | Data contracts and validation |
| `src/nhs_stats/quality.py` | Checks with severities and the JSON report |
| `src/nhs_stats/lineage.py` | Run-level lineage |
| `src/nhs_stats/pipeline.py`, `cli.py` | Orchestration and the `nhs-stats` command |
| `rust/nhs_stats_core/` | Optional PyO3 crate, placeholder |
| `infra/terraform/` | S3, Glue, Athena, budget, optional scheduled Lambda |

## Principles

1. Raw data is immutable; everything downstream is rebuildable.
2. Fail loudly on layout drift; never guess.
3. Every row says how much to trust it (tier and status) and where it came from (source hash).
4. Run locally without AWS; the same layout maps onto S3.
5. Decisions are written down in `docs/adr/`.

## Known gaps (tracked in `docs/process/initial-backlog.md`)

Reference layer (ODS lineage, ICB changes, calendar), series-break flags, S3 I/O, source catalogue,
reconciliation to published headline figures, revision history, and gold time-series tables.
