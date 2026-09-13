"""Local interpretable explanations using LIME (fallback to feature importances)."""
import numpy as np
import pandas as pd

from app.services.prediction import FEATURES


def explain_local(model, df: pd.DataFrame, sample_index: int = -1) -> dict:
    """Explain a single prediction using LIME if available, else fallback."""
    try:
        from lime.lime_tabular import LimeTabularExplainer
    except Exception:
        return _fallback(model, df)

    try:
        X = df[FEATURES].fillna(0).values
        explainer = LimeTabularExplainer(
            training_data=X,
            feature_names=FEATURES,
            mode="regression",
            discretize_continuous=True,
        )
        sample = X[sample_index]
        explanation = explainer.explain_instance(
            sample,
            model.predict,
            num_features=len(FEATURES),
        )

        weights = dict(explanation.as_list())
        return {
            "method": "LIME",
            "feature_weights": {k: round(float(v), 4) for k, v in weights.items()},
            "local_prediction": round(float(explanation.predicted_value), 2),
            "intercept": round(float(explanation.intercept[0]), 2),
        }
    except Exception:
        return _fallback(model, df)


def _fallback(model, df: pd.DataFrame) -> dict:
    """Fallback: return global feature importances."""
    try:
        importances = dict(zip(FEATURES, model.feature_importances_.tolist()))
        return {
            "method": "feature_importance (LIME fallback)",
            "feature_weights": {k: round(float(v), 4) for k, v in importances.items()},
        }
    except Exception:
        return {"method": "unavailable", "feature_weights": {}}
