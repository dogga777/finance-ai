import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.company import Company
from app.models.report import Report
from app.models.statement import FinancialStatement
from app.models.user import User
from app.services import (anomaly, prediction as prediction_service, preprocessing,
                         ratios, recommendation, reporting, scoring)

router = APIRouter(prefix="/reports", tags=["Reports"])


def _build(db: Session, company: Company) -> dict:
    rows = (db.query(FinancialStatement)
            .filter(FinancialStatement.company_id == company.id)
            .order_by(FinancialStatement.period).all())
    if not rows:
        raise HTTPException(status_code=400, detail="No statements found")

    df = preprocessing.statements_to_df(rows)
    ratio_result = ratios.compute_ratios(df)
    score = scoring.financial_health_score(ratio_result)

    if len(df) >= 6:
        pred = prediction_service.predict(df, company.id, horizon=3)
    else:
        pred = {"predicted_values": [], "confidence": 0.0, "model_name": "n/a"}

    anomalies = anomaly.detect(df)
    recs = recommendation.build_recommendations(ratio_result, anomalies, pred["predicted_values"])

    summary = {
        "ratios": ratio_result,
        "score": score,
        "predictions": pred,
        "anomalies": anomalies,
        "recommendations": recs,
    }

    db.add(Report(
        company_id=company.id,
        financial_health_score=score["score"],
        risk_level=score["risk_level"],
        summary_json=json.dumps(summary),
    ))
    db.commit()
    return summary


@router.get("/{company_id}")
def get_report(company_id: int, db: Session = Depends(get_db),
               user: User = Depends(get_current_user)):
    c = db.query(Company).filter(Company.id == company_id, Company.owner_id == user.id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")
    return _build(db, c)


@router.get("/{company_id}/pdf")
def get_pdf(company_id: int, db: Session = Depends(get_db),
            user: User = Depends(get_current_user)):
    c = db.query(Company).filter(Company.id == company_id, Company.owner_id == user.id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")

    summary = _build(db, c)
    pdf_bytes = reporting.build_pdf(summary, c.name)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=finsight_report_{company_id}.pdf"},
    )
