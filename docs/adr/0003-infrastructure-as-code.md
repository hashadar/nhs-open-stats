# 0003. Infrastructure as code: Terraform

Date: 2026-10-07. Status: accepted.

## Context

AWS target, solo maintainer now, community contributors in about a year, public repository. The footprint is
small: S3, Glue and Athena, a scheduled Lambda, a budget alarm.

## Options

- **Terraform (or OpenTofu).** Declarative HCL, readable by non-developers, large community and examples,
  plan output is easy to review in pull requests, `terraform validate` runs offline in CI. Needs a state
  backend (S3 with locking). Licence is BUSL for HashiCorp's builds; OpenTofu is a compatible MPL-2.0 fork, and
  these files work with both.
- **AWS CDK (Python).** Same language as the pipeline, but synthesises CloudFormation, needs bootstrapping and
  Node tooling, and ties contributors to AWS-specific constructs. Diffs are harder to review.
- **Console clicks or CloudFormation by hand.** Rejected: not reproducible or reviewable.

## Decision

Terraform, in `infra/terraform`, with no account IDs or secrets in the repository (variables and a
gitignored `terraform.tfvars`). CI runs `fmt`, `init -backend=false` and `validate`. Apply is manual until
there is a reason to automate it.

## Consequences

- Contributors without AWS can still validate infrastructure changes.
- Switching to OpenTofu is a configuration change if the Terraform licence becomes a concern.
- The pipeline Lambda is behind `enable_pipeline` so foundations can be applied first.
