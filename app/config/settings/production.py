"""
Production environment settings.
"""

import os
from .base_settings import BaseAppSettings


class ProductionSettings(BaseAppSettings):
    """Production environment configuration."""

    debug: bool = False
    environment: str = "production"

    # Stricter logging in production
    log_level: str = "WARNING"

    # Database configuration for Render
    database_host: str = os.getenv("DATABASE_HOST", "localhost")
    database_port: int = int(os.getenv("DATABASE_PORT", "3306"))
    database_user: str = os.getenv("DATABASE_USER", "root")
    database_password: str = os.getenv("DATABASE_PASSWORD", "")
    database_name: str = os.getenv("DATABASE_NAME", "restaurant_dp2")

    @property
    def database_url(self) -> str:
        """Database connection URL for production."""
        return f"mysql+aiomysql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    # Production CORS settings
    allowed_origins: list = [
        "https://your-frontend.vercel.app",
        "https://your-frontend.netlify.app",
        "http://localhost:3000",  # For development
    ]

    # Server configuration
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", "8000"))

    class Config:
        env_file = ".env"