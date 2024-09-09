#!/bin/bash
set -e
set -x
eval "$(jq -r '@sh "MACHINE=\(.machine)"')"
RESULT=$(docker-machine ip $(docker-machine ls -q --filter NAME=$MACHINE))
jq -n --arg result "$RESULT" '{"ip":$result}'