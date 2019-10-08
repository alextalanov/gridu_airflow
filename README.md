## GridU Airflow

Go to the <b>airflow_in_docker_compose</b> folder.

<p>
<h4>For the first run use following commands:</h4>
<ul>
<li><i>docker pull redis:5.0.5</i></li>
<li><i>docker pull postgres:9.6</i></li>
<li><i>docker-compose up postgres</i></li>
<li><i>docker-compose up initdb</i></li>
<li><i>docker-compose up init_fs_path</i></li>
<li><i>docker-compose up --scale worker=2 webserver scheduler redis worker flower</i></li>
<li><i>mkdir <b>project-dir</b>/shared_fs/finished</i></li>
<li><i>mkdir <b>project-dir</b>/shared_fs/trigger_files</i></li>
</ul>
</p>

<p>
<h4>Login to postgres DB using:</h4>
<ul>
<li>url: jdbc:postgresql://localhost:5432/airflow </li>
<li>user: airflow </li>
<li>password: airflow </li>
</ul>
<p>Execute sql query: <b><i>update connection set login='airflow' where conn_id='postgres_default'</i></b><p>
</p>

<p>
<h4>Next time you can use: </h4>
<ul>
<li><i>docker-compose up -d --scale worker=2 postgres webserver scheduler redis worker flower</i></li>
</ul>
</p>

<p>
<h4>For run pipeline:</h4>
<ol>
 <li>enable <b>dag_id_1</b> and <b>trigger_dag</b></li>
 <li>trigger <b>trigger_dag</b></li>
 <li>create <b>run</b> file in <i><b>project-dir</b>/shared_fs/trigger_files</i> dir</li>
</ol>
</p>

