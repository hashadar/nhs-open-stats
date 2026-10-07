# Architecture decision records

Short, dated records of decisions that are costly to reverse. Format: context, decision, consequences.
Status is one of proposed, accepted, superseded. Add new records as the next number; never rewrite history,
supersede instead. Process changes go through a pull request like any other change.

| ADR | Decision | Status |
|---|---|---|
| [0001](0001-dataframe-library.md) | polars primary, DuckDB for SQL, Rust only where justified, pandas at the edges | accepted |
| [0002](0002-medallion-layers.md) | Bronze, silver and gold layers with a fixed storage layout | accepted |
| [0003](0003-infrastructure-as-code.md) | Terraform for AWS infrastructure | accepted |
| [0004](0004-aws-compute-and-query.md) | Lambda container on a schedule; DuckDB to build, Athena to serve | accepted |
| [0005](0005-data-contracts-and-quality.md) | YAML data contracts plus a blocking quality gate | accepted |
| [0006](0006-lineage-metadata.md) | Run-level JSONL lineage plus row-level source hash | accepted |
| [0007](0007-licensing.md) | Apache-2.0 for code, OGL v3.0 attribution for data | accepted |
