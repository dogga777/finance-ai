import pandas as pd


def _safe_div(a, b, default=0.0):
    try:
        if b in (0, None):
            return default
        return float(a) / float(b)
    except Exception:
        return default


def compute_ratios(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}

    latest = df.iloc[-1]

    revenue = latest.get("revenue", 0) or 0
    expenses = latest.get("expenses", 0) or 0
    assets = latest.get("assets", 0) or 0
    liabilities = latest.get("liabilities", 0) or 0
    equity = latest.get("equity", 0) or 0
    inventory = latest.get("inventory", 0) or 0
    net_profit = latest.get("net_profit", 0) or 0

    return {
        "current_ratio": round(_safe_div(assets, liabilities), 4),
        "quick_ratio": round(_safe_div(assets - inventory, liabilities), 4),
        "debt_ratio": round(_safe_div(liabilities, assets), 4),
        "roa": round(_safe_div(net_profit, assets), 4),
        "roe": round(_safe_div(net_profit, equity), 4),
        "gross_margin": round(_safe_div(revenue - expenses, revenue), 4),
        "net_profit_margin": round(_safe_div(net_profit, revenue), 4),
    }
