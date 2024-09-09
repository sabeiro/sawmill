#%pylab inline
import os, sys, gzip, random, csv, json, datetime, re
sys.path.append(os.environ['LAV_DIR']+'/src/')
baseDir = os.environ['LAV_DIR']
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt

cred = json.load(open(baseDir + '/credenza/geomadi.json'))
metr = json.load(open(baseDir + '/raw/basics/metrics.json'))['metrics']

import pymongo
client = pymongo.MongoClient(cred['mongo']['address'],cred['mongo']['port'])

plog("-------------------------download-network----------------------------")

BBox = [[11.5702,48.0388],[11.61327,48.03675],[11.61233,48.0114],[11.56789,48.01317]]
BBox = [11.5695,11.6112,48.01097,48.0385]
coll = client["tdg_infra"]["segments_col"]
neiN = coll.find({'loc':{'$geoIntersects':{'$geometry':{
    "type":"Polygon"
    ,"coordinates":[
        [ [BBox[0],BBox[3]],[BBox[1],BBox[3]],[BBox[1],BBox[2]],[BBox[0],BBox[2]],[BBox[0],BBox[3]] ]
    ]}}}})
pointL, lineL, lineS = [],[],[]
for neii in neiN:
    lineL.append({"src":neii['src'],"trg":neii['trg'],"speed":neii['maxspeed'],"highway":neii['highway']})
    lineS.append(sh.geometry.LineString([(neii['loc']['coordinates'][0][0],neii['loc']['coordinates'][0][1]),(neii['loc']['coordinates'][1][0],neii['loc']['coordinates'][1][1])]))

lineL = pd.DataFrame(lineL)
colorL = ["firebrick","sienna","olivedrab","crimson","steelblue","tomato","palegoldenrod","darkgreen","limegreen","navy","darkcyan","darkorange","brown","lightcoral","blue","red","green","yellow","purple","black"]
colorI, _ = pd.factorize(lineL['highway'])
lineL = gpd.GeoDataFrame(lineL)
nx, ny = (100, 100)
lineL.loc[:,"color"] = [colorL[int(i)] for i in colorI]
lineL.loc[:,"weight"] = lineL['speed']/max(lineL['speed'])*(BBox[3]-BBox[2])/nx
lineL.geometry = lineS
lineL.loc[:,"geometry"] = [x.buffer(y,resolution=2) for x,y in zip(lineL['geometry'],lineL['weight'])]
lineL.to_file(baseDir + "gis/ptv/network.geojson")

lineL.plot()
plt.show()
