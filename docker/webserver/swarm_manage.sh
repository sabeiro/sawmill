#https://blog.alexellis.io/docker-stacks-attachable-networks/
SWARM_NAME=malestro
SWARM_NODE=malestro
NET_NAME=webserver-net
SERVICE_NAME=db
SUBNET="10.11.0.0/16"
GATEWAY="10.11.0.1"
docker swarm init

#docker network create --scope=swarm $NET_NAME
#docker network create --scope=swarm --driver overlay --attachable $NET_NAME
docker network create --driver=overlay --attachable $NET_NAME
#docker network create --scope=swarm --driver overlay --ingress --opt com.docker.network.driver.mtu=1200 $NET_NAME
docker network create --driver overlay --ingress --subnet=$SUBNET --gateway=$GATEWAY --opt com.docker.network.driver.mtu=1200 traefik-ingress

docker network create --subnet $SUBNET --opt com.docker.network.bridge.name=docker_gwbridge --opt com.docker.network.bridge.enable_icc=false --opt com.docker.network.bridge.enable_ip_masquerade=true docker_gwbridge

#docker network create --subnet=172.20.0.1/16 -o com.docker.network.bridge.enable_icc=false -o com.docker.network.bridge.name=docker_gwbridge docker_gwbridge

#docker service update --network-rm traefik-net myservice
#docker service create --publish 80:80 --network=$NET_NAME --name nginx nginx
docker service update --network-add $NET_NAME db

docker node update --availability active $SWARM_NODE
docker swarm init

