# 0001. Dataframe library and language mix

Date: 2026-10-07. Status: accepted.

## Context

The pipeline turns messy monthly spreadsheets and CSVs into typed parquet tables. Gold serving tables are
planned later as multi-year time series. Volumes are small (low single-digit gigabytes curated, files up to
roughly 60 MB), so raw speed is not the deciding factor. Correctness of types, readable transformations and
low operating cost matter more. Contributors will mostly be data scientists and software developers, so
familiarity matters too.

## Options

| | polars | pandas |
|---|---|---|
| Typing | Strict dtypes, real nulls for every type, nullable integers by default | Mixed NaN and nullable extension types; silent upcasts (int to float) when nulls appear |
| Read raw files as text first | `infer_schema=False` gives all-string columns, explicit casts | Possible (`dtype=str`), but defaults infer |
| Parquet and Arrow | Native Arrow, lazy scans, streaming for larger files | Arrow optional via backend |
| Transformation style | Expressions, no index, easy to test and read | Index semantics and chained assignment are common sources of bugs |
| Performance | Multi-threaded, lazy; far beyond need here | Adequate at this scale |
| Ecosystem | Smaller; Excel needs `fastexcel`, plotting and scikit-learn expect pandas or NumPy | Largest ecosystem and familiarity |

## Decision

- **polars is the primary dataframe library** for bronze to silver cleaning and all in-memory work.
- **DuckDB** (or Athena SQL) is reserved for a future gold build over silver parquet; it is not a dependency
  while the pipeline stops at silver.
- **Rust via PyO3 and maturin only where profiling shows a need.** `rust/nhs_stats_core` is a placeholder
  with two small functions. The Python implementation stays the reference, with parity tests, until a hot path
  justifies switching. Nothing in the Python package imports the crate today.
- **pandas only at the edges:** `df.to_pandas()` at the boundary with libraries that require it (for example
  statistical modelling in a later analytical area, or a notebook). It is not a core dependency.

## Consequences

- Strict typing catches layout drift early (a column that becomes text fails the contract).
- Contributors who know only pandas have a small learning curve; the codebase keeps expressions simple.
- Revisit if polars Excel support proves inadequate for the XLS-only series; a pandas or calamine read at the
  bronze boundary is the fallback.
