#docker-compose exec coordinator presto-cli --catalog kafka --schema default --server coordinator:8090
docker-compose exec coordinator presto-cli --server coordinator:8090 --catalog kafka --schema default --user api_ingest
#netstat -an |grep 8081 |grep LISTEN
