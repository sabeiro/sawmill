from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime, random, shutil, json, os, io, re
import boto3
from boto3.s3.transfer import S3Transfer
from time import sleep
from kafka import KafkaConsumer, KafkaProducer, TopicPartition, KafkaAdminClient
import tarfile
import numpy as np
import dag_library as d_l

KAFKA_SERVER = "kafka:9093"
mexH = ['creation_time','direction','sender','recipients','queue_id','categories']
bucketN = "lightmeter"
minutes = 60*24*3
payload = {"data":"ciccia","metadata":"ciccio"}
payload = {"payload":[payload,payload]}
fileN = 'kafka/' + "/payload.parquet"
GROUP_ID = "kafka_dump"
metaD = {}
yesterday = str(datetime.date.today()-datetime.timedelta(days=1))

def get_consumer(group="mail-group"):
  return KafkaConsumer(bootstrap_servers=[KAFKA_SERVER],auto_offset_reset='earliest'
                       ,consumer_timeout_ms=1000,group_id=group,api_version=(0,11,15)
                       #,value_deserializer=lambda v: json.loads(v.decode('ascii'))
                       #,key_deserializer=lambda v: json.loads(v.decode('ascii'))
                       ,enable_auto_commit=False,auto_commit_interval_ms=1000)

def dumpTopicAll(topic='test_topic'):
  consumer = KafkaConsumer(bootstrap_servers=[KAFKA_SERVER],auto_offset_reset='earliest',consumer_timeout_ms=1000,group_id=GROUP_ID,api_version=(0, 10, 1), )
  topicL = list(consumer.topics())
  topic_partition = TopicPartition(topic, 0)
  consumer.assign([topic_partition])
  consumer.seek_to_beginning()
  consumer.seek(partition=topic_partition, offset=0)
  pos = consumer.position(topic_partition)
  resL = []
  for msg in consumer:
    resL.append(msg)
  consumer.close()
  print("dumping %d messages" % len(resL))
  for r in resL:
    d = json.loads(r.value)
    if d.get('parsed_content') == None: ## TO REMOVE AFTER MIGRATION
      continue
    metaD = {}
    for i in mexH:
      metaD[i] = str(d[i])
    metaD['timestamp'] = str(r.timestamp)
    fileN = 'live/' + "/".join(d['filename'].split("/")[1:])
    day = datetime.datetime.fromtimestamp(r.timestamp/1000).strftime("%Y-%m-%d")
    dirSave = day + "_" + topic
    try:
      os.makedirs("/tmp/live/"+dirSave)
    except:
      pass
    try:
      mexId = re.sub(">","",re.sub("<","",d['parsed_content']['headers']['Message-Id'][0]))
    except:
      mexId = "random_" + re.sub("\.","",str(random.uniform(0,1)))
    fName = mexId + ".json"
    fName = re.sub("/","",fName)
    open("/tmp/live/"+dirSave+"/"+fName, 'wb').write(r.value)

def compressSend(rootDir="/tmp/live",day=''):
  client, bucket = d_l.connectS3()
  dL = os.listdir(rootDir)
  tL = [x[:10] for x in dL]
  fL = [x for x in dL if not re.match(min(tL),x)]
  fL = [x for x in dL if not re.match(max(tL),x)]
  d = fL[0]
  for d in fL:
    if d != None and not bool(re.search(day,d)):
        continue
    print(d)
    try:
      os.makedirs(rootDir + "_zip")
    except:
      pass
    fileZ = rootDir + "_zip/" + d + ".tar.gz"
    tar = tarfile.open(fileZ, "w:gz")
    tar.add(rootDir+"/"+d,arcname=d)
    tar.close()
    fileN = "live_zip/" + d + ".tar.gz"
    client.upload_file(fileZ,bucketN,fileN)
    # with open(fileZ,"rb") as f:
    #   client.put_object(Body=f,Bucket=bucketN,Key=fileN)

def checkDirS3():
  client, bucket = d_l.connectS3()
  for obj in bucket.objects.filter(Prefix="live_zip/"):
    print(obj.key)

def dumpTopic(topic='test_topic',minutes=20):
    consumer = get_consumer()
    client = d_l.connectS3()
    topicL = list(consumer.topics())
    topic_partition = TopicPartition(topic, 0)
    consumer.assign([topic_partition])
    last_offset = consumer.position(topic_partition)
    ts = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
    ts_milliseconds = ts.timestamp()*1000.0
    timestamps = {topic_partition: ts_milliseconds}
    offsets = consumer.offsets_for_times(timestamps)
    print(offsets)
    offset = offsets[topic_partition]
    if offset is None:
        return
    
    consumer.seek(partition=topic_partition,offset=offset.offset)
    records = consumer.poll(timeout_ms=1000)
    resL = records[topic_partition]
    print("dumping %d messages" % len(resL))
    
    for topic_data, consumer_records in records.items():
      for r in consumer_records:
        d = json.loads(r.value)
        if d.get('parsed_content') == None: ## TO REMOVE AFTER MIGRATION
          continue
        metaD = {}
        for i in mexH:
          metaD[i] = str(d[i])
        metaD['timestamp'] = str(r.timestamp)
        day = datetime.datetime.fromtimestamp(int(x.split(".")[0])).strftime("%Y-%m-%d")
        fileN = 'live/' + "/".join(d['filename'].split("/")[1:])
        client.put_object(Body=r.value,Bucket=bucketN,Key=fileN,Metadata=metaD,ACL='private')
    consumer.close()

#Configs:retention.ms=18000000
def dumpAll(day=''):
  consumer = get_consumer()
  topicL = list(consumer.topics())
  consumer.close()
  for t in topicL:
    print(t)
    dumpTopicAll(topic=t)
    #dumpTopic(topic=t,minutes=minutes)
  compressSend(rootDir="/tmp/live",day=day)
  shutil.rmtree("/tmp/live")
  shutil.rmtree("/tmp/live_zip")

with DAG(dag_id="kafka_dump",start_date=datetime.datetime(2022,11,14),catchup=False
         ,tags=["tos3","kafka"],schedule='0 3 * * *') as dag:
    #@task(task_id="dump_from_kafka")
    def kafka_dump():
      dumpAll(day=yesterday)
      print("Enkület")
    PythonOperator(task_id="kafka_dump",python_callable=kafka_dump)
    
