variable "project_name" {}
variable "db_host" {}
variable "db_password" { sensitive = true }
variable "db_username" {}
variable "db_name" {}
variable "private_subnet_1a" {}
variable "vpc_id" {}
variable "lambda_sg_id" {}
