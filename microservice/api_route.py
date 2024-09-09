#%pylab inline
import os, sys, gzip, random, csv, json, datetime, re, time
sys.path.append(os.environ['LAV_DIR']+'/src/')
baseDir = os.environ['LAV_DIR']
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import pymongo
import geomadi.kernel_lib as k_l
from scipy import signal as sg
import urllib3,requests

cred = json.load(open(baseDir + "credenza/geomadi.json"))
metr = json.load(open(baseDir + "raw/basics/metrics.json"))

if False: # node location
    job = json.load(open(baseDir + "src/job/odm_via/qsm.odm_extraction.odm_via_via_thuering.json"))
    locL = pd.DataFrame(job['odm_via_conf']['input_locations'])
    locL.loc[:,"id"] = locL['node_list'].apply(lambda x: x[0])
    headers = {"Accept":"application/json","Content-type":"application/x-www-form-urlencoded; charset=UTF-8","User_Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5"}
    baseUrl = "https://api.openstreetmap.org/" + "/api/0.6/node/"
    import xmltodict
    nodeL = []
    for i,g in locL.iterrows():
        resq = requests.get(baseUrl+str(g['id']))#,headers=headers)
        tree = xmltodict.parse(resq.content)
        nodeL.append({"id":g['id'],"loc":g['location_id'],"x":tree['osm']['node']['@lon'],"y":tree['osm']['node']['@lat']})
    nodeL = pd.DataFrame(nodeL)
    nodeL.loc[1,['x','y']] = nodeL.loc[0,['x','y']]
    nodeL.to_csv(baseDir + "raw/nissan/junct_loc.csv",index=False)

    
if True: # routing api
    ##https://developer.mapquest.com/documentation/directions-api/
    ##https://openrouteservice.org/documentation/#/authentication/UserSecurity
    nodeL = pd.read_csv(baseDir + "raw/nissan/junct_loc.csv")
    nodeL.loc[:,"cross"] = nodeL['loc'].apply(lambda x: x.split("_")[0])
    nodeU = nodeL.groupby("cross").first().reset_index()
    baseUrl = "https:www.openstreetmap.org/directions?engine=osrm_car&route="
    baseUrl = "https://api.openrouteservice.org/directions?"
    nodeD = []
    for i in range(nodeU.shape[0]):
        for j in range(i+1,nodeU.shape[0]):
            g1 = nodeU.iloc[i]
            g2 = nodeU.iloc[j]
            print("%s - %s : %.2f%%" % (g1['loc'],g2['loc'],(i*j)/(nodeEn.shape[0]*nodeEx.shape[0])))
            queryS = "api_key=" + cred['openroute']['token']
            queryS += "&coordinates="+str(g1['x'])+"%2C"+str(g1['y'])+"%7C"+str(g2['x'])+"%2C"+str(g2['y'])
            queryS += "&profile=driving-car&preference=fastest&format=json&units=m&language=en&geometry=true&geometry_format=encodedpolyline&geometry_simplify=&instructions=true&instructions_format=text&roundabout_exits=&attributes=&maneuvers=&radiuses=&bearings=&continue_straight=&elevation=&extra_info=&optimized=true&options=%7B%7D&id="
            resq = requests.get(baseUrl+queryS)#,headers=headers)
            if resq.status_code > 300:
                print(resq.text)
                time.sleep(60)
                resq = requests.get(baseUrl+queryS)#,headers=headers)
                print(resq.text)
                continue
            rout = resq.json()['routes'][0]['summary']
            nodeD.append({"en":g1['loc'],"ex":g2['loc'],"dist":rout['distance'],"time":rout['duration']})
            time.sleep(10)
    nodeD = pd.DataFrame(nodeD)
    nodeD = pd.merge(nodeD,nodeL,how="left",left_on="en",right_on="loc",suffixes=["","_en"])
    nodeD = pd.merge(nodeD,nodeL,how="left",left_on="ex",right_on="loc",suffixes=["","_ex"])
    nodeD.loc[:,"cross"] = nodeD['loc'].apply(lambda x: x.split("_")[0])
    nodeD.to_csv(baseDir + "raw/nissan/en2ex_dist.csv",index=False) a
