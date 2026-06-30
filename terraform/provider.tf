terraform {
  required_providers {

    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

provider "aws" {
  region = "us-west-1"
}

terraform {
  backend "s3" {
    bucket = "task5-terraform-state-1234"
    key    = "terraform.tfstate"
    region = "us-west-1"
  }
}