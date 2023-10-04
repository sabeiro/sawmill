provider "docker" {
  alias = "swarm_manager"
  host  = data.terraform_remote_state.docker_swarm_manager.outputs.swarm_manager_url
  cert_path = pathexpand(
    "~/.docker/machine/machines/${data.terraform_remote_state.docker_swarm_manager.outputs.swarm_manager_name}",
  )
}

