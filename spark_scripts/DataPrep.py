import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

if __name__ == "__main__":
    
    input_path = "/home/user/proj/raw_data/Airline_Delay_Cause.csv" # Path of input CSV
    output_path = "/home/user/proj/spark_output/ada_pq" # Path to store CSV

    spark = SparkSession \
        .builder \
        .appName('Airline Delay Analysis') \
        .getOrCreate()

    schema = StructType([
        StructField("year", IntegerType(), True),
        StructField("month", IntegerType(), True),
        StructField("carrier", StringType(), True),
        StructField("carrier_name", StringType(), True),
        StructField("airport", StringType(), True),
        StructField("airport_name", StringType(), True),
        StructField("arr_flights", DoubleType(), True),
        StructField("arr_del15", DoubleType(), True),
        StructField("carrier_ct", DoubleType(), True),
        StructField("weather_ct", DoubleType(), True),
        StructField("nas_ct", DoubleType(), True),
        StructField("security_ct", DoubleType(), True),
        StructField("late_aircraft_ct", DoubleType(), True),
        StructField("arr_cancelled", DoubleType(), True),
        StructField("arr_diverted", DoubleType(), True),
        StructField("arr_delay", DoubleType(), True),
        StructField("carrier_delay", DoubleType(), True),
        StructField("weather_delay", DoubleType(), True),
        StructField("nas_delay", DoubleType(), True),
        StructField("security_delay", DoubleType(), True),
        StructField("late_aircraft_delay", DoubleType(), True),
    ])

    df = spark.read.csv(input_path, header=True, schema=schema)

    df = df.dropna(subset=['arr_flights'])

    # Define a UDF to fill null values in arr_del15 column with the sum of other columns
    def fill_arr_del15_na(arr_del15, carrier_ct, weather_ct, nas_ct, security_ct, late_aircraft_ct):
        if arr_del15 == None:
            return carrier_ct + weather_ct + nas_ct + security_ct + late_aircraft_ct
        else:
            return arr_del15

    fill_arr_del15_na_udf = udf(fill_arr_del15_na)

    # Apply the UDF to fill null values in arr_del15 column
    df = df.withColumn('arr_del15', fill_arr_del15_na_udf(df.arr_del15, df.carrier_ct, df.weather_ct, df.nas_ct, df.security_ct, df.late_aircraft_ct))

    for i in range(2003, 2023):
        df \
            .filter(col('year') == i) \
            .coalesce(1) \
            .write \
            .parquet(f"{output_path}/{i}/", mode='overwrite')
        
        print(f"The data has been saved to the directory located at {output_path}/{i}.")
