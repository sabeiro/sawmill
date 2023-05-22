from airflow import DAG
from airflow.operators.python import PythonOperator
import json, os, base64, io, re, datetime, tarfile
import hashlib,  mailparser
from time import sleep
import pandas as pd
import pytz
from ast import literal_eval
import dag_library as d_l
from sqlalchemy import create_engine, types

mexH = ['creation_time','direction','sender','recipients','queue_id','categories']
bucketN = "lightmeter"
minutes = 60*24
cred = json.loads(os.environ['CRED_DICT'])['digOce']
bucketN = "lightmeter"
folderN = "live_zip/"
dateL = ['Date','timestamp_filename']
headerL = ['from','to','subject','body','date','message-id','auto-submitted','return-path','timezone','received','delivered-to','to_domains']
headerL = ['Date','From', 'In-Reply-To','Message-Id','Received','References','Subject','To']
objH = ['creation_time','direction','sender','recipients','queue_id','categories','filename','relay']
fileH = ['domain','user','folder','folder_current','filename']
metaH = ['categories','creation-time','direction','queue-id','recipients','sender','timestamp']
vectL = ['recipients','categories']

blockL = ['dovecot.index.cache','dovecot.index.log']
lastMod = datetime.datetime(2022,9,1,tzinfo=None)
yesterday = str(datetime.date.today()-datetime.timedelta(days=1))

def listObj():
    ts = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
    ts_milliseconds = ts.timestamp()*1000.0
    client, bucket = d_l.connectS3(bucketN)
    dL = []
    paginator = client.get_paginator('list_objects')
    for page in paginator.paginate(Bucket=bucketN,Prefix=folderN,Delimiter='/'):
        for obj in page.get('Contents'):
            dL.append(obj.get('Key'))
    return dL

def parseObj(fileByt):
  objJ = json.loads(fileByt)
  l1 = objJ['filename'].split("/")[1:]
  if len(l1) < 4: return
  if len(l1) == 4: l1 = l1[:2] + ["Inbox"] + l1[2:]
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
    objJ['categories'] = str(objJ['categories'])
    objJ['recipients'] = str(objJ['recipients'])
  except:
    pass
  for i in objH:
    try:
      l2[i] = objJ[i]
    except:
      continue
  for i in ['In-Reply-To','Message-Id']:
      try:
        l2[i] = re.sub(">","",re.sub("<","",l2[i]))
      except:
        pass
  for i, k in enumerate(fileH):
    l2[k] = l1[i]
  return l2

def parseTar(obj,contL):
  client, bucket = d_l.connectS3(bucketN)
  metadata = client.head_object(Bucket=bucketN,Key=obj.key)
  if obj.size == 0:
      return
  buf = io.BytesIO()
  bucket.download_file(obj.key,"/tmp/s3_file.tar.gz")
  s3Dir = "/tmp/s3_dir/"
  file_obj = tarfile.open("/tmp/s3_file.tar.gz","r:gz")
  file_obj.extractall(s3Dir)
  namelist = file_obj.getnames()
  fL = [x for x in namelist if re.search("\.json",x)]
  fL1 = [x for x in namelist if re.search("\.txt",x)]
  fL = fL + fL1
  print("processing %s folder with %d files" % (obj.key,len(fL)))
  if len(fL) == 0: return
  for f in fL:
      fileByt = open(s3Dir+f,'rb').read()
      if fileByt == b'': continue
      mex = parseObj(fileByt)
      contL.append(mex)
  file_obj.close()

def parseDataframe(contL):
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
  
  mailD.loc[:,"partition"] = mailD["timestamp_filename"].apply(lambda x: try_convert(x))
  importType = {}
  for i in mailD.columns:
    importType[i] = types.VARCHAR()
  
  for i in dateL:
    importType[i] = types.DateTime()
    
  #for i in vectL:
    #mailD[i] = mailD[i].apply(literal_eval)
    #importType[i] = types.ARRAY(types.VARCHAR())
  return mailD, importType

def parseS3(day=None):
    contL = []
    client, bucket = d_l.connectS3(bucketN)
    for obj in bucket.objects.filter(Prefix=folderN):
        if day != None and not bool(re.search(day,obj.key)):
            continue
        print(obj.key)
        parseTar(obj,contL)
    
    print("adding %d messages" % len(contL))
    if len(contL) == 0:
        print("no objects retrieved")
    else:
        mailD, importType  = parseDataframe(contL)
        db = d_l.connectDb()
        mailD.to_sql("live",db,if_exists="append",dtype=importType)

with DAG(dag_id="s3_pull",start_date=datetime.datetime(2022,11,14),tags=["froms3"],schedule='30 3 * * *') as dag:
    def s3_pull():
        parseS3(day=yesterday)
        print("Enkület")
    PythonOperator(task_id="s3_pull", python_callable=s3_pull)
