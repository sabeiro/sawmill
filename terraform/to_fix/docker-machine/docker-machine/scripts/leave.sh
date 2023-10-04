#!/usr/bin/env bash
docker-machine ssh "$1" "docker swarm leave --force"