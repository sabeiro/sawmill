import os, sys, gzip, random, csv, json, datetime, re, time
sys.path.append(os.environ['LAV_DIR']+'/src/')
baseDir = os.environ['LAV_DIR']
import pandas as pd
import urllib3, requests
import psycopg2
from sqlalchemy import create_engine

if __name__=="__main__":
  db_name, db_user, db_pass = os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_PASS']
  db_host, db_port = os.environ['DB_HOST'], os.environ['DB_PORT']
  db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
  db = create_engine(db_string)
  
  res = db.execute("SELECT datname FROM pg_database;")
  for r in res: print(r)
  res = db.execute("select * from pg_catalog.pg_tables where schemaname = 'public';")
  for r in res: print(r)
  print('------------------------te-se-qe-te-ve-be-te-ne------------------------')
