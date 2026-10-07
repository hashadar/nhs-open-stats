# Delivery process

Agile, with GitHub as the single place for code, issues and the board. Built for one maintainer now and kept
light enough to hand to contributors later. Short and revisable: change it through a pull request.

| Page | Contents |
|---|---|
| [definitions.md](definitions.md) | Definition of ready and of done |
| [backlog-and-epics.md](backlog-and-epics.md) | Backlog structure and epics mapped to the plan's three areas |
| [github-project.md](github-project.md) | GitHub Projects board layout and label scheme |
| [branching-and-prs.md](branching-and-prs.md) | Trunk-based flow, conventional commits, required CI |
| [initial-backlog.md](initial-backlog.md) | Seeded epics and stories for sprints 1 to 3 |

## Cadence

Two-week sprints, starting on a Monday (GitHub Projects iterations). Sprint 0 is the initial repository draft.

| When | What | Time-box |
|---|---|---|
| Day 1 | Sprint planning: pick ready stories to the sprint goal; set the goal in one sentence | 45 min |
| Daily | Move cards, note blockers on the issue (async; no stand-up while solo) | 5 min |
| Mid-sprint | Backlog refinement: make the next sprint's top items ready | 30 min |
| Last day | Review (demo what is done, on `main`) and retrospective (one comment on the sprint's tracking issue: keep, stop, try) | 45 min |

Principles: a small first slice, recent data first, quality before breadth, work-in-progress limit of two,
and decisions recorded in public. Capacity is a guide, not a commitment: size items S, M or L (S is under half a
day, M up to two days, L up to five). Split anything larger.

Expect roughly 20 to 25 percent of each sprint to be unplanned work (data surprises, upstream layout changes).
Spikes are time-boxed and end with a written finding, a decision or a follow-up story.
