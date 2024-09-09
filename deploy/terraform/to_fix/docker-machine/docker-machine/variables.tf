variable "machines" {
  description = "A list of machine names to create"
  type        = list(string)
}

variable "http_proxy" {
  description = "The URL of the HTTP proxy server."
  default     = ""
}

variable "https_proxy" {
  description = "The URL of the HTTPS proxy server."
  default     = ""
}

variable "no_proxy" {
  description = "A string list of No Proxy addresses"
  default     = ""
}

variable "driver" {
  description = "The driver to use for creating the docker machines"
  default     = "virtualbox"
}

variable "insecure_registries" {
  description = "A string list of comma seperated insecure registries."
  default     = ""
}

variable "virtualbox_url" {
  description = "The URL for the virtualbox image to use. Will do nothing if you do not use the virtual box driver. Eg: https://github.com/boot2docker/boot2docker/releases/download/v18.06.0-ce/boot2docker.iso"
  default     = ""
}

variable "virtualbox_memory" {
  description = "Amount of Memory to assign to each virtual box machine, will do nothing if not using the virtual box driver"
  default     = "2048"
}

variable "swarm_manager" {
  description = "Name of the swarm manager if you want to create a swarm. If not provided it will just create a normal docker cluster"
  default     = ""
}

