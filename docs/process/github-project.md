# GitHub Projects board and labels

One project, "nhs-stats", owned by the repository owner and linked to the repository.

## Fields

| Field | Type | Values |
|---|---|---|
| Status | single select | Backlog, Ready, In progress, In review, Done |
| Iteration | iteration | 2-week sprints |
| Size | single select | S, M, L |
| Priority | single select | P0 (urgent), P1, P2 |
| Area | single select | Governance, Data, Analytics (mirrors the `area:` labels) |

## Views

| View | Layout | Filter, grouping |
|---|---|---|
| Sprint board | Board | Current iteration, columns by Status, WIP limit 2 on In progress |
| Backlog | Table | Status is Backlog or Ready, grouped by parent epic, sorted by Priority |
| Roadmap | Roadmap | Epics only (`type:epic`), by iteration |
| Bugs and spikes | Table | `type:bug` or `type:spike`, not Done |

## Automations (built-in workflows)

Auto-add new issues and pull requests from the repository; set Status to Backlog on add; In review when a
pull request is opened; Done when closed or merged; archive Done items after 14 days.

## Labels

Defined in [`.github/labels.yml`](../../.github/labels.yml). Colours group families.

| Family | Labels |
|---|---|
| Type | `type:epic`, `type:story`, `type:bug`, `type:spike`, `type:chore` |
| Area | `area:governance`, `area:data`, `area:analytics` |
| Layer | `layer:bronze`, `layer:silver`, `layer:gold`, `layer:infra`, `layer:docs`, `layer:process` |
| Source | `source:ae`, `source:rtt`, `source:cancer`, `source:ambulance`, `source:reference` (add one per series) |
| State | `blocked`, `needs-info`, `data-quality` (issue concerns published-number correctness) |
| Community | `good first issue`, `help wanted` |
| Automation | `dependencies` |

Every issue gets one `type:`, one `area:` and, where it applies, one `layer:` and `source:` label. Size, priority
and iteration are project fields, not labels. Sync labels with a label-sync action or `gh label create`.
