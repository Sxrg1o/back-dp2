"""
Production environment settings.
"""

from .base_settings import BaseAppSettings


class ProductionSettings(BaseAppSettings):
    """Production environment configuration."""

    debug: bool = False
    environment: str = "production"

    # Stricter logging in production
    log_level: str = "WARNING"

    # More restrictive CORS in production
    # Override these with proper domains in your .env file

    class Config:
        env_file = ".env"