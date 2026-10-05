import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import (
    advanced, analysis, anomalies, auth, companies, health, predictions, reports, statements,
)
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(title=settings.APP_NAME)

# CORS — kept for local dev + fallback
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://finsight-frontned.onrender.com",   # ← your real frontend URL
        "https://finsight-frontend-laxo.onrender.com",  # old URL (keep for safety)
        "*",   # wildcard - allows any origin
    ],
    allow_origin_regex=r"https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()


# ---------- API routes (must be registered BEFORE static files) ----------
for _router in [
    health.router,
    auth.router,
    companies.router,
    statements.router,
    analysis.router,
    predictions.router,
    anomalies.router,
    reports.router,
    advanced.router,
]:
    app.include_router(_router, prefix=settings.API_V1_PREFIX)


# ---------- Serve React build (if present) ----------
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend_dist"

if FRONTEND_DIR.exists():
    # Static assets (js, css, images)
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIR / "assets"),
        name="assets",
    )

    # Root + SPA fallback
    @app.get("/")
    def serve_root():
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        # Don't intercept API routes
        if full_path.startswith("api/") or full_path == "docs" or full_path.startswith("openapi"):
            return {"detail": "Not found"}

        # If a real file exists (favicon, manifest), serve it
        file_path = FRONTEND_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)

        # Otherwise, fall back to React's index.html
        return FileResponse(FRONTEND_DIR / "index.html")
else:
    @app.get("/")
    def root():
        return {"app": settings.APP_NAME, "status": "running", "note": "frontend not built"}