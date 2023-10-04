variable "public_key_path" {
  description = "Path to the SSH public key to be used for authentication"
  default = "/home/sabeiro/.ssh/id_rsa.pub"
}

variable "do_key_name" {
  description = "Name of the key on Digital Ocean"
  default     = "terraform"
}
