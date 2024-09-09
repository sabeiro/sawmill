provider "aws" {
    access_key = module.access.env.aws_access_key
    secret_key = module.access.env.aws_secret_key
    region = module.access.env.aws_region
}
module "access" {
	source = "../access_aws"
}
resource "aws_instance" "web" {
  ami = "ami-04e601abe3e1a910f" # ubuntu
  instance_type = "t2.micro"
  subnet_id = aws_subnet.frontend.id
}
resource "aws_subnet" "frontend" {
  vpc_id = aws_vpc.apps.id
  cidr_block = "10.0.1.0/24"
}
resource "aws_vpc" "apps" {
  cidr_block = "10.0.0.0/16"
}

