import os, sys, gzip, random, csv, json, datetime, re, time
import pandas as pd
import urllib3, requests
import psycopg2
from sqlalchemy import create_engine
import prestodb

PRESTO_SERVER="coordinator"
PRESTO_SERVER="localhost"

if __name__=="__main__":
  conn = prestodb.dbapi.connect(host=PRESTO_SERVER,port=8090,user=os.environ['DB_USER'],catalog='kafka',schema='default')
  cur = conn.cursor()
  cur.execute('SHOW TABLES')
  rows = cur.fetchall()
  print(rows)
  print('------------------------te-se-qe-te-ve-be-te-ne------------------------')
