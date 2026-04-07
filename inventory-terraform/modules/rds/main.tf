resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-subnet-group"
  subnet_ids = [var.private_subnet_1a, var.private_subnet_1b]

  tags = {
    Name = "${var.project_name}-subnet-group"
  }
}

resource "aws_db_instance" "main" {
  identifier           = "${var.project_name}-database"
  engine               = "postgres"
  engine_version       = "16.6"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  storage_type         = "gp2"
  db_name              = var.db_name
  username             = var.db_username
  password             = var.db_password
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.rds_sg_id]
  publicly_accessible  = false
  skip_final_snapshot  = true
  deletion_protection  = false

  tags = {
    Name = "${var.project_name}-database"
  }
}
