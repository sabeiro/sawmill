provider "aws" {
    access_key = module.access.env.aws_access_key
    secret_key = module.access.env.aws_secret_key
    region = module.access.env.aws_region
}
module "access" {
        source = "../access_aws"
}

