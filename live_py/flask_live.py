#https://github.com/ftisiot/flask-apache-kafka-demo/blob/main/code/app.py
import os, sys, gzip, random, csv, json, datetime, re, time, io
import signal, uuid, jwt
from threading import Event
from flask_kafka import FlaskKafka
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from kafka import KafkaConsumer, KafkaProducer, TopicPartition, KafkaAdminClient
from flasgger import Swagger, swag_from
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger, SwaggerView, Schema, fields
from flasgger.utils import swag_from

app = Flask(__name__,static_url_path='')
swag = Swagger(app)
  
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'pbkdf2:sha256:260000$RszmWRvWp5oZbz29$855f861419d178227bb28b1f0e0eb62c2bc8b1ed8e9cc80334845eb7cc2760dc'
TOPIC_NAME = "email"
KAFKA_SERVER = "localhost:9092"
KAFKA_SERVER = "kafka:9093"
GROUP_ID = "mail-group"
IF_KAFKA = True

def retDict(payload={},error_code=200):
  #return Response(payload, status=error_code, mimetype='application/json')
  return payload, error_code

def get_producer():
  return KafkaProducer(bootstrap_servers=[KAFKA_SERVER],api_version=(0,11,15)
                       ,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def get_consumer():
  return KafkaConsumer(bootstrap_servers=[KAFKA_SERVER],auto_offset_reset='latest'
                       ,consumer_timeout_ms=1000,group_id=GROUP_ID,api_version=(0,11,15)
                       ,fetch_max_bytes=50*1024*1024
                       ,value_deserializer=lambda v: json.loads(v.decode('ascii'))
                       #,key_deserializer=lambda v: json.loads(v.decode('ascii'))
                       ,enable_auto_commit=False,auto_commit_interval_ms=1000)

try:
  INTERRUPT_EVENT = Event()
  bus = FlaskKafka(INTERRUPT_EVENT,bootstrap_servers=",".join([KAFKA_SERVER]),group_id=GROUP_ID)
except:
  IF_KAFKA = False
  print("kafka connection on %s not established" % (KAFKA_SERVER))

def token_required(f):
  @wraps(f)
  def token_dec(*args, **kwargs):
    token = request.headers.get('token')
    if not token:
      return retDict({"status":"token rejected","message":"Missing Token!"}, 400)
    if token != app.config['SECRET_KEY']:
      return retDict({"status":"token rejected","message":"Invalid Token"}, 401)
    return f(*args, **kwargs)
  return token_dec

@app.route('/push/<topic>', methods=['POST'])
@token_required
def kafkaPush(topic):
  """
    Push to kafka
    post a message to a topic
    ---
    tags:
      - push
    parameters:
      - name: topic
        in: path
        type: string
        required: true
        description: The topic name
      - name: json-payload
        in: query
        type: json
        description: message to the topic
    responses:
      500:
        description: wrong token/topic
      200:
        description: message added to the topic
  """
  req = request.get_json()
  try:
    producer = get_producer()
    producer.send(topic, req)
    producer.flush()
    return retDict({"message":"added message to producer","status": "Pass"}, 200)
  except:
    return retDict({"message":"kafka not available","status": "error"}, 503)
  
@app.route('/consume/<topic>')
@token_required
def kafkaStream(topic):
  """
    Read topic from kafka
    read messages from a topic
    ---
    tags:
      - consume
    parameters:
      - name: topic
        in: path
        type: string
        required: true
        description: The topic name
      - name: offset
        in: get
        type: int
        required: false
        description: The offset
    responses:
      500:
        description: wrong token/topic
      200:
        description: json of the messages in the topic
  """
  #topic = request.args.get('id_topic')
  if topic is None:
    return retDict({"message":"id_topic missing","status":"invalid"}, 400)
  try:
    topic_partition = TopicPartition(topic, 0)
    consumer = get_consumer()
    consumer.assign([topic_partition])
  except:
    return retDict({"message":"kafka not available","status": "error"}, 503)
  try:
    offset = int(request.args.get("offset"))
    consumer.seek(topic_partition,offset)
  except:
    consumer.seek_to_beginning()
  resL = []
  for message in consumer:
    if message is not None:
       resL.append(message.value)
    consumer.commit()
  consumer.close()
  print("found %d messages" % len(resL))
  return retDict(resL, 200)

@app.route('/latest/<topic>')
@token_required
def kafkaLatest(topic):
  """
    Read topic latest __offset__ from kafka
    read messages from a topic
    ---
    tags:
      - consume
    parameters:
      - name: topic
        in: path
        type: string
        required: true
        description: The topic name
      - name: offset
        in: get
        type: int
        required: false
        description: The offset
    responses:
      500:
        description: wrong token/topic
      200:
        description: json of the messages in the topic
  """
  if topic is None:
    return retDict({"message":"id_topic missing","status":"invalid"}, 400)
  try:
    topic_partition = TopicPartition(topic, 0)
    consumer = get_consumer()
    consumer.assign([topic_partition])
  except:
    return retDict({"message":"kafka not available","status": "error"}, 503)
  offset = request.args.get("offset")
  if offset is None:
    offset = 10
  else:
    offset = int(offset)
  last_offset = consumer.position(topic_partition)
  offset = max(0,last_offset - offset)
  consumer.seek(topic_partition,offset)
  resL = []
  for message in consumer:
    if message is not None:
       resL.append(message.value)
    consumer.commit()
  consumer.close()
  return retDict(resL, 200)

@app.route('/latest_time/<topic>')
@token_required
def kafkaLatestTime(topic):
  """
    Read topic latest n seconds from kafka
    read messages from a topic
    ---
    tags:
      - consume
    parameters:
      - name: topic
        in: path
        type: string
        required: true
        description: The topic name
      - name: offset
        in: get
        type: int
        required: false
        description: The offset in seconds
    responses:
      500:
        description: wrong tocken/topic
      200:
        description: json of the messages in the topic
  """
  #topic = request.args.get('id_topic')
  if topic is None:
    return retDict({"message":"id_topic missing","status":"invalid"}, 400)
  try:
    topic_partition = TopicPartition(topic, 0)
    consumer = get_consumer()
    consumer.assign([topic_partition])
  except:
    return retDict({"message":"kafka not available","status":"error"}, 503)
  offset = request.args.get("offset")
  if offset is not None:
    timeL = time.time() - int(offset)
  else:
    timeL = time.time() - 60*60
  time_ms = timeL*1000
  offsetD = consumer.offsets_for_times({topic_partition:time_ms})
  offsetL = offsetD.values()
  offsetL = offsets[topic_partition]
  if offset is None:
    return retDict([], 200)
  consumer.seek(partition=topic_partition, offset=offset.offset)
  records = consumer.poll(timeout_ms=1000)
  resL = records[topic_partition]
  return retDict(resL, 200)


@app.route('/realtime/<topic>')
@token_required
def kafkaStreamReal(topic):
  """
    Read topic from kafka
    read messages from a topic
    ---
    tags:
      - consume
    parameters:
      - name: topic
        in: path
        type: string
        required: true
        description: The topic name
      - name: offset
        in: get
        type: int
        required: false
        description: The offset
    responses:
      500:
        description: wrong token/topic
      200:
        description: json of the messages in the topic
  """
  #topic = request.args.get('id_topic')
  if topic is None:
    topic = "realtime"
  try:
    topic_partition = TopicPartition(topic, 0)
    consumer = get_consumer()
    consumer.assign([topic_partition])
  except:
    return retDict({"message":"kafka not available","status": "error"}, 503)
  try:
    offset = int(request.args.get("offset"))
    consumer.seek(topic_partition,offset)
  except:
    consumer.seek_to_beginning()
  resL = []
  for message in consumer:
    if message is not None:
       resL.append(message.value)
    consumer.commit()
  consumer.close()
  print("found %d messages" % len(resL))
  return retDict(resL, 200)

@app.route('/delete/<topic>')
@token_required
def kafkaDelete(topic):
  """
    Delete topic from kafka
    delete all messages and the topic
    ---
    tags:
      - delete
    parameters:
      - name: topic
        in: path
        type: string
        required: true
        description: The topic name
    responses:
      500:
        description: wrong tocken/topic
      200:
        description: delete successful
  """
  try:
    admin_client = KafkaAdminClient(bootstrap_servers=[KAFKA_SERVER])
    admin_client.delete_topics(topics=[topic])
  except:
    return retDict({"status":"error","message":"topic " + topic + " not found"}, 400)
  return retDict({"status":"pass","message":"topic " + topic + " deleted"}, 200)

@app.route('/topics/')
@token_required
def KafkaTopics():
  """
    Fetch all topics from kafka
    List of all topics
    ---
    tags:
      - list
    responses:
      500:
        description: wrong token/topic
      200:
        description: topic list
  """
  try:
    consumer = get_consumer()
    topicL = list(consumer.topics())
    consumer.close()
  except:
    return retDict({"message":"kafka not available","status": "error"}, 503)
  return retDict(topicL, 200)

@app.route('/realtime_test/')
def realtime():
  for i in range(1,10):
    yield str(i) + '\n'
    time.sleep(0.2)

@app.route('/connection/')
def connection():
  try:
    admin_client = KafkaAdminClient(bootstrap_servers=[KAFKA_SERVER])
    return retDict({"status":"success","message":"listening on %s" % KAFKA_SERVER}, 200)
  except:
    print("kafka connection on %s not established" % (KAFKA_SERVER))
    return retDict({"status":"error","message":"no borkers available on %s " % KAFKA_SERVER}, 503)
    
@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "kafka flask interface"
    return jsonify(swag)

@app.route('/')
def index():
  return retDict(render_template('index.html',port=5005), 200)

if IF_KAFKA:
  def listen_kill_server():
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGINT, bus.interrupted_process)
    signal.signal(signal.SIGQUIT, bus.interrupted_process)
    signal.signal(signal.SIGHUP, bus.interrupted_process)
  @bus.handle('test_topic')
  def test_topic_handler(msg):
    print("consumed {} from test_topic".format(msg))

if __name__ == '__main__':
    #bus.run()
    #listen_kill_server()
    app.run(debug=True, port=5005)


    

