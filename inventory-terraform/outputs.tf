output "api_gateway_url" {
  value = module.apigateway.api_url
}

output "cloudfront_url" {
  value = module.cloudfront.cloudfront_url
}

output "rds_endpoint" {
  value = module.rds.rds_endpoint
}

output "s3_website_url" {
  value = module.s3.website_url
}
