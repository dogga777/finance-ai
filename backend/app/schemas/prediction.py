from typing import List
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    company_id: int
    horizon: int = 3


class PredictionResponse(BaseModel):
    predicted_values: List[float]
    confidence: float
    model_name: str
