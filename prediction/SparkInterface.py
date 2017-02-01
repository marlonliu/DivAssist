import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import Row, SparkSession, SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import udf

import time
import os,sys
import unicodedata
from datetime import datetime

"""
Converts a Divvy-format timestamp to a datetime.
"""
def toTimestamp(timeStr):
	month, day, year = int(timeStr[:2]), int(timeStr[3:5]), int(timeStr[6:10])
	hour, minute, sec= int(timeStr[11:13]), int(timeStr[14:16]), int(timeStr[17:19])
	if timeStr[-2:] == "PM" and hour != 12:
		hour += 12
	return datetime(year, month, day, hour, minute, sec)

"""
Handles Spark initializion, data population, and queries.
"""
class SparkInterface():

    def load_data(self):
        cwd = os.getcwd() # get the cwd
        timestampUDF = udf(toTimestamp, TimestampType()) # register toTimestamp as a UDF
        parquet_path = "/".join([cwd, self.parquet_filename]) # derive the parquet file path

        if self.parquet_filename in os.listdir(cwd):
            print("Importing data from " + self.parquet_filename + "...")
            self.data = self.sqlc.read.parquet(parquet_path)
        else:
            print("Importing data from " + self.csv_filename + "...")
            divvySchema = StructType([
                            StructField("ID", StringType(), nullable=True), 
                            StructField("Timestamp", StringType(), nullable=True), 
                            StructField("Station_Name", StringType(), nullable=True), 
                            StructField("Address", StringType(), nullable=True), 
                            StructField("Total_Docks", IntegerType(), nullable=True), 
                            StructField("Docks_in_Service", IntegerType(), nullable=True), 
                            StructField("Available_Docks", IntegerType(), nullable=True), 
                            StructField("Available_Bikes", IntegerType(), nullable=True), 
                            StructField("Percent_Full", FloatType(), nullable=True) , 
                            StructField("Status", StringType(), nullable=True), 
                            StructField("Latitude", FloatType(), nullable=True), 
                            StructField("Longitude", FloatType(), nullable=True), 
                            StructField("Location", StringType(), nullable=True)])
            csv_path = "/".join([cwd, self.csv_filename])
            rawData = self.sqlc.read.csv(csv_path, header='true', schema=divvySchema)
            print("Converting strings to timestamps...")
            self.data = rawData.withColumn("Timestamp",timestampUDF("Timestamp"))
            print("Writing parquet file to " + self.parquet_filename + "...")
            self.data.write.parquet(parquet_path)
    
    """
    Initializes Spark and loads data.
    """
    def __init__(self, parquet_filename = "divvyData.parquet", csv_filename = "Divvy_Bicycle_Stations_-_Historical.csv"):
        # initialize Spark
        self.spark = pyspark.SparkContext("local[*]")
        self.spark.setLogLevel("OFF")
        self.sqlc = SQLContext(self.spark)
        # initialize other vars
        self.parquet_filename = parquet_filename
        self.csv_filename = csv_filename
        # load data
        self.load_data()