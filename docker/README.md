# sawmill docker 

This is a docker based on-prem data cloud including

* webserver (nginx)
* database (postgres)
* UI (metabase)
* tracking (prometheus)

optional:

* messaging (kafka/mosquitto)
* presto
* dbt
* runner (gitlab)
* ui-docker 
* airflow
* logstash-elasticsearch-kibana

# setup

copy `credenza/database.env` into a safe place, polulate it and run it.
take `swarm_manage.sh` and create what is missing (log folders and network at least).

run `docker-compose up -d`

cd into the optional service you need and run docker-compose again.


