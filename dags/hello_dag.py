from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import json, os, base64, io, re, requests, datetime

with DAG(dag_id="hello_nkület", start_date=datetime.datetime(2022,11,14),schedule=None,schedule_interval='0 0 * * *') as dag:
    def say_hello():
        print("Enkület")
    PythonOperator(task_id="say_hello", python_callable=say_hello)
