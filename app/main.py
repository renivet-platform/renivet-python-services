from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.v1.router import router as v1_router
from app.core.settings import AppSettings


def create_app(settings: AppSettings | None = None) -> FastAPI:
    """Validate configuration at startup without initializing external AI providers."""
    configuration = settings if settings is not None else AppSettings()
    is_deployment = configuration.environment in {"staging", "production"}
    application = FastAPI(
        title="Renivet Private AI Services",
        version="0.1.0",
        # Do not publish API discovery endpoints on staged/production instances.
        docs_url=None if is_deployment else "/docs",
        redoc_url=None if is_deployment else "/redoc",
        openapi_url=None if is_deployment else "/openapi.json",
    )
    application.state.settings = configuration
    application.include_router(health_router)
    application.include_router(v1_router)
    return application


app = create_app()
