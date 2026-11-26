output "state_bucket_name" {
  description = "The S3 bucket name used for Terraform state storage"
  value       = aws_s3_bucket.terraform_state.id
}

output "state_lock_table_name" {
  description = "The DynamoDB table name used for Terraform state locking"
  value       = aws_dynamodb_table.terraform_state_lock.name
}

output "state_bucket_region" {
  description = "The AWS region where the state bucket lives"
  value       = var.aws_region
}