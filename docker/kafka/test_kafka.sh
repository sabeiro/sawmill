

# step 1: create consumer
curl -X POST \
  -H "Content-Type: application/vnd.kafka.v2+json" \
  --data '{"name": '"$CONSUMER_ID"', "format": "json", "auto.offset.reset": "earliest"}' \
  http://127.0.0.1:8082/consumers/$CONSUMER_GROUP_ID

# step 2: subscribe
curl -X POST \
  -H "Content-Type: application/vnd.kafka.v2+json" \
  --data '{"topics":["character.json.schemaless"]}' \
  http://localhost:8082/consumers/$CONSUMER_GROUP_ID/instances/$CONSUMER_ID/subscription

# step 3: consume
curl -X GET \
  -H "Accept: application/vnd.kafka.json.v2+json" \
  http://localhost:8082/consumers/$CONSUMER_GROUP_ID/instances/$CONSUMER_ID/records

# step 4: close consumer
curl -X DELETE \
  -H "Content-Type: application/vnd.kafka.v2+json" \
  http://localhost:8082/consumers/$CONSUMER_GROUP_ID/instances/$CONSUMER_ID



curl -X POST -H "Content-Type: application/vnd.kafka.json.v2+json" -H "Accept: application/vnd.kafka.v2+json" --data '{"records":[{"value":{"foo":"bar"}}]}' "http://localhost:9092/topics/jsontest"
curl -s localhost:9092/connector-plugins
curl -s -XGET "http://localhost:9092/connectors/source-debezium-orders-00/topics" | jq '.'
curl -s -X GET 'localhost:9092/v3/clusters'
## create topic
curl -s -X POST 'http://localhost:9092/v3/clusters/rgfnzs2RS3O65A7VSpNatg/topics' \
--header 'Content-Type: application/vnd.api+json' \
--data-raw '{"data": {"attributes": {"topic_name": "rmoff_topic03","partitions_count": 12,"replication_factor": 1}}}'
echo dump | nc localhost 2181 | grep brokers 

