from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd


def load_financial_data(input_path: Union[str, Path]) -> pd.DataFrame:
    """Load financial data from a CSV file."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path)
    required_columns = {"invoice_id", "customer", "amount", "currency", "status"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    return df


def transform_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize and clean the financial data for reporting."""
    transformed = df.copy()
    transformed["invoice_id"] = transformed["invoice_id"].astype(str).str.strip()
    transformed["customer"] = transformed["customer"].astype(str).str.strip()
    transformed["currency"] = transformed["currency"].astype(str).str.upper().str.strip()
    transformed["status"] = transformed["status"].astype(str).str.strip().str.lower()
    transformed["amount"] = pd.to_numeric(transformed["amount"], errors="coerce")

    transformed["net_amount"] = transformed["amount"].where(transformed["status"] != "void", 0)
    transformed = transformed.dropna(subset=["net_amount"])

    return transformed[["invoice_id", "customer", "currency", "status", "amount", "net_amount"]]


def run_pipeline(input_path: Union[str, Path], output_path: Union[str, Path]) -> Path:
    """Run the end-to-end pipeline and write a processed CSV output."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    raw_data = load_financial_data(input_path)
    transformed_data = transform_financial_data(raw_data)
    transformed_data.to_csv(output, index=False)

    return output
