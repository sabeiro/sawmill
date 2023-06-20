IMG_NAME=airflow-boto-kafka
#docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
docker build  --pull -t $IMG_NAME .
docker tag $IMG_NAME $IMG_NAME:latest 
#docker push $IMG_NAME
#docker tag $IMG_NAME localhost:5000/$IMG_NAME
#docker push localhost:5000/$IMG_NAME
#docker image remove $IMG_NAME
#docker image remove localhost:5000/$IMG_NAME
#docker pull localhost:5000/$IMG_NAME
