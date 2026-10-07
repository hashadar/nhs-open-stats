# 0002. Bronze, silver and gold layers

Date: 2026-10-07. Status: accepted.

## Decision

| Layer | Contents | Rules |
|---|---|---|
| Bronze (raw) | Files exactly as published, plus `.meta.json` with URL, fetch time, SHA-256, status | Immutable. Named by content hash, so revisions append and identical refetches are no-ops |
| Silver (cleansed) | One typed table per source and month, snake_case columns, contract-validated | Written only if the quality gate passes. Carries `quality_tier`, `status`, `source_sha256` |
| Gold (serving) | Tidy, documented, dashboard-ready tables built by SQL | Rebuilt from all silver partitions, so it is idempotent |

Layout (local directory or S3 prefix, identical):

```
data/bronze/<source>/reporting_month=YYYY-MM/<source>_<month>_<sha12>.csv(.meta.json)
data/silver/<source>/reporting_month=YYYY-MM/data.parquet
data/gold/<table>/<table>.parquet
data/quality/<source>/<month>.json
data/lineage/runs.jsonl
```

## Consequences

- Any silver or gold table can be rebuilt from bronze, so cleaning bugs are fixable retrospectively.
- Revisions are retained at bronze and traceable through `source_sha256`. Silver holds the latest revision
  for a month; a point-in-time version history for silver and gold is deferred (open question in the backlog).
- Hive-style `reporting_month=` partitions work in DuckDB, Athena and polars.
- Recent months load first; backfill is the same command run over older months, with per-series layout
  handling added to `sources/`.
