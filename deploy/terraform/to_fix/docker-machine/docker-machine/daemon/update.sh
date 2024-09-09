#!/usr/bin/env bash

docker-machine scp daemon.json $1:/home/docker
docker-machine ssh $1 "sudo mv /home/docker/daemon.json /etc/docker"
docker-machine ssh $1 "sudo /etc/init.d/docker restart"
