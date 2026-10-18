"""Validated non-secret runtime configuration for the private AI service."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Load RENIVET_-prefixed settings from the environment or ignored local .env."""

    model_config = SettingsConfigDict(
        env_prefix="RENIVET_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Literal["local", "development", "test", "staging", "production"] = "local"
    service_name: str = Field(
        default="renivet-python-services",
        min_length=1,
        max_length=64,
        pattern=r"^[a-z][a-z0-9-]*$",
    )
