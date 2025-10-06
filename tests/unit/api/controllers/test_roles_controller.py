"""
Pruebas unitarias para los endpoints de roles.
"""

import pytest
from unittest.mock import AsyncMock, patch
import uuid
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.controllers.roles_controller import router, get_database_session
from src.business_logic.auth.rol_service import RolService
from src.business_logic.exceptions.rol_exceptions import (
    RolNotFoundError,
    RolConflictError,
    RolValidationError,
)
from src.api.schemas.rol_schema import RolResponse, RolList

app = FastAPI()
app.include_router(router)

# Mock de sesión de base de datos para pruebas unitarias
@pytest.fixture
def mock_db_session_dependency():
    """
    Fixture que reemplaza la dependencia de la sesión de base de datos
    con un mock para evitar intentar conexiones reales durante pruebas unitarias
    """
    async def override_get_db():
        mock_session = AsyncMock()
        yield mock_session

    app.dependency_overrides[get_database_session] = override_get_db
    yield
    app.dependency_overrides.clear()

# Crear el cliente después de configurar las dependencias
client = TestClient(app)


@pytest.fixture
def mock_rol_service():
    """
    Fixture que proporciona un mock del servicio de roles.

    PROCESO:
        - Crea un mock del servicio para simular sus comportamientos.
        - Configura el parche para reemplazar la inicialización del servicio.

    POSTCONDICIONES:
        - El servicio está mockeado para todas las pruebas.
    """
    with patch("src.api.controllers.roles_controller.RolService") as mock:
        service_instance = AsyncMock(spec=RolService)
        mock.return_value = service_instance
        yield service_instance


@pytest.fixture
def sample_rol_id():
    """
    Fixture que proporciona un ID de rol de muestra.
    """
    return str(uuid.uuid4())


@pytest.fixture
def sample_rol_data():
    """
    Fixture que proporciona datos de muestra para un rol.
    """
    return {
        "id": str(uuid.uuid4()),
        "nombre": "Administrador",
        "descripcion": "Rol con permisos administrativos",
        "activo": True,
        "fecha_creacion": "2025-10-06T12:00:00",
        "fecha_modificacion": "2025-10-06T12:00:00",
    }


def test_create_rol_success(mock_db_session_dependency, mock_rol_service, sample_rol_data):
    """
    Prueba la creación exitosa de un rol.

    PROCESO:
        - Configura el mock para simular una creación exitosa.
        - Realiza una solicitud POST al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
    """
    # Arrange
    rol_data = {
        "nombre": "Administrador",
        "descripcion": "Rol con permisos administrativos",
    }
    mock_rol_service.create_rol.return_value = RolResponse(**sample_rol_data)

    # Act
    response = client.post("/roles", json=rol_data)

    # Assert
    assert response.status_code == 201
    assert response.json()["nombre"] == sample_rol_data["nombre"]
    assert response.json()["descripcion"] == sample_rol_data["descripcion"]
    mock_rol_service.create_rol.assert_awaited_once()


def test_create_rol_conflict(mock_db_session_dependency, mock_rol_service):
    """
    Prueba el manejo de errores al crear un rol con nombre duplicado.

    PROCESO:
        - Configura el mock para simular un error de conflicto.
        - Realiza una solicitud POST al endpoint.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange
    rol_data = {
        "nombre": "Administrador",
        "descripcion": "Rol con permisos administrativos",
    }
    mock_rol_service.create_rol.side_effect = RolConflictError(
        "Ya existe un rol con el nombre 'Administrador'"
    )

    # Act
    response = client.post("/roles", json=rol_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un rol" in response.json()["detail"]
    mock_rol_service.create_rol.assert_awaited_once()


def test_get_rol_success(mock_db_session_dependency, mock_rol_service, sample_rol_id, sample_rol_data):
    """
    Prueba la obtención exitosa de un rol por su ID.

    PROCESO:
        - Configura el mock para simular la existencia de un rol.
        - Realiza una solicitud GET al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
    """
    # Arrange
    mock_rol_service.get_rol_by_id.return_value = RolResponse(**sample_rol_data)

    # Act
    response = client.get(f"/roles/{sample_rol_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == sample_rol_data["id"]
    assert response.json()["nombre"] == sample_rol_data["nombre"]
    mock_rol_service.get_rol_by_id.assert_awaited_once()


def test_get_rol_not_found(mock_db_session_dependency, mock_rol_service, sample_rol_id):
    """
    Prueba el manejo de errores al buscar un rol que no existe.

    PROCESO:
        - Configura el mock para simular que el rol no existe.
        - Realiza una solicitud GET al endpoint.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange
    mock_rol_service.get_rol_by_id.side_effect = RolNotFoundError(
        f"No se encontró el rol con ID {sample_rol_id}"
    )

    # Act
    response = client.get(f"/roles/{sample_rol_id}")

    # Assert
    assert response.status_code == 404
    assert f"No se encontró el rol con ID {sample_rol_id}" in response.json()["detail"]
    mock_rol_service.get_rol_by_id.assert_awaited_once()


