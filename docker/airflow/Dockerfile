FROM apache/airflow:latest
COPY ./requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app
# RUN apt update
# RUN apt install -y python3-dev gcc libc-dev libffi-dev postgresql-contrib
RUN pip3 install --no-cache-dir -r requirements.txt
# RUN chmod +x entrypoint.sh   
#ENTRYPOINT ["./entrypoint.sh"] 
