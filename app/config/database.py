"""
Database configuration and connection management.
"""

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config.settings.base_settings import BaseAppSettings

# Create declarative base for all models
Base = declarative_base()

# Global variables for database connection
engine = None
AsyncSessionLocal = None


def get_settings() -> BaseAppSettings:
    """Get settings based on environment."""
    environment = os.getenv("ENVIRONMENT", "development")

    if environment == "development":
        from app.config.settings.development import DevelopmentSettings
        return DevelopmentSettings()
    elif environment == "production":
        from app.config.settings.production import ProductionSettings
        return ProductionSettings()
    elif environment == "testing":
        from app.config.settings.testing import TestingSettings
        return TestingSettings()
    else:
        from app.config.settings.development import DevelopmentSettings
        return DevelopmentSettings()


def init_database():
    """Initialize database connection."""
    global engine, AsyncSessionLocal

    settings = get_settings()

    # Create async engine
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,  # Log SQL queries in debug mode
        pool_pre_ping=True,   # Enable pessimistic disconnect handling
        pool_size=10,         # Connection pool size
        max_overflow=20,      # Max overflow connections
    )

    # Create async session factory
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.

    Yields:
        AsyncSession: Database session
    """
    if AsyncSessionLocal is None:
        init_database()

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables():
    """Create all database tables."""
    if engine is None:
        init_database()

    # Import all models to ensure they are registered
    from app.data.models.auth.usuario_model import UsuarioModel  # noqa: F401
    from app.data.models.auth.rol_model import RolModel  # noqa: F401
    from app.data.models.menu.alergeno_model import AlergenoModel  # noqa: F401
    from app.data.models.menu.categoria_model import CategoriaModel  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Drop all database tables (useful for testing)."""
    if engine is None:
        init_database()

    # Import all models to ensure they are registered
    from app.data.models.auth.usuario_model import UsuarioModel  # noqa: F401
    from app.data.models.auth.rol_model import RolModel  # noqa: F401
    from app.data.models.menu.alergeno_model import AlergenoModel  # noqa: F401
    from app.data.models.menu.categoria_model import CategoriaModel  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def close_database():
    """Close database connection."""
    global engine
    if engine:
        await engine.dispose()
        engine = None