from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_name: str = "AI Lead Qualifier"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    secret_key: str

    admin_username: str
    admin_password: str

    database_url: str

    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"

    smtp_host: str
    smtp_port: int = 587
    smtp_username: str
    smtp_password: str
    smtp_from_email: str
    lead_notification_email: str

    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_from_number: Optional[str] = None
    twilio_sales_number: Optional[str] = None

    crm_base_url: Optional[str] = None
    crm_api_key: Optional[str] = None
    crm_pipeline_id: Optional[str] = None

    rate_limit_requests_per_minute: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()