# locals {
#  envs = { for tuple in regexall("(.*)=(.*)", file("aws.sh")) : tuple[0] => sensitive(tuple[1]) }
# }
# output "envs" {
#  value = local.envs["HOST"]
#  sensitive = true # this is required if the sensitive function was used when loading .env file (more secure way)
#}

data "external" "env" {
  program = ["${path.module}/env.sh"]
}
output "env" {
  value = data.external.env.result
}
