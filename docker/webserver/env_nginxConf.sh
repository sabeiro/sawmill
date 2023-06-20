export DOLLAR="$"

domains=(schedule.${PROD_SERVER} docker.${PROD_SERVER} metabase.${PROD_SERVER} interface.${PROD_SERVER} ingest.${PROD_SERVER})
#domains=(${PROD_SERVER} schedule.${PROD_SERVER} interface.${PROD_SERVER} ingest.${PROD_SERVER})
envsubst < pre_nginx_env.conf.template > nginx/conf.d/default.conf
#echo "" > nginx/conf.d/default.conf
for domain in "${domains[@]}"; do
        export DOMAIN_RED=${domain}
        #envsubst < redirect_https.conf >> nginx/conf.d/default.conf
        #envsubst < init_cert.conf >> nginx/conf.d/default.conf
done






