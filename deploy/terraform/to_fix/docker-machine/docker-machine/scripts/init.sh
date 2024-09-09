#!/usr/bin/env bash
set -e
ip=$(docker-machine ls --filter NAME=$1 -f {{.URL}} | awk -F[/:] '{print $4}')
docker-machine ssh "$1" "docker swarm init --advertise-addr $ip"
