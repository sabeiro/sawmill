# Create a topic

#kafka-configs --zookeeper zookeeper:2181 --alter --entity-type topics --add-config retention.ms=1000 --entity-name text_topic
#kafka-configs --zookeeper zookeeper:2181 --entity-type topics --describe --entity-name text_topic
#kafka-configs --zookeeper zookeeper:2181 --alter --entity-type topics --delete-config retention.ms --entity-name text_topic
K_TOPIC='lightmetermailio_outbound'
K_SERVER="kafka:9093"
K_GROUP="mail-group"
CLASSPATH="/usr/share/java/kafka/"

#kafka-topics --bootstrap-server $K_SERVER --delete --topic $K_TOPIC
kafka-topics --bootstrap-server $K_SERVER --describe --topic $K_TOPIC
kafka-topics --bootstrap-server $K_SERVER --create --topic $K_TOPIC
kafka-topics --bootstrap-server $K_SERVER --list
#kafka-topics --create --bootstrap-server kafka:9093 --replication-factor 1 --partitions 13 --topic my-topic

kafka-console-producer --broker-list $K_SERVER --topic $K_TOPIC

kafka-console-consumer --bootstrap-server $K_SERVER --topic $K_TOPIC --from-beginning

# count messages in topic
kafka-run-class kafka.tools.SimpleConsumerShell --broker-list $K_SERVER --topic $K_TOPIC --partition 0*
kafka-run-class kafka.admin.ConsumerGroupCommand --group $K_GROUP --bootstrap-server $K_SERVER --describe
kafka-run-class kafka.tools.GetOffsetShell --broker-list $K_SERVER --topic $K_TOPIC
#kafkacat -b $K_SERVER -t $K_TOPIC -C -e -q -f 'Offset: %o\n' | wc -l


kafka-console-consumer --bootstrap-server $K_SERVER --topic $K_TOPIC --group $K_GROUP --key-deserializer org.apache.kafka.common.serialization.StringDeserializer --value-deserializer org.apache.kafka.common.serialization.StringDeserializer --from-beginning

kafkacat -b $K_SERVER -t $K_TOPIC -G $K_GROUP
kafka-consumer-groups --bootstrap-server $K_SERVER --list

