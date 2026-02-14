from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Load .env file if it exists locally
if os.path.exists(".env"):
    load_dotenv(".env")


class Settings(BaseSettings):
    """Settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
    )

    # Application
    app_env: str = Field(default="development", validation_alias="APP_ENV")
    app_name: str = Field(default="AI Lead Qualifier", validation_alias="APP_NAME")
    app_host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
    app_port: int = Field(default=8000, validation_alias="APP_PORT")

    # Required
    secret_key: str = Field(validation_alias="SECRET_KEY")
    admin_username: str = Field(validation_alias="ADMIN_USERNAME")
    admin_password: str = Field(validation_alias="ADMIN_PASSWORD")
    database_url: str = Field(validation_alias="DATABASE_URL")
    openai_api_key: str = Field(validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", validation_alias="OPENAI_MODEL")

    # SMTP
    smtp_host: str = Field(validation_alias="SMTP_HOST")
    smtp_port: int = Field(default=587, validation_alias="SMTP_PORT")
    smtp_username: str = Field(validation_alias="SMTP_USERNAME")
    smtp_password: str = Field(validation_alias="SMTP_PASSWORD")
    smtp_from_email: str = Field(validation_alias="SMTP_FROM_EMAIL")
    lead_notification_email: str = Field(validation_alias="LEAD_NOTIFICATION_EMAIL")

    # Twilio (Optional)
    twilio_account_sid: Optional[str] = Field(default=None, validation_alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = Field(default=None, validation_alias="TWILIO_AUTH_TOKEN")
    twilio_from_number: Optional[str] = Field(default=None, validation_alias="TWILIO_FROM_NUMBER")
    twilio_sales_number: Optional[str] = Field(default=None, validation_alias="TWILIO_SALES_NUMBER")

    # CRM (Optional)
    crm_base_url: Optional[str] = Field(default=None, validation_alias="CRM_BASE_URL")
    crm_api_key: Optional[str] = Field(default=None, validation_alias="CRM_API_KEY")
    crm_pipeline_id: Optional[str] = Field(default=None, validation_alias="CRM_PIPELINE_ID")

    # Rate Limiting
    rate_limit_requests_per_minute: int = Field(default=30, validation_alias="RATE_LIMIT_REQUESTS_PER_MINUTE")


@lru_cache
def get_settings() -> Settings:
    return Settings()