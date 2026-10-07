# 0004. AWS compute and query engine

Date: 2026-10-07. Status: accepted.

## Context

Monthly cadence, files of at most tens of megabytes, a budget ceiling of 50 USD per month, and a target of
dashboard-serving data.

## Decision

- **Build:** a container-image **Lambda** triggered by **EventBridge Scheduler**. It runs the same
  `nhs_stats` code as local runs. 15 minutes and up to 10 GB of memory are ample for monthly files.
- **Serve:** gold parquet on S3, catalogued in **Glue**, queried through an **Athena** workgroup with a
  per-query scan cap (1 GB by default) and CloudWatch metrics. Dashboards connect over JDBC or ODBC. A thin API
  is deferred.
- **SQL while building:** DuckDB (see ADR 0001). DuckDB on S3 is also the fallback if Athena costs or
  latency disappoint.
- **Not yet:** Step Functions (add when ingestion fans out across many series or needs retries per stage),
  ECS Fargate scheduled tasks (use for long backfills that exceed Lambda limits), always-on databases.

## Cost sketch (to be verified against real bills)

Order of magnitude per month: S3 storage for a few GB under 1 USD; Lambda under 1 USD at a few runs;
Athena at roughly 5 USD per TB scanned, so gold tables of tens of megabytes cost cents; CloudWatch logs a few
USD at most with 30-day retention. AWS Budgets alerts at 50, 80 and 100 percent of 50 USD (actual) and
100 percent (forecast).

## Consequences

- Near-zero idle cost and no servers to patch.
- S3 reads and writes are not implemented in the Python package yet (local paths only); the next backlog
  item is an object-store abstraction. The Lambda stays disabled until then.
