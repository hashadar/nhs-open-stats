resource "aws_glue_catalog_database" "gold" {
  name        = replace("${var.project}_gold", "-", "_")
  description = "Dashboard-serving tables. Table definitions are added per gold table."
}

resource "aws_athena_workgroup" "main" {
  name = var.project

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true
    bytes_scanned_cutoff_per_query     = var.athena_bytes_scanned_cutoff

    result_configuration {
      output_location = "s3://${aws_s3_bucket.lake.bucket}/athena-results/"

      encryption_configuration {
        encryption_option = "SSE_S3"
      }
    }
  }
}
