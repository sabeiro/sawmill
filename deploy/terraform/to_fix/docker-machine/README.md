# terraform-docker-machine

A Terraform Module that provisions Docker Machines, either in stand alone mode, or as a docker swarm. The purpose of the
module is to provide a local swarm environment for testing and building docker swarms. It tries to be as simple as 
possible and allow a single terraform up to create. With orchestration solutions being more common and the problems I
often experience trying to test a orchestrated deployment, I often turn to docker-machine to determine possible problems
before putting services on a production cluster.

_This module is a work in progress and may contain weird bugs, assumptions or unseen issues. For that reason I would
not recommend this as a Production Ready solution. Feel free to add or extend the module for your own requirements. This
is in no way a complete example of how to manage docker machines._

## Usage

Examples can be found in the examples directory, with additional README's in each example describing usage and use
cases.

The simpliest example however would look as follows

```hcl
module "docker-machine" {
  source = "git::https://github.com/stevenandrewcarter/terraform-docker-machine.git//docker-machine"
  machines = ["local"]
}
```

which will create a single docker machine instance.

## Concepts

Terraform allows you to provision infrastructure fairly easily, at least in most cases. The problem I wanted to solve
with this module is to allow you to easily create a sandbox environment to test docker swarm solutions without
having to either spin up a lot of cloud infrastructure or having existing environments in place to test swarm on.

As of writing this module, Docker-Machine does not have a supported Terraform provider, and its not likely that a
provider will be made anytime soon. It is possible to build a swarm cluster outside of terraform by just using the 
docker-machine CLI, but I found that it can sometimes get a little manual to configure a cluster everytime you want to
test swarm concepts. This becomes even more tedious if you have to make mass changes to the cluster, such as configuring
proxy settings or adjusting the Docker Engine settings.

## Issues

At the current version of terraform (0.11.x), you will get errors with the output when trying to destroy a docker-machine
cluster. I have been looking into work arounds to try and remove this error. The current solution is to add the environment
variable as [issue](https://github.com/hashicorp/terraform/issues/18197) recommends.

Also making changes will force the entire cluster to be rebuilt, which is obviously a bad thing if you have any sort of
persistence on the cluster. I would not recommend running *Production* workloads using this solution.
