"""Composition root: the ONLY place that wires concrete adapters to ports."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.application.use_cases.get_health import GetHealth
from app.infrastructure.config import Settings
from app.infrastructure.scale.factory import build_scale
from app.interfaces.api.router import router

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    app = FastAPI(title="CubitMat")

    app.state.settings = settings
    app.state.scale = build_scale(settings)  # used by future pour-detection use cases
    app.state.get_health = GetHealth(scale_driver=settings.scale_driver)

    app.include_router(router)
    # Mounted last so /api/* and /docs take precedence over static files.
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
    return app


app = create_app()
