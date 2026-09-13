"""Parse uploaded Excel files into the combined statement format."""
import io
from typing import List

import pandas as pd

NUMERIC_FIELDS = [
    "revenue", "expenses", "assets", "liabilities", "equity",
    "inventory", "operating_cash_flow", "investing_cash_flow",
    "financing_cash_flow", "net_profit",
]


def parse_excel(content: bytes) -> List[dict]:
    df = pd.read_excel(io.BytesIO(content))
    df.columns = [str(c).strip().lower() for c in df.columns]

    if "period" not in df.columns:
        raise ValueError("Excel file must have a 'period' column")

    statements = []
    for _, row in df.iterrows():
        obj = {"period": str(row["period"]).strip()}
        for f in NUMERIC_FIELDS:
            v = row.get(f, 0)
            if pd.isna(v):
                v = 0
            obj[f] = float(v)
        statements.append(obj)
    return statements
