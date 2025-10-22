"""
Pruebas unitarias para los endpoints de alérgenos.
"""

import pytest
from unittest.mock import AsyncMock, patch
from ulid import ULID
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.controllers.alergeno_controller import router, get_database_session
from src.business_logic.menu.alergeno_service import AlergenoService
from src.business_logic.exceptions.alergeno_exceptions import (
    AlergenoNotFoundError,
    AlergenoConflictError,
    AlergenoValidationError,
)
from src.api.schemas.alergeno_schema import AlergenoResponse, AlergenoList
from src.core.enums.alergeno_enums import NivelRiesgo

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
def mock_alergeno_service():
    """
    Fixture que proporciona un mock del servicio de alérgenos.
    
    PRECONDICIONES:
        - La clase AlergenoService debe estar importada correctamente
    
    PROCESO:
        - Crea un patch del servicio de alérgenos
        - Configura el servicio mock con métodos asíncronos
    
    POSTCONDICIONES:
        - Devuelve una instancia mock de AlergenoService lista para usar en pruebas
        - El mock puede configurarse para simular diferentes comportamientos
    """
    with patch("src.api.controllers.alergeno_controller.AlergenoService") as mock:
        service_instance = AsyncMock(spec=AlergenoService)
        mock.return_value = service_instance
        yield service_instance


@pytest.fixture
def sample_alergeno_id():
    """
    Fixture que proporciona un ID de alérgeno de muestra.
    
    PRECONDICIONES:
        - La biblioteca uuid debe estar importada correctamente
    
    PROCESO:
        - Genera un UUID v4 único
        - Lo convierte a string para usarlo en las pruebas
    
    POSTCONDICIONES:
        - Devuelve un string con formato UUID válido para usar como ID de alérgeno
    """
    return str(str(ULID()))


@pytest.fixture
def sample_alergeno_data():
    """
    Fixture que proporciona datos de muestra para un alérgeno.
    
    PRECONDICIONES:
        - La biblioteca uuid debe estar importada correctamente
        - El enum NivelRiesgo debe estar disponible
    
    PROCESO:
        - Crea un diccionario con datos ficticios de un alérgeno
        - Incluye id, nombre, descripción, icono, nivel_riesgo, estado y fechas
    
    POSTCONDICIONES:
        - Devuelve un diccionario con todos los campos necesarios para un alérgeno
        - Los datos pueden ser usados para construir objetos AlergenoModel o AlergenoResponse
    """
    return {
        "id": str(str(ULID())),
        "nombre": "Gluten",
        "descripcion": "Proteína presente en cereales como trigo, cebada y centeno",
        "icono": "🌾",
        "nivel_riesgo": "alto",
        "activo": True,
        "fecha_creacion": "2025-10-06T12:00:00",
        "fecha_modificacion": "2025-10-06T12:00:00",
    }


def test_create_alergeno_success(
    test_client, mock_db_session_dependency, mock_alergeno_service, sample_alergeno_data
):
    """
    Prueba la creación exitosa de un alérgeno.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)
        - Los datos de muestra deben estar disponibles (sample_alergeno_data)

    PROCESO:
        - Configura el mock para simular una creación exitosa.
        - Realiza una solicitud POST al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 201 (Created)
        - Los datos devueltos deben coincidir con los proporcionados
        - El método create_alergeno del servicio debe haber sido llamado una vez
    """
    # Arrange
    alergeno_data = {
        "nombre": "Gluten",
        "descripcion": "Proteína presente en cereales como trigo, cebada y centeno",
        "icono": "🌾",
        "nivel_riesgo": "alto",
    }
    mock_alergeno_service.create_alergeno.return_value = AlergenoResponse(**sample_alergeno_data)

    # Act
    response = test_client.post("/api/v1/alergenos", json=alergeno_data)

    # Assert
    assert response.status_code == 201
    assert response.json()["nombre"] == sample_alergeno_data["nombre"]
    assert response.json()["descripcion"] == sample_alergeno_data["descripcion"]
    assert response.json()["icono"] == sample_alergeno_data["icono"]
    mock_alergeno_service.create_alergeno.assert_awaited_once()


