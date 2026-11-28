variable "aws_region" {
  description = "AWS region for the Terraform state bucket and lock table"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (used in tags and resource names)"
  type        = string
  default     = "bootstrap"
}

variable "project" {
  description = "Project name (used in tags and resource names)"
  type        = string
  default     = "bootstrap"
}

variable "owner" {
  description = "Owner name (used in tags and resource names)"
  type        = string
  default     = "bootstrap"
}

variable "team" {
  description = "Team name (used in tags and resource names)"
  type        = string
  default     = "bootstrap"
}

variable "state_bucket_name" {
  description = "Globally unique S3 bucket name for Terraform state storage"
  type        = string
}

variable "state_lock_table_name" {
  description = "DynamoDB table name for Terraform state locking"
  type        = string
  default     = "terraform-state-lock"
}
variable "aws_profile" {
  description = "Named AWS CLI profile used by the bootstrap provider"
  type        = string
  default     = "aws-batch-data-platform"
}
