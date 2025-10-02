"""
Configuración global de pytest para todos los tests del proyecto.
"""
import pytest
import sys
import os
from typing import Generator
from fastapi.testclient import TestClient

# Agregar el directorio raíz al path para importar la app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

# Configuración global de pytest
pytest_plugins = []

def pytest_configure(config):
    """Configuración inicial de pytest"""
    config.addinivalue_line(
        "markers", "unit: marca tests unitarios"
    )
    config.addinivalue_line(
        "markers", "integration: marca tests de integración"
    )
    config.addinivalue_line(
        "markers", "api: marca tests de API endpoints"
    )
    config.addinivalue_line(
        "markers", "slow: marca tests que tardan más tiempo"
    )

@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """
    Fixture global para el cliente de prueba de FastAPI.
    Se crea una vez por sesión de tests.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def fresh_client() -> Generator[TestClient, None, None]:
    """
    Fixture para un cliente de prueba fresco en cada test.
    Útil para tests que necesitan estado limpio.
    """
    with TestClient(app) as test_client:
        yield test_client

# Configuración de logging para tests
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pytest_collection_modifyitems(config, items):
    """
    Modifica la colección de items de pytest.
    Aquí se pueden agregar marcadores automáticos basados en el nombre del archivo.
    """
    for item in items:
        # Marcar automáticamente tests de API
        if "test_" in item.name and "api" in item.nodeid:
            item.add_marker(pytest.mark.api)
        
        # Marcar tests lentos basados en el nombre
        if "integration" in item.name or "e2e" in item.name:
            item.add_marker(pytest.mark.slow)
