"""Compute historical trends for revenue, expenses, profit, and ratios."""
import pandas as pd


def _safe_div(a, b, default=0.0):
    try:
        if b in (0, None):
            return default
        return float(a) / float(b)
    except Exception:
        return default


def compute_trends(df: pd.DataFrame) -> dict:
    """Return time series for revenue, expense, profit, and ratios."""
    if df.empty:
        return {"periods": [], "revenue": [], "expenses": [], "net_profit": [],
                "operating_cash_flow": [], "current_ratio": [], "net_margin": []}

    periods = df["period"].astype(str).tolist()
    revenue = df["revenue"].astype(float).tolist()
    expenses = df["expenses"].astype(float).tolist()
    net_profit = df["net_profit"].astype(float).tolist()
    ocf = df["operating_cash_flow"].astype(float).tolist()

    current_ratio, net_margin = [], []
    for _, row in df.iterrows():
        cr = _safe_div(row.get("assets", 0), row.get("liabilities", 0))
        nm = _safe_div(row.get("net_profit", 0), row.get("revenue", 0))
        current_ratio.append(round(cr, 4))
        net_margin.append(round(nm, 4))

    return {
        "periods": periods,
        "revenue": revenue,
        "expenses": expenses,
        "net_profit": net_profit,
        "operating_cash_flow": ocf,
        "current_ratio": current_ratio,
        "net_margin": net_margin,
    }
