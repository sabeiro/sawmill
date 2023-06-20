---
title: "Sawmill library description"
author: Giovanni Marelli
date: 2017-01-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# Sawmill

Infra for data pipeline ingesting real time and batch data, processing logs and visualize data.

![log](docs/f/log2.jpg "log")
_processing big logs_

# data-pipeline

This project is a collection of jobs and configurations to set up a data anlytics cluster. 

## Getting started

Clone the repository on the target instance, cd into `/docker` and run

```
docker-compose up -d
```

## Features

* nginx ~~traefik~~ webserver 8080
* postgres database :5432
* docker-ui :9000
* prometheus :6032 
* airflow and dags
* custom ETL scripts
* kubernetes

## Project structure

* `airflow/`: configuration files for airflow
* `dags/`: list of jobs to run periodically
* `db_connect/`: `golang` backend for db communication
* `parse_sources/`: `python` ETL jobs
* `docker/`: docker compose file 
* `docker/postgres/`: configurations and environment for postgres
* `docker/db-data/`: all the db data external from the container to backup
* `docker/logs/`: all the docker logs data 
* `docker/traefik/`: configuration and routes
* `terraform/`: terraform configuration, currently on digital ocean



## Support

Open an issue tracker

## Roadmap

- **cluster**: build the cluster, prepare the containers and link them
- **central db**: set up a central db (digital ocean?) and create an API
- **platform integration**: ad-hoc ETL, lambda, postman
- **replace routines**: decouple from the monolith to single services
- **refining requirements**: metrics, data structure, touchpoints
- **API building**: document with swagger


## License

[CC by-sa-nc](https://creativecommons.org/licenses/by-nc-sa/4.0/)


