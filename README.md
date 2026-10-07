# nhs-open-stats

Python package and CLI: `nhs-stats`. Cleansed, documented, dashboard-ready tables built from NHS England's published statistical work areas.

**Status: early draft.** One vertical slice works end to end (monthly A&E: bronze, silver, quality gate, gold, lineage).
No hosted dashboards or published datasets yet. Data quality, assurance and lineage come before breadth.
The project is a personal public project and is intended to open to contributors in about a year.

## What it does

Takes a monthly A&E CSV, stores it unchanged with provenance, cleans and types it with polars, validates it
against a data contract, runs quality checks (blocking and advisory), writes parquet, builds a serving table
with DuckDB SQL, and records lineage. Everything runs locally without AWS.

## Quick start

Requires Python 3.11 or later and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest                                   # offline tests

# Offline, using the synthetic fixture
uv run nhs-stats fetch --month 2026-03 --file tests/fixtures/ae_monthly_2026-03.csv
uv run nhs-stats build --month 2026-03

# From NHS England: copy the monthly CSV link from the A&E landing page (see sources/ae_monthly.py).
# The column layout is not yet verified against a live file (see docs/process/initial-backlog.md, S1.1-S1.2).
uv run nhs-stats fetch --month 2026-03 --url "<monthly A&E CSV URL>"
```

Output lands in `./data` (gitignored) or `$NHS_STATS_DATA_DIR`. See `docs/architecture.md`; delivery process is in `docs/process/`.

Checks used in CI:

```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
cd rust/nhs_stats_core && cargo fmt --check && cargo clippy -- -D warnings && cargo test
cd infra/terraform && terraform fmt -check && terraform init -backend=false && terraform validate
```

## Layout

| Path | Contents |
|---|---|
| `src/nhs_stats/` | Python package |
| `contracts/` | Data contracts (YAML) |
| `sql/gold/` | Serving-table SQL |
| `rust/nhs_stats_core/` | Optional Rust crate (placeholder) |
| `infra/terraform/` | AWS infrastructure skeleton |
| `docs/` | Architecture, ADRs, data dictionary, process |
| `tests/` | Offline tests and synthetic fixtures |

## Licence and data

Code: [Apache-2.0](LICENSE). Source data is published by NHS England under the Open Government Licence v3.0
(to be confirmed per series); see [DATA_LICENCE.md](DATA_LICENCE.md) and [NOTICE](NOTICE).
This project is not endorsed by NHS England. The data is aggregate and organisational and cannot support patient-level inference.

## Contributing

Not yet open to external contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) and `docs/process/`.
