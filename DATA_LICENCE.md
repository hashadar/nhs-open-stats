# Data licence and attribution

This repository contains code, not NHS data. Source data is downloaded by the pipeline from NHS England and
other public bodies, and is not committed (the `data/` directory is gitignored). Test fixtures are synthetic.

## Position

- **Code:** Apache License 2.0 (see `LICENSE`).
- **Source data:** NHS England states that statistics are published under the
  [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) (OGL).
  This is the working assumption and must be confirmed per series before a series is added to the
  catalogue. Series with third-party content, survey data or different terms must record that explicitly.
- **Derived datasets** (silver and gold tables, if ever published): OGL v3.0 permits adaptation and
  redistribution provided attribution is given and the licence is linked. Derived datasets will carry the
  same OGL v3.0 licence and the attribution statement below.

## Attribution statement

> Source: NHS England, statistical work areas (https://www.england.nhs.uk/statistics/statistical-work-areas/).
> Contains public sector information licensed under the Open Government Licence v3.0.
> Processed by the nhs-stats project; this is not an official NHS England product and has not been endorsed by them.

## Other obligations

- Do not imply endorsement by NHS England or any NHS organisation.
- Respect small-number suppression and disclosure-control notes in the source. Do not attempt to reverse them.
- The data is aggregate and organisational. It must not be used to identify individuals.
- No dataset is published yet. Publishing requires a decision recorded in `docs/adr/`.

This note is a working record, not legal advice.
