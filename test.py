# test_spark.py
from pyspark.sql import SparkSession
import sys


spark = SparkSession.builder \
    .appName("File Test") \
    .getOrCreate()

try:
    files = spark.sparkContext.wholeTextFiles("C:/Users/valor/Desktop/nire/corpus/*.txt")
    sys.stdout.reconfigure(encoding='utf-8')
    print("Found files:", [str(x).encode('utf-8', 'replace') for x in files.collect()])
except Exception as e:
    print("Error:", e)
finally:
    spark.stop()