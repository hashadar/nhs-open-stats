variable "project" {
  description = "Name prefix for resources."
  type        = string
  default     = "nhs-stats"
}

variable "region" {
  description = "Primary AWS region."
  type        = string
  default     = "eu-west-2"
}

variable "bucket_suffix" {
  description = "Globally unique suffix for bucket names (for example a short random string)."
  type        = string
}

variable "monthly_budget_usd" {
  description = "Monthly cost ceiling used by the budget alarm."
  type        = number
  default     = 50
}

variable "alert_emails" {
  description = "Addresses notified when spend crosses budget thresholds."
  type        = list(string)
}

variable "enable_pipeline" {
  description = "Create the scheduled ingestion Lambda. Requires pipeline_image_uri."
  type        = bool
  default     = false
}

variable "pipeline_image_uri" {
  description = "ECR image URI for the pipeline Lambda."
  type        = string
  default     = ""
}

variable "pipeline_schedule" {
  description = "EventBridge Scheduler expression for the monthly run (UTC)."
  type        = string
  default     = "cron(0 9 ? * THU *)"
}

variable "athena_bytes_scanned_cutoff" {
  description = "Per-query Athena scan limit in bytes (10 MB minimum)."
  type        = number
  default     = 1073741824
}
