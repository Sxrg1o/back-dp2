"""
Pruebas unitarias para el servicio de alérgenos.
"""

import pytest
from unittest.mock import AsyncMock
from ulid import ULID
from datetime import datetime

from src.business_logic.menu.alergeno_service import AlergenoService
from src.models.menu.alergeno_model import AlergenoModel
from src.api.schemas.alergeno_schema import AlergenoCreate, AlergenoUpdate
from src.business_logic.exceptions.alergeno_exceptions import (
    AlergenoValidationError,
    AlergenoNotFoundError,
    AlergenoConflictError,
)
from src.core.enums.alergeno_enums import NivelRiesgo
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def mock_repository():
    """
    Fixture que proporciona un mock del repositorio de alérgenos.
    """
    repository = AsyncMock()
    return repository


@pytest.fixture
def alergeno_service(mock_repository):
    """
    Fixture que proporciona una instancia del servicio de alérgenos con un repositorio mockeado.
    """
    service = AlergenoService(AsyncMock())
    service.repository = mock_repository
    return service


@pytest.fixture
def sample_alergeno_data():
    """
    Fixture que proporciona datos de muestra para un alérgeno.
    """
    return {
        "id": str(ULID()),
        "nombre": "Test Alérgeno",
        "descripcion": "Alérgeno para pruebas",
        "icono": "🧪",
        "nivel_riesgo": NivelRiesgo.MEDIO,
        "activo": True,
        "fecha_creacion": datetime.now(),
        "fecha_modificacion": datetime.now(),
    }


@pytest.mark.asyncio
async def test_create_alergeno_success(alergeno_service, mock_repository, sample_alergeno_data):
    """
    Prueba la creación exitosa de un alérgeno.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una creación exitosa.
        - Llama al método create_alergeno con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe crear el alérgeno correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    alergeno_create = AlergenoCreate(
        nombre=sample_alergeno_data["nombre"],
        descripcion=sample_alergeno_data["descripcion"],
        icono=sample_alergeno_data["icono"],
        nivel_riesgo=sample_alergeno_data["nivel_riesgo"]
    )
    mock_repository.create.return_value = AlergenoModel(**sample_alergeno_data)

    # Act
    result = await alergeno_service.create_alergeno(alergeno_create)

    # Assert
    assert result.id == sample_alergeno_data["id"]
    assert result.nombre == sample_alergeno_data["nombre"]
    assert result.descripcion == sample_alergeno_data["descripcion"]
    assert result.icono == sample_alergeno_data["icono"]
    assert result.nivel_riesgo == sample_alergeno_data["nivel_riesgo"]
    mock_repository.create.assert_called_once()

    # Verificar que se pasó un objeto AlergenoModel al repositorio
    args, _ = mock_repository.create.call_args
    assert isinstance(args[0], AlergenoModel)
    assert args[0].nombre == sample_alergeno_data["nombre"]
    assert args[0].descripcion == sample_alergeno_data["descripcion"]
    assert args[0].icono == sample_alergeno_data["icono"]
    assert args[0].nivel_riesgo == sample_alergeno_data["nivel_riesgo"]


@pytest.mark.asyncio
async def test_create_alergeno_duplicate_name(alergeno_service, mock_repository, sample_alergeno_data):
    """
    Prueba el manejo de errores al intentar crear un alérgeno con nombre duplicado.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método create_alergeno con un nombre duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar AlergenoConflictError.
    """
    # Arrange
    alergeno_create = AlergenoCreate(
        nombre=sample_alergeno_data["nombre"],
        descripcion=sample_alergeno_data["descripcion"]
    )
    mock_repository.create.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(AlergenoConflictError) as excinfo:
        await alergeno_service.create_alergeno(alergeno_create)

    assert "Ya existe un alérgeno con el nombre" in str(excinfo.value)
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_alergeno_by_id_success(alergeno_service, mock_repository, sample_alergeno_data):
    """
    Prueba la obtención exitosa de un alérgeno por su ID.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia del alérgeno.
        - Llama al método get_alergeno_by_id con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar el alérgeno correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    alergeno_id = sample_alergeno_data["id"]
    mock_repository.get_by_id.return_value = AlergenoModel(**sample_alergeno_data)

    # Act
    result = await alergeno_service.get_alergeno_by_id(alergeno_id)

    # Assert
    assert result.id == alergeno_id
    assert result.nombre == sample_alergeno_data["nombre"]
    assert result.descripcion == sample_alergeno_data["descripcion"]
    assert result.icono == sample_alergeno_data["icono"]
    assert result.nivel_riesgo == sample_alergeno_data["nivel_riesgo"]
    mock_repository.get_by_id.assert_called_once_with(alergeno_id)


