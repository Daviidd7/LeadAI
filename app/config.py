from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from environment variables (Railway) or .env (development)."""
    
    model_config = SettingsConfigDict(
        # Only load .env in development (when file exists locally)
        env_file=".env" if os.path.exists(".env") else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_env: str = Field(default="development")
    app_name: str = Field(default="AI Lead Qualifier")
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    # Required
    secret_key: str = Field(...)
    admin_username: str = Field(...)
    admin_password: str = Field(...)
    database_url: str = Field(...)
    openai_api_key: str = Field(...)
    openai_model: str = Field(default="gpt-4o-mini")

    # SMTP
    smtp_host: str = Field(...)
    smtp_port: int = Field(default=587)
    smtp_username: str = Field(...)
    smtp_password: str = Field(...)
    smtp_from_email: str = Field(...)
    lead_notification_email: str = Field(...)

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

    @model_validator(mode="before")
    @classmethod
    def load_from_env(cls, data):
        """Explicitly load all environment variables."""
        if not isinstance(data, dict):
            data = {}
        
        # Map environment variable names to field names
        env_mapping = {
            "APP_ENV": "app_env",
            "APP_NAME": "app_name",
            "APP_HOST": "app_host",
            "APP_PORT": "app_port",
            "SECRET_KEY": "secret_key",
            "ADMIN_USERNAME": "admin_username",
            "ADMIN_PASSWORD": "admin_password",
            "DATABASE_URL": "database_url",
            "OPENAI_API_KEY": "openai_api_key",
            "OPENAI_MODEL": "openai_model",
            "SMTP_HOST": "smtp_host",
            "SMTP_PORT": "smtp_port",
            "SMTP_USERNAME": "smtp_username",
            "SMTP_PASSWORD": "smtp_password",
            "SMTP_FROM_EMAIL": "smtp_from_email",
            "LEAD_NOTIFICATION_EMAIL": "lead_notification_email",
            "TWILIO_ACCOUNT_SID": "twilio_account_sid",
            "TWILIO_AUTH_TOKEN": "twilio_auth_token",
            "TWILIO_FROM_NUMBER": "twilio_from_number",
            "TWILIO_SALES_NUMBER": "twilio_sales_number",
            "CRM_BASE_URL": "crm_base_url",
            "CRM_API_KEY": "crm_api_key",
            "CRM_PIPELINE_ID": "crm_pipeline_id",
            "RATE_LIMIT_REQUESTS_PER_MINUTE": "rate_limit_requests_per_minute",
        }
        
        # Read from environment variables and populate data
        for env_name, field_name in env_mapping.items():
            env_value = os.getenv(env_name)
            if env_value is not None:
                data[field_name] = env_value
        
        return data


@lru_cache
def get_settings() -> Settings:
    return Settings()