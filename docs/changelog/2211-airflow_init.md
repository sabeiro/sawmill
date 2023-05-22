Changelog: 22-11-08

* added airflow (init, webserver, worker, redis, scheduler, flower)
* airflow connected to existing db
* postgres ports masked
* traefik insecure disabled
* changed database password
* closed postgres ports outside of container network
* created a light image for live middleware (apline)
* created a full feature image for batch processes
* separated live containers from batch containers
* kafka interface doesn't quit if connection with kafka is broken. No more timeout
* `ingest.` reworked on the `/consume/` endpoint
* tested `ingest.` and `interface.` endpoints

