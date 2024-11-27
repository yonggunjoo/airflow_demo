from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import requests


def fetch_data(**context):
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        headers={"Content-Type": "application/json"},
    )
    data = response.json()

    # task_id에 따라 성공/실패 분기
    if context["task"].task_id == "fetch_failure_data":
        raise Exception("의도적 실패 발생")
    return data


# retry 이후에도 최종 실패
def send_error_email(context):
    EmailOperator(
        task_id="error_email",
        to="study.jyg@gmail.com",
        subject=f"작업 실패: {context['task'].task_id}",
        html_content=f"에러 발생: {context.get('exception')}",
    ).execute(context=context)


with DAG(
    "parallel_api_pipeline",
    default_args={
        "owner": "airflow",
        "email": ["study.jyg@gmail.com"],
        "email_on_failure": True,
        "retries": 1,  # retry 횟수 1회
        "retry_delay": timedelta(minutes=1),
        "on_failure_callback": send_error_email,
    },
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    fetch_success = PythonOperator(
        task_id="fetch_success_data", python_callable=fetch_data
    )

    fetch_failure = PythonOperator(
        task_id="fetch_failure_data", python_callable=fetch_data
    )

    success_email = EmailOperator(
        task_id="success_email",
        to="study.jyg@gmail.com",
        subject="API 요청 성공",
        html_content="데이터를 성공적으로 가져왔습니다.",
    )

    [fetch_success, fetch_failure]  # 병렬 실행
    fetch_success >> success_email