def test_list_roles_success(mock_db_session_dependency, mock_rol_service, sample_rol_data):
    """
    Prueba la obtención exitosa de una lista de roles.

    PROCESO:
        - Configura el mock para simular una lista de roles.
        - Realiza una solicitud GET al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
    """
    # Arrange
    rol_summary = {
        "id": sample_rol_data["id"],
        "nombre": sample_rol_data["nombre"],
        "activo": True,
    }
    rol_list = {"items": [rol_summary, rol_summary], "total": 2}
    mock_rol_service.get_roles.return_value = RolList(**rol_list)

    # Act
    response = client.get("/roles?skip=0&limit=10")

    # Assert
    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert len(response.json()["items"]) == 2
    mock_rol_service.get_roles.assert_awaited_once_with(0, 10)


def test_list_roles_validation_error(mock_db_session_dependency, mock_rol_service):
    """
    Prueba el manejo de errores de validación en los parámetros de paginación.

    PROCESO:
        - Configura el mock para simular un error de validación.
        - Realiza una solicitud GET al endpoint con parámetros inválidos.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange
    mock_rol_service.get_roles.side_effect = RolValidationError(
        "El parámetro 'limit' debe ser mayor a cero"
    )

    # Act
    response = client.get("/roles?skip=0&limit=0")

    # Assert
    # FastAPI valida automáticamente los parámetros y devuelve 422 para errores de validación
    assert response.status_code == 422
    # Verificamos que el error esté relacionado con el parámetro limit
    error_detail = response.json()["detail"]
    assert any("limit" in str(err).lower() for err in error_detail)
    # No debe llamar al servicio porque la validación falla antes
    mock_rol_service.get_roles.assert_not_called()


def test_update_rol_success(mock_db_session_dependency, mock_rol_service, sample_rol_id, sample_rol_data):
    """
    Prueba la actualización exitosa de un rol.

    PROCESO:
        - Configura el mock para simular una actualización exitosa.
        - Realiza una solicitud PUT al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
    """
    # Arrange
    update_data = {"nombre": "Administrador Actualizado"}
    updated_data = {**sample_rol_data, "nombre": "Administrador Actualizado"}
    mock_rol_service.update_rol.return_value = RolResponse(**updated_data)

    # Act
    response = client.put(f"/roles/{sample_rol_id}", json=update_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["nombre"] == "Administrador Actualizado"
    mock_rol_service.update_rol.assert_awaited_once()


def test_update_rol_not_found(mock_db_session_dependency, mock_rol_service, sample_rol_id):
    """
    Prueba el manejo de errores al actualizar un rol que no existe.

    PROCESO:
        - Configura el mock para simular que el rol no existe.
        - Realiza una solicitud PUT al endpoint.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange
    update_data = {"nombre": "Administrador Actualizado"}
    mock_rol_service.update_rol.side_effect = RolNotFoundError(
        f"No se encontró el rol con ID {sample_rol_id}"
    )

    # Act
    response = client.put(f"/roles/{sample_rol_id}", json=update_data)

    # Assert
    assert response.status_code == 404
    assert f"No se encontró el rol con ID {sample_rol_id}" in response.json()["detail"]
    mock_rol_service.update_rol.assert_awaited_once()


def test_update_rol_conflict(mock_db_session_dependency, mock_rol_service, sample_rol_id):
    """
    Prueba el manejo de errores al actualizar un rol con nombre duplicado.

    PROCESO:
        - Configura el mock para simular un error de conflicto.
        - Realiza una solicitud PUT al endpoint.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange
    update_data = {"nombre": "Otro Rol"}
    mock_rol_service.update_rol.side_effect = RolConflictError(
        "Ya existe un rol con el nombre 'Otro Rol'"
    )

    # Act
    response = client.put(f"/roles/{sample_rol_id}", json=update_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un rol" in response.json()["detail"]
    mock_rol_service.update_rol.assert_awaited_once()


def test_delete_rol_success(mock_db_session_dependency, mock_rol_service, sample_rol_id):
    """
    Prueba la eliminación exitosa de un rol.

    PROCESO:
        - Configura el mock para simular una eliminación exitosa.
        - Realiza una solicitud DELETE al endpoint.
        - Verifica que se retorne el código HTTP apropiado.
    """
    # Arrange
    mock_rol_service.delete_rol.return_value = True

    # Act
    response = client.delete(f"/roles/{sample_rol_id}")

    # Assert
    assert response.status_code == 204
    assert response.content == b""  # No content
    mock_rol_service.delete_rol.assert_awaited_once_with(uuid.UUID(sample_rol_id))


def test_delete_rol_not_found(mock_db_session_dependency, mock_rol_service, sample_rol_id):
    """
    Prueba el manejo de errores al eliminar un rol que no existe.

    PROCESO:
        - Configura el mock para simular que el rol no existe.
        - Realiza una solicitud DELETE al endpoint.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange
    mock_rol_service.delete_rol.side_effect = RolNotFoundError(
        f"No se encontró el rol con ID {sample_rol_id}"
    )

    # Act
    response = client.delete(f"/roles/{sample_rol_id}")

    # Assert
    assert response.status_code == 404
    assert f"No se encontró el rol con ID {sample_rol_id}" in response.json()["detail"]
    mock_rol_service.delete_rol.assert_awaited_once()
