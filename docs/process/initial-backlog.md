# Initial backlog (sprints 1 to 3)

Derived from the plan's 0 to 3 month actions and first steps (sections 3 to 7). Sprint 0 (this repository
draft) is done: licence, README, CI, one working A&E slice, AWS skeleton, ADRs, process.

Sizes: S under half a day, M up to two days, L up to five. IDs are working references; they become GitHub
issue numbers when created (not created yet). Mark each item with labels from
[github-project.md](github-project.md). Acceptance criteria are summarised; refine at planning.

## Epics

| ID | Epic | Area | Outcome |
|---|---|---|---|
| E1 | Repository, licensing and governance | governance | Public-ready repository with confirmed licences, principles, quality tiers and a revisions policy |
| E2 | AWS foundations and cost control | governance | Terraform applied, budget alarm live, scheduled pipeline running monthly within 50 USD |
| E3 | Source catalogue and prioritisation | governance | Every in-scope series recorded with owner, cadence, format, status and licence, ranked |
| E4 | A&E monthly | data | Recent 12 months ingested, verified against live files, reconciled |
| E5 | RTT | data | Recent 12 months ingested through the same pattern |
| E6 | Reference layer | data | Calendar and organisation lineage including April 2026 ICB changes |
| E7 | Quality, revisions and assurance | data | Reconciliation, provisional or final tracking, series-break flags, point-in-time versions |
| E8 | Serving layer and data dictionary | data | Gold tables queryable in Athena, documented, example queries published |
| E9 | Lighthouse questions | analytics | Two dashboard-answerable questions chosen and shaping the gold tables |

Later (not yet broken down): cancer waiting times, ambulance indicators, capacity and flow, release monitoring
and schema-drift alerts, versioned API, benchmarking and forecasting prototypes, contributor readiness
(DCO enforcement, full code of conduct, good first issues), other UK nations, external reference data.

## Sprint 1: make the slice real

Goal: the A&E slice runs on a genuine file, the repository is configured on GitHub, and the first source records exist.

| ID | Type | Epic | Item | Size | Acceptance criteria |
|---|---|---|---|---|---|
| S1.1 | spike | E4 | Confirm scripted download from england.nhs.uk works (user agent, redirects, bot challenge) | S | Written finding: URL pattern for a monthly CSV, whether `httpx` succeeds, fallback if blocked (manual download via `fetch --file`) |
| S1.2 | story | E4 | Verify the A&E column layout and period label against a real monthly CSV; update column map and fixture | M | Real March 2026 file ingests; fixture mirrors its headers; drift error message tested |
| S1.3 | story | E4 | Ingest the latest 12 months of A&E, recent first, with status (provisional, revised) recorded | M | 12 silver partitions; gold has 12 months; quality reports archived; revised files kept as new bronze versions |
| S1.4 | chore | E1 | Configure GitHub: branch protection, required checks, labels (`labels.yml`), Project board, Dependabot, CODEOWNERS handle | S | Settings match `docs/process`; first PR merged through the required checks |
| S1.5 | story | E1 | Confirm the OGL v3.0 position for A&E and RTT from NHS England's terms and record it | S | Terms page cited in `DATA_LICENCE.md`; per-series licence field in the catalogue |
| S1.6 | story | E3 | Source catalogue v0: `catalogue/sources.yaml` with all series on the plan's index (owner, cadence, format, status, licence, tractability) | L | Validated by a schema and a test; ranking rationale documented; first slice choice confirmed |
| S1.7 | story | E2 | Apply Terraform foundations with remote state and confirm the budget alarm sends email | M | Buckets, Glue, Athena workgroup exist; test alert received; no account IDs in the repository |
| S1.8 | story | E1 | Data principles one-pager and quality tiers (official, experimental, management information) | S | ADR 0008 accepted; tier labels used in contracts |

## Sprint 2: second source, reference data, AWS runtime

Goal: RTT ingested through the same pattern, the reference layer started, and the pipeline able to run on AWS.

| ID | Type | Epic | Item | Size | Acceptance criteria |
|---|---|---|---|---|---|
| S2.1 | spike | E5 | RTT file structure: choose between XLSX per pathway and the full CSV in ZIP; record revision behaviour | S | Finding with sample headers and chosen file; fixture plan |
| S2.2 | story | E5 | RTT bronze to silver for incomplete pathways, provider level, recent 12 months | L | Contract, quality checks, fixtures, offline tests; layout drift detected |
| S2.3 | story | E5 | RTT gold table with weeks-waiting bands and 18-week performance | M | SQL in `sql/gold/`; dictionary entry; reconciles to published headline within tolerance |
| S2.4 | story | E6 | Calendar reference table (month, quarter, financial year) | S | Built in Python; parity test with the Rust `financial_year` function or decision to drop the crate |
| S2.5 | spike | E6 | Organisation lineage sources: ODS data, ICB closures and creations from April 2026, Frimley split | M | Finding listing sources, licences and a proposed table design |
| S2.6 | story | E6 | Organisation reference table v0 (provider to ICB to region, valid-from and valid-to) | L | Joined to gold tables; unmapped codes reported by a quality check |
| S2.7 | story | E2 | Object-store abstraction so bronze, silver and gold read and write `s3://` paths | M | Tests against a local S3 stand-in; no change to local behaviour |
| S2.8 | story | E2 | Container image and Lambda enabled behind `enable_pipeline`; monthly schedule | M | Scheduled run succeeds; lineage written to S3; cost recorded |
| S2.9 | story | E8 | Generate data dictionary pages from contracts | S | Command regenerates `docs/data-dictionary/*`; CI checks no drift |

## Sprint 3: assurance and serving

Goal: trustworthy numbers that a dashboard can query, with revisions and breaks visible.

| ID | Type | Epic | Item | Size | Acceptance criteria |
|---|---|---|---|---|---|
| S3.1 | story | E7 | Reconcile A&E and RTT gold headline measures to published figures | M | Tolerances in code; failing reconciliation blocks gold |
| S3.2 | spike | E7 | Revisions policy: how silver and gold keep point-in-time versions | M | ADR 0009 with chosen approach and storage cost estimate |
| S3.3 | story | E7 | Implement the revisions approach and status tracking (provisional, revised, final) | L | Query "as published on date X" works for one month |
| S3.4 | story | E7 | Series-break flags and comparability notes per source | M | Flag column in gold; notes in the dictionary |
| S3.5 | story | E8 | Glue table definitions for gold and Athena smoke test with scan cost recorded | M | Query returns expected rows; bytes scanned and cost noted in an ADR addendum |
| S3.6 | story | E8 | Example query pack and BI connection guide (no hosted dashboard) | S | Documented SQL for three dashboard questions; tested in CI against fixtures |
| S3.7 | story | E9 | Choose two lighthouse questions and trial them on the gold tables | S | Questions and required columns written; gaps raised as stories |
| S3.8 | spike | E2 | Release monitoring: detect new publications and layout changes | M | Finding and a minimal scheduled check design |
| S3.9 | chore | E1 | Sprint review of cost, scope and next-quarter plan | S | Actual AWS spend recorded; backlog for sprints 4 to 6 refined |

## Open questions to resolve early

1. Plan names RTT as the first anchor series; the draft slice uses A&E because the monthly CSV is a single tidy
   file. Confirm the order (S1.6).
2. Real file layout and automated download are unverified (S1.1, S1.2).
3. GitHub handle for CODEOWNERS and the repository location (S1.4).
