from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.v1.router import router as v1_router


def create_app() -> FastAPI:
    """Assemble HTTP adapters without initializing external AI providers."""
    application = FastAPI(title="Renivet Private AI Services", version="0.1.0")
    application.include_router(health_router)
    application.include_router(v1_router)
    return application


app = create_app()
