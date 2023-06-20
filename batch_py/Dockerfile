FROM python:latest
COPY ./requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app
RUN apt update && apt install -y python3-dev gcc libc-dev libffi-dev postgresql-contrib
RUN pip3 install -r requirements.txt
RUN chmod +x entrypoint.sh   
ENTRYPOINT ["./entrypoint.sh"] 
