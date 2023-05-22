#!/bin/bash

if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

domains=$CERT_DOMAINS
rsa_key_size=4096
data_path="${HOME}/certbot"
email=$CERT_EMAIL
staging=0

if [ -d "$data_path" ]; then
  read -p "Existing data found for $CERT_DOMAINS. Continue and replace existing certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi

if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi

echo "### Creating dummy certificate for $CERT_DOMAINS ..."
path="/etc/letsencrypt/live/$CERT_DOMAINS"
mkdir -p "$data_path/conf/live/$CERT_DOMAINS"
docker-compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo

echo "### Starting nginx ..."
docker-compose up --force-recreate -d nginx
echo

echo "### Deleting dummy certificate for $CERT_DOMAINS ..."
docker-compose run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$CERT_DOMAINS && \
  rm -Rf /etc/letsencrypt/archive/$CERT_DOMAINS && \
  rm -Rf /etc/letsencrypt/renewal/$CERT_DOMAINS.conf" certbot
echo

echo "### Requesting Let's Encrypt certificate for $CERT_DOMAINS ..."
#Join $domains to -d args
domain_args=""
for domain in "${CERT_DOMAINS[@]}"; do
  domain_args="$domain_args -d $domain"
done

# Select appropriate email arg
case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="--email $email" ;;
esac

# Enable staging mode if needed
if [ $staging != "0" ]; then staging_arg="--staging"; fi

docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg  $email_arg  $domain_args --rsa-key-size $rsa_key_size --agree-tos -v --force-renewal" certbot

echo "### Reloading nginx ..."
docker-compose exec nginx nginx -s reload


docker-compose run --rm certbot certbot renew 
docker-compose run --rm certbot certbot certonly --nginx -n -v -d intertino.it --dry-run
docker-compose run --rm certbot certbot certonly --test-cert --dry-run -d intertino.it --nginx-sleep-seconds 30


