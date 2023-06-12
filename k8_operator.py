from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


with DAG(
    dag_id='k8s_dag',
    schedule_interval='@daily',
    start_date=datetime(2022, 3, 1),
    catchup=False
) as dag:
    write_xcom = KubernetesPodOperator(
        namespace="airflow-cluster",
        image="alpine",
        cmds=["sh", "-c", "sleep 180; mkdir -p /airflow/xcom/;echo '[1,2,3,4]' > /airflow/xcom/return.json"],
        name="write-xcom",
        do_xcom_push=True,
        is_delete_operator_pod=False,
        in_cluster=True,
        task_id="write-xcom",
        get_logs=True,
    )
    pod_task_xcom_result = BashOperator(
        bash_command="echo \"{{ task_instance.xcom_pull('write-xcom')[0] }}\"",
        task_id="pod_task_xcom_result",
    )
    write_xcom >> pod_task_xcom_result
