docker-compose exec airflow-worker airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password ${AIRFLOW_ADMIN}
