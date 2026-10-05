"""Advanced ML endpoints: LSTM, Prophet, XGBoost comparison, trends, Z-Score, LIME."""
import io
import math

import numpy as np
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.company import Company
from app.models.statement import FinancialStatement
from app.models.user import User
from app.services import (
    advanced_prediction,
    anomaly as anomaly_service,
    excel_reader,
    excel_report,
    explanation_text,
    lime_explain,
    lstm_model,
    prediction,
    preprocessing,
    prophet_model,
    ratios,
    recommendation,
    scoring,
    trends,
    zscore,
)

router = APIRouter(prefix="/advanced", tags=["Advanced"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _sanitize(obj):
    """Recursively replace NaN/Infinity with None so JSON serialization succeeds."""
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def _load_df(db: Session, company_id: int, user: User):
    """Return (company, dataframe) for a company owned by the current user."""
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


# ---------------------------------------------------------------------------
# Excel upload
# ---------------------------------------------------------------------------
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

    return {
        "count": len(created),
        "statements": [{"id": c.id, "period": c.period} for c in created],
    }


# ---------------------------------------------------------------------------
# Multi-model prediction (RF + XGBoost + Linear across 4 targets)
# ---------------------------------------------------------------------------
@router.get("/predict/{company_id}")
def advanced_predict(
    company_id: int,
    horizon: int = 3,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    result = advanced_prediction.predict_all(df, company_id, horizon)
    return _sanitize(result)


# ---------------------------------------------------------------------------
# LSTM prediction
# ---------------------------------------------------------------------------
@router.get("/predict/lstm/{company_id}")
def predict_lstm_endpoint(
    company_id: int,
    horizon: int = 3,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    return _sanitize(lstm_model.predict_lstm(df, company_id, horizon))


# ---------------------------------------------------------------------------
# Prophet prediction
# ---------------------------------------------------------------------------
@router.get("/predict/prophet/{company_id}")
def predict_prophet_endpoint(
    company_id: int,
    horizon: int = 3,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    return _sanitize(prophet_model.predict_prophet(df, company_id, horizon))


# ---------------------------------------------------------------------------
# Model comparison
# ---------------------------------------------------------------------------
@router.get("/compare/{company_id}")
def compare_models(
    company_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    result = {"company_id": company_id, "models": {}}

    # Random Forest / XGBoost / Linear (via advanced_prediction)
    try:
        rf_result = advanced_prediction.predict_all(df, company_id, 3)
        result["models"]["random_forest"] = rf_result.get("operating_cash_flow", {})
    except Exception as e:
        result["models"]["random_forest"] = {"error": str(e)}

    # LSTM
    try:
        result["models"]["lstm"] = lstm_model.predict_lstm(df, company_id, 3)
    except Exception as e:
        result["models"]["lstm"] = {"error": str(e)}

    # Prophet
    try:
        result["models"]["prophet"] = prophet_model.predict_prophet(df, company_id, 3)
    except Exception as e:
        result["models"]["prophet"] = {"error": str(e)}

    return _sanitize(result)


# ---------------------------------------------------------------------------
# Trends
# ---------------------------------------------------------------------------
@router.get("/trends/{company_id}")
def get_trends(
    company_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    return _sanitize(trends.compute_trends(df))


# ---------------------------------------------------------------------------
# Z-Score anomaly detection
# ---------------------------------------------------------------------------
@router.get("/zscore/{company_id}")
def zscore_detect(
    company_id: int,
    threshold: float = 2.0,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    return _sanitize(zscore.detect(df, threshold))


# ---------------------------------------------------------------------------
# LIME explanation
# ---------------------------------------------------------------------------
@router.get("/lime/{company_id}")
def lime_explain_endpoint(
    company_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    model = prediction.load_model(company_id) or prediction.train_and_save(df, company_id)
    return _sanitize(lime_explain.explain_local(model, df))


# ---------------------------------------------------------------------------
# Natural-language explanation
# ---------------------------------------------------------------------------
@router.get("/explanation/{company_id}")
def text_explanation(
    company_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _, df = _load_df(db, company_id, user)
    ratio_result = ratios.compute_ratios(df)
    pred = prediction.predict(df, company_id, 3)
    anom = anomaly_service.detect(df)
    return _sanitize(explanation_text.explain_prediction(ratio_result, pred, anom))


# ---------------------------------------------------------------------------
# Excel report download
# ---------------------------------------------------------------------------
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
    anom = anomaly_service.detect(df)
    recs = recommendation.build_recommendations(
        ratio_result, anom, pred["predicted_values"]
    )

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
        headers={
            "Content-Disposition": f"attachment; filename=finsight_report_{company_id}.xlsx"
        },
    )