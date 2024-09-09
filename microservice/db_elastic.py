import os, sys, gzip, random, csv, json, datetime, re, time
import numpy as np
import pandas as pd
import requests
import string
import simplejson
from collections import OrderedDict as odict

sys.path.append(os.environ['LAV_DIR']+'/src/')
baseDir = os.environ['LAV_DIR']

headers = {"Accept":"application/json","Content-type":"application/x-www-form-urlencoded; charset=UTF-8","User_Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5"}
baseUrl = 'http://localhost:9200/'
sData = {"pretty":""}
indexN = 'tank'
if True: #recreate
    requests.delete(baseUrl+indexN+"?pretty",headers=headers)
    sData = {"mappings":{"log":{
        "_all":{"enabled":True}
        #,"_timestamp":{"enabled":True}
        ,"properties":{
            "name":{"type":"string"}
            ,"coordinates":{"type":"geo_point"}#,"lat_lon":True,"validate":True,"store":"yes","geohash_prefix":True,"geohash_precision":"1km"}
#            ,"timestamp":{"type":"date","format":"YYYY-MM-DD'T'HH:mm:ssZ"}
        }
    }}}
    resq = requests.put(baseUrl+indexN+'?pretty&pretty',headers={},data=json.dumps(sData))
    {"index":{"_id":"1"}}
    print(resq.status_code)
resq = requests.get(baseUrl+'_cat/indices?v&pretty',headers=headers)
print(pd.DataFrame(resq.json()))
##set geo points
notA = pd.read_csv(os.environ['LAV_DIR'] + "out/tank_activity_50.csv.tar.gz",compression="gzip")
#notA = np.round(notA,decimals=4)
hL = notA.columns[[bool(re.search(':',x)) for x in notA.columns]]
pL = list(notA.columns[[not bool(re.search(':',x)) for x in notA.columns]])
for i in ['x','X','y','Y']:
    pL.remove(i)
pL = ['cilac','tech','cluster']
    
#notA = pd.melt(notA,id_vars=pL,value_vars=hL)
def toString(*args):
    together = ''.join(map(str, args))
    together = re.sub('nan','"nan"',together)
    return re.sub("'",'"',together)
if False:
    sucS = ""
    for i, lac in notA.iterrows():
        idx = lac['cilac']
        for k in hL:
            logE = {}
            logE['@timestamp'] = k + "Z"#".000Z"
            for j in pL:
                logE[j] = notA.loc[i][j]
                logE['coordinates'] = {"lon":lac['X'],"lat":lac['Y']}
                logE['count'] = lac[k]
                idS = {"index":{"_index":indexN,"_type":"log"}}
                sucS += json.dumps(idS) + "\n" + toString(logE) + "\n"
    with open(baseDir + "log/tank.json",'w') as f:
        f.write(sucS)
        print('curl -H "Content-Type: application/json" -XPOST "'+baseUrl+indexN+'/_bulk?pretty&refresh" --data-binary "@log/tank.json"')

#geoquery
sData = {"query":{"filtered":{"filter":{"geo_distance":{"distance":"100km","pin":{"lat":49.7,"lon":9.95}}}}}}
sData = {"filtered" : {"query" : {"field" : { "text" : "restaurant" }},
        "filter" : {"geo_distance" : {"distance" : "12km","pin.location" : {"lat": 49.7655493849187, "lon": 9.954733173211382}}}
    }}
