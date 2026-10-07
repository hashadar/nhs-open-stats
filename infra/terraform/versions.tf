terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.67"
    }
  }

  # Remote state is configured per environment, not committed:
  #   terraform init -backend-config="bucket=<state-bucket>" -backend-config="key=nhs-stats/terraform.tfstate"
  # backend "s3" {}
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project   = var.project
      ManagedBy = "terraform"
    }
  }
}

# AWS Budgets is a global service served from us-east-1.
provider "aws" {
  alias  = "budgets"
  region = "us-east-1"
}
