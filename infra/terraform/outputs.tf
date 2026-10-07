output "raw_bucket" {
  value = aws_s3_bucket.raw.bucket
}

output "lake_bucket" {
  value = aws_s3_bucket.lake.bucket
}

output "athena_workgroup" {
  value = aws_athena_workgroup.main.name
}
