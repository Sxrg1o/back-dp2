"""
Global fixtures for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from src.main import app


@pytest.fixture
def test_client():
    """Fixture para TestClient de FastAPI"""
    return TestClient(app)


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
