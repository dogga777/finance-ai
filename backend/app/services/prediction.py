import os
from typing import List

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

from app.core.config import settings

FEATURES = [
    "revenue", "expenses", "assets", "liabilities",
    "equity", "inventory", "net_profit",
]
TARGET = "operating_cash_flow"


def _model_path(company_id: int) -> str:
    return f"{settings.MODEL_DIR}/cashflow_company_{company_id}.joblib"


def train(df: pd.DataFrame) -> RandomForestRegressor:
    df = df.sort_values("period").reset_index(drop=True)
    if len(df) < 6:
        raise ValueError("At least 6 periods of data are required for training.")

    X = df[FEATURES].shift(1).dropna()
    y = df[TARGET].iloc[1:]

    model = RandomForestRegressor(n_estimators=300, max_depth=8, random_state=42)
    model.fit(X, y)
    return model


def train_and_save(df: pd.DataFrame, company_id: int):
    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    model = train(df)
    joblib.dump(model, _model_path(company_id))
    return model


def load_model(company_id: int):
    try:
        return joblib.load(_model_path(company_id))
    except FileNotFoundError:
        return None


def predict(df: pd.DataFrame, company_id: int, horizon: int = 3) -> dict:
    model = load_model(company_id) or train_and_save(df, company_id)

    last = df.iloc[-1]

    # Compute average growth rate for each feature from history
    trends = {}
    for f in FEATURES:
        if len(df) >= 3:
            changes = df[f].pct_change().replace([float("inf"), float("-inf")], 0).dropna()
            trends[f] = float(changes.mean()) if len(changes) else 0.0
        else:
            trends[f] = 0.0

    current = last[FEATURES].to_dict()
    predictions = []

    for _ in range(horizon):
        X_next = pd.DataFrame([current])
        y_next = float(model.predict(X_next)[0])
        predictions.append(round(y_next, 2))
        # Apply historical trend to each feature so the next step differs
        for f in FEATURES:
            current[f] = current[f] * (1 + trends[f])

    confidence = 0.85
    if len(df) >= 8:
        try:
            X = df[FEATURES].shift(1).dropna()
            y = df[TARGET].iloc[1:]
            r2 = r2_score(y, model.predict(X))
            confidence = round(max(0.0, min(1.0, (r2 + 1) / 2)), 2)
        except Exception:
            pass

    return {
        "predicted_values": predictions,
        "confidence": confidence,
        "model_name": "RandomForestRegressor",
    }