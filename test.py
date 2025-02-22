from pyspark.sql import SparkSession
import os
import sys
import findspark
findspark.init("D:\\spark\\spark-3.5.4-bin-hadoop3")

# Initialize Spark session
spark = SparkSession.builder \
    .appName("PySpark Example") \
    .getOrCreate()

# Create a DataFrame
data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
df = spark.createDataFrame(data, ["Name", "Age"])

# Show the DataFrame
df.show()

# Stop the Spark session
spark.stop()