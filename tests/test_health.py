from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "renivet-python-services"}


def test_unapproved_inference_routes_are_absent() -> None:
    client = TestClient(app)
    assert client.get("/api/v1/recommendations").status_code == 404
    assert client.post("/api/v1/embeddings").status_code == 404


def test_openapi_exposes_health_but_no_inference() -> None:
    schema = TestClient(app).get("/openapi.json").json()
    assert "/health" in schema["paths"]
    assert "/api/v1/recommendations" not in schema["paths"]
