# Financial Data Pipeline

This repo contains a sanitized, standalone version of a financial data pipeline that was designed to mirror the structure of a company-facing Airflow workflow without including any sensitive information.

## What is included
- A lightweight Python pipeline for loading, cleaning, and exporting financial data
- A sample CSV input file for demonstration
- An Airflow DAG definition for orchestration
- A small test suite to verify the pipeline behaviour

## Project structure
- src/pipeline.py: core ETL logic
- dags/financial_data_pipeline.py: Airflow DAG definition
- data/sample_financial_data.csv: sample input data
- tests/test_pipeline.py: regression tests

## Quick start
1. Install dependencies:
   pip install -r requirements.txt
2. Run the pipeline:
   python -c "from src.pipeline import run_pipeline; run_pipeline('data/sample_financial_data.csv', 'data/processed_financial_data.csv')"
3. Run tests:
   pytest -q

## Notes
- No production credentials, internal URLs, or company-specific identifiers are included.
- The sample data is synthetic and safe for public GitHub use.
