"""
Configuration settings for the restaurant backend application.
Unified configuration file with support for different environments.
"""

import os
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment-specific configurations."""

    # Application info
    app_name: str = Field(default="Restaurant Backend API", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    app_description: str = Field(
        default="Sistema de gestión de restaurantes con arquitectura en capas",
        env="APP_DESCRIPTION"
    )
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="production", env="ENVIRONMENT")

    # Server configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")

    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_test_url: Optional[str] = Field(None, env="DATABASE_TEST_URL")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=30, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # CORS
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000"],
        env="ALLOWED_ORIGINS"
    )
    allowed_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH"],
        env="ALLOWED_METHODS"
    )
    allowed_headers: List[str] = Field(default=["*"], env="ALLOWED_HEADERS")

    # File uploads
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    upload_dir: str = Field(default="uploads", env="UPLOAD_DIR")
    allowed_extensions: List[str] = Field(
        default=["jpg", "jpeg", "png", "gif", "webp"],
        env="ALLOWED_EXTENSIONS"
    )

    # Email configuration (optional)
    smtp_host: Optional[str] = Field(None, env="SMTP_HOST")
    smtp_port: Optional[int] = Field(None, env="SMTP_PORT")
    smtp_user: Optional[str] = Field(None, env="SMTP_USER")
    smtp_password: Optional[str] = Field(None, env="SMTP_PASSWORD")
    email_from: Optional[str] = Field(None, env="EMAIL_FROM")

    # WebSocket
    ws_heartbeat_interval: int = Field(default=30, env="WS_HEARTBEAT_INTERVAL")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    # Pagination
    default_page_size: int = Field(default=20, env="DEFAULT_PAGE_SIZE")
    max_page_size: int = Field(default=100, env="MAX_PAGE_SIZE")

    @validator("allowed_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @validator("allowed_methods", pre=True)
    def parse_cors_methods(cls, v):
        """Parse CORS methods from string or list."""
        if isinstance(v, str):
            return [method.strip() for method in v.split(",")]
        return v

    @validator("allowed_headers", pre=True)
    def parse_cors_headers(cls, v):
        """Parse CORS headers from string or list."""
        if isinstance(v, str):
            return [header.strip() for header in v.split(",")]
        return v

    @validator("allowed_extensions", pre=True)
    def parse_allowed_extensions(cls, v):
        """Parse allowed file extensions from string or list."""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


# Singleton instance
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get or create the settings instance (singleton pattern).

    Returns:
        Settings instance
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
