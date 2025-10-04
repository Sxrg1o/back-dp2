"""
Testing environment settings.
"""

from .base_settings import BaseAppSettings


class TestingSettings(BaseAppSettings):
    """Testing environment configuration."""

    debug: bool = True
    environment: str = "testing"

    # Use test database
    @property
    def database_url(self) -> str:
        """Return test database URL if available, otherwise use main URL with test suffix."""
        if self.database_test_url:
            return self.database_test_url
        # Fallback to test database name
        return self.database_url.replace("restaurant_db", "restaurant_test_db")

    # Disable external services during testing
    redis_url: str = "redis://localhost:6379/15"  # Use different Redis DB for tests

    # Faster token expiration for testing
    access_token_expire_minutes: int = 5

    # Simple logging for tests
    log_level: str = "ERROR"

    class Config:
        env_file = ".env.test"