# Assigns all other machines as workers to the swarm
resource "null_resource" "swarm-workers" {
  depends_on = [null_resource.swarm-manager]

  count = length(var.machines) - 1

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
    command     = "./join.sh ${var.swarm_manager} ${var.machines[count.index + 1]}"
    working_dir = "${path.module}/scripts"
  }

  provisioner "local-exec" {
    when        = destroy
    command     = "./leave.sh ${var.machines[count.index + 1]}"
    working_dir = "${path.module}/scripts"
  }
}

