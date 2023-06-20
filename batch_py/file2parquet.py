import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import boto3
from boto3.s3.transfer import S3Transfer
import json, os, base64, io
import hashlib,  mailparser
from time import sleep
import pandas as pd
import pytz

bucketN = "lightmeter"
cred = json.loads(os.environ['CRED_DICT'])['digOce']
folderN = "live-daily/"



db_name, db_user, db_pass = os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_PASS']
db_host, db_port = os.environ['DB_HOST'], os.environ['DB_PORT']
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

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

def parseObj(obj,contL):
  metadata = client.head_object(Bucket=bucketN,Key=obj.key)
  l1 = obj.key.split("/")[1:]
  if len(l1) < 4:
    return
  if len(l1) == 4:
    l1 = l1[:2] + ["Inbox"] + l1[2:]
  buf = io.BytesIO()
  bucket.download_fileobj(obj.key, buf)
  fileByt = buf.getvalue()
  if fileByt == b'': return
  objJ = json.loads(fileByt)
  try:
    msg = objJ['parsed_content']
  except:
    return
  l2 = {}
  for i in headerL:
    try:
      l2[i] = msg['headers'][i][0]
    except:
      continue
  for k in msg['parts']:
    try:
      l2['body'] = k['text']
      break
    except:
      continue
  try:
    l2['timestamp'] = metadata['Metadata']['timestamp']
  except:
    pass
  for i in objH:
    try:
      l2[i] = objJ[i]
    except:
      continue
  for i in ['In-Reply-To','Message-Id']:
      l2[i] = re.sub(">","",re.sub("<","",l2[i]))
  for i, k in enumerate(fileH):
    l2[k] = l1[i]
  contL.append(l2)  

def dump2sql(contL):
  mailD = pd.DataFrame(contL)
  def try_convert(x):
    try:
      return datetime.datetime.strptime(x,"%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=pytz.utc)
    except:
      return None
  
  mailD["Date"] = mailD['Date'].apply(lambda x: try_convert(x))
  def try_convert(x):
    try:
      return datetime.datetime.fromtimestamp(int(x.split(".")[0]))
    except:
      return 0
  
  mailD["timestamp_filename"] = mailD["filename"].apply(lambda x: try_convert(x))
  def try_convert(x):
    try:
      return "%04d-%02d" % (x.year,x.month)
    except:
      return "unknown"
  
  mailD.loc[:,"partition"] = mailD["Date"].apply(lambda x: try_convert(x))
  importType = {}
  for i in mailD.columns:
    importType[i] = types.VARCHAR()
  
  for i in dateL:
    importType[i] = types.DateTime()
  
  #for i in vectL:
    #mailD[i] = mailD[i].apply(literal_eval)
    #importType[i] = types.ARRAY(types.VARCHAR())
  
  mailD.to_sql("live",db,if_exists="replace",dtype=importType)


contL = []
for obj in bucket.objects.filter(Prefix=folderN):
  parseObj(obj,contL)

print("adding %d messages" % len(contL))
dump2sql(contL)


# def parseS3():

    
with DAG(dag_id="kafka_dump", start_date=datetime(2018,11,14),schedule=None) as dag:
    def say_hello():
        print("Enkület")
    PythonOperator(task_id="kafka_dump", python_callable=say_hello)
