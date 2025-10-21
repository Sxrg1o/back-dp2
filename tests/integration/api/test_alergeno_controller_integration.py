"""
Pruebas de integración para los endpoints de alérgenos.
"""

import pytest
from ulid import ULID
from src.models.menu.alergeno_model import AlergenoModel
from src.repositories.menu.alergeno_repository import AlergenoRepository
from src.core.enums.alergeno_enums import NivelRiesgo


@pytest.mark.asyncio
async def test_create_alergeno_integration(async_client, db_session):
    """
    Prueba de integración para la creación de alérgenos.
    
    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La sesión de base de datos (db_session) debe estar disponible y en estado limpio
        - La API y repositorios deben estar funcionando correctamente

    PROCESO:
        - Envía una solicitud POST real al endpoint.
        - Verifica la respuesta completa y el estado de la base de datos.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 201 (Created)
        - Los datos devueltos deben coincidir con los enviados
        - El alérgeno debe estar persistido en la base de datos y ser recuperable
    """
    # Arrange
    alergeno_data = {
        "nombre": "Test Integration Alergeno",
        "descripcion": "Alérgeno para pruebas de integración",
        "icono": "🧪",
        "nivel_riesgo": "medio",
    }

    # Act
    response = await async_client.post("/api/v1/alergenos", json=alergeno_data)

    # Assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["nombre"] == alergeno_data["nombre"]
    assert response_data["descripcion"] == alergeno_data["descripcion"]
    assert response_data["icono"] == alergeno_data["icono"]
    assert response_data["nivel_riesgo"] == alergeno_data["nivel_riesgo"]
    assert "id" in response_data
    assert response_data["activo"] is True

    # Verify in database
    repo = AlergenoRepository(db_session)
    alergeno = await repo.get_by_id(response_data["id"])
    assert alergeno is not None
    assert alergeno.nombre == alergeno_data["nombre"]


