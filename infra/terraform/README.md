# Infrastructure

Terraform for the AWS foundations: two S3 buckets (raw and lake), a Glue database and Athena workgroup with a
scan cap, a 50 USD monthly budget alarm, and an optional scheduled Lambda. See `docs/adr/0003` and `0004`.

```bash
cp terraform.tfvars.example terraform.tfvars   # gitignored; never commit account details
terraform init -backend=false && terraform validate   # offline check
terraform plan                                        # needs AWS credentials
```

OpenTofu is compatible with these files.
