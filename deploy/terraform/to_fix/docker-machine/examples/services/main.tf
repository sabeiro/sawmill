data "terraform_remote_state" "docker_swarm_manager" {
  backend = "local"
  config = {
    path = "${path.module}/../swarm-cluster/terraform.tfstate"
  }
}

resource "docker_network" "nginx" {
  name     = "nginx"
  provider = docker.swarm_manager
  driver   = "overlay"
}

resource "docker_service" "nginx" {
  provider = docker.swarm_manager
  name     = "nginx"
  task_spec {
    container_spec {
      image = "nginx"
    }
    networks = [
      docker_network.nginx.name,
    ]
  }
  mode {
    global = true
  }
  endpoint_spec {
    ports {
      published_port = "80"
      target_port    = "80"
    }
  }
}

