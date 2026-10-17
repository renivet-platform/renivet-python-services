from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Typed non-secret service configuration; no credentials at this stage."""

    model_config = SettingsConfigDict(env_prefix="RENIVET_", extra="ignore")

    environment: str = "local"
    service_name: str = "renivet-python-services"
