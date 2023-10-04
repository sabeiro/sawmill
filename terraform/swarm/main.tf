resource "null_resource" "docker_swarm" {

    provisioner "local-exec" {
      command = "docker swarm init"
    }

    provisioner "local-exec" {
      command = <<EOF
        docker swarm leave --force

        # Careful here. This assumes you want a clean Docker slate,
        # remove all Docker volumes from your machine.
        docker volume rm -f $(docker volume ls -q) 
EOF
      when = "destroy"
    }
}

resource "null_resource" "start_stack" {

    provisioner "local-exec" {
      command = "docker stack deploy -c ./docker-stack.yml demostack"
    }

    provisioner "local-exec" {
      command = "docker stack rm demostack"
      when = "destroy"
    }

    depends_on = ["null_resource.docker_swarm"]
}
