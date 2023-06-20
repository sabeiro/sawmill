import os, sys, gzip, random, csv, json, datetime, re, time
import urllib3, requests, jwt

def printOutput(resq):
  if resq.status_code < 400:
    print(resq.json())
  else:
    print(resq)
    print(resq.text)

url = "http://0.0.0.0:5005"
#url = "https://interface.storage.lightmeter.io"
headers = {"token":"pbkdf2:sha256:260000$RszmWRvWp5oZbz29$855f861419d178227bb28b1f0e0eb62c2bc8b1ed8e9cc80334845eb7cc2760dc"}
inMex = {
  "content": "base64-encoded message raw content (unparsed)"
  ,"sender": "sender@example.com"
  ,"id":0
  ,"recipients": ["recipient1@gmail.com","recipient2@yahoo.com"]
}
token = jwt.encode(payload=inMex,key=headers['token'])
data = jwt.decode(token,headers['token'],algorithms=['HS256'])
timeOff = time.time() - 60*60
topic = "test_topic"

if __name__=="__main__":
  print("test connection")
  resq = requests.get(url+"/connection/")
  print(resq.text)
  print("test doc")
  resq = requests.get(url+"/apidocs/")
  print(resq.status_code)
  print("test list topics")
  resq = requests.get(url+"/topics/",headers=headers)
  printOutput(resq)
  print("test push message")
  inMex['id'] = inMex['id'] + 1
  resq = requests.post(url+"/push/"+topic,json=inMex,headers=headers)
  printOutput(resq)
  print("test consume message")
  # topic = 'lightmetermailio_outbound'
  # resq = requests.get(url+"/consume/"+topic,headers=headers,params={"offset":1})
  resq = requests.get(url+"/consume/"+topic,headers=headers)
  printOutput(resq)
  resD = resq.json()
  print("test consume message")
  resq = requests.get(url+"/latest/"+topic,headers=headers,params={"offset":5})
  printOutput(resq)
  print("test consume message")
  resq = requests.get(url+"/latest_time/"+topic,headers=headers)
  printOutput(resq)
  print("test delete")
  resq = requests.get(url+"/delete/"+topic,headers=headers)
  printOutput(resq)
  print('------------------------te-se-qe-te-ve-be-te-ne------------------------')


if False: #websocket
  url = "http://0.0.0.0:5007"
  topic = "test_topic"
  print("test connection")
  print("test list topics")
  resq = requests.get(url+"/v1/topics",headers=headers)
  printOutput(resq)
  print("test push message")
  inMex['id'] = inMex['id'] + 1
  resq = requests.post(url+"/v1/push/"+topic,json=inMex,headers=headers)
  printOutput(resq)
  print("test consume message")
  resq = requests.get(url+"/v1/consume/"+topic,headers=headers)
  printOutput(resq)
  resD = resq.json()
  print("test consume message")
  resq = requests.get(url+"/v1/subscribe/"+topic,headers=headers,params={"offset":5})
  printOutput(resq)
  print("test consume message")
  resq = requests.get(url+"/v1/publish/"+topic,headers=headers,params={"offset":60*1})
  printOutput(resq)
  print("test delete")
  # resq = requests.get(url+"/delete/"+topic,headers=headers)
  # printOutput(resq)

if False: #test websocket
  # wscat --connect 'ws://127.0.0.1:5007/v1/subscribe/test_topic'
  import asyncio
  import websockets
  url = "ws://127.0.0.1:5057"
  topic = "test_topic"

  async def handler(websocket):
    while True:
      message = await websocket.recv()
      print(message)
    
  async def listen_consume():
    async with websockets.connect(url+"/v1/consume/"+topic) as ws:
      await handler(ws)
      await asyncio.Future()  # run forever

  async def listen2():
    async with websockets.connect(url+"/v1/consume/"+topic) as ws:
      await ws.send("hello")
      response = await ws.recv()
      print(response)

  asyncio.run(listen_consume())
  asyncio.get_event_loop().run_until_complete(listen2())
  #asyncio.get_event_loop().run_forever()
