"""
Pruebas unitarias para los endpoints de roles.
"""

import pytest
from unittest.mock import AsyncMock, patch
from ulid import ULID
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.controllers.rol_controller import router, get_database_session
from src.business_logic.auth.rol_service import RolService
from src.business_logic.exceptions.rol_exceptions import (
    RolNotFoundError,
    RolConflictError,
    RolValidationError,
)
from src.api.schemas.rol_schema import RolResponse, RolList

app = FastAPI()
app.include_router(router)


# Mock de sesión de base de datos para pruebas unitarias usando el fixture global
@pytest.fixture
def mock_db_session_dependency(async_mock_db_session, cleanup_app):
    """
    Fixture que reemplaza la dependencia de la sesión de base de datos
    con un mock global de conftest.py para evitar conexiones reales durante pruebas unitarias
    
    PRECONDICIONES:
        - El fixture async_mock_db_session debe estar disponible en conftest.py
        - El fixture cleanup_app debe estar disponible para limpiar dependencias
    
    PROCESO:
        - Sobrescribe la dependencia get_database_session en la app de FastAPI
        - Configura una función asíncrona que devuelve el mock de sesión
    
    POSTCONDICIONES:
        - Las llamadas a get_database_session devolverán un mock en lugar de una conexión real
        - Las pruebas pueden ejecutarse sin depender de una base de datos real
    """

    async def override_get_db():
        yield async_mock_db_session

    app.dependency_overrides[get_database_session] = override_get_db


@pytest.fixture
def mock_rol_service():
    """
    Fixture que proporciona un mock del servicio de roles.
    
    PRECONDICIONES:
        - La clase RolService debe estar importada correctamente
    
    PROCESO:
        - Crea un patch del servicio de roles
        - Configura el servicio mock con métodos asíncronos
    
    POSTCONDICIONES:
        - Devuelve una instancia mock de RolService lista para usar en pruebas
        - El mock puede configurarse para simular diferentes comportamientos
    """
    with patch("src.api.controllers.rol_controller.RolService") as mock:
        service_instance = AsyncMock(spec=RolService)
        mock.return_value = service_instance
        yield service_instance


@pytest.fixture
def sample_rol_id():
    """
    Fixture que proporciona un ID de rol de muestra.
    
    PRECONDICIONES:
        - La biblioteca uuid debe estar importada correctamente
    
    PROCESO:
        - Genera un UUID v4 único
        - Lo convierte a string para usarlo en las pruebas
    
    POSTCONDICIONES:
        - Devuelve un string con formato UUID válido para usar como ID de rol
    """
    return str(str(ULID()))


@pytest.fixture
def sample_rol_data():
    """
    Fixture que proporciona datos de muestra para un rol.
    
    PRECONDICIONES:
        - La biblioteca uuid debe estar importada correctamente
    
    PROCESO:
        - Crea un diccionario con datos ficticios de un rol
        - Incluye id, nombre, descripción, estado y fechas
    
    POSTCONDICIONES:
        - Devuelve un diccionario con todos los campos necesarios para un rol
        - Los datos pueden ser usados para construir objetos RolModel o RolResponse
    """
    return {
        "id": str(str(ULID())),
        "nombre": "Administrador",
        "descripcion": "Rol con permisos administrativos",
        "activo": True,
        "fecha_creacion": "2025-10-06T12:00:00",
        "fecha_modificacion": "2025-10-06T12:00:00",
    }


def test_create_rol_success(
    test_client, mock_db_session_dependency, mock_rol_service, sample_rol_data
):
    """
    Prueba la creación exitosa de un rol.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)
        - Los datos de muestra deben estar disponibles (sample_rol_data)

    PROCESO:
        - Configura el mock para simular una creación exitosa.
        - Realiza una solicitud POST al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 201 (Created)
        - Los datos devueltos deben coincidir con los proporcionados
        - El método create_rol del servicio debe haber sido llamado una vez
    """
    # Arrange
    rol_data = {
        "nombre": "Administrador",
        "descripcion": "Rol con permisos administrativos",
    }
    mock_rol_service.create_rol.return_value = RolResponse(**sample_rol_data)

    # Act
    response = test_client.post("/api/v1/roles", json=rol_data)

    # Assert
    assert response.status_code == 201
    assert response.json()["nombre"] == sample_rol_data["nombre"]
    assert response.json()["descripcion"] == sample_rol_data["descripcion"]
    mock_rol_service.create_rol.assert_awaited_once()