@pytest.mark.asyncio
async def test_create_alergeno_duplicate_integration(async_client, db_session):
    """
    Prueba de integración para la creación de alérgenos con nombre duplicado.

    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La sesión de base de datos (db_session) debe estar disponible y en estado limpio
        - El modelo AlergenoModel debe ser accesible para crear registros directamente

    PROCESO:
        - Inserta un alérgeno directamente en la base de datos.
        - Intenta crear un alérgeno con el mismo nombre vía API.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 409 (Conflict)
        - El mensaje de error debe indicar la duplicidad del alérgeno
        - No se debe crear un segundo alérgeno con el mismo nombre en la base de datos
    """
    # Arrange - Create an alergeno directly in DB
    alergeno_nombre = "Test Duplicate Alergeno"
    test_alergeno = AlergenoModel(
        nombre=alergeno_nombre, 
        descripcion="Alérgeno existente para prueba",
        nivel_riesgo=NivelRiesgo.MEDIO
    )
    db_session.add(test_alergeno)
    await db_session.commit()

    # Intentar crear un alérgeno con el mismo nombre
    alergeno_data = {
        "nombre": alergeno_nombre, 
        "descripcion": "Intento de alérgeno duplicado",
        "nivel_riesgo": "alto"
    }

    # Act
    response = await async_client.post("/api/v1/alergenos", json=alergeno_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un alérgeno" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_alergeno_by_id_integration(async_client, db_session):
    """
    Prueba de integración para obtener un alérgeno por su ID.

    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La sesión de base de datos (db_session) debe estar disponible y en estado limpio
        - El modelo AlergenoModel debe ser accesible para crear registros directamente

    PROCESO:
        - Inserta un alérgeno directamente en la base de datos.
        - Solicita el alérgeno por su ID vía API.
        - Verifica la respuesta completa.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 200 (OK)
        - Los datos devueltos deben coincidir con los del alérgeno creado
        - Todos los campos esperados deben estar presentes en la respuesta
    """
    # Arrange - Create an alergeno directly in DB
    test_alergeno = AlergenoModel(
        nombre="Test Get Alergeno", 
        descripcion="Alérgeno para prueba de obtención",
        icono="🔍",
        nivel_riesgo=NivelRiesgo.BAJO
    )
    db_session.add(test_alergeno)
    await db_session.commit()
    await db_session.refresh(test_alergeno)

    # Act
    response = await async_client.get(f"/api/v1/alergenos/{test_alergeno.id}")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == str(test_alergeno.id)
    assert response_data["nombre"] == test_alergeno.nombre
    assert response_data["descripcion"] == test_alergeno.descripcion
    assert response_data["icono"] == test_alergeno.icono
    assert response_data["nivel_riesgo"] == test_alergeno.nivel_riesgo.value


@pytest.mark.asyncio
async def test_get_alergeno_by_id_not_found_integration(async_client):
    """
    Prueba de integración para obtener un alérgeno que no existe.

    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La biblioteca uuid debe estar disponible para generar un ID aleatorio

    PROCESO:
        - Solicita un alérgeno con ID inexistente.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 404 (Not Found)
        - El mensaje de error debe indicar que no se encontró el alérgeno
    """
    # Arrange
    non_existent_id = str(str(ULID()))

    # Act
    response = await async_client.get(f"/api/v1/alergenos/{non_existent_id}")

    # Assert
    assert response.status_code == 404
    # El mensaje de error puede variar según la implementación
    error_detail = response.json().get("detail", "")
    assert (
        "no se encontró" in error_detail.lower() or "not found" in error_detail.lower()
    )


@pytest.mark.asyncio
async def test_list_alergenos_integration(async_client, db_session):
    """
    Prueba de integración para listar alérgenos con paginación.

    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La sesión de base de datos (db_session) debe estar disponible y en estado limpio
        - El modelo AlergenoModel debe ser accesible para crear registros directamente

    PROCESO:
        - Inserta varios alérgenos directamente en la base de datos.
        - Solicita la lista paginada vía API.
        - Verifica la respuesta completa incluyendo metadatos de paginación.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 200 (OK)
        - La respuesta debe incluir una lista de alérgenos y el contador total
        - La paginación debe funcionar correctamente limitando los resultados
    """
    # Arrange - Create multiple alergenos
    alergenos = [
        AlergenoModel(
            nombre=f"Test List Alergeno {i}", 
            descripcion=f"Descripción {i}",
            icono=f"🔢{i}",
            nivel_riesgo=NivelRiesgo.MEDIO
        )
        for i in range(5)
    ]
    for alergeno in alergenos:
        db_session.add(alergeno)
    await db_session.commit()

    # Act - Get first page with limit 3
    response = await async_client.get("/api/v1/alergenos?skip=0&limit=3")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert "items" in response_data
    assert len(response_data["items"]) <= 3  # Puede haber menos de 5 si hay otros alérgenos
    assert response_data["total"] >= 5  # Debe haber al menos 5


@pytest.mark.asyncio
async def test_update_alergeno_integration(async_client, db_session):
    """
    Prueba de integración para actualizar un alérgeno.

    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La sesión de base de datos (db_session) debe estar disponible y en estado limpio
        - El modelo AlergenoModel debe ser accesible para crear registros directamente

    PROCESO:
        - Inserta un alérgeno directamente en la base de datos.
        - Actualiza el alérgeno vía API.
        - Verifica la respuesta y el estado actualizado en la base de datos.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 200 (OK)
        - Los datos devueltos deben reflejar los cambios realizados
        - El alérgeno debe estar actualizado en la base de datos con los nuevos valores
    """
    # Arrange - Create an alergeno directly in DB
    test_alergeno = AlergenoModel(
        nombre="Test Update Alergeno", 
        descripcion="Descripción original",
        icono="📝",
        nivel_riesgo=NivelRiesgo.MEDIO
    )
    db_session.add(test_alergeno)
    await db_session.commit()
    await db_session.refresh(test_alergeno)

    update_data = {
        "nombre": "Test Updated Alergeno",
        "descripcion": "Descripción actualizada",
        "icono": "✅",
        "nivel_riesgo": "alto",
    }

    # Act
    response = await async_client.put(f"/api/v1/alergenos/{test_alergeno.id}", json=update_data)

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["nombre"] == update_data["nombre"]
    assert response_data["descripcion"] == update_data["descripcion"]
    assert response_data["icono"] == update_data["icono"]
    assert response_data["nivel_riesgo"] == update_data["nivel_riesgo"]

    # Verify in database
    await db_session.refresh(test_alergeno)
    assert test_alergeno.nombre == update_data["nombre"]
    assert test_alergeno.descripcion == update_data["descripcion"]
    assert test_alergeno.icono == update_data["icono"]
    assert test_alergeno.nivel_riesgo.value == update_data["nivel_riesgo"]


@pytest.mark.asyncio
async def test_update_alergeno_not_found_integration(async_client):
    """
    Prueba de integración para actualizar un alérgeno que no existe.

    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La biblioteca uuid debe estar disponible para generar un ID aleatorio

    PROCESO:
        - Intenta actualizar un alérgeno con ID inexistente.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 404 (Not Found)
        - El mensaje de error debe indicar que no se encontró el alérgeno
    """
    # Arrange
    non_existent_id = str(str(ULID()))
    update_data = {"nombre": "Alérgeno Inexistente"}

    # Act
    response = await async_client.put(
        f"/api/v1/alergenos/{non_existent_id}", json=update_data
    )

    # Assert
    assert response.status_code == 404
    # El mensaje de error puede variar según la implementación
    error_detail = response.json().get("detail", "")
    assert (
        "no se encontró" in error_detail.lower() or "not found" in error_detail.lower()
    )


@pytest.mark.asyncio
async def test_update_alergeno_duplicate_integration(async_client, db_session):
    """
    Prueba de integración para actualizar un alérgeno con nombre duplicado.

    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La sesión de base de datos (db_session) debe estar disponible y en estado limpio
        - El modelo AlergenoModel debe ser accesible para crear registros directamente

    PROCESO:
        - Inserta dos alérgenos directamente en la base de datos.
        - Intenta actualizar un alérgeno para tener el mismo nombre que el otro.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 409 (Conflict)
        - El mensaje de error debe indicar la duplicidad del nombre
        - El alérgeno no debe ser actualizado con el nombre duplicado
    """
    # Arrange - Create two alergenos
    alergeno1 = AlergenoModel(
        nombre="Alérgeno Uno", 
        descripcion="Descripción uno",
        nivel_riesgo=NivelRiesgo.BAJO
    )
    alergeno2 = AlergenoModel(
        nombre="Alérgeno Dos", 
        descripcion="Descripción dos",
        nivel_riesgo=NivelRiesgo.MEDIO
    )
    db_session.add(alergeno1)
    db_session.add(alergeno2)
    await db_session.commit()
    await db_session.refresh(alergeno1)
    await db_session.refresh(alergeno2)

    # Intentar actualizar alergeno2 para tener el mismo nombre que alergeno1
    update_data = {"nombre": "Alérgeno Uno"}

    # Act
    response = await async_client.put(f"/api/v1/alergenos/{alergeno2.id}", json=update_data)

    # Assert
    assert response.status_code == 409
    assert "Ya existe un alérgeno" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_alergeno_integration(async_client, db_session):
    """
    Prueba de integración para eliminar un alérgeno.

    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La sesión de base de datos (db_session) debe estar disponible y en estado limpio
        - El modelo AlergenoModel debe ser accesible para crear registros directamente

    PROCESO:
        - Inserta un alérgeno directamente en la base de datos.
        - Elimina el alérgeno vía API.
        - Verifica la respuesta y que el alérgeno ya no exista en la base de datos.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 204 (No Content)
        - La respuesta no debe tener contenido
        - El alérgeno no debe existir en la base de datos después de la eliminación
    """
    # Arrange - Create an alergeno directly in DB
    test_alergeno = AlergenoModel(
        nombre="Test Delete Alergeno", 
        descripcion="Alérgeno para eliminar",
        nivel_riesgo=NivelRiesgo.ALTO
    )
    db_session.add(test_alergeno)
    await db_session.commit()
    await db_session.refresh(test_alergeno)
    alergeno_id = test_alergeno.id

    # Act
    response = await async_client.delete(f"/api/v1/alergenos/{alergeno_id}")

    # Assert
    assert response.status_code == 204
    assert response.content == b""  # No content

    # Verify in database
    repo = AlergenoRepository(db_session)
    deleted_alergeno = await repo.get_by_id(alergeno_id)
    assert deleted_alergeno is None


@pytest.mark.asyncio
async def test_delete_alergeno_not_found_integration(async_client):
    """
    Prueba de integración para eliminar un alérgeno que no existe.

    PRECONDICIONES:
        - El cliente asincrónico (async_client) debe estar configurado
        - La biblioteca uuid debe estar disponible para generar un ID aleatorio

    PROCESO:
        - Intenta eliminar un alérgeno con ID inexistente.
        - Verifica que se retorne el código de error apropiado.
        
    POSTCONDICIONES:
        - La respuesta debe tener código HTTP 404 (Not Found)
        - El mensaje de error debe indicar que no se encontró el alérgeno
    """
    # Arrange
    non_existent_id = str(str(ULID()))

    # Act
    response = await async_client.delete(f"/api/v1/alergenos/{non_existent_id}")

    # Assert
    assert response.status_code == 404
    # El mensaje de error puede variar según la implementación
    error_detail = response.json().get("detail", "")
    assert (
        "no se encontró" in error_detail.lower() or "not found" in error_detail.lower()
    )
