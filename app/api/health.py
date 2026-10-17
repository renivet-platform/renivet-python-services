from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness only; never implies model readiness or backend permissions."""
    return HealthResponse(status="ok", service="renivet-python-services")
