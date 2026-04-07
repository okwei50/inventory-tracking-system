output "rds_endpoint" {
  value = aws_db_instance.main.address
}

output "rds_arn" {
  value = aws_db_instance.main.arn
}
