terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "inventory-data-buckett"
    key    = "terraform/state/terraform.tfstate"
    region = "ca-central-1"
  }
}

provider "aws" {
  region = var.aws_region
}
