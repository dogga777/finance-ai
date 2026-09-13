"""Bootstrap script — writes all FinSight AI backend files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FILES = {}

# ---------------- app/__init__.py ----------------
FILES["app/__init__.py"] = ""

# ---------------- app/main.py ----------------
FILES["app/main.py"] = '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    analysis, anomalies, auth, companies, health, predictions, reports, statements
)
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"app": settings.APP_NAME, "status": "running"}


for _router in [
    health.router,
    auth.router,
    companies.router,
    statements.router,
    analysis.router,
    predictions.router,
    anomalies.router,
    reports.router,
]:
    app.include_router(_router, prefix=settings.API_V1_PREFIX)
'''

# ---------------- app/core ----------------
FILES["app/core/__init__.py"] = ""

FILES["app/core/config.py"] = '''
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FinSight AI"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "change-this-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DATABASE_URL: str = "sqlite:///./finsight.db"
    MODEL_DIR: str = "./app/ml/artifacts"
    UPLOAD_DIR: str = "./uploads"
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
'''

FILES["app/core/security.py"] = '''
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload.get("sub")
    except JWTError:
        return None
'''

FILES["app/core/logging.py"] = "import logging\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger('finsight')\n"

# ---------------- app/db ----------------
FILES["app/db/__init__.py"] = ""

FILES["app/db/base.py"] = '''
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
'''

FILES["app/db/session.py"] = '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
'''

FILES["app/db/init_db.py"] = '''
from app.db.base import Base
from app.db.session import engine

# Register models
from app.models import user, company, statement, prediction, anomaly, report  # noqa


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
'''

# ---------------- app/models ----------------
FILES["app/models/__init__.py"] = ""

FILES["app/models/user.py"] = '''
from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="analyst")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    companies = relationship("Company", back_populates="owner", cascade="all, delete")
'''

FILES["app/models/company.py"] = '''
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    industry: Mapped[str] = mapped_column(String(128), default="General")
    currency: Mapped[str] = mapped_column(String(8), default="USD")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="companies")
    statements = relationship(
        "FinancialStatement", back_populates="company", cascade="all, delete"
    )
'''

FILES["app/models/statement.py"] = '''
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
'''

FILES["app/models/prediction.py"] = '''
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    model_name: Mapped[str] = mapped_column(String(64))
    horizon: Mapped[int] = mapped_column(Integer, default=3)
    predicted_values: Mapped[str] = mapped_column(String(1024))
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
'''

FILES["app/models/anomaly.py"] = '''
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Anomaly(Base):
    __tablename__ = "anomalies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    statement_id: Mapped[int] = mapped_column(ForeignKey("financial_statements.id"))
    score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_level: Mapped[str] = mapped_column(String(16), default="Low")
    reason: Mapped[str] = mapped_column(String(512), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
'''

FILES["app/models/report.py"] = '''
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    financial_health_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_level: Mapped[str] = mapped_column(String(16), default="Low")
    summary_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
'''

# ---------------- app/schemas ----------------
FILES["app/schemas/__init__.py"] = ""

FILES["app/schemas/auth.py"] = '''
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
'''

FILES["app/schemas/user.py"] = '''
from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

    class Config:
        from_attributes = True
'''

FILES["app/schemas/company.py"] = '''
from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    industry: str = "General"
    currency: str = "USD"


class CompanyOut(CompanyCreate):
    id: int

    class Config:
        from_attributes = True
'''

FILES["app/schemas/statement.py"] = '''
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
'''

FILES["app/schemas/prediction.py"] = '''
from typing import List
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    company_id: int
    horizon: int = 3


class PredictionResponse(BaseModel):
    predicted_values: List[float]
    confidence: float
    model_name: str
'''

FILES["app/schemas/report.py"] = '''
from typing import Any, Dict, List
from pydantic import BaseModel


class ReportResponse(BaseModel):
    company_id: int
    financial_health_score: float
    risk_level: str
    ratios: Dict[str, Any]
    predictions: List[float]
    anomalies: List[Dict[str, Any]]
    recommendations: List[str]
'''

# ---------------- app/services ----------------
FILES["app/services/__init__.py"] = ""

FILES["app/services/preprocessing.py"] = '''
import pandas as pd

NUMERIC_FIELDS = [
    "revenue",
    "expenses",
    "assets",
    "liabilities",
    "equity",
    "inventory",
    "operating_cash_flow",
    "investing_cash_flow",
    "financing_cash_flow",
    "net_profit",
]


def statements_to_df(rows) -> pd.DataFrame:
    data = [
        {**{f: getattr(r, f, 0) for f in NUMERIC_FIELDS},
         "period": r.period,
         "id": getattr(r, "id", None)}
        for r in rows
    ]
    return clean_df(pd.DataFrame(data))


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates(subset=["period"]).sort_values("period").reset_index(drop=True)

    for col in NUMERIC_FIELDS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median()).fillna(0)

    return df
'''

FILES["app/services/ratios.py"] = '''
import pandas as pd


def _safe_div(a, b, default=0.0):
    try:
        if b in (0, None):
            return default
        return float(a) / float(b)
    except Exception:
        return default


def compute_ratios(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}

    latest = df.iloc[-1]

    revenue = latest.get("revenue", 0) or 0
    expenses = latest.get("expenses", 0) or 0
    assets = latest.get("assets", 0) or 0
    liabilities = latest.get("liabilities", 0) or 0
    equity = latest.get("equity", 0) or 0
    inventory = latest.get("inventory", 0) or 0
    net_profit = latest.get("net_profit", 0) or 0

    return {
        "current_ratio": round(_safe_div(assets, liabilities), 4),
        "quick_ratio": round(_safe_div(assets - inventory, liabilities), 4),
        "debt_ratio": round(_safe_div(liabilities, assets), 4),
        "roa": round(_safe_div(net_profit, assets), 4),
        "roe": round(_safe_div(net_profit, equity), 4),
        "gross_margin": round(_safe_div(revenue - expenses, revenue), 4),
        "net_profit_margin": round(_safe_div(net_profit, revenue), 4),
    }
'''

FILES["app/services/scoring.py"] = '''
def financial_health_score(ratios: dict) -> dict:
    if not ratios:
        return {"score": 0.0, "risk_level": "Unknown"}

    score = 0.0
    score += min(ratios.get("current_ratio", 0) / 2.0, 1) * 20
    score += min(ratios.get("quick_ratio", 0) / 1.5, 1) * 15
    score += max(0.0, 1 - ratios.get("debt_ratio", 1)) * 20
    score += min(max(ratios.get("roa", 0), 0) / 0.10, 1) * 15
    score += min(max(ratios.get("roe", 0), 0) / 0.15, 1) * 15
    score += min(max(ratios.get("net_profit_margin", 0), 0) / 0.20, 1) * 15

    score = round(min(score, 100), 2)

    if score >= 80:
        risk = "Low"
    elif score >= 60:
        risk = "Medium"
    else:
        risk = "High"

    return {"score": score, "risk_level": risk}
'''

FILES["app/services/prediction.py"] = '''
import os
from typing import List

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

from app.core.config import settings

FEATURES = [
    "revenue", "expenses", "assets", "liabilities",
    "equity", "inventory", "net_profit",
]
TARGET = "operating_cash_flow"


def _model_path(company_id: int) -> str:
    return f"{settings.MODEL_DIR}/cashflow_company_{company_id}.joblib"


def train(df: pd.DataFrame) -> RandomForestRegressor:
    df = df.sort_values("period").reset_index(drop=True)
    if len(df) < 6:
        raise ValueError("At least 6 periods of data are required for training.")

    X = df[FEATURES].shift(1).dropna()
    y = df[TARGET].iloc[1:]

    model = RandomForestRegressor(n_estimators=300, max_depth=8, random_state=42)
    model.fit(X, y)
    return model


def train_and_save(df: pd.DataFrame, company_id: int):
    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    model = train(df)
    joblib.dump(model, _model_path(company_id))
    return model


def load_model(company_id: int):
    try:
        return joblib.load(_model_path(company_id))
    except FileNotFoundError:
        return None


def predict(df: pd.DataFrame, company_id: int, horizon: int = 3) -> dict:
    model = load_model(company_id) or train_and_save(df, company_id)

    last = df.iloc[-1]
    current_row = last[FEATURES].to_dict()

    predictions: List[float] = []
    for _ in range(horizon):
        X_next = pd.DataFrame([current_row])
        y_next = float(model.predict(X_next)[0])
        predictions.append(round(y_next, 2))
        current_row = {**current_row, "net_profit": current_row.get("net_profit", 0) * 1.01}

    confidence = 0.85
    if len(df) >= 8:
        try:
            X = df[FEATURES].shift(1).dropna()
            y = df[TARGET].iloc[1:]
            r2 = r2_score(y, model.predict(X))
            confidence = round(max(0.0, min(1.0, (r2 + 1) / 2)), 2)
        except Exception:
            pass

    return {
        "predicted_values": predictions,
        "confidence": confidence,
        "model_name": "RandomForestRegressor",
    }
'''

FILES["app/services/anomaly.py"] = '''
import pandas as pd
from sklearn.ensemble import IsolationForest

FEATURES = ["revenue", "expenses", "operating_cash_flow", "net_profit"]


def detect(df: pd.DataFrame) -> dict:
    if len(df) < 4:
        return {"indices": [], "scores": [], "risk_level": "Low", "reasons": []}

    X = df[FEATURES].fillna(0)
    model = IsolationForest(contamination=0.15, random_state=42)
    labels = model.fit_predict(X)
    scores = model.decision_function(X)

    indices, reasons = [], []
    for i, (label, score) in enumerate(zip(labels, scores)):
        if label == -1:
            indices.append(i)
            reasons.append(f"Period {df.iloc[i]['period']} flagged (score={round(float(score), 3)})")

    if len(indices) > len(df) * 0.2:
        risk = "High"
    elif indices:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "indices": indices,
        "scores": [round(float(s), 4) for s in scores],
        "risk_level": risk,
        "reasons": reasons,
    }
'''

FILES["app/services/explainability.py"] = '''
import numpy as np
import pandas as pd
import shap


def explain(model, df: pd.DataFrame, features: list) -> dict:
    try:
        X = df[features].fillna(0)
        explainer = shap.Explainer(model, X)
        values = explainer(X)
        importance = np.abs(values.values).mean(axis=0)
        return {f: round(float(v), 4) for f, v in zip(features, importance)}
    except Exception as error:
        return {"error": str(error)}
'''

FILES["app/services/recommendation.py"] = '''
def build_recommendations(ratios: dict, anomalies: dict, predictions: list) -> list:
    recs = []

    if ratios.get("current_ratio", 1) < 1:
        recs.append("Increase short-term liquidity to cover current liabilities.")
    if ratios.get("debt_ratio", 0) > 0.6:
        recs.append("Reduce overall debt — solvency risk is elevated.")
    if ratios.get("net_profit_margin", 0) < 0.05:
        recs.append("Improve net profit margin by reviewing cost structure.")
    if ratios.get("roe", 0) < 0.08:
        recs.append("Enhance return on equity — consider capital efficiency.")
    if anomalies.get("risk_level") == "High":
        recs.append("Investigate abnormal transactions flagged by the anomaly engine.")
    if predictions and predictions[0] < 0:
        recs.append("Cash flow is projected negative — delay non-critical spending.")
    if not recs:
        recs.append("Financial position is stable. Continue monitoring.")

    return recs
'''

FILES["app/services/reporting.py"] = '''
import json
from typing import Any, Dict

from fpdf import FPDF


def build_summary_json(ratios, score, predictions, anomalies, recommendations) -> str:
    return json.dumps({
        "ratios": ratios,
        "score": score,
        "predictions": predictions,
        "anomalies": anomalies,
        "recommendations": recommendations,
    })


def build_pdf(summary: Dict[str, Any], company_name: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"FinSight AI Report - {company_name}", ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.ln(4)
    pdf.cell(0, 8, f"Health Score: {summary['score']['score']}/100", ln=True)
    pdf.cell(0, 8, f"Risk Level: {summary['score']['risk_level']}", ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Financial Ratios", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for k, v in summary["ratios"].items():
        pdf.cell(0, 7, f"{k}: {v}", ln=True)

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Cash Flow Forecast", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for i, v in enumerate(summary["predictions"]["predicted_values"], start=1):
        pdf.cell(0, 7, f"Period +{i}: {v}", ln=True)

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Recommendations", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for rec in summary["recommendations"]:
        pdf.multi_cell(0, 7, f"- {rec}")

    return bytes(pdf.output(dest="S").encode("latin-1"))
'''

# ---------------- app/api ----------------
FILES["app/api/__init__.py"] = ""

FILES["app/api/deps.py"] = '''
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    subject = decode_token(token)
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = db.query(User).filter(User.email == subject).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
'''

FILES["app/api/routes/__init__.py"] = ""

FILES["app/api/routes/health.py"] = '''
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {"status": "ok", "app": "FinSight AI"}
'''

FILES["app/api/routes/auth.py"] = '''
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(subject=user.email))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(subject=user.email))


@router.get("/me", response_model=UserOut)
def me(current: User = Depends(get_current_user)):
    return current
'''

FILES["app/api/routes/companies.py"] = '''
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyOut

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("", response_model=CompanyOut)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    company = Company(owner_id=user.id, **payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get("", response_model=List[CompanyOut])
def list_companies(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Company).filter(Company.owner_id == user.id).all()


@router.get("/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db),
                user: User = Depends(get_current_user)):
    c = db.query(Company).filter(Company.id == company_id, Company.owner_id == user.id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")
    return c
'''

FILES["app/api/routes/statements.py"] = '''
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
'''

FILES["app/api/routes/analysis.py"] = '''
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
'''

FILES["app/api/routes/predictions.py"] = '''
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
'''

FILES["app/api/routes/anomalies.py"] = '''
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
'''

FILES["app/api/routes/reports.py"] = '''
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
'''

# ---------------- app/ml ----------------
FILES["app/ml/__init__.py"] = ""
FILES["app/ml/artifacts/.gitkeep"] = ""

FILES["app/ml/synthetic.py"] = '''
import random


def generate_synthetic(periods: int = 36, base_revenue: float = 100000) -> list:
    rows = []
    revenue = base_revenue
    for i in range(periods):
        revenue *= 1 + random.uniform(-0.03, 0.06)
        expenses = revenue * random.uniform(0.6, 0.85)
        assets = revenue * random.uniform(3.5, 6.0)
        liabilities = assets * random.uniform(0.3, 0.55)
        equity = assets - liabilities
        inventory = assets * random.uniform(0.08, 0.18)
        net_profit = revenue - expenses
        operating_cf = net_profit * random.uniform(0.7, 1.2)
        year = 2022 + (i // 12)
        month = (i % 12) + 1
        rows.append({
            "period": f"{year}-{month:02d}",
            "revenue": round(revenue, 2),
            "expenses": round(expenses, 2),
            "assets": round(assets, 2),
            "liabilities": round(liabilities, 2),
            "equity": round(equity, 2),
            "inventory": round(inventory, 2),
            "operating_cash_flow": round(operating_cf, 2),
            "investing_cash_flow": round(-revenue * 0.03, 2),
            "financing_cash_flow": round(revenue * 0.02, 2),
            "net_profit": round(net_profit, 2),
        })
    return rows
'''

# ---------------- Write all files ----------------
def main():
    count = 0
    for rel_path, content in FILES.items():
        p = ROOT / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content.lstrip("\n"), encoding="utf-8")
        count += 1
        print(f"  created  {rel_path}")
    print(f"\nDone. {count} files written to {ROOT}")


if __name__ == "__main__":
    main()