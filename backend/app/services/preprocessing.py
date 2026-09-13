import pandas as pd

NUMERIC_FIELDS = [
    "revenue",
    "expenses",
    "assets",
    "liabilities",
    "equity",
    "inventory",
    "operating_cash_flow",
    "investing_cash_flow",
    "financing_cash_flow",
    "net_profit",
]


def statements_to_df(rows) -> pd.DataFrame:
    data = [
        {**{f: getattr(r, f, 0) for f in NUMERIC_FIELDS},
         "period": r.period,
         "id": getattr(r, "id", None)}
        for r in rows
    ]
    return clean_df(pd.DataFrame(data))


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates(subset=["period"]).sort_values("period").reset_index(drop=True)

    for col in NUMERIC_FIELDS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median()).fillna(0)

    return df
