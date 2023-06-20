from airflow import DAG
from airflow.operators.python import PythonOperator
import json, os, base64, io, re, datetime, tarfile
import dag_library as d_l

with DAG(dag_id="bi_prep",start_date=datetime.datetime(2022,11,14),tags=["sql","BI"],schedule='0 5 * * *') as dag:
    def bi_prep():
      db = d_l.connectDb()
      db.execute("call prepare_bi();")
      print("Enkület")
    PythonOperator(task_id="bi_prep_pull",python_callable=bi_prep)
