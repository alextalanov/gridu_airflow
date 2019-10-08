FROM puckel/docker-airflow:1.10.3
RUN pip install --user psycopg2-binary
RUN pip install --user werkzeug==0.15.5
ENV AIRFLOW_HOME=/usr/local/airflow
RUN chown -R airflow: $AIRFLOW_HOME
USER airflow
WORKDIR $AIRFLOW_HOME
COPY ./airflow.cfg $AIRFLOW_HOME/airflow.cfg