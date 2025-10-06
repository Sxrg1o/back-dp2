"""
Global fixtures for all tests.
"""

import pytest
import asyncio
import httpx
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.main import app
from src.core.database import get_database_session as get_db, DatabaseManager
from src.models.base_model import BaseModel as Base

# Database fixtures for integration tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db_manager():
    """Crea un DatabaseManager para pruebas usando una base de datos en memoria."""

    # Creamos una clase que hereda de DatabaseManager para tests
    class TestDatabaseManager(DatabaseManager):
        def __new__(cls):
            # Aseguramos que siempre se cree una nueva instancia para tests
            return super(DatabaseManager, cls).__new__(cls)

        def __init__(self):
            # Configuramos la base de datos en memoria para tests
            self._engine = create_async_engine(
                TEST_DATABASE_URL, echo=False, future=True
            )

            # Session factory para tests
            self._session_factory = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )

            self._initialized = True

    # Creamos una instancia del manejador de BD para tests
    test_db = TestDatabaseManager()

    # Importamos los modelos para registrarlos con Base
    from src.models.auth.rol_model import RolModel  # noqa: F401

    # Creamos las tablas
    async with test_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield test_db

    # Limpiamos después de los tests
    async with test_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_db.close()


@pytest.fixture
async def db_session(test_db_manager):
    """Crea una sesión de base de datos para pruebas de integración."""
    async with test_db_manager.session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def override_get_db(db_session):
    """Proporciona una dependencia de DB para inyección."""

    async def _get_db():
        try:
            yield db_session
        finally:
            pass

    return _get_db


@pytest.fixture
def test_client():
    """Fixture para TestClient de FastAPI"""
    return TestClient(app)


@pytest.fixture
async def async_client(override_get_db):
    """Cliente async para pruebas de integración."""
    app.dependency_overrides[get_db] = override_get_db
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides = {}


@pytest.fixture
def mock_db_session():
    """Fixture para mock de sesión de BD (sync)"""
    mock_session = MagicMock()
    return mock_session


@pytest.fixture
def async_mock_db_session():
    """Fixture para mock de sesión de BD (async)"""
    mock_session = AsyncMock()
    return mock_session


@pytest.fixture
def cleanup_app():
    """Limpia dependency_overrides después de cada test"""
    yield
    app.dependency_overrides = {}
