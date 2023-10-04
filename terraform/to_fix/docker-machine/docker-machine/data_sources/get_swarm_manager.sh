#!/bin/bash
set -e
eval "$(jq -r '@sh "HOST=\(.host)"')"
RESULT=""
if [ ! "${HOST}" = "" ]
then
  RESULT=`docker-machine ls --filter NAME=$HOST --format={{.URL}}`
fi
jq -n --arg result "$RESULT" '{"url":$result}'