# Branching and pull request conventions

## Trunk-based development

- `main` is always releasable and is the only long-lived branch.
- Work on short-lived branches off `main`: aim to merge within two days, never longer than five. Split work
  instead of keeping a branch open.
- Branch name: `<type>/<issue>-<slug>`, for example `feat/42-ae-reconciliation`. Types match conventional
  commit types. Automated agents may use their own prefix.
- Open a draft pull request early; mark ready when CI is green and the checklist is complete.
- Keep pull requests small (about 400 changed lines or fewer) and focused on one issue.
- Unfinished work merges behind configuration or stays out of the default pipeline, not on a long branch.

## Merging

- Squash merge only; linear history. The pull request title becomes the commit message, so it must be a conventional commit.
- Link the issue in the description (`Closes #42`).
- Delete the branch on merge.

## Conventional commits

`<type>(<scope>): <summary>` in the imperative, British English, no full stop.

| Type | Use |
|---|---|
| `feat` | New capability (source, table, check) |
| `fix` | Bug fix |
| `docs` | Documentation and ADRs |
| `refactor`, `perf` | Internal change, speed |
| `test` | Tests only |
| `build`, `ci`, `chore` | Tooling, workflows, dependencies |

Scopes: `ingest`, `silver`, `gold`, `quality`, `lineage`, `contracts`, `sql`, `infra`, `rust`, `docs`, `deps`,
`process`. Breaking changes to a serving table schema use `!` (`feat(gold)!: ...`) and need an ADR or changelog note.
Add `Signed-off-by` (`git commit -s`) once the DCO is enforced.

## Required checks on `main` (branch protection)

- Status checks must pass and branches be up to date: `python (3.11)`, `python (3.12)`, `rust`, `terraform`.
- Pull request required; no direct pushes; no force pushes; linear history; resolve conversations.
- Reviews: zero required while solo (self-review with the template checklist). Raise to one review and
  enable "Require review from Code Owners" ([CODEOWNERS](../../.github/CODEOWNERS)) when contributors join.
- Dependabot pull requests follow the same rules; security updates are merged promptly.

## Releases

None yet. When datasets or the package are published: semantic versioning for the package, tags on `main`,
and a dated release log for data.
