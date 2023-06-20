import os, sys, gzip, random, csv, json, datetime, re, time, io
import boto3
from boto3.s3.transfer import S3Transfer
from io import BytesIO
import hashlib,  mailparser, email
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, types
import pytz

cred = json.loads(os.environ['CRED_DICT'])['digOce']
bucketN = "lightmeter"
folderN = "vmail"
dateL = ['Date','date_insertion']
headerL = ['Return-Path','Delivered-To','Received','From','Sender','Reply-To','In-Reply-To','References','Date','Message-ID', 'Subject', 'To']
#headerL = ['from','to','subject','body','date','message-id','auto-submitted','return-path','timezone','received','delivered-to','to_domains']
fileH = ["domain","user","folder","folder_current","filename"]
blockL = ['dovecot.index.cache','dovecot.index.log']
lastMod = datetime.datetime(2022,9,1,tzinfo=None)
yesterday = datetime.datetime.fromisoformat(str(datetime.date.today()-datetime.timedelta(days=1)))

session = boto3.session.Session()
client = session.client(**cred)
resource = boto3.resource(**cred)
transfer = S3Transfer(client)
response = client.list_buckets()
bucket = resource.Bucket(bucketN)
print(response['Buckets'])

if False: #write
  client.put_object(Bucket='lightmeter',Key='ciccia/hello-world.txt',Body=b'Hello, World!',ACL='private',Metadata={'x-amz-meta-my-key':'your-value'})
  transfer.upload_file("/tmp/" + "sync_s3.sh", 'lightmeter', 'ciccia'+"/"+'ciccio.txt')
  obj.download_file('/tmp/demo.txt')

def parseObj(obj,contL):
  l1 = obj.key.split("/")[1:]
  if len(l1) < 4: return
  if len(l1) == 4: l1 = l1[:2] + ["Inbox"] + l1[2:]
  buf = io.BytesIO()
  bucket.download_fileobj(obj.key, buf)
  fileByt = buf.getvalue()
  if fileByt == b'':
    return
  msg = mailparser.parse_from_bytes(fileByt)
  # msgJ = json.loads(msg.mail_json)
  # mL = msgJ.keys()
  msgD = {}
  try:
    hL = [i for i in msg.headers.keys() if i in headerL]
    for i in hL:
      msgD[i] = msg.headers[i]
    for i, k in enumerate(fileH):
      msgD[k] = l1[i]
  except:
    pass
  msg2 = email.message_from_bytes(fileByt)
  failed, feedback = '', ''
  try:
    if msg2.is_multipart():
      for part in msg2.iter_parts():
        if "message/delivery-status" == part.get_content_type():
          failed = part.as_string()
        if "message/feedback-report" == part.get_content_type():
          feedback = part.as_string()
  except:
    pass
  msgD['bounce_text'] = failed
  msgD['feedback_text'] = feedback
  contL.append(msgD)  

def dumpFile(feedD, k):
  feedD["date_insertion"] = datetime.datetime.today().replace(microsecond=0).replace(tzinfo=pytz.utc)
  def try_convert(x):
    try:
      return datetime.datetime.strptime(x,"%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=pytz.utc)
    except:
      return None
  feedD["Date"] = feedD["Date"].apply(lambda x: try_convert(x))
  def try_convert(x):
    try:
      return "%04d-%02d" % (x.year,x.month)
    except:
      return "unknown"
  feedD["partition"] = feedD["Date"].apply(lambda x: try_convert(x))
  def try_convert(x):
    try:
      return datetime.datetime.fromtimestamp(int(x.split(".")[0]))
    except:
      return 0
  feedD["timestamp_filename"] = feedD["filename"].apply(lambda x: try_convert(x))
  fileN = "/raw/" + "dovecot_email_%s.csv.gz" % (k)
  feedD.to_csv(fileN,sep=',',escapechar='\x2f',compression="gzip",index=False)

if False: # account wise
  # fL = []
  # for obj in bucket.objects.filter(Prefix=folderN):
  #   fL.append(obj.key)
  # fD.columns = ['email']
  # fD.to_csv("/app/file_list.csv.gz",compression="gzip")
  dL = []
  paginator = client.get_paginator('list_objects')
  for page in paginator.paginate(Bucket=bucketN,Prefix="vmail/",Delimiter='/'):
    for obj in page.get('CommonPrefixes'):
      dL.append(obj.get('Prefix'))

  bucket = resource.Bucket(bucketN)
  for d in dL:
    print(d)
    fileL, contL = [], []
    for obj in bucket.objects.filter(Prefix=d):
      parseObj(obj.key,fileL,contL)
      break
    s = d.split("/")[1]
    dumpFile(fileL,contL,s)

i, k = 0, 0
contL = []
for obj in bucket.objects.filter(Prefix=folderN):
  parseObj(obj,contL)
  i = i + 1
  if i > 100000:
    print("dumping file %d" % k)
    s = "%05d" % k
    feedD = pd.DataFrame(contL)
    dumpFile(feedD,s)
    contL = []
    i = 0
    k = k + 1

db_name, db_user, db_pass = os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_PASS']
db_host, db_port = os.environ['DB_HOST'], os.environ['DB_PORT']
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

d = "/app/"
fL = os.listdir(d)
fL = sorted([x for x in fL if re.search("dovecot_email",x)])
f = fL[0]
mailD = pd.read_csv(d+f,parse_dates=["Date","date_insertion"],keep_default_na=False)
mailH = mailD.columns
importType = {}
csvType = {}
for i in mailD.columns:
  importType[i] = types.VARCHAR()
  csvType[i] = str

for i in dateL:
  importType[i] = types.DateTime()

for f in fL:
  print(f)
  mailD = pd.read_csv(d+f,parse_dates=["Date","date_insertion"],keep_default_na=False,dtype=csvType)
  for i in dateL:
    mailD[i] = mailD[i].apply(lambda x: x.replace(tzinfo=pytz.timezone('utc')))
  for i in mailH.drop('Date','date_inserted'):
    try:
      mailD[i] = mailD[i].apply(lambda x: str(x))
    except:
      mailD[i] = ''
  mailD = mailD[mailH]
  mailD.to_sql("dovecot",db,if_exists="append",dtype=importType)

