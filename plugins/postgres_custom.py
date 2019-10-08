import logging
from airflow.plugins_manager import AirflowPlugin
from airflow.operators import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults

log = logging.getLogger(__name__)


class PostgreSQLCountRows(BaseOperator):

    @apply_defaults
    def __init__(self, schema, table, conn_id=None, *args, **kvargs):
        self.hook = PostgresHook(conn_id=conn_id) if conn_id else PostgresHook()

        if not schema or not table:
            raise ValueError('Schema and table params must be set!')
        self.schema = schema
        self.table = table

        super(PostgreSQLCountRows, self).__init__(*args, **kvargs)

    def execute(self, context):
        log.info(f'''
            schema = {self.schema},
            table = {self.table}
        ''')
        return self.hook.get_first(sql=f'SELECT COUNT(1) FROM {self.schema}.{self.table}')[0]


class AirflowTestPlugin(AirflowPlugin):
    name = "postgres_custom"
    operators = [PostgreSQLCountRows]