resq = requests.put(baseUrl+indexN+'?pretty&pretty',headers=headers,data=json.dumps(sData))
{"index":{"_id":"1"}}
print(resq.status_code)
print(resq.text)
print('-------------------------shape-------------------------')
for g in ["ags5"]: 
    indexN = g
    with open(baseDir + "gis/geo/"+g+".geojson",'r') as f:
        shap = json.load(f)
    sData = {"mappings":{"doc":{
        #"_all":{"enabled":True}
        "properties":{
            "location":{"type":"geo_shape","tree": "quadtree","precision": "100m"}
        }
    }}}
    requests.delete(baseUrl+indexN+"?pretty",headers=headers)
    resq = requests.put(baseUrl+indexN+'?pretty&pretty',headers={},data=json.dumps(sData))
    print(resq.status_code)

    sucS = ""
    for i,s in enumerate(shap['features']):
        logE = odict()
        logE['type'] = "multipolygon"
        logE['coordinates'] = s['geometry']['coordinates']
        #,"name":i,"id":s['properties']['id']}
        sData = {"location":logE}
        #sData = {"location" : {"type" : "multipolygon","coordinates" : [[ [[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]] ],[ [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]], [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]] ]] }}
        resq = requests.post(baseUrl+indexN+"/doc"+"?pretty",headers=headers,data=json.dumps(sData))
        if resq.status_code >= 400:
            print(resq.json())
        sucS += " " + str(resq.status_code) #+ resq.text
        if i%20 == 0:
            print(sucS)
            sucS = ""


sData = {
    "mappings": {
        "doc": {
            "properties": {
                "location": {
                    "type": "geo_shape"
                }
            }
        }
    }
}

resq = requests.put(baseUrl+'example/'+'?pretty&pretty',headers=,data={})
print(resq.status_code)
resq = requests.put(baseUrl+'example/'+'?pretty&pretty',headers=headers,data=json.dumps(sData))
print(resq.status_code)


curl -XPUT 'localhost:9200/example?pretty' -H 'Content-Type: application/json' -d
sData = {"mappings": {"doc": {"properties": {"location": {"type": "geo_shape"}}}}}
resq = requests.put(baseUrl+'example'+"?refresh&pretty",headers=headers,data=json.dumps(sData))
print(resq.status_code)
print(resq.text)

curl -XPOST 'localhost:9200/example/doc?refresh&pretty' -H 'Content-Type: application/json' 
sData = {"name": "Wind & Wetter, Berlin, Germany","location": {"type": "point","coordinates": [13.400544, 52.530286] }}
resq = requests.post(baseUrl+'example/doc'+"?refresh&pretty",headers=headers,data=json.dumps(sData))
print(resq.status_code)
print(resq.text)

curl -XGET 'localhost:9200/example/_search?pretty' -H 'Content-Type: application/json' -d
sData = {"query":{"bool": {"must": {"match_all": {}},
        "filter": {"geo_shape": {"location": {"shape": {"type": "envelope","coordinates" : [[13.0, 53.0], [14.0, 52.0]] },"relation": "within"} } } } }}
resq = requests.get(baseUrl+'example/_search'+"?pretty",headers=headers,data=json.dumps(sData))
print(resq.status_code)
print(resq.text)

for i in ['logstash-2015.05.18','logstash-2015.05.19','logstash-2015.05.20','logstash-2015.05.21']:
    requests.delete(baseUrl+i+"?pretty",headers=headers)
    sData = {"mappings":{"log":{"properties":{"geo": {"properties": {"coordinates": {"type": "geo_point"}}}}}  }}
    resq = requests.put(baseUrl+i+"?pretty",headers=headers,data=json.dumps(sData))
    print(resq.status_code)
    print(resq.text)
    

dateL = os.listdir(baseDir + "log/demo/")
for d in dateL:
    df = pd.read_csv(baseDir + "log/demo/" + d,compression="gzip")
    indexN = re.sub(".csv.tar.gz","",d)
    requests.delete(baseUrl+indexN+"?pretty",headers=headers)
    sData = {"mappings":{"demo":{
        "_all":{"enabled":True}
        ,"properties":{
            "dominant_zone":{"type":"integer"}
    }}}}
    resq = requests.put(baseUrl+indexN+'?pretty&pretty',headers={},data=json.dumps(sData))
    print(resq.status_code)
    sucS = ""
    for i,s in df.iterrows():
        resq = requests.post(baseUrl+indexN+"/demo"+"?pretty",headers=headers,data=json.dumps(s.to_dict()))
        if resq.status_code >= 400:
            print(resq.json())
        sucS += " " + str(resq.status_code) #+ resq.text
        if i%20 == 0:
            print(sucS)
            sucS = ""
    
