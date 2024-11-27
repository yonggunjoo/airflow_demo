from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import requests
import json
import csv
import os


def fetch_api_data(**context):
    """API에서 데이터 가져오기"""
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        headers={"Content-Type": "application/json"},
    )
    return response.json()


def process_data(**context):
    """데이터 처리 및 CSV 저장"""
    task_instance = context["task_instance"]
    data = task_instance.xcom_pull(task_ids="fetch_api_data")

    output_dir = "/opt/airflow/bucket/data/success"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir, f'data_{context["execution_date"].strftime("%Y%m%d")}.csv'
    )

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    return output_file


with DAG(
    "api_data_pipeline",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # API 데이터 수집
    fetch_data = PythonOperator(
        task_id="fetch_api_data", python_callable=fetch_api_data
    )

    # 데이터 처리
    process_data = PythonOperator(task_id="process_data", python_callable=process_data)

    # 알림 전송
    send_notification = EmailOperator(
        task_id="send_notification",
        to="study.jyg@gmail.com",
        subject="데이터 파이프라인 실행 완료",
        html_content="파이프라인이 성공적으로 완료되었습니다.",
    )

    # 작업 순서 정의
    fetch_data >> process_data >> send_notification
