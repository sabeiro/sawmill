docker-compose run runner register \
  --url "https://gitlab.com/" \
  --registration-token "GR1348941JZ8Jxi1YKRpNpQumw5zZ" \
  --description "docker-dind" \
  --executor "docker" \
  --template-config ./config.toml \
  --docker-image docker:dind

docker-compose exec runner gitlab-runner register --template-config ./config.toml 

sudo gitlab-runner register -n \
  --url https://gitlab.com/ \
  --registration-token "GR1348941JZ8Jxi1YKRpNpQumw5zZ" \
  --executor docker \
  --description "storage Runner" \
  --docker-image "docker:20.10.16" \
  --docker-privileged \
  --docker-volumes "/certs/client"
