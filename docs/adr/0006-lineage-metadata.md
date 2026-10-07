# 0006. Lineage metadata

Date: 2026-10-07. Status: accepted.

## Decision

Two levels, both file based so they work locally and on S3:

1. **Row level:** every silver and gold row carries `source_sha256`, the hash of the bronze file it derives
   from, plus `ingested_at` (silver). Together with the bronze `.meta.json` this answers "where did this number
   come from".
2. **Run level:** each `build` appends a JSON line to `data/lineage/runs.jsonl`: run ID, job, code version,
   start and end times, result, inputs and outputs (layer, relative path, SHA-256, row count) and the quality
   report path. The shape follows OpenLineage run, job and dataset concepts, so an emitter can be added later
   without changing what is recorded.

## Alternatives

Full OpenLineage or Marquez, Glue Data Catalog lineage, or dbt docs were rejected for now: they add services
or tools without improving what a single-source pipeline needs to prove.

## Consequences

- Failed runs are recorded as well as successful ones.
- `NHS_STATS_GIT_SHA` is recorded when set (CI and Lambda builds should set it).
