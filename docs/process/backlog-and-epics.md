# Backlog and epic structure

Hierarchy: **epic** (a few sprints, one outcome) contains **stories** (one sprint or less, user value),
**bugs** and **spikes** (time-boxed questions). Chores are small enabling tasks. Epics are GitHub issues labelled
`type:epic`, with children attached as sub-issues so progress rolls up on the board.

## Epics map to the plan's three areas

| Plan area | Label | Epic themes |
|---|---|---|
| 1. Strategy, governance and architecture | `area:governance` | Repository, licensing and open-source readiness; AWS foundations and cost control; source catalogue and prioritisation; data principles, quality tiers and revisions policy |
| 2. Optimised cleansed datasets | `area:data` | One epic per source series (RTT, A&E, then cancer waiting times and ambulance); reference layer (ODS lineage, calendar); quality, reconciliation and revisions; dashboard-serving layer and data dictionary |
| 3. Data science and engineering | `area:analytics` | Lighthouse questions and exploratory analysis; benchmarking; forecasting; metrics layer (later) |

Cross-cutting work (CI, tooling, docs) lives under the area it serves, with the `layer:` label showing where.

## Rules

- Order the backlog by value to the dashboard end goal, then by risk. Priority is a board field (P0 to P2).
- Epics are expanded just in time: only the next two sprints are broken into stories.
- A new source is always an epic with the same child stories: spike the layout, ingest, contract, quality checks,
  gold table, dictionary, backfill. This doubles as the contributor onboarding playbook.
- Bugs affecting published numbers are P0 and jump the queue.
- Anything not needed for the sprint goal stays in the backlog; do not widen scope mid-sprint.
