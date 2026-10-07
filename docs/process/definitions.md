# Definitions of ready and done

## Definition of ready

A story can enter a sprint when:

- It has a goal in user terms ("as a dashboard author, I can ...") and a stated reason, linked to an epic.
- Acceptance criteria are written and testable.
- Licence and quality tier of any source involved are known, or the story is a spike to find out.
- Dependencies and blockers are named; it fits in a sprint (size S, M or L, not larger).
- Test data approach is clear (synthetic fixture, never real or restricted data).

## Definition of done

- Acceptance criteria met and demonstrated on `main`.
- Code reviewed (self-review against the PR checklist while solo) and merged by squash with a conventional commit title.
- CI green: ruff, mypy, pytest (offline), plus Rust and Terraform checks when touched.
- New or changed tables: contract updated, quality checks added or adjusted, data dictionary entry updated,
  lineage still recorded.
- New decisions recorded as an ADR; user-facing behaviour in the README or docs.
- No secrets, account identifiers or real data committed.
- Issue closed with a link to the merged PR; any follow-up work raised as new issues.

## Definition of done for a data source

Licence confirmed and recorded; recent months ingested; layout drift detected; reconciled to published
totals within an agreed tolerance; quality tier and status labelled; known breaks documented; dictionary entry published.
