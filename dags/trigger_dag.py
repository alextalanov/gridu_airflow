from airflow import DAG
from datetime import datetime
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.contrib.hooks.fs_hook import FSHook
from pathlib import Path

SHARED_FS_CONN_ID = 'docker_compose_shared'
DEFAULT_FILE_PATH = 'trigger_files/run'
DEFAULT_FINISH_DIR = 'finished/'
DEFAULT_TRIGGER_DAG = 'dag_id_1'

shared_fs_path = Path(FSHook(conn_id=SHARED_FS_CONN_ID).get_path())
trigger_file = Variable.get('trigger_file_path', default_var=DEFAULT_FILE_PATH)
finish_dir = Variable.get('finished_dir', default_var=DEFAULT_FINISH_DIR)
trigger_dag_id = Variable.get('trigger_dag_id', default_var=DEFAULT_TRIGGER_DAG)


def print_result_func(external_dag_id, last_task_id):
    def init(**context):
        msg = context['ti'].xcom_pull(dag_id=external_dag_id, task_ids=last_task_id)
        print(f'Dag={external_dag_id}, task={last_task_id} return value={msg}')

    return init


def create_monitoring_dag(
        parent_dag, start_date, schedule_interval, triggered_dag_id, finish_file_dir, trigger_file_path):
    with DAG(
            dag_id=f'{parent_dag}.monitoring_dag',
            start_date=start_date,
            schedule_interval=schedule_interval
    ) as sub_dag:
        external_dag_sensor = ExternalTaskSensor(
            task_id='external_dag_sensor',
            external_dag_id=triggered_dag_id,
            external_task_id='',
            poke_interval=10)

        print_result = PythonOperator(
            task_id='print_result',
            provide_context=True,
            python_callable=print_result_func(external_dag_id=triggered_dag_id, last_task_id='end'))

        remove_file = BashOperator(
            task_id='remove_file',
            bash_command=f'rm -f {trigger_file_path}')

        create_finish_file = BashOperator(
            task_id='create_finish_file',
            bash_command="touch {{ params.finish_file_dir }}/finished_{{ ts_nodash }}",
            params={'finish_file_dir': finish_file_dir}
        )

    external_dag_sensor >> print_result >> remove_file >> create_finish_file

    return sub_dag


with DAG(
        dag_id='trigger_dag',
        start_date=datetime(2019, 10, 3),
        schedule_interval=None
) as dag:
    file_sensor = FileSensor(
        task_id='file_sensor', filepath=trigger_file, poke_interval=10, fs_conn_id=SHARED_FS_CONN_ID)
    dug_trigger = TriggerDagRunOperator(
        task_id='dug_trigger', trigger_dag_id=trigger_dag_id, execution_date='{{ execution_date }}')
    monitoring_subdag = SubDagOperator(
        task_id='monitoring_dag',
        subdag=create_monitoring_dag(parent_dag=dag.dag_id,
                                     start_date=dag.start_date,
                                     schedule_interval=dag.schedule_interval,
                                     triggered_dag_id=trigger_dag_id,
                                     finish_file_dir=shared_fs_path / finish_dir,
                                     trigger_file_path=shared_fs_path / trigger_file))

file_sensor >> dug_trigger >> monitoring_subdag
