"""Add LSTM + Prophet + PostgreSQL support to the backend."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "app"
FILES = {}

# =====================================================
# services/lstm_model.py — LSTM time-series
# =====================================================
FILES["services/lstm_model.py"] = '''
"""LSTM time-series model for cash flow prediction."""
import os

import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

from app.core.config import settings

SEQUENCE_LEN = 6
FEATURES = ["revenue", "expenses", "operating_cash_flow", "net_profit"]


def _path(company_id: int) -> str:
    return f"{settings.MODEL_DIR}/lstm_company_{company_id}.keras"


def _build_model(input_shape):
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.LSTM(64, return_sequences=True),
        layers.Dropout(0.2),
        layers.LSTM(32),
        layers.Dropout(0.2),
        layers.Dense(16, activation="relu"),
        layers.Dense(1),
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return model


def _train(df: pd.DataFrame, company_id: int, epochs: int = 50):
    df = df.sort_values("period").reset_index(drop=True)
    if len(df) < SEQUENCE_LEN + 2:
        raise ValueError(f"Need at least {SEQUENCE_LEN + 2} periods")

    data = df[FEATURES].astype(float).values
    mean = data.mean(axis=0)
    std = data.std(axis=0) + 1e-8
    norm = (data - mean) / std

    target = norm[SEQUENCE_LEN:, 2]
    X = np.array([norm[i: i + SEQUENCE_LEN] for i in range(len(norm) - SEQUENCE_LEN)])

    model = _build_model((SEQUENCE_LEN, len(FEATURES)))
    model.fit(X, target, epochs=epochs, verbose=0)

    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    model.save(_path(company_id))
    return model, mean, std


def predict_lstm(df: pd.DataFrame, company_id: int, horizon: int = 3):
    df = df.sort_values("period").reset_index(drop=True)
    data = df[FEATURES].astype(float).values
    mean = data.mean(axis=0)
    std = data.std(axis=0) + 1e-8

    model = _train(df, company_id, epochs=50)[0]

    seq = ((data - mean) / std)[-SEQUENCE_LEN:]
    predictions = []

    for _ in range(horizon):
        x = np.array([seq])
        y_norm = float(model.predict(x, verbose=0)[0][0])
        y = y_norm * std[2] + mean[2]
        predictions.append(round(float(y), 2))
        new_row = seq[-1].copy()
        new_row[2] = y_norm
        seq = np.vstack([seq[1:], new_row])

    return {"predictions": predictions, "model": "LSTM", "sequence_length": SEQUENCE_LEN}
'''

# =====================================================
# services/prophet_model.py — Prophet time-series
# =====================================================
FILES["services/prophet_model.py"] = '''
"""Prophet time-series model for cash flow prediction."""
import pandas as pd
from prophet import Prophet


def predict_prophet(df: pd.DataFrame, company_id: int, horizon: int = 3):
    df = df.sort_values("period").reset_index(drop=True)
    if len(df) < 6:
        raise ValueError("Need at least 6 periods")

    prophet_df = pd.DataFrame({
        "ds": pd.to_datetime(df["period"] + "-01"),
        "y": df["operating_cash_flow"].astype(float),
    })

    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
    )
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=horizon, freq="MS")
    forecast = model.predict(future)
    tail = forecast.tail(horizon)

    return {
        "predictions": tail["yhat"].round(2).tolist(),
        "lower_bound": tail["yhat_lower"].round(2).tolist(),
        "upper_bound": tail["yhat_upper"].round(2).tolist(),
        "model": "Prophet",
    }
'''

# =====================================================
# api/routes/advanced.py — add LSTM + Prophet endpoints
# =====================================================
path_adv = ROOT / "api" / "routes" / "advanced.py"
src = path_adv.read_text(encoding="utf-8")

# Add imports at top of advanced.py
if "lstm_model" not in src:
    src = src.replace(
        "from app.services import (",
        "from app.services import (\n    lstm_model, prophet_model,"
    )

# Append new endpoints
NEW_ENDPOINTS = '''

# ---------- LSTM prediction ----------
@router.get("/predict/lstm/{company_id}")
def predict_lstm_endpoint(
    company_id: int,
    horizon: int = 3,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    return lstm_model.predict_lstm(df, company_id, horizon)


# ---------- Prophet prediction ----------
@router.get("/predict/prophet/{company_id}")
def predict_prophet_endpoint(
    company_id: int,
    horizon: int = 3,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    return prophet_model.predict_prophet(df, company_id, horizon)


# ---------- Model comparison (all models) ----------
@router.get("/compare/{company_id}")
def compare_models(
    company_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    result = {"company_id": company_id, "models": {}}

    try:
        result["models"]["random_forest"] = advanced_prediction.predict_all(
            df, company_id, 3
        ).get("operating_cash_flow", {})
    except Exception as e:
        result["models"]["random_forest"] = {"error": str(e)}

    try:
        result["models"]["lstm"] = lstm_model.predict_lstm(df, company_id, 3)
    except Exception as e:
        result["models"]["lstm"] = {"error": str(e)}

    try:
        result["models"]["prophet"] = prophet_model.predict_prophet(df, company_id, 3)
    except Exception as e:
        result["models"]["prophet"] = {"error": str(e)}

    return result
'''

if "predict/lstm" not in src:
    src = src + NEW_ENDPOINTS
    path_adv.write_text(src, encoding="utf-8")
    print("  updated  app/api/routes/advanced.py")

# ---------- Write all new service files ----------
for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"  created  app/{rel}")

print("\n✅ Backend tech-stack files added.")