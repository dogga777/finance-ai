import pandas as pd
from sklearn.ensemble import IsolationForest

FEATURES = ["revenue", "expenses", "operating_cash_flow", "net_profit"]


def detect(df: pd.DataFrame) -> dict:
    if len(df) < 4:
        return {"indices": [], "scores": [], "risk_level": "Low", "reasons": []}

    X = df[FEATURES].fillna(0)
    model = IsolationForest(contamination=0.15, random_state=42)
    labels = model.fit_predict(X)
    scores = model.decision_function(X)

    indices, reasons = [], []
    for i, (label, score) in enumerate(zip(labels, scores)):
        if label == -1:
            indices.append(i)
            reasons.append(f"Period {df.iloc[i]['period']} flagged (score={round(float(score), 3)})")

    if len(indices) > len(df) * 0.2:
        risk = "High"
    elif indices:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "indices": indices,
        "scores": [round(float(s), 4) for s in scores],
        "risk_level": risk,
        "reasons": reasons,
    }
