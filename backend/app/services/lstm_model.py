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
