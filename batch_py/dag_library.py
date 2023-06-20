import datetime
import json, os, base64, io
from sqlalchemy import create_engine, types
import pandas as pd
import pytz
import pyarrow as pa
import pyarrow.parquet as pq
from zipfile import ZipFile
import boto3
from boto3.s3.transfer import S3Transfer

def connectS3(bucketN="lightmeter"):
    cred = json.loads(os.environ['CRED_DICT'])
    digOce = cred['digOce']
    session = boto3.session.Session()
    client = session.client(**digOce)
    resource = boto3.resource(**digOce)
    transfer = S3Transfer(client)
    response = client.list_buckets()
    print(response['Buckets'])
    bucket = resource.Bucket(bucketN)
    return client, bucket

def connectDb():
  db_name, db_user, db_pass = os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_PASS']
  db_host, db_port = os.environ['DB_HOST'], os.environ['DB_PORT']
  db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
  db = create_engine(db_string)
  return db

def writeParquet(payload,fileN,metaD={}):
  table = pa.Table.from_pydict(payload)
  buf = pa.BufferOutputStream()
  buf = io.BytesIO()
  pq.write_table(table,buf,compression="lz4")
  byteF = buf.getvalue() # buf.getvalue().to_pybytes() 
  client = connectS3()
  client.put_object(Body=byteF,Bucket=bucketN,Key=fileN,Metadata=metaD,ACL='private')

def readParquet(fileN):
  buf = io.BytesIO()
  bucket.download_fileobj(fileN, buf)
  fileByt = buf.getvalue()
  reader = pa.BufferReader(fileByt)
  table = pq.read_table(reader)
  payload = pq.read_table(reader).to_pydict()
  return payload

