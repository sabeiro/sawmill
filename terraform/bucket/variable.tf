data "external" "env" {
  program = ["${path.module}/env.sh"]
}
output "env" {
  value = data.external.env.result["aws_region"]
}
variable "bucket_name" {
        default = "intertino"
}
variable "acl_value" {
    default = "private"
}

