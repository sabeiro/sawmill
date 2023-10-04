output "swarm_manager_name" {
  value = var.machines[0]
}

output "swarm_manager_url" {
  value = chomp(module.docker_machine.swarm_manager_host_url)
}

output "swarm_manager_host_ip" {
  value = module.docker_machine.machine_ips
}
