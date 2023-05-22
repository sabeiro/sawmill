IMG_NAME=php-lib
#docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
docker build  --pull -t $IMG_NAME .
docker tag $IMG_NAME $IMG_NAME:latest

