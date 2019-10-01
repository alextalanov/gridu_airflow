from datetime import datetime
from airflow import DAG


def create_dag(dag_id, start_date, schedule_interval=None):
    with DAG(dag_id=dag_id, start_date=datetime.fromisoformat(start_date), schedule_interval=schedule_interval) as dag:
        pass  # TODO init operators here
    return dag


config = {
    'dag_id_1': {'schedule_interval': None, 'start_date': '2019-10-01'},
    'dag_id_2': {'schedule_interval': None, 'start_date': '2019-10-01'},
    'dag_id_3': {'schedule_interval': None, 'start_date': '2019-10-01'}
}

for key, value in config.items():
    globals()[key] = create_dag(dag_id=key,
                                start_date=value['start_date'],
                                schedule_interval=value['schedule_interval'])
