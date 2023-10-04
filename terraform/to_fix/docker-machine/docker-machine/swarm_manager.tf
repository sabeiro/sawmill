# Creates a new swarm manager (based on the given name)
resource "null_resource" "swarm-manager" {
  count      = var.swarm_manager != "" ? 1 : 0
  depends_on = [null_resource.create]

  triggers = {
    driver              = var.driver
    virtualbox_url      = var.virtualbox_url
    virtualbox_memory   = var.virtualbox_memory
    http_proxy          = var.http_proxy
    no_proxy            = var.no_proxy
    insecure_registries = var.insecure_registries
    machines            = join(" ", var.machines)
  }
  provisioner "local-exec" {
    command     = "./init.sh ${var.swarm_manager}"
    working_dir = "${path.module}/scripts"
  }

  provisioner "local-exec" {
    when        = destroy
    command     = "./leave.sh ${var.swarm_manager}"
    working_dir = "${path.module}/scripts"
  }
}

data "external" "swarm_manager_ip" {
  program    = ["${path.module}/data_sources/get_swarm_manager.sh"]
  depends_on = [null_resource.swarm-manager]
  query = {
    host = var.swarm_manager
  }
}

