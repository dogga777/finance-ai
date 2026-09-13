import numpy as np
import pandas as pd
import shap


def explain(model, df: pd.DataFrame, features: list) -> dict:
    try:
        X = df[features].fillna(0)
        explainer = shap.Explainer(model, X)
        values = explainer(X)
        importance = np.abs(values.values).mean(axis=0)
        return {f: round(float(v), 4) for f, v in zip(features, importance)}
    except Exception as error:
        return {"error": str(error)}
