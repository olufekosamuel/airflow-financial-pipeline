from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pipeline import load_financial_data, run_pipeline, transform_financial_data


def test_transform_financial_data_creates_expected_columns():
    input_path = Path(__file__).resolve().parent.parent / "data" / "sample_financial_data.csv"
    df = load_financial_data(input_path)

    assert not df.empty

    transformed = transform_financial_data(df)
    assert {"invoice_id", "customer", "currency", "net_amount"}.issubset(transformed.columns)
    assert transformed["net_amount"].sum() > 0


def test_run_pipeline_writes_output_file(tmp_path):
    input_path = Path(__file__).resolve().parent.parent / "data" / "sample_financial_data.csv"
    output_path = tmp_path / "processed_financial_data.csv"

    run_pipeline(input_path=input_path, output_path=output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0
