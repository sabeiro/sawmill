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

headers = {"Accept":"application/json","Content-type":"application/x-www-form-urlencoded; charset=UTF-8","User_Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5"}


plog('-----------------------grafana-report--------------------------')
key_file = baseDir + '/credenza/geomadi.json'
cred = []
with open(key_file) as f:
    cred = json.load(f)
cred = cred['grafana']

dirT = pd.read_csv(baseDir + "out/telia_dir_loc.csv")
datem = int(time.mktime(datetime.datetime.strptime(min(dirT['time']),"%Y-%m-%d %H:%M").timetuple()))
dateM = int(time.mktime(datetime.datetime.strptime(max(dirT['time']),"%Y-%m-%d %H:%M").timetuple()))

grafU = "http://"+cred['user']+":"+cred['pass']+"@"+cred['address']+":"+str(cred['port'])+cred['service']
grafQ = odict([("db",cred['db']),("q",'SELECT sum("'+cred['field']+'") FROM "'+cred['table']+'" WHERE time > '+str(datem)+'s and time < '+str(dateM)+'s GROUP BY time(1h), "job_id" fill(null)'),("epoch","ms")])
resq = requests.get(grafU,headers=headers,params=grafQ)
inD = resq.json()['results'][0]['series']
for ind in inD:
    indN = re.sub("count_mediation_","",ind['tags']['job_id'])
    tmp = pd.DataFrame({"time":[x[0] for x in ind['values']],indN:[x[1] for x in ind['values']]})
    if ind == inD[0]:
        grafD = tmp
    else :
        grafD = pd.concat([grafD,tmp[indN]],axis=1)

grafD = grafD.replace(np.nan,0)
grafS = np.array(grafD[[x for x in grafD.columns if not x == "time"]])
grafS = grafS.sum(axis=1)
grafD = pd.DataFrame({"time":grafD['time'],"count":grafS})
grafD.loc[:,"time"] = grafD['time'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000.).strftime("%Y-%m-%d %H:%M"))
grafD.loc[:,"count"] = grafD.loc[:,"count"] / grafD.loc[:,"count"].sum()


plog('--------------------comparison----------------------')
grafS = np.array(dirT[[x for x in dirT.columns if not x == "time"]].replace(np.nan,0))
grafS = grafS.sum(axis=1)
grafS = pd.DataFrame({"time":dirT['time'],"count":grafS}).replace(np.nan,0)
grafS.loc[:,"count"] = grafS.loc[:,"count"] / grafS.loc[:,"count"].sum()

grafD = pd.merge(grafD,grafS,on="time",how="outer",suffixes=["_grafana","_api"]).replace(np.nan,0)
grafD.index = grafD['time']
del grafD['time']

grafD.plot()
plt.show()

from scipy.stats.stats import pearsonr
cline = sp.stats.pearsonr(grafD['count_grafana'],grafD['count_api'])

print('-----------------te-se-qe-te-ve-be-te-ne------------------------')
