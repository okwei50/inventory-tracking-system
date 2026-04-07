module "vpc" {
  source       = "./modules/vpc"
  project_name = var.project_name
}

module "s3" {
  source       = "./modules/s3"
  project_name = var.project_name
}

module "rds" {
  source            = "./modules/rds"
  project_name      = var.project_name
  db_password       = var.db_password
  db_username       = var.db_username
  db_name           = var.db_name
  private_subnet_1a = module.vpc.private_subnet_1a
  private_subnet_1b = module.vpc.private_subnet_1b
  vpc_id            = module.vpc.vpc_id
  rds_sg_id         = module.vpc.rds_sg_id
}

module "lambda" {
  source       = "./modules/lambda"
  project_name = var.project_name
  db_host      = module.rds.rds_endpoint
  db_password  = var.db_password
  db_username  = var.db_username
  db_name      = var.db_name
  private_subnet_1a = module.vpc.private_subnet_1a
  vpc_id            = module.vpc.vpc_id
  lambda_sg_id      = module.vpc.lambda_sg_id
}

module "apigateway" {
  source        = "./modules/apigateway"
  project_name  = var.project_name
  lambda_arn    = module.lambda.lambda_arn
  lambda_name   = module.lambda.lambda_name
}

module "cloudfront" {
  source            = "./modules/cloudfront"
  project_name      = var.project_name
  s3_website_endpoint = module.s3.website_endpoint
}
