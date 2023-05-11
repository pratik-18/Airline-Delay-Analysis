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
    'spark_master' : 'spark://ada-vm.us-west4-b.c.airline-delay-analysis-proj.internal:7077',
    'spark_script' : '/home/pratikkakadiya18/proj/spark_scripts/DataPrep.py',
    'shell_script' : '/home/pratikkakadiya18/proj/bash_script/copy_pq_local_to_gcs.sh',
    'spark_op' : '/home/pratikkakadiya18/proj/spark_output/ada_pq'
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
