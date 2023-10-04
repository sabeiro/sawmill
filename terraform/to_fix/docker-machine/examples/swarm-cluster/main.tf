# This creates a single docker machine node (Not in swarm mode). This would be essentially the same as running
#   docker-machine create <NAME>
# The difference is that the terraform state will try and determine if the machine has changed.
module "docker_machine" {
  source        = "../../docker-machine"
  machines      = var.machines
  swarm_manager = var.machines[0]
}
