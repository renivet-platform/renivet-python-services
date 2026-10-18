import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.settings import AppSettings
from app.main import create_app


def test_local_settings_have_safe_defaults() -> None:
    settings = AppSettings(_env_file=None)
    assert settings.environment == "local"
    assert settings.service_name == "renivet-python-services"


def test_invalid_environment_is_rejected() -> None:
    with pytest.raises(ValidationError, match="environment"):
        AppSettings(_env_file=None, environment="pr0duction")


def test_invalid_service_name_is_rejected() -> None:
    for invalid in ("", "Team Name", "bad/name"):
        with pytest.raises(ValidationError, match="service_name"):
            AppSettings(_env_file=None, service_name=invalid)


def test_environment_variables_are_loaded_and_validated(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RENIVET_ENVIRONMENT", "staging")
    settings = AppSettings(_env_file=None)
    assert settings.environment == "staging"
    monkeypatch.setenv("RENIVET_ENVIRONMENT", "invalid")
    with pytest.raises(ValidationError, match="environment"):
        create_app()


@pytest.mark.parametrize("environment", ["staging", "production"])
def test_deployment_hides_api_documentation(environment: str) -> None:
    settings = AppSettings(_env_file=None, environment=environment)
    client = TestClient(create_app(settings))
    assert client.get("/health").status_code == 200
    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404
    assert client.get("/openapi.json").status_code == 404
    assert client.get("/api/v1/recommendations").status_code == 404


def test_local_environment_retains_development_documentation() -> None:
    client = TestClient(create_app(AppSettings(_env_file=None, environment="local")))
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200
