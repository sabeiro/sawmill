#!/usr/bin/env bash

for i in {2..3} ; do
    docker-machine ssh local${i} "docker swarm leave"
done

for i in {1..3} ; do
    echo "### Refreshing certs local$i..."
    docker-machine regenerate-certs -f local${i}
done

# Rejoin swarm
token=$(docker-machine ssh local1 "docker swarm join-token -q worker")
ip=$(docker-machine ls --filter NAME=local1 -f {{.URL}} | awk -F[/:] '{print $4}')
for i in {2..3} ; do
    docker-machine ssh local${i} "docker swarm leave"
    docker-machine ssh local${i} "docker swarm join --token $token $ip:2377"
done