# Create the Docker Machines, this will invoke a external script so that empty / blank parameters can be ignored. In
# addition it also configures the docker engine based on the Daemon.JSON and sets some vm properties on each docker
# machine
resource "null_resource" "create" {
  count = length(var.machines)

  triggers = {
    driver              = var.driver
    virtualbox_url      = var.virtualbox_url
    virtualbox_memory   = var.virtualbox_memory
    http_proxy          = var.http_proxy
    no_proxy            = var.no_proxy
    insecure_registries = var.insecure_registries
    machines            = join(" ", var.machines)
  }

  # Provision docker machines based on the scripts/create.sh
  provisioner "local-exec" {
    command = <<EOF
    ./create.sh \
      --driver=${var.driver} \
      --virtualbox-boot2docker-url=${var.virtualbox_url} \
      --virtualbox-memory=${var.virtualbox_memory} \
      --HTTP_PROXY=${var.http_proxy} \
      --HTTPS_PROXY=${var.https_proxy} \
      --NO_PROXY=${var.no_proxy}  \
      --engine-insecure-registry=${var.insecure_registries} \
      --name=${element(var.machines, count.index)}

EOF
    working_dir = "${path.module}/scripts"
  }

  # Sets the vm.max_map_count on the Docker Machines
  provisioner "local-exec" {
    command = "docker-machine ssh ${var.machines[count.index]} 'sudo sysctl -w vm.max_map_count=262144'"
  }

  # Updates the Daemon with a new daemon.json
  provisioner "local-exec" {
    command = "./update.sh ${var.machines[count.index]}"
    working_dir = "${path.module}/daemon"
  }

  # Removes the machines on Terraform Destroy
  provisioner "local-exec" {
    when = destroy
    command = "docker-machine rm -y ${var.machines[count.index]}"
  }
}

data "external" "docker_machine_ips" {
  count = length(var.machines)
  program = ["${path.module}/data_sources/get_machine.sh"]
  depends_on = [null_resource.create]
  query = {
    machine = var.machines[count.index]
  }
}
