Provider "aws" {
     Access_key = "ACCESS_KEY_HERE"
     Secret_key= "SECRET_KEY_HERE"
     REGION = "us-east-1"
}
Resource "aws_instance" "forexample" {
    Ami = "ami-13be557e"
    Instance_type = "t2.micro"
}