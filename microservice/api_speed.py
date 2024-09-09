#%pylab inline
import os, sys, gzip, random, csv, json, re, time
import urllib3,requests
import base64
sys.path.append(os.environ['LAV_DIR']+'/src/')
baseDir = os.environ['LAV_DIR']
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import datetime
from collections import OrderedDict as odict

def plog(text):
    print(text)

key_file = baseDir + '/credenza/geomadi.json'
cred = []
with open(key_file) as f:
    cred = json.load(f)
cred = cred['janus-se']

##token auth
headers = {"Accept":"application/json","Content-type":"application/x-www-form-urlencoded; charset=UTF-8","User_Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5"}
headers = {"Content-type":"application/x-www-form-urlencoded; charset=UTF-8","Authorization":"OAuth2"}
baseUrl = cred['api-url']+":"+str(cred['api-port'])

optL = {"debug":"debug=true","mtc":"geoType=mtc","days":"aggregation=days"}
repL = {"hello":"/tools/hello","dates":"/tools/availableDates"
        ,"login":"/v1/auth/login"
        ,"location":"/v1/locations/"
        ,"tiles":"/v1/tiles/location/"
        ,"counts":"/v1/reports/counts/overall/location/"
        ,"direction":"/v1/reports/directions/overall/location/"
        ,"odm":"/v1/reports/odm/counts/location/"
        ,"geometry":"/v1/tools/geometries/geoType/mtc?shapeIds=777,789"
        ,"overnight":"/v1/reports/overnight/overall/location/"
        ,"tourist":"/v1/reports/tourists/overall/location/"
}
plog('dowloading locations')

if True: #user auth
    auth_string = (cred['api-user']+":"+cred['api-pass']).encode()
    headers = {"Authorization":"Basic "+base64.standard_b64encode(auth_string).decode(),"Content-Type":"application/x-www-form-urlencoded"}
    baseUrl = cred['api-url']+":"+str(cred['api-port'])
    authP = ""

if False: #token auth
    sData = {"email":cred['t-user'],"password":cred['t-pass'],"customer":cred['t-customer']}
    resq = requests.post(baseUrl+repL['login'],headers=headers,data=sData,verify=False)
    if resq.status_code == 200:
        token = json.loads(resq.json()['response'])['access_token']
        authP = "?token=" + token
    else:
        print(resq.text)
    
resq = requests.get(baseUrl+repL['location']+authP,headers=headers,verify=False)
locL = []
if resq.status_code == 200:
    locL = resq.json()['results']

locL = pd.DataFrame(locL)
locL.to_csv(baseDir + "raw/telia/location_list.csv",index=False)
locL = locL[locL['locationId'].isin([116, 123, 124, 125, 126, 149, 159, 188, 190, 194, 215, 226, 227,228, 235, 236, 238, 239, 240, 242, 245])]

plog('dowloading dates')
resq = requests.get(baseUrl+repL['dates']+authP,headers=headers,verify=False)
dateL = []
if resq.status_code == 200:
    dateL = resq.json()['results'][0]['Dates']
dateL = np.unique(dateL)
dateL = dateL[dateL < '2018-03-30']; dateL = dateL[dateL >= '2018-03-01']
#dateL = dateL[dateL > '2018-02-15']
datem = int(time.mktime(datetime.datetime.strptime(min(dateL),"%Y-%m-%d").timetuple()))
dateM = int(time.mktime(datetime.datetime.strptime(max(dateL),"%Y-%m-%d").timetuple()))

plog('processing directions and speed')
i = 0
for i in range(locL.shape[0]):
    print('processing: ' + str(i))#,end="\r")
    getU = baseUrl + repL['direction'] + str(locL['locationId'].iloc[i]) + "/from/" + str(datem) + "/to/" + str(dateM) + authP
    resq = requests.get(getU,headers=headers,verify=False)
    if resq.status_code == 200:
        locId = str(locL['locationId'].iloc[i])
        dirL = pd.DataFrame(resq.json()['results'])
        dirL1 = pd.DataFrame.from_dict(dirL['metrics'].to_dict()).transpose()
        dirL2 = pd.concat([dirL[['fromDateTime','toDateTime']],dirL1],axis=1)
        dirL2.to_csv(baseDir + "raw/telia/dir_loc"+str(locL['locationId'].iloc[i])+".csv")
        hL = dirL2.columns[[bool(bool(re.search('in',x)) & ~bool(re.search('speed',x))) for x in dirL2.columns]]
        dirL2.loc[:,locId] = dirL2[hL].sum(axis=1)
        dirL2.loc[:,"time"] = dirL2['fromDateTime'].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M"))
        dirL2 = dirL2[['time',locId]]
        if i==0:
            dirT = dirL2
        else:
            dirT = pd.merge(dirT,dirL2,how="outer")
    getU = baseUrl + repL['counts'] + str(locL['locationId'].iloc[i]) + "/from/" + str(datem) + "/to/" + str(dateM) + authP
    resq = requests.get(getU,headers=headers,verify=False)
    if resq.status_code == 200:
        numL = resq.json()['results']
        # with gzip.open(baseDir + "out/telia_num_loc"+str(locL['locationId'].iloc[i])+".json.tar.gz",'w') as outfile:
        #     json.dump(numL,outfile,indent=2)

dirT.to_csv(baseDir + "out/telia_dir_loc.csv",index=False)


print('-----------------te-se-qe-te-ve-be-te-ne------------------------')

if False: #upload locations
    sData = {"name": "122","address": "address","latitude": "12.7465409208225","longitude": "50.1961298022105","comment": "tank","availableFrom": 1514764800,"availableTo": 1546214400,"gridVerticalRadius": 3,"gridHorizontalRadius": 3}
    poi = pd.read_csv(baseDir + "raw/tank/poi_upload.csv",sep=";",header=None)
    poi.columns = ["name","address","lat","lon","start-date","end-date","gridW","gridH","comment"]
    locL = []
    for i,p in poi.iterrows():
        sData['latitude'], sData['longitude'] = str(p['lat']), str(p['lon'])
        sData['name'] = p['name'] + '-' + str(p['comment'])
        sData['address'] = p['address']
        resq = requests.post(baseUrl+repL['location']+authP,headers=headers,verify=False,data=sData)
        if resq.status_code == 200:
            plog('uploaded')
            locL = resq.json()['results']
    print([x for x in resq.json()['results'] if x['comment'] == "tank"])
