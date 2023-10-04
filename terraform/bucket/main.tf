provider "aws" {
    access_key = module.access.env.aws_access_key
    secret_key = module.access.env.aws_secret_key
    region = module.access.env.aws_region
}
module "access" {
        source = "../access_aws"
}
module "s3_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"
  bucket = "intertino"
  acl    = "private"
  control_object_ownership = true
  object_ownership         = "ObjectWriter"
  versioning = { enabled = true }
}
