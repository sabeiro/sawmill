#FROM python:3.7-alpine
FROM python:latest

COPY ./requirements.txt /app/requirements.txt
COPY . /app
#COPY ../../credenza/lightmeter.json /app/light/credenza/lightmeter.json
WORKDIR /app
#RUN apk update && apk add python3-dev gcc libc-dev libffi-dev postgresql-contrib
RUN apt update && apt install -y python3-dev gcc libc-dev libffi-dev postgresql-contrib
RUN pip3 install -r requirements.txt
RUN chmod +x entrypoint.sh   
ENTRYPOINT ["./entrypoint.sh"] 
