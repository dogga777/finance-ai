from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    advanced,
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
    advanced.router,
    auth.router,
    companies.router,
    statements.router,
    analysis.router,
    predictions.router,
    anomalies.router,
    reports.router,
]:
    app.include_router(_router, prefix=settings.API_V1_PREFIX)
