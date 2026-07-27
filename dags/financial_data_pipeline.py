from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except ImportError:  # pragma: no cover - optional dependency for local execution
    DAG = None
    PythonOperator = None

from src.pipeline import run_pipeline

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "data" / "sample_financial_data.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed_financial_data.csv"


def run_pipeline_task(**_context) -> None:
    run_pipeline(input_path=INPUT_PATH, output_path=OUTPUT_PATH)


if DAG is not None and PythonOperator is not None:
    with DAG(
        dag_id="financial_data_pipeline",
        description="Sanitized standalone financial data pipeline",
        start_date=datetime(2024, 1, 1),
        schedule_interval="@daily",
        catchup=False,
        default_args={"owner": "data-engineer", "retries": 1, "retry_delay": timedelta(minutes=5)},
        tags=["finance", "standalone"],
    ) as dag:
        PythonOperator(task_id="run_financial_pipeline", python_callable=run_pipeline_task)