def test_create_rol_conflict(test_client, mock_db_session_dependency, mock_rol_service):
    """
    Prueba el manejo de errores al crear un rol con nombre duplicado.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)

    PROCESO:
        - Configura el mock para simular un error de conflicto.
        - Realiza una solicitud POST al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 409 (Conflict)
        - El mensaje de error debe indicar la duplicidad del rol
        - El método create_rol del servicio debe haber sido llamado una vez
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
    response = test_client.post("/api/v1/roles", json=rol_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un rol" in response.json()["detail"]
    mock_rol_service.create_rol.assert_awaited_once()


def test_get_rol_success(
    test_client,
    mock_db_session_dependency,
    mock_rol_service,
    sample_rol_id,
    sample_rol_data,
):
    """
    Prueba la obtención exitosa de un rol por su ID.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)
        - Se debe tener un ID de rol válido (sample_rol_id)
        - Los datos de muestra deben estar disponibles (sample_rol_data)

    PROCESO:
        - Configura el mock para simular la existencia de un rol.
        - Realiza una solicitud GET al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 200 (OK)
        - Los datos devueltos deben coincidir con los esperados
        - El método get_rol_by_id del servicio debe haber sido llamado una vez
    """
    # Arrange
    mock_rol_service.get_rol_by_id.return_value = RolResponse(**sample_rol_data)

    # Act
    response = test_client.get(f"/api/v1/roles/{sample_rol_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == sample_rol_data["id"]
    assert response.json()["nombre"] == sample_rol_data["nombre"]
    mock_rol_service.get_rol_by_id.assert_awaited_once()


def test_get_rol_not_found(
    test_client, mock_db_session_dependency, mock_rol_service, sample_rol_id
):
    """
    Prueba el manejo de errores al buscar un rol que no existe.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)
        - Se debe tener un ID de rol válido (sample_rol_id)

    PROCESO:
        - Configura el mock para simular que el rol no existe.
        - Realiza una solicitud GET al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 404 (Not Found)
        - El mensaje de error debe indicar que no se encontró el rol
        - El método get_rol_by_id del servicio debe haber sido llamado una vez
    """
    # Arrange
    mock_rol_service.get_rol_by_id.side_effect = RolNotFoundError(
        f"No se encontró el rol con ID {sample_rol_id}"
    )

    # Act
    response = test_client.get(f"/api/v1/roles/{sample_rol_id}")

    # Assert
    assert response.status_code == 404
    assert f"No se encontró el rol con ID {sample_rol_id}" in response.json()["detail"]
    mock_rol_service.get_rol_by_id.assert_awaited_once()


def test_list_roles_success(
    test_client, mock_db_session_dependency, mock_rol_service, sample_rol_data
):
    """
    Prueba la obtención exitosa de una lista de roles.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)
        - Los datos de muestra deben estar disponibles (sample_rol_data)

    PROCESO:
        - Configura el mock para simular una lista de roles.
        - Realiza una solicitud GET al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 200 (OK)
        - La respuesta debe incluir una lista de roles y el total
        - El método get_roles del servicio debe haber sido llamado con los parámetros correctos
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
    response = test_client.get("/api/v1/roles?skip=0&limit=10")

    # Assert
    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert len(response.json()["items"]) == 2
    mock_rol_service.get_roles.assert_awaited_once_with(0, 10)


def test_list_roles_validation_error(
    test_client, mock_db_session_dependency, mock_rol_service
):
    """
    Prueba el manejo de errores de validación en los parámetros de paginación.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)

    PROCESO:
        - Configura el mock para simular un error de validación.
        - Realiza una solicitud GET al endpoint con parámetros inválidos.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 422 (Unprocessable Entity)
        - Los detalles del error deben mencionar el parámetro limit
        - El servicio no debe ser llamado debido a la validación de FastAPI
    """
    # Arrange
    mock_rol_service.get_roles.side_effect = RolValidationError(
        "El parámetro 'limit' debe ser mayor a cero"
    )

    # Act
    response = test_client.get("/api/v1/roles?skip=0&limit=0")

    # Assert
    # FastAPI valida automáticamente los parámetros y devuelve 422 para errores de validación
    assert response.status_code == 422
    # Verificamos que el error esté relacionado con el parámetro limit
    error_detail = response.json()["detail"]
    assert any("limit" in str(err).lower() for err in error_detail)
    # No debe llamar al servicio porque la validación falla antes
    mock_rol_service.get_roles.assert_not_called()


