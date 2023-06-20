FROM golang:1.19

COPY . /app
WORKDIR /app
#COPY ../../credenza/lightmeter.json /app/light/credenza/lightmeter.json
COPY entrypoint.sh .
RUN go get
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"] 
