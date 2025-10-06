"""
Pruebas de integración para los endpoints de roles.
"""

import pytest
import uuid

from src.models.auth.rol_model import RolModel
from src.repositories.auth.rol_repository import RolRepository


@pytest.mark.asyncio
async def test_create_rol_integration(async_client, db_session):
    """
    Prueba de integración para la creación de roles.

    PROCESO:
        - Envía una solicitud POST real al endpoint.
        - Verifica la respuesta completa y el estado de la base de datos.
    """
    # Arrange
    rol_data = {
        "nombre": "Test Integration Rol",
        "descripcion": "Rol para pruebas de integración",
    }

    # Act
    response = await async_client.post("/api/v1/roles", json=rol_data)

    # Assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["nombre"] == rol_data["nombre"]
    assert response_data["descripcion"] == rol_data["descripcion"]
    assert "id" in response_data
    assert response_data["activo"] is True

    # Verify in database
    repo = RolRepository(db_session)
    rol = await repo.get_by_id(uuid.UUID(response_data["id"]))
    assert rol is not None
    assert rol.nombre == rol_data["nombre"]


@pytest.mark.asyncio
async def test_create_rol_duplicate_integration(async_client, db_session):
    """
    Prueba de integración para la creación de roles con nombre duplicado.

    PROCESO:
        - Inserta un rol directamente en la base de datos.
        - Intenta crear un rol con el mismo nombre vía API.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange - Create a rol directly in DB
    rol_nombre = "Test Duplicate Rol"
    test_rol = RolModel(nombre=rol_nombre, descripcion="Rol existente para prueba")
    db_session.add(test_rol)
    await db_session.commit()

    # Intentar crear un rol con el mismo nombre
    rol_data = {"nombre": rol_nombre, "descripcion": "Intento de rol duplicado"}

    # Act
    response = await async_client.post("/api/v1/roles", json=rol_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un rol" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_rol_by_id_integration(async_client, db_session):
    """
    Prueba de integración para obtener un rol por su ID.

    PROCESO:
        - Inserta un rol directamente en la base de datos.
        - Solicita el rol por su ID vía API.
        - Verifica la respuesta completa.
    """
    # Arrange - Create a rol directly in DB
    test_rol = RolModel(
        nombre="Test Get Rol", descripcion="Rol para prueba de obtención"
    )
    db_session.add(test_rol)
    await db_session.commit()
    await db_session.refresh(test_rol)

    # Act
    response = await async_client.get(f"/api/v1/roles/{test_rol.id}")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == str(test_rol.id)
    assert response_data["nombre"] == test_rol.nombre
    assert response_data["descripcion"] == test_rol.descripcion


@pytest.mark.asyncio
async def test_get_rol_by_id_not_found_integration(async_client):
    """
    Prueba de integración para obtener un rol que no existe.

    PROCESO:
        - Solicita un rol con ID inexistente.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange
    non_existent_id = str(uuid.uuid4())

    # Act
    response = await async_client.get(f"/api/v1/roles/{non_existent_id}")

    # Assert
    assert response.status_code == 404
    # El mensaje de error puede variar según la implementación
    error_detail = response.json().get("detail", "")
    assert (
        "no se encontró" in error_detail.lower() or "not found" in error_detail.lower()
    )


@pytest.mark.asyncio
async def test_list_roles_integration(async_client, db_session):
    """
    Prueba de integración para listar roles con paginación.

    PROCESO:
        - Inserta varios roles directamente en la base de datos.
        - Solicita la lista paginada vía API.
        - Verifica la respuesta completa incluyendo metadatos de paginación.
    """
    # Arrange - Create multiple roles
    roles = [
        RolModel(nombre=f"Test List Rol {i}", descripcion=f"Descripción {i}")
        for i in range(5)
    ]
    for rol in roles:
        db_session.add(rol)
    await db_session.commit()

    # Act - Get first page with limit 3
    response = await async_client.get("/api/v1/roles?skip=0&limit=3")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert "items" in response_data
    assert len(response_data["items"]) <= 3  # Puede haber menos de 5 si hay otros roles
    assert response_data["total"] >= 5  # Debe haber al menos 5


