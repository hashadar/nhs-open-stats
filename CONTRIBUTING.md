# Contributing

The project is a personal repository that is intended to open to contributors in about a year. Issues and
discussion are welcome now; pull requests may be slow to review. This is a stub that will be expanded.

## Set up

```bash
uv sync
uv run pre-commit install
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
```

Rust and Terraform checks are listed in the README.

## Working agreements

- Trunk-based development, short-lived branches, conventional commits, CI must pass:
  see [docs/process/branching-and-prs.md](docs/process/branching-and-prs.md).
- Work is tracked as GitHub issues; see [docs/process/README.md](docs/process/README.md).
- Tests run offline and use synthetic fixtures. Never commit real data, credentials or account identifiers.
- Significant decisions get an ADR in `docs/adr/`.
- British English, no emojis, comments that explain intent only.
- Sign off commits (`git commit -s`) to certify the [Developer Certificate of Origin](https://developercertificate.org/).
  Enforcement starts when contributions open.

## Adding a source

1. Confirm the licence and record it.
2. Add a module in `src/nhs_stats/sources/`, a contract in `contracts/`, SQL in `sql/gold/`, fixtures and tests.
3. Add a data dictionary entry.
