from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.company import Company
from app.models.statement import FinancialStatement
from app.models.user import User
from app.services import anomaly, preprocessing

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])


@router.get("/{company_id}")
def detect(company_id: int, db: Session = Depends(get_db),
           user: User = Depends(get_current_user)):
    c = db.query(Company).filter(Company.id == company_id, Company.owner_id == user.id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")

    rows = (db.query(FinancialStatement)
            .filter(FinancialStatement.company_id == company_id)
            .order_by(FinancialStatement.period).all())
    df = preprocessing.statements_to_df(rows)
    return anomaly.detect(df)
