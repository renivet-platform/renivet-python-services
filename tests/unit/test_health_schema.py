from app.schemas.health import HealthResponse


def test_health_schema_round_trip() -> None:
    response = HealthResponse(status="ok", service="renivet-python-services")
    assert response.model_dump() == {
        "status": "ok",
        "service": "renivet-python-services",
    }
