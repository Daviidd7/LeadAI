from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file():
    """Return .env path only if it exists locally (development)."""
    env_path = ".env"
    return env_path if os.path.exists(env_path) else None


class Settings(BaseSettings):
    """Settings loaded from environment variables (Railway) or .env (development)."""
    
    model_config = SettingsConfigDict(
        # Only load .env in development (when file exists locally)
        env_file=get_env_file(),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,  # Match SECRET_KEY to secret_key, etc.
    )

    # Application
    app_env: str = Field(default="development")
    app_name: str = Field(default="AI Lead Qualifier")
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    # Required - MUST be provided via environment or .env
    secret_key: str
    admin_username: str
    admin_password: str
    database_url: str
    openai_api_key: str
    openai_model: str = Field(default="gpt-4o-mini")

    # SMTP
    smtp_host: str
    smtp_port: int = Field(default=587)
    smtp_username: str
    smtp_password: str
    smtp_from_email: str
    lead_notification_email: str

    # Twilio (Optional)
    twilio_account_sid: Optional[str] = Field(default=None)
    twilio_auth_token: Optional[str] = Field(default=None)
    twilio_from_number: Optional[str] = Field(default=None)
    twilio_sales_number: Optional[str] = Field(default=None)

    # CRM (Optional)
    crm_base_url: Optional[str] = Field(default=None)
    crm_api_key: Optional[str] = Field(default=None)
    crm_pipeline_id: Optional[str] = Field(default=None)

    # Rate Limiting
    rate_limit_requests_per_minute: int = Field(default=30)


@lru_cache
def get_settings() -> Settings:
    return Settings()