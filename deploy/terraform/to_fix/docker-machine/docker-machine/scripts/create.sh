#!/bin/bash
# Creates a Docker-Machine based on the given parameters
cmd="docker-machine create"
name=""
while [ $# -gt 0 ]; do
  case "$1" in
    --driver=*)
      if [ ! "${1#*=}" = "" ]
      then
        cmd+=" --driver ${1#*=}"
      fi
      ;;
    --virtualbox-boot2docker-url=*)
      if [ ! "${1#*=}" = "" ]
      then
        cmd+=" --virtualbox-boot2docker-url ${1#*=}"
      fi   
      ;;
    --virtualbox-memory=*)
      if [ ! "${1#*=}" = "" ]
      then
        cmd+=" --virtualbox-memory ${1#*=}"
      fi      
      ;;
    --HTTP_PROXY=*)
      if [ ! "${1#*=}" = "" ]
      then
        cmd+=" --engine-env HTTP_PROXY=${1#*=}"
      fi
      ;;
    --HTTPS_PROXY=*)
      if [ ! "${1#*=}" = "" ]
      then
        cmd+=" --engine-env HTTPS_PROXY=${1#*=}"
      fi
      ;;
    --NO_PROXY=*)
      if [ ! "${1#*=}" = "" ]
      then
        cmd+=" --engine-env NO_PROXY=${1#*=}"
      fi
      ;;
    --engine-insecure-registry=*)
      if [ ! "${1#*=}" = "" ]
      then
        cmd+=" --engine-insecure-registry ${1#*=}"
      fi 
      ;;
    --name=*)
      if [ ! "${1#*=}" = "" ]
      then
        cmd+=" ${1#*=}"
        name="${1#*=}"
      fi
      ;;       
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.*\n"
      printf "***************************\n"
      exit 1
  esac
  shift
done
$cmd