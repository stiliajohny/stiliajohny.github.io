terraform {
  cloud {
    organization = "non-existing-organization"
    workspaces {
      name = "non_existing_organization-indraft"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.75.2"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}