@pytest.mark.asyncio
async def test_get_alergeno_by_id_not_found(alergeno_service, mock_repository):
    """
    Prueba el manejo de errores al intentar obtener un alérgeno que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el alérgeno no existe.
        - Llama al método get_alergeno_by_id con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar AlergenoNotFoundError.
    """
    # Arrange
    alergeno_id = str(ULID())
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(AlergenoNotFoundError) as excinfo:
        await alergeno_service.get_alergeno_by_id(alergeno_id)

    assert f"No se encontró el alérgeno con ID {alergeno_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(alergeno_id)


@pytest.mark.asyncio
async def test_delete_alergeno_success(alergeno_service, mock_repository, sample_alergeno_data):
    """
    Prueba la eliminación exitosa de un alérgeno.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia y eliminación exitosa del alérgeno.
        - Llama al método delete_alergeno con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe eliminar el alérgeno correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    alergeno_id = sample_alergeno_data["id"]
    mock_repository.get_by_id.return_value = AlergenoModel(**sample_alergeno_data)
    mock_repository.delete.return_value = True

    # Act
    result = await alergeno_service.delete_alergeno(alergeno_id)

    # Assert
    assert result is True
    mock_repository.get_by_id.assert_called_once_with(alergeno_id)
    mock_repository.delete.assert_called_once_with(alergeno_id)


@pytest.mark.asyncio
async def test_delete_alergeno_not_found(alergeno_service, mock_repository):
    """
    Prueba el manejo de errores al intentar eliminar un alérgeno que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el alérgeno no existe.
        - Llama al método delete_alergeno con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar AlergenoNotFoundError.
    """
    # Arrange
    alergeno_id = str(ULID())
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(AlergenoNotFoundError) as excinfo:
        await alergeno_service.delete_alergeno(alergeno_id)

    assert f"No se encontró el alérgeno con ID {alergeno_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(alergeno_id)
    mock_repository.delete.assert_not_called()


@pytest.mark.asyncio
async def test_get_alergenos_success(alergeno_service, mock_repository, sample_alergeno_data):
    """
    Prueba la obtención exitosa de una lista paginada de alérgenos.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una lista de alérgenos.
        - Llama al método get_alergenos con parámetros válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar la lista de alérgenos correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    alergenos = [
        AlergenoModel(**sample_alergeno_data),
        AlergenoModel(
            id=str(ULID()),
            nombre="Otro Alérgeno",
            descripcion="Otro alérgeno para pruebas",
            nivel_riesgo=NivelRiesgo.ALTO,
            activo=True,
        ),
    ]
    mock_repository.get_all.return_value = (alergenos, len(alergenos))

    # Act
    result = await alergeno_service.get_alergenos(skip=0, limit=10)

    # Assert
    assert result.total == 2
    assert len(result.items) == 2
    assert result.items[0].nombre == sample_alergeno_data["nombre"]
    assert result.items[1].nombre == "Otro Alérgeno"
    mock_repository.get_all.assert_called_once_with(0, 10)


