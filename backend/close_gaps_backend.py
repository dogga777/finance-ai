"""FinSight AI — Close critical backend gaps."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "app"
FILES = {}

# =====================================================
# services/advanced_prediction.py — XGBoost + Linear + Revenue/Expense
# =====================================================
FILES["services/advanced_prediction.py"] = '''
"""Multiple ML models for cash flow, revenue, expense, and working capital."""
import os
from typing import List

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

from app.core.config import settings
from app.services.preprocessing import NUMERIC_FIELDS

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
        return XGBRegressor(n_estimators=300, max_depth=5, learning_rate=0.1,
                            random_state=42, verbosity=0)
    if name == "linear":
        return LinearRegression()
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
    trends = {}
    for f in FEATURES:
        if len(df) >= 3:
            changes = df[f].pct_change().replace([np.inf, -np.inf], 0).dropna()
            trends[f] = float(changes.mean()) if len(changes) else 0.0
        else:
            trends[f] = 0.0

    current = df.iloc[-1][FEATURES].to_dict()
    preds = []
    for _ in range(horizon):
        X_next = pd.DataFrame([current])
        y_next = float(model.predict(X_next)[0])
        preds.append(round(y_next, 2))
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
    """Predict cash flow, revenue, expenses, net profit using 3 models each."""
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
'''

# =====================================================
# services/zscore.py — Z-Score anomaly detection
# =====================================================
FILES["services/zscore.py"] = '''
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
'''

# =====================================================
# services/lime_explain.py — LIME (with SHAP fallback)
# =====================================================
FILES["services/lime_explain.py"] = '''
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
'''

# =====================================================
# services/trends.py — Trend analysis over time
# =====================================================
FILES["services/trends.py"] = '''
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
'''

# =====================================================
# services/explanation_text.py — LLM-style natural language
# =====================================================
FILES["services/explanation_text.py"] = '''
"""Generate natural language explanations of predictions."""


def explain_prediction(ratios: dict, predictions: dict, anomalies: dict) -> dict:
    """Build a human-readable explanation for the current forecast."""
    parts = []
    drivers = []

    rev = ratios.get("net_profit_margin", 0)
    debt = ratios.get("debt_ratio", 0)
    current = ratios.get("current_ratio", 0)

    if rev > 0.10:
        parts.append(f"Strong net profit margin of {rev*100:.1f}%")
        drivers.append(("profitability", "positive", rev))
    elif rev > 0:
        parts.append(f"Modest net profit margin of {rev*100:.1f}%")
        drivers.append(("profitability", "neutral", rev))
    else:
        parts.append(f"Negative profit margin ({rev*100:.1f}%)")
        drivers.append(("profitability", "negative", rev))

    if current < 1.0:
        parts.append("Current ratio below 1.0 suggests liquidity pressure")
        drivers.append(("liquidity", "negative", current))
    elif current > 2.0:
        parts.append(f"Healthy liquidity (current ratio {current:.2f})")
        drivers.append(("liquidity", "positive", current))

    if debt > 0.6:
        parts.append(f"High leverage (debt ratio {debt:.2f})")
        drivers.append(("leverage", "negative", debt))

    cf_values = predictions.get("predicted_values") or []
    if cf_values and len(cf_values) >= 2:
        delta = (cf_values[-1] - cf_values[0]) / abs(cf_values[0]) if cf_values[0] else 0
        if delta > 0.05:
            parts.append(f"Cash flow is projected to grow {delta*100:.1f}% over the horizon")
        elif delta < -0.05:
            parts.append(f"Cash flow is projected to decline {abs(delta)*100:.1f}% — consider cost controls")
        else:
            parts.append("Cash flow is expected to remain roughly stable")

    if anomalies.get("risk_level") == "High":
        parts.append("Multiple anomalous periods detected — investigate unusual transactions")

    summary = ". ".join(parts) + "."
    return {
        "summary": summary,
        "drivers": [
            {"factor": f, "impact": i, "value": round(float(v), 4)}
            for f, i, v in drivers
        ],
    }
'''

# =====================================================
# services/excel_report.py — Excel export
# =====================================================
FILES["services/excel_report.py"] = '''
"""Generate Excel report from the summary."""
import io
from typing import Any, Dict

import pandas as pd


def build_excel(summary: Dict[str, Any], company_name: str) -> bytes:
    """Return Excel file as bytes with multiple sheets."""
    buf = io.BytesIO()

    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        # Sheet 1: Overview
        overview = pd.DataFrame({
            "Metric": ["Company", "Financial Health Score", "Risk Level"],
            "Value": [
                company_name,
                summary["score"]["score"],
                summary["score"]["risk_level"],
            ],
        })
        overview.to_excel(writer, sheet_name="Overview", index=False)

        # Sheet 2: Ratios
        ratios_df = pd.DataFrame(
            [{"Ratio": k, "Value": v} for k, v in summary["ratios"].items()]
        )
        ratios_df.to_excel(writer, sheet_name="Ratios", index=False)

        # Sheet 3: Cash Flow Forecast
        fc = pd.DataFrame({
            "Period": [f"+{i+1}" for i in range(len(summary["predictions"]["predicted_values"]))],
            "Predicted Cash Flow": summary["predictions"]["predicted_values"],
        })
        fc.to_excel(writer, sheet_name="Forecast", index=False)

        # Sheet 4: Anomalies
        anom = pd.DataFrame({
            "Flagged Period Index": summary["anomalies"].get("indices", []),
        })
        anom.to_excel(writer, sheet_name="Anomalies", index=False)

        # Sheet 5: Recommendations
        recs = pd.DataFrame({"Recommendation": summary["recommendations"]})
        recs.to_excel(writer, sheet_name="Recommendations", index=False)

    return buf.getvalue()
'''

# =====================================================
# services/excel_reader.py — Read .xlsx uploads
# =====================================================
FILES["services/excel_reader.py"] = '''
"""Parse uploaded Excel files into the combined statement format."""
import io
from typing import List

import pandas as pd

NUMERIC_FIELDS = [
    "revenue", "expenses", "assets", "liabilities", "equity",
    "inventory", "operating_cash_flow", "investing_cash_flow",
    "financing_cash_flow", "net_profit",
]


def parse_excel(content: bytes) -> List[dict]:
    df = pd.read_excel(io.BytesIO(content))
    df.columns = [str(c).strip().lower() for c in df.columns]

    if "period" not in df.columns:
        raise ValueError("Excel file must have a 'period' column")

    statements = []
    for _, row in df.iterrows():
        obj = {"period": str(row["period"]).strip()}
        for f in NUMERIC_FIELDS:
            v = row.get(f, 0)
            if pd.isna(v):
                v = 0
            obj[f] = float(v)
        statements.append(obj)
    return statements
'''

# =====================================================
# api/routes/advanced.py — new endpoints
# =====================================================
FILES["api/routes/advanced.py"] = '''
import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.company import Company
from app.models.statement import FinancialStatement
from app.models.user import User
from app.services import (
    advanced_prediction, excel_reader, excel_report, explanation_text,
    lime_explain, prediction, preprocessing, ratios, scoring, trends, zscore,
)

router = APIRouter(prefix="/advanced", tags=["Advanced"])


def _load_df(db: Session, company_id: int, user: User):
    company = (
        db.query(Company)
        .filter(Company.id == company_id, Company.owner_id == user.id)
        .first()
    )
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    rows = (
        db.query(FinancialStatement)
        .filter(FinancialStatement.company_id == company_id)
        .order_by(FinancialStatement.period)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=400, detail="No statements uploaded")
    return company, preprocessing.statements_to_df(rows)


# ---------- /advanced/upload/excel ----------
@router.post("/upload/excel/{company_id}")
async def upload_excel(
    company_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    company = (
        db.query(Company)
        .filter(Company.id == company_id, Company.owner_id == user.id)
        .first()
    )
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only .xlsx or .xls files allowed")

    content = await file.read()
    try:
        statements = excel_reader.parse_excel(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    created = []
    for s in statements:
        row = FinancialStatement(company_id=company_id, **s)
        db.add(row)
        created.append(row)
    db.commit()
    for c in created:
        db.refresh(c)
    return {"count": len(created), "statements": [{"id": c.id, "period": c.period} for c in created]}


# ---------- /advanced/predict/{company_id} ----------
@router.get("/predict/{company_id}")
def advanced_predict(
    company_id: int,
    horizon: int = 3,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    return advanced_prediction.predict_all(df, company_id, horizon)


# ---------- /advanced/trends/{company_id} ----------
@router.get("/trends/{company_id}")
def get_trends(
    company_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    return trends.compute_trends(df)


# ---------- /advanced/zscore/{company_id} ----------
@router.get("/zscore/{company_id}")
def zscore_detect(
    company_id: int,
    threshold: float = 2.0,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    return zscore.detect(df, threshold)


# ---------- /advanced/lime/{company_id} ----------
@router.get("/lime/{company_id}")
def lime_explain_endpoint(
    company_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    model = prediction.load_model(company_id) or prediction.train_and_save(df, company_id)
    return lime_explain.explain_local(model, df)


# ---------- /advanced/explanation/{company_id} ----------
@router.get("/explanation/{company_id}")
def text_explanation(
    company_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    ratio_result = ratios.compute_ratios(df)
    pred = prediction.predict(df, company_id, 3)
    from app.services import anomaly as anomaly_service
    anom = anomaly_service.detect(df)
    return explanation_text.explain_prediction(ratio_result, pred, anom)


# ---------- /advanced/report/{company_id}/excel ----------
@router.get("/report/{company_id}/excel")
def excel_report_endpoint(
    company_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    company, df = _load_df(db, company_id, user)

    ratio_result = ratios.compute_ratios(df)
    score = scoring.financial_health_score(ratio_result)
    pred = prediction.predict(df, company_id, 3)
    from app.services import anomaly as anomaly_service
    anom = anomaly_service.detect(df)
    from app.services import recommendation
    recs = recommendation.build_recommendations(ratio_result, anom, pred["predicted_values"])

    summary = {
        "ratios": ratio_result,
        "score": score,
        "predictions": pred,
        "anomalies": anom,
        "recommendations": recs,
    }
    excel_bytes = excel_report.build_excel(summary, company.name)

    return StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=finsight_report_{company_id}.xlsx"},
    )
'''

# =====================================================
# Register route in main.py
# =====================================================
path_main = ROOT / "main.py"
main_src = path_main.read_text(encoding="utf-8")

if "advanced" not in main_src:
    # add import
    main_src = main_src.replace(
        "from app.api.routes import (",
        "from app.api.routes import (\n    advanced,"
    )
    # add router to list
    main_src = main_src.replace(
        "for _router in [\n    health.router,",
        "for _router in [\n    health.router,\n    advanced.router,"
    )
    path_main.write_text(main_src, encoding="utf-8")
    print("  updated  app/main.py")

# ---------- Write all new files ----------
for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"  created  app/{rel}")

print("\n✅ Backend gap-closing script complete.")