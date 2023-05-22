from airflow import DAG
from airflow.operators.python import PythonOperator
import json, os, base64, io, datetime
import pandas as pd
import dag_library as d_l

def loadCsv():
    db = d_l.connectDb()
    mailM = pd.read_csv("/raw/mailboxes_client.csv")
    mailM.to_sql("client_mail",db,if_exists="replace")

with DAG(dag_id="upload_csv",start_date=datetime.datetime(2022,11,14),schedule='0 0 * * *',tags=["lookup","offline"]) as dag:
    def upload_csv():
        loadCsv()
        print("Enkület")
    PythonOperator(task_id="upload_csv", python_callable=upload_csv)
