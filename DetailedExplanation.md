# Detailed Explanation

### Google Compute Engine

For this project, I used VM with the configuration as follows:

![0](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/0.png)

After spinning up the VM clone the repository and install this

**Python**

```bash
sudo apt install python3-pip
pip3 install jupyterlab
pip3 install notebook
```

**PySpark**

Follow these [instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/linux.md)

> Make sure to download the correct version of Spark. The version mentioned is no longer available. I personally used [this](https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz) version.
> 

**Airflow**

```bash
pip3 install apache-airflow
mkdir airflow_home
export AIRFLOW_HOME=home/--user--/proj/airflow
cd airflow_home
mkdir dags
mkdir plugins
```

After all of this, I created one `.bashrc` file so I don’t have to export variables manually every time I restart my VM.

```bash
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"

export SPARK_HOME="${HOME}/spark/spark-3.2.3-bin-hadoop3.2"
export PATH="${SPARK_HOME}/bin:${PATH}"

export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"

export AIRFLOW_HOME=/home/--user--/proj/airflow
```

This file can be executed as follows:

```bash
source .bashrc
```

Now we have everything installed  & our environment variable initialized, we can start Spark cluster & Airflow using the following commands

 

```bash
/home/pratikkakadiya18/spark/spark-3.2.3-bin-hadoop3.2/sbin/start-master.sh
/home/pratikkakadiya18/spark/spark-3.2.3-bin-hadoop3.2/sbin/start-worker.sh --master url--
airflow scheduler
airflow webserver -p 5000
```

> Note: Do not forget to stop Spark master and worker after experiments commands for that are as follows
> 

```bash
path-of-spark-folder/spark/spark-3.2.3-bin-hadoop3.2/sbin/stop-master.sh
path-of-spark-folder/spark/spark-3.2.3-bin-hadoop3.2/sbin/stop-worker.sh
```

### Folder Structure

After proper configuration folder tree should look like this

> **Note**: While I was working on the project I ran out of names so I named my folder just **`proj`** but in your case, this will be the name of the repository 😅
> 

![1](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/1.png)

### **Understanding Raw Data**

**The followings are the columns in the CSV**

year, month

carrier, carrier_name

airport, airport_name

---

arr_flights → **Total flights count**

---

arr_del15 → **Total delayed flights count (sum of the following columns)**

carrier_ct, weather_ct ,nas_ct, security_ct, late_aircraft_ct

---

arr_cancelled, arr_diverted

---

arr_delay → **Total delay minutes (sum of the following columns)**

carrier_delay, weather_delay, nas_delay, security_delay, late_aircraft_delay

### PySpark

The  PySpark script will take the data from the `raw_data`  there we have a single CSV file that contains data from 2003 to 2022. We have to break down that data to make it easier to work with. As an example what if we want to work on data from 2005 only then we don’t need other data. So the script will break that data down according to year and instead of CSV, we are saving files in parquet format. Since Parquet is lightweight for saving dataframes and also Parquet uses efficient data compression and encoding scheme for fast data storing and retrieval. It will look as follows:

![2](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/2.png)

![3](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/3.png)

Now we have the output we want but let’s go one step further and take this output and generate a meaningful file name and upload it to the GCS for that we’ll use a Bash Script.

### Bash Script

The bash script takes the output path of the PySpark output as an argument and takes only parquet files from the given directory it renames files properly and puts them into the `temp` folder which then will be uploaded to GCS and the temp folder will be deleted leaving us with no unnecessary files.

![4](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/4.png)

### Google Cloud Storage

The above-mentioned file will be in GCS after a successful bash script run so it will look something like this.

![5](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/5.png)

### Google Cloud Function

Now we have data in the GCS. So we can configure a function that takes data as soon as it arrives in GCS and puts it into the Big Query and to accomplish that we’ll use **Pandas.** When dealing with datasets of small to medium size, and when the main objective is to cleanse, transform, and manipulate data, Pandas is a great choice for ETL tasks. It comes in handy, especially for tasks like data extraction, cleaning, transformation, and exporting to various formats such as Excel, CSV, Parquet file, or database.

Our function configuration will look like this:

![6](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/6.png)

![7](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/7.png)

### **Apache Airflow**

Now we have every piece of the puzzle so let's put it together.

We’ll submit our spark job using `spark-submit` so our first Task will use a BashOperator for that

Next, we want to run a bash script so our second operator will also be a BashOperator. What does this script do? I have already explained earlier.

Perfect now our DAG should look like this.

![8](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/8.png)

![9](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/9.png)

![10](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/10.png)

And as mentioned earlier in the next step Google Cloud Function will take this data and load it into the Google Big Query.

### Google BigQuery

> Note: Here make sure that we have a table as follows before our Google Cloud Function runs.
> 

![11](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/11.png)

Now after a perfect Data Pipeline execution, our BigQuery table will have 327716 records.

![12](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/12.png)

### **Look Studio**

Awesome, now we have some meaningful data in our BigQuery table that we can use for getting some insights and Look Studio is a perfect choice for that. We can connect it with our BigQuery table and start building reports as we want.

Here is the report that I created to answer the questions that came into my mind when I saw this data for the very first time.

![13](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/13.jpeg)
