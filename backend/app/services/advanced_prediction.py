"""Multiple ML models for cash flow, revenue, expense, and working capital."""
import os
from typing import List

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

from app.core.config import settings

FEATURES = [
    "revenue", "expenses", "assets", "liabilities",
    "equity", "inventory", "net_profit",
]
TARGETS = {
    "operating_cash_flow": "Cash Flow",
    "revenue": "Revenue",
    "expenses": "Expenses",
    "net_profit": "Net Profit",
}


def _model_path(company_id: int, target: str, model_name: str) -> str:
    return f"{settings.MODEL_DIR}/{target}_{model_name}_company_{company_id}.joblib"


def _build_model(name: str):
    if name == "random_forest":
        return RandomForestRegressor(n_estimators=300, max_depth=8, random_state=42)
    if name == "xgboost":
        return XGBRegressor(
            n_estimators=300, max_depth=5, learning_rate=0.1,
            random_state=42, verbosity=0,
        )
    if name == "linear":
        # Pipeline scales features first — prevents 10^14 predictions
        return make_pipeline(StandardScaler(), LinearRegression())
    raise ValueError(f"Unknown model: {name}")


def _prepare(df: pd.DataFrame, target: str):
    df = df.sort_values("period").reset_index(drop=True)
    if len(df) < 6:
        raise ValueError("Need at least 6 periods")
    X = df[FEATURES].shift(1).dropna()
    y = df[target].iloc[1:]
    return X, y


def train_model(df: pd.DataFrame, company_id: int, target: str, model_name: str):
    X, y = _prepare(df, target)
    model = _build_model(model_name)
    model.fit(X, y)
    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    joblib.dump(model, _model_path(company_id, target, model_name))
    return model


def load_model(company_id: int, target: str, model_name: str):
    try:
        return joblib.load(_model_path(company_id, target, model_name))
    except FileNotFoundError:
        return None


def _forecast(model, df: pd.DataFrame, target: str, horizon: int) -> List[float]:
    df = df.sort_values("period").reset_index(drop=True)

    # Historical trends, capped at ±5% to prevent runaway
    trends = {}
    for f in FEATURES:
        if len(df) >= 3:
            changes = df[f].pct_change().replace([np.inf, -np.inf], 0).dropna()
            mean_change = float(changes.mean()) if len(changes) else 0.0
            trends[f] = max(-0.05, min(0.05, mean_change))
        else:
            trends[f] = 0.0

    current = df.iloc[-1][FEATURES].to_dict()

    # Wide, forgiving sanity bounds
    target_last = float(df[target].iloc[-1])
    target_max = float(df[target].max())
    target_min = float(df[target].min())
    upper_bound = max(target_max * 2, target_last * 1.5)
    lower_bound = max(0.0, min(target_min * 0.5, target_last * 0.5))

    preds = []
    for _ in range(horizon):
        X_next = pd.DataFrame([current])
        y_next = float(model.predict(X_next)[0])

        # Only clamp truly insane values
        if not np.isfinite(y_next) or y_next > upper_bound:
            y_next = target_last * 1.05
        elif y_next < lower_bound:
            y_next = max(0.0, target_last * 0.95)

        preds.append(round(y_next, 2))

        # Roll features by their historical trend
        for f in FEATURES:
            current[f] = current[f] * (1 + trends[f])

    return preds


def evaluate_model(df: pd.DataFrame, target: str, model_name: str) -> dict:
    X, y = _prepare(df, target)
    if len(X) < 4:
        return {"mae": None, "r2": None}

    split = max(1, int(len(X) * 0.8))
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = _build_model(model_name)
    model.fit(X_train, y_train)

    if len(X_test) == 0:
        return {"mae": None, "r2": None}

    pred = model.predict(X_test)
    return {
        "mae": round(float(mean_absolute_error(y_test, pred)), 2),
        "r2": round(float(r2_score(y_test, pred)), 4),
    }


def predict_all(df: pd.DataFrame, company_id: int, horizon: int = 3) -> dict:
    results = {}
    for target in TARGETS.keys():
        if target not in df.columns:
            continue
        model_results = {}
        for model_name in ["random_forest", "xgboost", "linear"]:
            model = load_model(company_id, target, model_name)
            if model is None:
                try:
                    model = train_model(df, company_id, target, model_name)
                except Exception:
                    continue
            try:
                preds = _forecast(model, df, target, horizon)
                metrics = evaluate_model(df, target, model_name)
                model_results[model_name] = {
                    "predictions": preds,
                    "mae": metrics["mae"],
                    "r2": metrics["r2"],
                }
            except Exception:
                continue

        results[target] = {
            "label": TARGETS[target],
            "models": model_results,
            "best_model": min(
                model_results.items(),
                key=lambda kv: kv[1]["mae"] if kv[1]["mae"] is not None else 1e18
            )[0] if model_results else None,
        }
    return results