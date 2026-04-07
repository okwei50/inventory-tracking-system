variable "aws_region" {
  default = "ca-central-1"
}

variable "db_password" {
  description = "RDS master password"
  sensitive   = true
}

variable "db_username" {
  default = "postgres"
}

variable "db_name" {
  default = "postgres"
}

variable "project_name" {
  default = "inventory"
}