def test_create_alergeno_conflict(test_client, mock_db_session_dependency, mock_alergeno_service):
    """
    Prueba el manejo de errores al crear un alérgeno con nombre duplicado.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)

    PROCESO:
        - Configura el mock para simular un error de conflicto.
        - Realiza una solicitud POST al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 409 (Conflict)
        - El mensaje de error debe indicar la duplicidad del alérgeno
        - El método create_alergeno del servicio debe haber sido llamado una vez
    """
    # Arrange
    alergeno_data = {
        "nombre": "Gluten",
        "descripcion": "Proteína presente en cereales",
        "icono": "🌾",
        "nivel_riesgo": "alto",
    }
    mock_alergeno_service.create_alergeno.side_effect = AlergenoConflictError(
        "Ya existe un alérgeno con el nombre 'Gluten'"
    )

    # Act
    response = test_client.post("/api/v1/alergenos", json=alergeno_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un alérgeno" in response.json()["detail"]
    mock_alergeno_service.create_alergeno.assert_awaited_once()


def test_get_alergeno_success(
    test_client,
    mock_db_session_dependency,
    mock_alergeno_service,
    sample_alergeno_id,
    sample_alergeno_data,
):
    """
    Prueba la obtención exitosa de un alérgeno por su ID.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)
        - Se debe tener un ID de alérgeno válido (sample_alergeno_id)
        - Los datos de muestra deben estar disponibles (sample_alergeno_data)

    PROCESO:
        - Configura el mock para simular la existencia de un alérgeno.
        - Realiza una solicitud GET al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 200 (OK)
        - Los datos devueltos deben coincidir con los esperados
        - El método get_alergeno_by_id del servicio debe haber sido llamado una vez
    """
    # Arrange
    mock_alergeno_service.get_alergeno_by_id.return_value = AlergenoResponse(**sample_alergeno_data)

    # Act
    response = test_client.get(f"/api/v1/alergenos/{sample_alergeno_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == sample_alergeno_data["id"]
    assert response.json()["nombre"] == sample_alergeno_data["nombre"]
    mock_alergeno_service.get_alergeno_by_id.assert_awaited_once()


def test_get_alergeno_not_found(
    test_client, mock_db_session_dependency, mock_alergeno_service, sample_alergeno_id
):
    """
    Prueba el manejo de errores al buscar un alérgeno que no existe.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)
        - Se debe tener un ID de alérgeno válido (sample_alergeno_id)

    PROCESO:
        - Configura el mock para simular que el alérgeno no existe.
        - Realiza una solicitud GET al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 404 (Not Found)
        - El mensaje de error debe indicar que no se encontró el alérgeno
        - El método get_alergeno_by_id del servicio debe haber sido llamado una vez
    """
    # Arrange
    mock_alergeno_service.get_alergeno_by_id.side_effect = AlergenoNotFoundError(
        f"No se encontró el alérgeno con ID {sample_alergeno_id}"
    )

    # Act
    response = test_client.get(f"/api/v1/alergenos/{sample_alergeno_id}")

    # Assert
    assert response.status_code == 404
    assert f"No se encontró el alérgeno con ID {sample_alergeno_id}" in response.json()["detail"]
    mock_alergeno_service.get_alergeno_by_id.assert_awaited_once()


def test_list_alergenos_success(
    test_client, mock_db_session_dependency, mock_alergeno_service, sample_alergeno_data
):
    """
    Prueba la obtención exitosa de una lista de alérgenos.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)
        - Los datos de muestra deben estar disponibles (sample_alergeno_data)

    PROCESO:
        - Configura el mock para simular una lista de alérgenos.
        - Realiza una solicitud GET al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 200 (OK)
        - La respuesta debe incluir una lista de alérgenos y el total
        - El método get_alergenos del servicio debe haber sido llamado con los parámetros correctos
    """
    # Arrange
    alergeno_summary = {
        "id": sample_alergeno_data["id"],
        "nombre": sample_alergeno_data["nombre"],
        "nivel_riesgo": sample_alergeno_data["nivel_riesgo"],
        "activo": True,
    }
    alergeno_list = {"items": [alergeno_summary, alergeno_summary], "total": 2}
    mock_alergeno_service.get_alergenos.return_value = AlergenoList(**alergeno_list)

    # Act
    response = test_client.get("/api/v1/alergenos?skip=0&limit=10")

    # Assert
    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert len(response.json()["items"]) == 2
    mock_alergeno_service.get_alergenos.assert_awaited_once_with(0, 10)


def test_list_alergenos_validation_error(
    test_client, mock_db_session_dependency, mock_alergeno_service
):
    """
    Prueba el manejo de errores de validación en los parámetros de paginación.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)

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
    mock_alergeno_service.get_alergenos.side_effect = AlergenoValidationError(
        "El parámetro 'limit' debe ser mayor a cero"
    )

    # Act
    response = test_client.get("/api/v1/alergenos?skip=0&limit=0")

    # Assert
    # FastAPI valida automáticamente los parámetros y devuelve 422 para errores de validación
    assert response.status_code == 422
    # Verificamos que el error esté relacionado con el parámetro limit
    error_detail = response.json()["detail"]
    assert any("limit" in str(err).lower() for err in error_detail)
    # No debe llamar al servicio porque la validación falla antes
    mock_alergeno_service.get_alergenos.assert_not_called()


def test_update_alergeno_success(
    test_client,
    mock_db_session_dependency,
    mock_alergeno_service,
    sample_alergeno_id,
    sample_alergeno_data,
):
    """
    Prueba la actualización exitosa de un alérgeno.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)
        - Se debe tener un ID de alérgeno válido (sample_alergeno_id)
        - Los datos de muestra deben estar disponibles (sample_alergeno_data)

    PROCESO:
        - Configura el mock para simular una actualización exitosa.
        - Realiza una solicitud PUT al endpoint.
        - Verifica la respuesta HTTP y los datos retornados.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 200 (OK)
        - Los datos devueltos deben reflejar los cambios realizados
        - El método update_alergeno del servicio debe haber sido llamado una vez
    """
    # Arrange
    update_data = {"nombre": "Gluten Actualizado", "nivel_riesgo": "critico"}
    updated_data = {**sample_alergeno_data, "nombre": "Gluten Actualizado", "nivel_riesgo": "critico"}
    mock_alergeno_service.update_alergeno.return_value = AlergenoResponse(**updated_data)

    # Act
    response = test_client.put(f"/api/v1/alergenos/{sample_alergeno_id}", json=update_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["nombre"] == "Gluten Actualizado"
    mock_alergeno_service.update_alergeno.assert_awaited_once()


def test_update_alergeno_not_found(
    test_client, mock_db_session_dependency, mock_alergeno_service, sample_alergeno_id
):
    """
    Prueba el manejo de errores al actualizar un alérgeno que no existe.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)
        - Se debe tener un ID de alérgeno válido (sample_alergeno_id)

    PROCESO:
        - Configura el mock para simular que el alérgeno no existe.
        - Realiza una solicitud PUT al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 404 (Not Found)
        - El mensaje de error debe indicar que no se encontró el alérgeno
        - El método update_alergeno del servicio debe haber sido llamado una vez
    """
    # Arrange
    update_data = {"nombre": "Alérgeno Actualizado"}
    mock_alergeno_service.update_alergeno.side_effect = AlergenoNotFoundError(
        f"No se encontró el alérgeno con ID {sample_alergeno_id}"
    )

    # Act
    response = test_client.put(f"/api/v1/alergenos/{sample_alergeno_id}", json=update_data)

    # Assert
    assert response.status_code == 404
    assert f"No se encontró el alérgeno con ID {sample_alergeno_id}" in response.json()["detail"]
    mock_alergeno_service.update_alergeno.assert_awaited_once()


def test_update_alergeno_conflict(
    test_client, mock_db_session_dependency, mock_alergeno_service, sample_alergeno_id
):
    """
    Prueba el manejo de errores al actualizar un alérgeno con nombre duplicado.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)
        - Se debe tener un ID de alérgeno válido (sample_alergeno_id)

    PROCESO:
        - Configura el mock para simular un error de conflicto.
        - Realiza una solicitud PUT al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 409 (Conflict)
        - El mensaje de error debe indicar la duplicidad del nombre
        - El método update_alergeno del servicio debe haber sido llamado una vez
    """
    # Arrange
    update_data = {"nombre": "Otro Alérgeno"}
    mock_alergeno_service.update_alergeno.side_effect = AlergenoConflictError(
        "Ya existe un alérgeno con el nombre 'Otro Alérgeno'"
    )

    # Act
    response = test_client.put(f"/api/v1/alergenos/{sample_alergeno_id}", json=update_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un alérgeno" in response.json()["detail"]
    mock_alergeno_service.update_alergeno.assert_awaited_once()


def test_delete_alergeno_success(
    test_client, mock_db_session_dependency, mock_alergeno_service, sample_alergeno_id
):
    """
    Prueba la eliminación exitosa de un alérgeno.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)
        - Se debe tener un ID de alérgeno válido (sample_alergeno_id)

    PROCESO:
        - Configura el mock para simular una eliminación exitosa.
        - Realiza una solicitud DELETE al endpoint.
        - Verifica que se retorne el código HTTP apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 204 (No Content)
        - La respuesta no debe tener contenido
        - El método delete_alergeno del servicio debe haber sido llamado con el ID correcto
    """
    # Arrange
    mock_alergeno_service.delete_alergeno.return_value = True

    # Act
    response = test_client.delete(f"/api/v1/alergenos/{sample_alergeno_id}")

    # Assert
    assert response.status_code == 204
    assert response.content == b""  # No content
    mock_alergeno_service.delete_alergeno.assert_awaited_once_with(sample_alergeno_id)


def test_delete_alergeno_not_found(
    test_client, mock_db_session_dependency, mock_alergeno_service, sample_alergeno_id
):
    """
    Prueba el manejo de errores al eliminar un alérgeno que no existe.

    PRECONDICIONES:
        - El cliente de prueba (test_client) debe estar configurado
        - El servicio de alérgenos debe estar mockeado (mock_alergeno_service)
        - Se debe tener un ID de alérgeno válido (sample_alergeno_id)

    PROCESO:
        - Configura el mock para simular que el alérgeno no existe.
        - Realiza una solicitud DELETE al endpoint.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 404 (Not Found)
        - El mensaje de error debe indicar que no se encontró el alérgeno
        - El método delete_alergeno del servicio debe haber sido llamado una vez
    """
    # Arrange
    mock_alergeno_service.delete_alergeno.side_effect = AlergenoNotFoundError(
        f"No se encontró el alérgeno con ID {sample_alergeno_id}"
    )

    # Act
    response = test_client.delete(f"/api/v1/alergenos/{sample_alergeno_id}")

    # Assert
    assert response.status_code == 404
    assert f"No se encontró el alérgeno con ID {sample_alergeno_id}" in response.json()["detail"]
    mock_alergeno_service.delete_alergeno.assert_awaited_once()
