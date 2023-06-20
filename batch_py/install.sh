#!/bin/bash
echo "installing libraries"
apt update
apt install -y python3-dev gcc libc-dev libffi-dev postgresql-contrib
pip3 install --upgrade pip
pip3 install -r requirements.txt

