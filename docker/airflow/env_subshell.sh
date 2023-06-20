export AIRFLOW_UID=$(id -u) #> .env
echo $AIRFLOW_UID
mkdir -p ./dags ./logs ./plugins
echo "set enable-bracketed-paste off" >> ~/.inputrc
