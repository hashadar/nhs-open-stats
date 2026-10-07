# 0007. Licensing

Date: 2026-10-07. Status: accepted (code licence to be confirmed by the owner before the repository is public).

## Decision

- **Code: Apache License 2.0.**
- **Data attribution: OGL v3.0**, recorded in `NOTICE` and `DATA_LICENCE.md`.

## Why Apache-2.0 rather than MIT

| | Apache-2.0 | MIT |
|---|---|---|
| Patent grant | Explicit, with retaliation clause | None stated |
| Contributions | Inbound equals outbound by default (section 5) | Implicit |
| Attribution | `NOTICE` file mechanism suits mandatory OGL attribution | Copyright line only |
| Length and familiarity | Longer, widely accepted by companies | Shortest, most familiar |
| Compatibility | Compatible with GPLv3, not GPLv2 | Compatible with both |

The project expects outside contributors and corporate users within a year, and must carry a data
attribution notice. Apache-2.0's patent grant and `NOTICE` mechanism fit that better than MIT, at the cost of
more text. Dependencies (polars, DuckDB, httpx, PyYAML, PyO3) are MIT, Apache-2.0 or BSD licensed.

## Contributions

Use the Developer Certificate of Origin (`Signed-off-by` trailer) rather than a CLA, to keep the barrier low.
Not enforced yet; enforce when contributions open.

## Data

OGL v3.0 requires attribution and a link to the licence, and allows adaptation and redistribution. Terms must be
confirmed per series; NHS England's site terms were not verified during planning. No datasets are published yet.
