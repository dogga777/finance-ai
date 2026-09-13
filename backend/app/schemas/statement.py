from typing import List
from pydantic import BaseModel


class StatementIn(BaseModel):
    period: str
    revenue: float = 0
    expenses: float = 0
    assets: float = 0
    liabilities: float = 0
    equity: float = 0
    inventory: float = 0
    operating_cash_flow: float = 0
    investing_cash_flow: float = 0
    financing_cash_flow: float = 0
    net_profit: float = 0


class StatementOut(StatementIn):
    id: int

    class Config:
        from_attributes = True


class BulkStatementIn(BaseModel):
    statements: List[StatementIn]
