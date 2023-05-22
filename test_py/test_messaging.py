import json, datetime, base64, sys, os
from time import sleep
import requests, mailparser
from kafka import KafkaConsumer, KafkaProducer, TopicPartition, KafkaAdminClient

sys.path.append(os.environ['LAV_DIR']+'/src/')
baseDir = os.environ['LAV_DIR']
# mex = open(baseDir + "/light/raw/exp_autoreply.eml","rb").read()
mex = open(baseDir + "/light/raw/sample_bounce.eml","rb").read()
mexH = ['creation_time','direction','sender','recipients','queue_id','categories']
headerL = ['From','To','Subject','Date',"In-Reply-To","References",'Return-Path','Delivered-To','Message-ID']
dateL = ['Date','date_insertion']

KAFKA_SERVER = "kafka:9093"
topic = "test_topic"
inMex = {
  "content": "base64-encoded message raw content (unparsed)",
  "sender": "sender@example.com",
  "recipients": ["recipient1@gmail.com","recipient2@yahoo.com"],
}
GROUP_ID = "mail-group"

def get_producer():
  return KafkaProducer(bootstrap_servers=[KAFKA_SERVER],api_version=(0,11,15)
                       ,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def get_consumer():
  return KafkaConsumer(bootstrap_servers=[KAFKA_SERVER],auto_offset_reset='earliest'
                       ,consumer_timeout_ms=1000,group_id=GROUP_ID,api_version=(0,11,15)
                       ,value_deserializer=lambda v: json.loads(v.decode('ascii'))
                       #,key_deserializer=lambda v: json.loads(v.decode('ascii'))
                       ,enable_auto_commit=True)#,auto_commit_interval_ms=1000)

admin_client = KafkaAdminClient(bootstrap_servers=[KAFKA_SERVER],api_version=(0,11,15))
topic = 'lightmetermailio_unknown'
topic = 'lightmetermailio_outbound'

consumer = KafkaConsumer(bootstrap_servers=[KAFKA_SERVER],auto_offset_reset='earliest',consumer_timeout_ms=1000,group_id=GROUP_ID,value_deserializer=lambda m: json.loads(m.decode('utf-8')),api_version=(0, 10, 1), )

#consumer = get_consumer()
topicL = list(consumer.topics())
#consumer.subscribe([topic])
topic_partition = TopicPartition(topic, 0)
consumer.assign([topic_partition])
consumer.seek_to_beginning()
consumer.seek(partition=topic_partition, offset=0)
pos = consumer.position(topic_partition)
resL = []
for msg in consumer:
  resL.append(msg)

print(len(resL))


records = consumer.poll(timeout_ms=60*6*1000)
k = list(records.keys())[0]
len(records[k])


partL = consumer.partitions_for_topic(topic)
topic_partition = TopicPartition(topic, 0)
consumer.assign([topic_partition])
last_offset = consumer.position(topic_partition)
consumer.seek_to_beginning()
consumer.position(topic_partition)

topic_partition = TopicPartition(topic, 0)
consumer.assign([topic_partition])
last_offset = consumer.position(topic_partition)
consumer.seek_to_beginning()
consumer.position(topic_partition)
records = consumer.poll(timeout_ms=1000)
k = list(records.keys())[0]
len(records[k])


records = consumer.poll(60 * 1000)
print(len(records.items()))
resL = []
for tp, consumer_records in records.items():
  for consumer_record in consumer_records:
    resL.append(consumer_record.value)
print(len(resL))



ts = datetime.datetime.now() - datetime.timedelta(minutes=20)
ts_milliseconds = ts.timestamp()*1000.0
timestamps = {topic_partition: ts_milliseconds}
offsets = consumer.offsets_for_times(timestamps)
print(offsets)
offset = offsets[topic_partition]
if offset is None:
  print('ciccia')

consumer.seek(partition=topic_partition,offset=offset.offset)

consumer = get_consumer()
records = consumer.poll(timeout_ms=1000)
resL = records[topic_partition]

consumer = KafkaConsumer(bootstrap_servers=broker_list, group_id='test')
tp = TopicPartition(topic=topic, partition=0)
consumer.assign([tp])
consumer.seek(tp, offset) 
for msg in consumer:
  print(msg)

for topic_data, consumer_records in records.items():
  for r in consumer_records:
    d = r.value
    l = [d[i] for i in mexH] + [r.timestamp]
    s = base64.b64decode(d['content'])
    fileN = d['filename']
    msg = mailparser.parse_from_bytes(mex)
    msgD = {}
    mL = mail.headers.keys()
    hL = [i  for i in mail.headers.keys() if i in headerL]
    msgJ = json.loads(msg.mail_json)
    
for i in msgJ.keys():
  print("----------------", i)
  print(msgJ[i])

consumer.seek_to_beginning()
resL = []
for message in consumer:
  if message is not None:
    resL.append(message.value)
  consumer.commit()


if __name__=="__main__":
  print("test consume messages")

  # producer = get_producer()
  # producer.send(topic, req)
  # producer.flush()
  
  #admin_client.delete_topics(topics=[topic])
  #admin_client.create_topics(new_topics=topic_list, validate_only=False)
  print('------------------------te-se-qe-te-ve-be-te-ne------------------------')

