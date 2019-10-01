from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator


def check_table_exist():
    is_exist = True  # TODO check
    return ['create_table' if is_exist else 'do_nothing']


def create_dag(dag_id, start_date, table, database, schedule_interval=None):
    with DAG(dag_id=dag_id, start_date=datetime.fromisoformat(start_date), schedule_interval=schedule_interval) as dag:
        start = PythonOperator(task_id='start',
                               python_callable=lambda: print(f"{dag_id} start processing tables in DB: {database}"))
        check_exist = BranchPythonOperator(task_id="check_table_exist", python_callable=check_table_exist)
        create_table = DummyOperator(task_id='create_table')
        do_nothing = DummyOperator(task_id='do_nothing')
        insert_new_row = DummyOperator(task_id='insert_new_row', trigger_rule='none_failed')
        query_the_table = DummyOperator(task_id='query_the_table')

    start >> check_exist >> [create_table, do_nothing] >> insert_new_row >> query_the_table

    return dag


config = {
    'dag_id_1': {'schedule_interval': None, 'start_date': '2019-10-01', 'table_name': 'table_name_1'},
    'dag_id_2': {'schedule_interval': None, 'start_date': '2019-10-01', 'table_name': 'table_name_2'},
    'dag_id_3': {'schedule_interval': None, 'start_date': '2019-10-01', 'table_name': 'table_name_3'},
}

for key, value in config.items():
    globals()[key] = create_dag(dag_id=key,
                                start_date=value['start_date'],
                                schedule_interval=value['schedule_interval'],
                                table=value['table_name'],
                                database='airflow')
