from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.company import Company
from app.models.statement import FinancialStatement
from app.models.user import User
from app.services import preprocessing, ratios, scoring

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get("/{company_id}")
def analyze(company_id: int, db: Session = Depends(get_db),
            user: User = Depends(get_current_user)):
    c = db.query(Company).filter(Company.id == company_id, Company.owner_id == user.id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")

    rows = (db.query(FinancialStatement)
            .filter(FinancialStatement.company_id == company_id)
            .order_by(FinancialStatement.period).all())
    if not rows:
        raise HTTPException(status_code=400, detail="No statements uploaded yet")

    df = preprocessing.statements_to_df(rows)
    ratio_result = ratios.compute_ratios(df)
    score = scoring.financial_health_score(ratio_result)
    return {"company_id": company_id, "ratios": ratio_result, "score": score}