def test_update_rol_success(
    test_client,
    mock_db_session_dependency,
    mock_rol_service,
    sample_rol_id,
    sample_rol_data,
):
    """
    Prueba la actualización exitosa de un rol.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)
        - Se debe tener un ID de rol válido (sample_rol_id)
        - Los datos de muestra deben estar disponibles (sample_rol_data)

    PROCESO:
        - Configura el mock para simular una actualización exitosa.
        - Realiza una solicitud PUT al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 200 (OK)
        - Los datos devueltos deben reflejar los cambios realizados
        - El método update_rol del servicio debe haber sido llamado una vez
    """
    # Arrange
    update_data = {"nombre": "Administrador Actualizado"}
    updated_data = {**sample_rol_data, "nombre": "Administrador Actualizado"}
    mock_rol_service.update_rol.return_value = RolResponse(**updated_data)

    # Act
    response = test_client.put(f"/api/v1/roles/{sample_rol_id}", json=update_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["nombre"] == "Administrador Actualizado"
    mock_rol_service.update_rol.assert_awaited_once()


def test_update_rol_not_found(
    test_client, mock_db_session_dependency, mock_rol_service, sample_rol_id
):
    """
    Prueba el manejo de errores al actualizar un rol que no existe.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)
        - Se debe tener un ID de rol válido (sample_rol_id)

    PROCESO:
        - Configura el mock para simular que el rol no existe.
        - Realiza una solicitud PUT al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 404 (Not Found)
        - El mensaje de error debe indicar que no se encontró el rol
        - El método update_rol del servicio debe haber sido llamado una vez
    """
    # Arrange
    update_data = {"nombre": "Administrador Actualizado"}
    mock_rol_service.update_rol.side_effect = RolNotFoundError(
        f"No se encontró el rol con ID {sample_rol_id}"
    )

    # Act
    response = test_client.put(f"/api/v1/roles/{sample_rol_id}", json=update_data)

    # Assert
    assert response.status_code == 404
    assert f"No se encontró el rol con ID {sample_rol_id}" in response.json()["detail"]
    mock_rol_service.update_rol.assert_awaited_once()


def test_update_rol_conflict(
    test_client, mock_db_session_dependency, mock_rol_service, sample_rol_id
):
    """
    Prueba el manejo de errores al actualizar un rol con nombre duplicado.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)
        - Se debe tener un ID de rol válido (sample_rol_id)

    PROCESO:
        - Configura el mock para simular un error de conflicto.
        - Realiza una solicitud PUT al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 409 (Conflict)
        - El mensaje de error debe indicar la duplicidad del nombre
        - El método update_rol del servicio debe haber sido llamado una vez
    """
    # Arrange
    update_data = {"nombre": "Otro Rol"}
    mock_rol_service.update_rol.side_effect = RolConflictError(
        "Ya existe un rol con el nombre 'Otro Rol'"
    )

    # Act
    response = test_client.put(f"/api/v1/roles/{sample_rol_id}", json=update_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un rol" in response.json()["detail"]
    mock_rol_service.update_rol.assert_awaited_once()


def test_delete_rol_success(
    test_client, mock_db_session_dependency, mock_rol_service, sample_rol_id
):
    """
    Prueba la eliminación exitosa de un rol.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)
        - Se debe tener un ID de rol válido (sample_rol_id)

    PROCESO:
        - Configura el mock para simular una eliminación exitosa.
        - Realiza una solicitud DELETE al endpoint.
        - Verifica que se retorne el código HTTP apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 204 (No Content)
        - La respuesta no debe tener contenido
        - El método delete_rol del servicio debe haber sido llamado con el ID correcto
    """
    # Arrange
    mock_rol_service.delete_rol.return_value = True

    # Act
    response = test_client.delete(f"/api/v1/roles/{sample_rol_id}")

    # Assert
    assert response.status_code == 204
    assert response.content == b""  # No content
    mock_rol_service.delete_rol.assert_awaited_once_with(sample_rol_id)


def test_delete_rol_not_found(
    test_client, mock_db_session_dependency, mock_rol_service, sample_rol_id
):
    """
    Prueba el manejo de errores al eliminar un rol que no existe.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de roles debe estar mockeado (mock_rol_service)
        - Se debe tener un ID de rol válido (sample_rol_id)

    PROCESO:
        - Configura el mock para simular que el rol no existe.
        - Realiza una solicitud DELETE al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 404 (Not Found)
        - El mensaje de error debe indicar que no se encontró el rol
        - El método delete_rol del servicio debe haber sido llamado una vez
    """
    # Arrange
    mock_rol_service.delete_rol.side_effect = RolNotFoundError(
        f"No se encontró el rol con ID {sample_rol_id}"
    )

    # Act
    response = test_client.delete(f"/api/v1/roles/{sample_rol_id}")

    # Assert
    assert response.status_code == 404
    assert f"No se encontró el rol con ID {sample_rol_id}" in response.json()["detail"]
    mock_rol_service.delete_rol.assert_awaited_once()