@pytest.mark.asyncio
async def test_get_alergenos_validation_error(alergeno_service):
    """
    Prueba el manejo de errores al proporcionar parámetros inválidos para obtener alérgenos.

    PRECONDICIONES:
        - El servicio debe estar configurado.

    PROCESO:
        - Llama al método get_alergenos con parámetros inválidos.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar AlergenoValidationError.
    """
    # Act & Assert - Parámetro skip negativo
    with pytest.raises(AlergenoValidationError) as excinfo:
        await alergeno_service.get_alergenos(skip=-1, limit=10)
    assert "El parámetro 'skip' debe ser mayor o igual a cero" in str(excinfo.value)

    # Act & Assert - Parámetro limit no positivo
    with pytest.raises(AlergenoValidationError) as excinfo:
        await alergeno_service.get_alergenos(skip=0, limit=0)
    assert "El parámetro 'limit' debe ser mayor a cero" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_alergeno_success(alergeno_service, mock_repository, sample_alergeno_data):
    """
    Prueba la actualización exitosa de un alérgeno.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la actualización exitosa de un alérgeno.
        - Llama al método update_alergeno con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe actualizar el alérgeno correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    alergeno_id = sample_alergeno_data["id"]
    update_data = AlergenoUpdate(
        nombre="Alérgeno Actualizado",
        descripcion="Descripción actualizada",
        nivel_riesgo=NivelRiesgo.ALTO
    )

    updated_alergeno = AlergenoModel(
        **{
            **sample_alergeno_data,
            "nombre": "Alérgeno Actualizado",
            "descripcion": "Descripción actualizada",
            "nivel_riesgo": NivelRiesgo.ALTO,
        }
    )
    mock_repository.update.return_value = updated_alergeno

    # Act
    result = await alergeno_service.update_alergeno(alergeno_id, update_data)

    # Assert
    assert result.id == alergeno_id
    assert result.nombre == "Alérgeno Actualizado"
    assert result.descripcion == "Descripción actualizada"
    assert result.nivel_riesgo == NivelRiesgo.ALTO
    mock_repository.update.assert_called_once_with(
        alergeno_id,
        nombre="Alérgeno Actualizado",
        descripcion="Descripción actualizada",
        nivel_riesgo=NivelRiesgo.ALTO
    )


@pytest.mark.asyncio
async def test_update_alergeno_not_found(alergeno_service, mock_repository):
    """
    Prueba el manejo de errores al intentar actualizar un alérgeno que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el alérgeno no existe.
        - Llama al método update_alergeno con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar AlergenoNotFoundError.
    """
    # Arrange
    alergeno_id = str(ULID())
    update_data = AlergenoUpdate(nombre="Alérgeno Actualizado")
    mock_repository.update.return_value = None

    # Act & Assert
    with pytest.raises(AlergenoNotFoundError) as excinfo:
        await alergeno_service.update_alergeno(alergeno_id, update_data)

    assert f"No se encontró el alérgeno con ID {alergeno_id}" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(alergeno_id, nombre="Alérgeno Actualizado")


@pytest.mark.asyncio
async def test_update_alergeno_duplicate_name(alergeno_service, mock_repository, sample_alergeno_data):
    """
    Prueba el manejo de errores al intentar actualizar un alérgeno con un nombre duplicado.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método update_alergeno con un nombre duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar AlergenoConflictError.
    """
    # Arrange
    alergeno_id = sample_alergeno_data["id"]
    update_data = AlergenoUpdate(nombre="Alérgeno Duplicado")
    mock_repository.update.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(AlergenoConflictError) as excinfo:
        await alergeno_service.update_alergeno(alergeno_id, update_data)

    assert "Ya existe un alérgeno con el nombre" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(alergeno_id, nombre="Alérgeno Duplicado")


@pytest.mark.asyncio
async def test_update_alergeno_no_changes(alergeno_service, mock_repository, sample_alergeno_data):
    """
    Prueba la actualización de un alérgeno cuando no se proporcionan cambios.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia del alérgeno.
        - Llama al método update_alergeno sin proporcionar campos para actualizar.
        - Verifica que se recupere el alérgeno existente sin cambios.

    POSTCONDICIONES:
        - El servicio debe retornar el alérgeno existente sin modificaciones.
        - El método update del repositorio no debe ser llamado.
    """
    # Arrange
    alergeno_id = sample_alergeno_data["id"]
    update_data = AlergenoUpdate()  # Sin datos para actualizar
    mock_repository.get_by_id.return_value = AlergenoModel(**sample_alergeno_data)

    # Act
    result = await alergeno_service.update_alergeno(alergeno_id, update_data)

    # Assert
    assert result.id == alergeno_id
    assert result.nombre == sample_alergeno_data["nombre"]
    mock_repository.get_by_id.assert_called_once_with(alergeno_id)
    mock_repository.update.assert_not_called()
