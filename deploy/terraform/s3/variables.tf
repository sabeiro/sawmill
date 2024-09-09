locals {
  dot_env_file_path = "/home/sabeiro/credenza/aws.sh"
  dot_env_regex     = "(?m:^\\s*([^#\\s]\\S*)\\s*=\\s*[\"']?(.*[^\"'\\s])[\"']?\\s*$)"
  dot_env           = { for tuple in regexall(local.dot_env_regex, file(local.dot_env_file_path)) : tuple[0] => sensitive(tuple[1]) }
  aws_access_key    = local.dot_env["aws_acccess_key"]
  aws_secret_key    = local.dot_env["aws_secret_key"]
  region            = local.dot_env["aws_region"]
}
variable "bucket_name" {
  	description = "Name of the s3 bucket. Must be unique."
	type        = string
	default	= "dauvi"
}

variable "tags" {
  description = "Tags to set on the bucket."
  type        = map(string)
  default     = {}
}

