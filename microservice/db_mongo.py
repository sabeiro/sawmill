# Query tiles in test area

# Connect to the MongoDB database holding the tile geometry,
# then subset the tiles intersecting with the GeoJSON (created in QGIS from the SHP from the past 
# delivery and pasted here from above under "$geometry")

from pymongo import MongoClient
import os
import json

client = MongoClient('172.25.219.115', 27017)
db = client['tdg_grid']
key_file = os.environ['LAV_DIR'] + '/raw/grid.json'
gridJ = {}
with open(key_file) as f:
    gridJ = json.load(f)

cursor = db.grid_250.find(gridJ)

# Create the variables holding the subset

area_tile_ids_arr = []
area_tile_to_geo = {}
for document in cursor:
    area_tile_ids_arr.append(document['tile_id'])
    area_tile_to_geo[document['tile_id']] = document['geom']


    
