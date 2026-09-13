"""Statistical Z-Score based anomaly detection."""
import numpy as np
import pandas as pd

FEATURES = ["revenue", "expenses", "operating_cash_flow", "net_profit"]


def detect(df: pd.DataFrame, threshold: float = 2.0) -> dict:
    """Flag periods where any feature deviates more than `threshold` std devs."""
    if len(df) < 4:
        return {"indices": [], "z_scores": {}, "risk_level": "Low", "reasons": []}

    z_scores = {}
    flags = set()
    reasons = []

    for col in FEATURES:
        if col not in df.columns:
            continue
        series = df[col].astype(float)
        mean = series.mean()
        std = series.std(ddof=0)
        if std == 0:
            z = np.zeros(len(series))
        else:
            z = (series - mean) / std
        z_scores[col] = [round(float(v), 3) for v in z]

        for i, val in enumerate(z):
            if abs(val) > threshold:
                flags.add(i)
                reasons.append(
                    f"Period {df.iloc[i]['period']}: {col} Z-score = {round(float(val), 2)}"
                )

    indices = sorted(flags)
    if len(indices) > len(df) * 0.2:
        risk = "High"
    elif indices:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "indices": indices,
        "z_scores": z_scores,
        "threshold": threshold,
        "risk_level": risk,
        "reasons": reasons,
    }
