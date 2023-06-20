import os, sys, gzip, random, csv, json, datetime, re, time
import urllib3, requests, jwt
from requests.auth import HTTPBasicAuth
import requests, base64

url = "http://0.0.0.0:5006"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
payload = {"id":1,"action":"(name, price) values ('test_product',11.25)","table":"products","filter":""}
usrPass = ""

def printOutput(resq):
  if resq.status_code < 400:
    print(resq.json())
  else:
    print(resq)
    print(resq.reason)
    print(resq.text)

if __name__=="__main__":
  print("test auth")
  b64Val = base64.b64encode(usrPass.encode()).decode()
  resq = requests.get(url+"/authenticate",headers={"Authentication": "%s" % b64Val})
  print(resq.status_code)
  token = resq.json()
  headers["Authentication"] = token
  print("test entry")
  resq = requests.get(url+"/book/page/4",headers=headers)
  printOutput(resq)
  resq = requests.get(url+"/book/page/1",headers=headers)
  printOutput(resq)
  print("test create")
  resq = requests.get(url+"/")
  print(resq.status_code)
  payload = {"id": 1, "action": "*", "table": "products", "filter": ""} 
  payload['action'] = "(name, price) values ('test_product',%f)" % random.uniform(1,30)
  payload['filter'] = ""
  resq = requests.post(url+"/create",json=payload,headers=headers)
  printOutput(resq)
  print("test read products")
  payload = {"id": 1, "action": "*", "table": "products", "filter": ""} 
  resq = requests.post(url+"/select",headers=headers,json=payload)
  printOutput(resq)
  prodL = resq.json()
  print("test sql ingestion")
  payload = {"id": 1, "action": "1; drop products;", "table": "products", "filter": ""} 
  resq = requests.post(url+"/select",headers=headers,json=payload)
  printOutput(resq)  
  print("test delete message")
  resq = requests.delete(url+"/delete/"+payload['table']+"/1",headers=headers)
  for i in prodL:
    resq = requests.delete(url+"/delete/"+payload['table']+"/"+str(i['id']),headers=headers)
    printOutput(resq)
  print('------------------------te-se-qe-te-ve-be-te-ne------------------------')


