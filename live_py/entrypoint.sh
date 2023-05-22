#!/bin/sh
gunicorn -w 4 --forwarded-allow-ips="<traefik_reverse_proxy_ip>" --bind 0.0.0.0:5005 wsgi:app
#uvicorn fast_live:app --reload
