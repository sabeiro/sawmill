"""
proc_lib:
spark utils to process and search for the output
"""

import os, json, re, datetime, random
import pandas as pd
import matplotlib.pyplot as plt

baseDir = os.environ['LAV_DIR']


import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import udf
from pyspark.sql.functions import to_utc_timestamp, from_utc_timestamp
from pyspark.sql.functions import date_format
from pyspark.sql import functions as func
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("my_app").config('spark.sql.codegen.wholeStage', False).getOrCreate()

df = spark.read.parquet("s3://path/to/parquet/file.parquet")

spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", "mykey")
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "mysecret")
spark._jsc.hadoopConfiguration().set("fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem")
spark._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
spark._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider","org.apache.hadoop.fs.s3a.BasicAWSCredentialsProvider")
spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "eu-central-1.amazonaws.com")

