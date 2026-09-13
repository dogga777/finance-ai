from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FinancialStatement(Base):
    __tablename__ = "financial_statements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    period: Mapped[str] = mapped_column(String(16), index=True)
    revenue: Mapped[float] = mapped_column(Float, default=0)
    expenses: Mapped[float] = mapped_column(Float, default=0)
    assets: Mapped[float] = mapped_column(Float, default=0)
    liabilities: Mapped[float] = mapped_column(Float, default=0)
    equity: Mapped[float] = mapped_column(Float, default=0)
    inventory: Mapped[float] = mapped_column(Float, default=0)
    operating_cash_flow: Mapped[float] = mapped_column(Float, default=0)
    investing_cash_flow: Mapped[float] = mapped_column(Float, default=0)
    financing_cash_flow: Mapped[float] = mapped_column(Float, default=0)
    net_profit: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="statements")
