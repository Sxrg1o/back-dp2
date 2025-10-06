"""
Unit tests for RolesController
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.main import app
from src.business_logic.auth.rol_service import RolService
from src.core.database import get_database_session


# Cliente de prueba
client = TestClient(app)


def test_create_rol_success(cleanup_app):
    """
    Verifica que POST /api/v1/roles/ crea un rol correctamente.
    """
    # Mock del servicio
    mock_service = AsyncMock()
    mock_service.create_rol = AsyncMock(return_value=type('Rol', (), {
        'id_rol': 1,
        'nombre': 'Admin',
        'descripcion': 'Administrador del sistema',
        'activo': True
    })())

    # Override del servicio
    with patch('src.api.controllers.roles_controller.rol_service', mock_service):
        # Mock de la sesión de BD
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.post("/api/v1/roles/", json={
            "nombre": "Admin",
            "descripcion": "Administrador del sistema"
        })

        # Verificar
        assert response.status_code == 201
        # El servicio fue llamado
        mock_service.create_rol.assert_called_once()


def test_create_rol_validation_error(cleanup_app):
    """
    Verifica que POST /api/v1/roles/ retorna 400 con error de validación.
    """
    from src.business_logic.exceptions.base_exceptions import ValidationError

    # Mock del servicio que lanza ValidationError
    mock_service = AsyncMock()
    mock_service.create_rol = AsyncMock(
        side_effect=ValidationError("Role name is required")
    )

    with patch('src.api.controllers.roles_controller.rol_service', mock_service):
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.post("/api/v1/roles/", json={
            "nombre": "",
            "descripcion": "Test"
        })

        # Verificar
        assert response.status_code == 400


def test_get_rol_by_id_success(cleanup_app):
    """
    Verifica que GET /api/v1/roles/{id} obtiene un rol correctamente.
    """
    # Mock del servicio
    mock_service = AsyncMock()
    mock_service.get_rol_by_id = AsyncMock(return_value=type('Rol', (), {
        'id_rol': 1,
        'nombre': 'Mesero',
        'descripcion': 'Personal de servicio',
        'activo': True
    })())

    with patch('src.api.controllers.roles_controller.rol_service', mock_service):
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.get("/api/v1/roles/1")

        # Verificar
        assert response.status_code == 200
        mock_service.get_rol_by_id.assert_called_once()


def test_get_rol_by_id_not_found(cleanup_app):
    """
    Verifica que GET /api/v1/roles/{id} retorna 404 si no existe.
    """
    from src.business_logic.exceptions.base_exceptions import NotFoundError

    # Mock del servicio que lanza NotFoundError
    mock_service = AsyncMock()
    mock_service.get_rol_by_id = AsyncMock(
        side_effect=NotFoundError("Rol not found")
    )

    with patch('src.api.controllers.roles_controller.rol_service', mock_service):
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.get("/api/v1/roles/999")

        # Verificar
        assert response.status_code == 404


def test_get_all_roles(cleanup_app):
    """
    Verifica que GET /api/v1/roles/ lista todos los roles.
    """
    # Mock del servicio
    mock_service = AsyncMock()
    mock_service.get_all_roles = AsyncMock(return_value=[
        type('Rol', (), {'id_rol': 1, 'nombre': 'Admin', 'activo': True})(),
        type('Rol', (), {'id_rol': 2, 'nombre': 'Mesero', 'activo': True})(),
    ])

    with patch('src.api.controllers.roles_controller.rol_service', mock_service):
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.get("/api/v1/roles/")

        # Verificar
        assert response.status_code == 200
        # Verificar que se llamó al servicio
        mock_service.get_all_roles.assert_called_once()
