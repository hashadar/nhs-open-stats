# 0005. Data contracts and quality checks

Date: 2026-10-07. Status: accepted.

## Decision

- **Contracts** live in `contracts/*.yaml`: column names, dtypes, nullability, patterns, minimums, primary key
  and descriptions. They are the single source for validation and, later, for generating the data dictionary
  and Glue table definitions.
- **Quality checks** (`nhs_stats/quality.py`) run after cleaning and before silver is written. Each check has a
  severity:
  - `error` blocks the write: schema contract, expected reporting month, duplicate keys, over-four-hour counts
    above attendances.
  - `warning` is recorded but does not block: implausibly few providers, high null rates, reconciliation of
    provider sums to the published England row (1 percent tolerance).
- Every run writes `data/quality/<source>/<month>.json`, including on failure.
- **Layout drift** (missing or unexpected raw columns, wrong period label) raises `SchemaDriftError` rather
  than guessing.
- **Tiering:** every row carries `quality_tier` (official, experimental, management_information) and `status`
  (provisional, revised, final) so dashboards can label data. Series-break flags arrive with the reference layer.

## Consequences

- Bad data fails loudly and leaves bronze and the previous silver untouched.
- Tolerances and checks are code, reviewed in pull requests, and tested offline.
- Reconciliation currently covers a few type 1 measures; full reconciliation to published headline figures is
  a backlog item.