@pytest.mark.asyncio
async def test_update_rol_integration(async_client, db_session):
    """
    Prueba de integración para actualizar un rol.

    PROCESO:
        - Inserta un rol directamente en la base de datos.
        - Actualiza el rol vía API.
        - Verifica la respuesta y el estado actualizado en la base de datos.
    """
    # Arrange - Create a rol directly in DB
    test_rol = RolModel(nombre="Test Update Rol", descripcion="Descripción original")
    db_session.add(test_rol)
    await db_session.commit()
    await db_session.refresh(test_rol)

    update_data = {
        "nombre": "Test Updated Rol",
        "descripcion": "Descripción actualizada",
    }

    # Act
    response = await async_client.put(f"/api/v1/roles/{test_rol.id}", json=update_data)

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["nombre"] == update_data["nombre"]
    assert response_data["descripcion"] == update_data["descripcion"]

    # Verify in database
    await db_session.refresh(test_rol)
    assert test_rol.nombre == update_data["nombre"]
    assert test_rol.descripcion == update_data["descripcion"]


@pytest.mark.asyncio
async def test_update_rol_not_found_integration(async_client):
    """
    Prueba de integración para actualizar un rol que no existe.

    PROCESO:
        - Intenta actualizar un rol con ID inexistente.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange
    non_existent_id = str(uuid.uuid4())
    update_data = {"nombre": "Rol Inexistente"}

    # Act
    response = await async_client.put(
        f"/api/v1/roles/{non_existent_id}", json=update_data
    )

    # Assert
    assert response.status_code == 404
    # El mensaje de error puede variar según la implementación
    error_detail = response.json().get("detail", "")
    assert (
        "no se encontró" in error_detail.lower() or "not found" in error_detail.lower()
    )


@pytest.mark.asyncio
async def test_update_rol_duplicate_integration(async_client, db_session):
    """
    Prueba de integración para actualizar un rol con nombre duplicado.

    PROCESO:
        - Inserta dos roles directamente en la base de datos.
        - Intenta actualizar un rol para tener el mismo nombre que el otro.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange - Create two roles
    rol1 = RolModel(nombre="Rol Uno", descripcion="Descripción uno")
    rol2 = RolModel(nombre="Rol Dos", descripcion="Descripción dos")
    db_session.add(rol1)
    db_session.add(rol2)
    await db_session.commit()
    await db_session.refresh(rol1)
    await db_session.refresh(rol2)

    # Intentar actualizar rol2 para tener el mismo nombre que rol1
    update_data = {"nombre": "Rol Uno"}

    # Act
    response = await async_client.put(f"/api/v1/roles/{rol2.id}", json=update_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un rol" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_rol_integration(async_client, db_session):
    """
    Prueba de integración para eliminar un rol.

    PROCESO:
        - Inserta un rol directamente en la base de datos.
        - Elimina el rol vía API.
        - Verifica la respuesta y que el rol ya no exista en la base de datos.
    """
    # Arrange - Create a rol directly in DB
    test_rol = RolModel(nombre="Test Delete Rol", descripcion="Rol para eliminar")
    db_session.add(test_rol)
    await db_session.commit()
    await db_session.refresh(test_rol)
    rol_id = test_rol.id

    # Act
    response = await async_client.delete(f"/api/v1/roles/{rol_id}")

    # Assert
    assert response.status_code == 204
    assert response.content == b""  # No content

    # Verify in database
    repo = RolRepository(db_session)
    deleted_rol = await repo.get_by_id(rol_id)
    assert deleted_rol is None


@pytest.mark.asyncio
async def test_delete_rol_not_found_integration(async_client):
    """
    Prueba de integración para eliminar un rol que no existe.

    PROCESO:
        - Intenta eliminar un rol con ID inexistente.
        - Verifica que se retorne el código de error apropiado.
    """
    # Arrange
    non_existent_id = str(uuid.uuid4())

    # Act
    response = await async_client.delete(f"/api/v1/roles/{non_existent_id}")

    # Assert
    assert response.status_code == 404
    # El mensaje de error puede variar según la implementación
    error_detail = response.json().get("detail", "")
    assert (
        "no se encontró" in error_detail.lower() or "not found" in error_detail.lower()
    )
