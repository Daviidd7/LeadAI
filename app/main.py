from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.config import get_settings
from app.logging_config import configure_logging
from app.routers import leads as leads_router
from app.routers import web as web_router

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

# Force docs to be enabled at /docs and OpenAPI at /openapi.json
app = FastAPI(
    title=settings.app_name,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path("app/static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers (web has the HTML form, leads has the JSON API)
app.include_router(leads_router.router)
app.include_router(web_router.router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root() -> str:
    # Simple HTML so we know the app works even if templates break
    return "<html><body><h1>AI Lead Qualifier is running</h1><p>Go to <a href=\"/docs\">/docs</a> or <a href=\"/admin/login\">/admin/login</a>.</p></body></html>"


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}