# 0002. Bronze, silver and gold layers

Date: 2026-10-07. Status: accepted.

## Decision

| Layer | Contents | Rules |
|---|---|---|
| Bronze (raw) | Files exactly as published, plus `.meta.json` with URL, fetch time, SHA-256, status | Immutable. Named by content hash, so revisions append and identical refetches are no-ops |
| Silver (cleansed) | One typed table per source and month, snake_case columns, contract-validated | Written only if the quality gate passes. Carries `quality_tier`, `status`, `source_sha256` |
| Gold (serving) | Multi-year, normalised time-series tables for dashboards | Deferred until silver has enough history; not built by the current pipeline |

Layout (local directory or S3 prefix, identical):

```
data/bronze/<source>/reporting_month=YYYY-MM/<source>_<month>_<sha12>.csv(.meta.json)
data/silver/<source>/reporting_month=YYYY-MM/data.parquet
data/quality/<source>/<month>.json
data/lineage/runs.jsonl
# later: data/gold/<table>/<table>.parquet
```

## Consequences

- Silver can be rebuilt from bronze, so cleaning bugs are fixable retrospectively.
- Revisions are retained at bronze and traceable through `source_sha256`. Silver holds the latest revision
  for a month; a point-in-time version history is deferred (open question in the backlog).
- Hive-style `reporting_month=` partitions work in Athena and polars.
- Recent months load first; backfill is the same command run over older months, with per-series layout
  handling added to `sources/`.

## Amendment (2026-10-07)

The first pipeline implementation stops at silver. Gold remains the intended serving layer but will be a
cross-year normalised table, not a per-month DuckDB rebuild of the current silver shape.
