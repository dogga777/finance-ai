from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    industry: str = "General"
    currency: str = "USD"


class CompanyOut(CompanyCreate):
    id: int

    class Config:
        from_attributes = True
