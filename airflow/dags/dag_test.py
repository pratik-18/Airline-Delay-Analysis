from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'pratik',
    'retries': 0,
    'retry_delay': timedelta(minutes=2)
}

dag_info = {
    'id' : 'dag_ada_v1',
    'description': 'DAG Test',
    'start_date': datetime(2023, 4, 4, 14)
}

command_infos = {
    'spark_master' : 'spark://*.airline-delay-analysis-proj.internal:7077', # Spark master URI
    'spark_script' : '/home/user/proj/spark_scripts/DataPrep.py', # Path of Spark Script
    'shell_script' : '/home/user/proj/bash_script/copy_pq_local_to_gcs.sh', # Path of Shell Script
    'spark_op' : '/home/user/proj/spark_output/ada_pq' # Path of the folder where Spark output should be stored
}


with DAG(
        dag_id= dag_info['id'], 
        default_args=default_args, 
        description=dag_info['description'] , 
        start_date=dag_info['start_date'], 
        schedule_interval='@yearly'
    ) as dag:

    task1 = BashOperator(
        task_id='execute_pyspark',
        bash_command=f"spark-submit --master={command_infos['spark_master']} {command_infos['spark_script']}"
    )

    task2 = BashOperator(
        task_id='move_data_to_gcs',
        bash_command=f"sh {command_infos['shell_script']} {command_infos['spark_op']}"
    )

    task1 >> task2
