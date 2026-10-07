# Scheduled ingestion: EventBridge Scheduler -> Lambda (container image).
# Disabled by default so the foundations can be applied before an image exists.

resource "aws_ecr_repository" "pipeline" {
  count                = var.enable_pipeline ? 1 : 0
  name                 = "${var.project}-pipeline"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_cloudwatch_log_group" "pipeline" {
  count             = var.enable_pipeline ? 1 : 0
  name              = "/aws/lambda/${var.project}-pipeline"
  retention_in_days = 30
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "pipeline" {
  statement {
    actions = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
    resources = [
      aws_s3_bucket.raw.arn, "${aws_s3_bucket.raw.arn}/*",
      aws_s3_bucket.lake.arn, "${aws_s3_bucket.lake.arn}/*",
    ]
  }
}

resource "aws_iam_role" "pipeline" {
  count              = var.enable_pipeline ? 1 : 0
  name               = "${var.project}-pipeline"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy" "pipeline" {
  count  = var.enable_pipeline ? 1 : 0
  name   = "data-access"
  role   = aws_iam_role.pipeline[0].id
  policy = data.aws_iam_policy_document.pipeline.json
}

resource "aws_iam_role_policy_attachment" "pipeline_logs" {
  count      = var.enable_pipeline ? 1 : 0
  role       = aws_iam_role.pipeline[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "pipeline" {
  count         = var.enable_pipeline ? 1 : 0
  function_name = "${var.project}-pipeline"
  role          = aws_iam_role.pipeline[0].arn
  package_type  = "Image"
  image_uri     = var.pipeline_image_uri
  timeout       = 900
  memory_size   = 2048

  environment {
    variables = {
      NHS_STATS_RAW_BUCKET  = aws_s3_bucket.raw.bucket
      NHS_STATS_LAKE_BUCKET = aws_s3_bucket.lake.bucket
    }
  }

  depends_on = [aws_cloudwatch_log_group.pipeline]
}

data "aws_iam_policy_document" "scheduler_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "scheduler" {
  count              = var.enable_pipeline ? 1 : 0
  name               = "${var.project}-scheduler"
  assume_role_policy = data.aws_iam_policy_document.scheduler_assume.json
}

resource "aws_iam_role_policy" "scheduler" {
  count = var.enable_pipeline ? 1 : 0
  name  = "invoke-pipeline"
  role  = aws_iam_role.scheduler[0].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "lambda:InvokeFunction"
      Resource = aws_lambda_function.pipeline[0].arn
    }]
  })
}

resource "aws_scheduler_schedule" "pipeline" {
  count               = var.enable_pipeline ? 1 : 0
  name                = "${var.project}-pipeline"
  schedule_expression = var.pipeline_schedule

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.pipeline[0].arn
    role_arn = aws_iam_role.scheduler[0].arn
  }
}
