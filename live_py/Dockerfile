FROM python:3.7-alpine
#FROM python:latest
COPY ./requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app
RUN apk update 
RUN apk add python3-dev gcc libc-dev libffi-dev 
RUN pip3 install -r requirements.txt

ADD  entrypoint.sh /entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh   
ENTRYPOINT ["/entrypoint.sh"]
