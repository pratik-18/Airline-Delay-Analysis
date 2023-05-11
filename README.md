### Introduction:

The Airline Data Analysis Project aims to provide insights into airline data, helping end users understand the number of delays that happened and also the minutes of delay in a specific year. The project uses tools like Python, PySpark, Airflow, Pandas, SQL, and data visualization tools to analyze data that will be described later on. The outcomes will be in the form of a dashboard that includes insights like airline performance, time series analysis etc.

### Objectives:

1. The data has been gathered in a CSV file (but that is not in good shape as it is raw data).
2. Data Cleaning and Transformation: The collected data needs to be cleaned and transformed to make it consistent and of good quality.
3. Loading Data into a Data Warehouse: The transformed data will be loaded into a data warehouse, enabling data analysis and visualization.
4. Creation of Dashboard.

### The following tools have been used for this project:

1. **Google Compute Engine:** All of the activities of this project were done using GCE.
2. **Python**: Python was utilized to code ETL (Extract, Transform, Load) scripts for data processing.
3. **PySpark**: We have a large data file (assumption) containing multiple years of data, PySpark was the tool of choice due to its distributed computing design. It allowed us to break down the data into manageable chunks for further processing.
4. **Bash Script**: Once the data was processed, it needed to be uploaded to a GCS (Google Cloud Storage) Bucket with proper naming conventions. A Bash script was employed to transform the PySpark output and load it into the bucket.
5. **Google Cloud Storage**: Google Cloud Storage served as the data storage solution for PySpark processed data.
6. **Google Cloud Functions**: With the data in perfect shape and split into smaller files, an ETL pipeline was triggered as soon as a file arrived in the GCS bucket. This process fine-tuned the data and loaded it into Google BigQuery for storage.
7. **Pandas**: Pandas was used for data cleaning and manipulation within the Google Cloud Function.
8. **Apache Airflow**: Airflow was utilized for the automation and scheduling of the ETL process.
9. **Google BigQuery**: Google BigQuery was used as a data warehouse for storing transformed data, making it accessible for analysis and reporting purposes.
10. **Look Studio**: Finally, Looker Studio was used for dashboard creation.

### System Architecture

![Untitled](https://github.com/pratik-18/Airline-Delay-Analysis/blob/main/images/System_Design.jpeg)

Let’s look in detail at how everything works together: [Click here](...)  👈

### Installation:

1. Clone the project repository.
2. Create a GCP account and set up a VM, GCS Bucket and Big Query.
3. Install PySpark on VM for that follow these [instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/linux.md) after that install Airflow as well.
4. Create a GCS function and paste this code (Configure this function to get triggered when data in GCS Bucket arrives).
5. Create a table in Big Query as per this screenshot.
6. Configure the Airflow DAG & PySpark script to match your GCS and BigQuery configurations.
7. Strat Spark master & worker.
8. Start the Airflow scheduler using the following command:
**`airflow scheduler`**
9. Start the Airflow webserver using the following command:
**`airflow webserver -p 8080`**

### Usage:

1. Make sure that everything has been configured properly.
2. Run the Airflow DAG to start the ETL process.
3. Check the Big Query to ensure that the transformed data has been loaded correctly. It should have **327716 rows**.
4. Use data analysis tools to generate insights from the transformed data.
