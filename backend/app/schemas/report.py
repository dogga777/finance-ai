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
