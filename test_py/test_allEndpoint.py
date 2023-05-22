import os, sys, gzip, random, csv, json, datetime, re, time
import urllib3, requests, jwt

def printOutput(resq):
  if resq.status_code < 400:
    print(resq.json())
  else:
    print(resq)
    print(resq.text)

url = "http://0.0.0.0:5005"

if __name__=="__main__":
  print("test db middleware")
  url = "http://0.0.0.0:5006"
  resq = requests.get(url+"/apidocs/")
  print(resq.status_code)
  print("test messaging middleware")
  url = "http://0.0.0.0:5005/"
  resq = requests.get(url+"/apidocs/")
  print(resq.status_code)



  print("test push message")
  inMex['id'] = inMex['id'] + 1
  resq = requests.post(url+"/push/"+topic,json=inMex,headers=headers)
  printOutput(resq)
  print("test consume message")
  resq = requests.get(url+"/consume/"+topic,headers=headers,params={"offset":1})
  printOutput(resq) 
  print("test consume message")
  resq = requests.get(url+"/latest/"+topic,headers=headers,params={"offset":5})
  printOutput(resq)
  print("test consume message")
  resq = requests.get(url+"/latest_time/"+topic,headers=headers,params={"offset":60*1})
  printOutput(resq)
  print("test list topics")
  resq = requests.get(url+"/topics/",headers=headers)
  printOutput(resq)
  print("test delete")
  resq = requests.get(url+"/delete/"+topic,headers=headers)
  printOutput(resq)
  print('------------------------te-se-qe-te-ve-be-te-ne------------------------')


