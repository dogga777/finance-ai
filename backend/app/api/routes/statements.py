from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.company import Company
from app.models.statement import FinancialStatement
from app.models.user import User
from app.schemas.statement import BulkStatementIn, StatementOut

router = APIRouter(prefix="/statements", tags=["Statements"])


def _owned(db: Session, company_id: int, user: User) -> Company:
    c = db.query(Company).filter(Company.id == company_id, Company.owner_id == user.id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")
    return c


@router.post("/{company_id}/bulk", response_model=List[StatementOut])
def bulk_upload(company_id: int, payload: BulkStatementIn,
                db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _owned(db, company_id, user)
    created = []
    for row in payload.statements:
        stmt = FinancialStatement(company_id=company_id, **row.model_dump())
        db.add(stmt)
        created.append(stmt)
    db.commit()
    for s in created:
        db.refresh(s)
    return created


@router.get("/{company_id}", response_model=List[StatementOut])
def list_statements(company_id: int, db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    _owned(db, company_id, user)
    return (db.query(FinancialStatement)
            .filter(FinancialStatement.company_id == company_id)
            .order_by(FinancialStatement.period).all())
