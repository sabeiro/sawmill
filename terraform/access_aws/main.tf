provider "aws" {
    access_key = data.external.env.result["aws_access_key"]
    secret_key = data.external.env.result["aws_secret_key"]
    region = data.external.env.result["aws_region"]
}

