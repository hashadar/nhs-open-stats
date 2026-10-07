<!-- Title must be a conventional commit, for example: feat(quality): reconcile A&E totals to England row -->

## What and why

Closes #

## How it was checked

- [ ] `uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest`
- [ ] Rust and Terraform checks, if touched

## Checklist

- [ ] Meets the issue's acceptance criteria and the definition of done
- [ ] Contract, quality checks and data dictionary updated for any table change
- [ ] ADR added for any significant decision
- [ ] No secrets, account identifiers or real data committed
- [ ] Commits are signed off (once DCO is enforced)
