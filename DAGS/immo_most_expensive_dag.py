import logging, sys
from airflow.decorators import dag
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator

# Set up logging to stdout
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Since you're always running from Docker, set the host to 'host.docker.internal'
host = "host.docker.internal"


@dag(
    start_date=datetime(2024, 5, 1),
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=["example"],
)
def immo_most_expensive_dag():
    run_docker = DockerOperator(
        task_id="run_immo",
        image="immo-most-expensive",
        auto_remove=True,
        command="",
        docker_url=f"tcp://{host}:2375",
        network_mode="bridge",
        tty=True,  # Set tty to True
        do_xcom_push=True,  # Set do_xcom_push to True
        mount_tmp_dir=False,  # Disable mounting of temporary directory
    )


immo_most_expensive_dag = immo_most_expensive_dag()
