from airflow import DAG
from datetime import datetime
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.bash_operator import BashOperator

FILE_PATH = '/Users/atalanov/Desktop/run'

with DAG(dag_id='trigger_dag', start_date=datetime.fromisoformat('2019-10-01'), schedule_interval=None) as dag:
    file_sensor = FileSensor(task_id='file_sensor', filepath=FILE_PATH, poke_interval=10)
    dug_trigger = TriggerDagRunOperator(task_id='dug_trigger', trigger_dag_id='dag_id_1')
    remove_file = BashOperator(task_id='remove_file', bash_command=f'rm -f {FILE_PATH}')

file_sensor >> dug_trigger >> remove_file
