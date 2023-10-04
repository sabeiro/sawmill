#!/usr/bin/env bash
set -e
token=$(docker-machine ssh "$1" "docker swarm join-token -q worker")
ip=$(docker-machine ls --filter NAME="$1" -f {{.URL}} | awk -F[/:] '{print $4}')
docker-machine ssh "$2" "docker swarm join --token $token $ip:2377"