import sys
import csv
import json
import time
import datetime
from ast import literal_eval
import numpy as np
#import geohash
from pyspark.sql import SQLContext
from pyspark import SparkConf, SparkContext
from pyspark.sql.types import *
from pyspark.sql.functions import udf
import matplotlib.pyplot as plt
from pyspark.sql.functions import mean, min, max, sum
from pyspark.sql import functions as func

from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

datestr="/tdg/2017/04/11"

# df = spark.read.json("examples/src/main/resources/people.json")
# df = spark.read.load("examples/src/main/resources/users.parquet")
#df.select("name", "favorite_color").write.save("namesAndFavColors.parquet")
df = spark.read.parquet(datestr+"/aggregated_events")

#EMR_CLIENT = client('emr')
conf = SparkConf().setAppName('Canvas Requests Logs')
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
df=sqlContext.read.parquet(datestr+"/aggregated_events")

df.printSchema()
df.select("name").show()
df.select(df['name'], df['age'] + 1).show()
df.filter(df['age'] > 21).show()
df.groupBy("age").count().show()
df.show()

# import glob
#load aggregator output
df=sqlContext.read.parquet(datestr+"/aggregated_events")

def get_db_connection(host_name, port, database, collection):
    client = pymongo.MongoClient(host_name, port)
    db_connection = client[database][collection]
    return db_connection

def get_bse(infra_conn_dev, cilac):
    response = infra_conn_dev.find({"cell_ci":int(cilac.split("-")[0]), "cell_lac":int(cilac.split("-")[1])})
    #print response[0]
    lista = (response[0]["geom"])
    return {"type":lista["type"], "coordinates":lista["coordinates"]}
def get_centroid(infra_conn_dev, cilac):
    response = infra_conn_dev.find({"cell_ci":int(cilac.split("-")[0]), "cell_lac":int(cilac.split("-")[1])})
    #print response[0]
    lista = (response[0]["centroid"])
    return lista

def get_mongo_cilac_xy(db_conn, list_of_lines):
    """
    Makes dictionary of cilac: list of coordinates after filtering the specific lacs
    :param list_of_lacs: list of lacs that define a region
    :return: dictionary cilac: [x, y]
    """
    results_dict = {}
    for line in list_of_lines:
        response = db_conn.find(build_line_query(line))
    
        for document in response:
            results_dict[int(document['node_id'])] = [document["name"]] + [document["line"]]+ document['coordinates']
    return results_dict


#connect to mongo
infra_conn_dev = get_db_connection("172.25.100.21", 31024, "tdg_17d08", "infrastructure")
