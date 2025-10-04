"""
Development environment settings.
"""

from .base_settings import BaseAppSettings


class DevelopmentSettings(BaseAppSettings):
    """Development environment configuration."""

    debug: bool = True
    environment: str = "development"

    # More verbose logging in development
    log_level: str = "DEBUG"

    # Allow all origins in development (be careful in production)
    allowed_origins: list = ["*"]

    # Database settings for development
    # The DATABASE_URL will be loaded from .env file

    class Config:
        env_file = ".env"