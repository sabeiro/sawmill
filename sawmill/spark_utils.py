#https://github.com/UrbanInstitute/pyspark-tutorials/blob/master/05_moving-average-imputation.ipynb
#--------------------------------------import-------------------------------------
import os, sys, gzip, random, json, datetime, re, io
import pandas as pd
from pathlib import Path
from scipy import stats as st
#-----------------------------------environment------------------------------------
dL = os.listdir(os.environ['LAV_DIR']+'/src/')
sys.path = list(set(sys.path + [os.environ['LAV_DIR']+'/src/'+x for x in dL]))
baseDir = os.environ['LAV_DIR']
projDir = baseDir + "/rem/src/feature_exp/"
#------------------------------------local-import----------------------------------
#-----------------------------pyspark-import----------------------
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-1.8.0-openjdk-amd64'
import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import udf
from pyspark.sql.functions import to_utc_timestamp, from_utc_timestamp
from pyspark.sql.functions import date_format
from pyspark.sql import functions as func
from pyspark.sql.functions import col
from pyspark.sql.window import Window

conf = (SparkConf()
    .setMaster("yarn-client")
    .setAppName("proc library")
    .set("spark.deploy-mode", "cluster"))
conf.set("spark.executor.memory", "10g")
conf.set("spark.executor.cores", "10")
conf.set("spark.executor.instances", "2")
conf.set("spark.driver.maxResultSize", "10g")
conf.set("spark.driver.memory", "10g")
conf.set("spark.sql.crossJoin.enabled", "true")

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
sc.setLogLevel("ERROR")

timeFmt = "yyyy-MM-dd HH:mm:ss.SSS"
#----------------------load-data-frame---------------------------
df = sqlContext.read.parquet(baseDir + "/rem/log/" + 'telemetry')
df = df.orderBy(['session_id','timestamp_ms'])
df.printSchema()
#----------------------group-by-deci-seconds---------------------
df = df.withColumn('deci',(func.col('timestamp_ms').cast('double')*10.).cast('long'))
ddf = df.groupBy(["session_id","deci"]).agg(
    func.mean('speed').alias('speed_avg'))
ddf.show(1)
window = Window.partitionBy('session_id').orderBy('deci').rowsBetween(-3, 3)
window = Window.partitionBy('session_id').rowsBetween(-3, 3)
tL = ['speed_avg']
for t in tL:
    ddf = ddf.withColumn(t,func.mean(ddf[t]).over(window))
ddf.show(1)

def replace_null(orig, ma):
    return func.when(orig.isNull(), ma).otherwise(orig)
ddf = ddf.withColumn('stream_speed',replace_null(col('speed'), col('speed_avg')))
ddf.show(1)

ddf1 = df.where(df.speed != 0)
ddf1.select("speed").take(1)

sec_delta = lambda i: i * 1
w = (Window.orderBy(func.col("timestamp_ms").cast('long')).rangeBetween(-sec_delta(1), 0))
ddf = ddf.withColumn('avg', func.avg("speed").over(w))

ddf.agg({'deci':'min'}).show()

def get_sub(row): 
    return row['latency_ms']

udf_sub = udf(get_sub,LongType())
udf1 = udf(lambda x: x['latency'],IntegerType())
ddf = ddf.withColumn("speed_latency",udf_sub("speed"))
df.describe()
