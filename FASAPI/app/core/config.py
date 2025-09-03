"""
Application configuration settings.
"""
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Restaurant Platform API"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: Optional[PostgresDsn] = None
    DATABASE_TEST_URL: str = "sqlite+aiosqlite:///./test.db"
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str]) -> Any:
        if isinstance(v, str):
            return v
        # For Pydantic v2, we'll use a simple string format since PostgresDsn.build is deprecated
        return "postgresql+asyncpg://postgres:password@localhost:5432/restaurant_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 3600
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # External Integrations
    SCRAPING_USER_AGENT: str = "RestaurantPlatform/1.0"
    SCRAPING_DELAY_MIN: int = 1
    SCRAPING_DELAY_MAX: int = 3
    RPA_HEADLESS: bool = True
    RPA_TIMEOUT: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Jobs/Scheduler
    SCHEDULER_ENABLED: bool = True
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }


settings = Settings()