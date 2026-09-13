import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.company import Company
from app.models.prediction import Prediction
from app.models.statement import FinancialStatement
from app.models.user import User
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services import prediction as prediction_service
from app.services import preprocessing

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("", response_model=PredictionResponse)
def predict(payload: PredictionRequest, db: Session = Depends(get_db),
            user: User = Depends(get_current_user)):
    c = db.query(Company).filter(Company.id == payload.company_id, Company.owner_id == user.id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")

    rows = (db.query(FinancialStatement)
            .filter(FinancialStatement.company_id == payload.company_id)
            .order_by(FinancialStatement.period).all())
    if len(rows) < 6:
        raise HTTPException(status_code=400, detail="At least 6 periods of statements required")

    df = preprocessing.statements_to_df(rows)
    result = prediction_service.predict(df, payload.company_id, payload.horizon)

    db.add(Prediction(
        company_id=payload.company_id,
        model_name=result["model_name"],
        horizon=payload.horizon,
        predicted_values=json.dumps(result["predicted_values"]),
        confidence=result["confidence"],
    ))
    db.commit()
    return result
