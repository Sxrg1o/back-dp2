"""
Pruebas unitarias para el servicio de tipos de opciones.
"""

import pytest
from unittest.mock import AsyncMock
from ulid import ULID
from datetime import datetime

from src.business_logic.pedidos.tipo_opciones_service import TipoOpcionService
from src.models.pedidos.tipo_opciones_model import TipoOpcionModel
from src.api.schemas.tipo_opciones_schema import TipoOpcionCreate, TipoOpcionUpdate
from src.business_logic.exceptions.tipo_opciones_exceptions import (
    TipoOpcionValidationError,
    TipoOpcionNotFoundError,
    TipoOpcionConflictError,
)
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def mock_repository():
    """
    Fixture que proporciona un mock del repositorio de tipos de opciones.
    """
    repository = AsyncMock()
    return repository


@pytest.fixture
def tipo_opcion_service(mock_repository):
    """
    Fixture que proporciona una instancia del servicio de tipos de opciones con un repositorio mockeado.
    """
    service = TipoOpcionService(AsyncMock())
    service.repository = mock_repository
    return service


@pytest.fixture
def sample_tipo_opcion_data():
    """
    Fixture que proporciona datos de muestra para un tipo de opción.
    """
    return {
        "id": str(ULID()),
        "codigo": "nivel_aji",
        "nombre": "Nivel de Ají",
        "descripcion": "Nivel de picante del plato",
        "activo": True,
        "orden": 1,
        "fecha_creacion": datetime.now(),
        "fecha_modificacion": datetime.now(),
    }


@pytest.mark.asyncio
async def test_create_tipo_opcion_success(tipo_opcion_service, mock_repository, sample_tipo_opcion_data):
    """
    Prueba la creación exitosa de un tipo de opción.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una creación exitosa.
        - Llama al método create_tipo_opcion con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe crear el tipo de opción correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    tipo_opcion_create = TipoOpcionCreate(
        codigo=sample_tipo_opcion_data["codigo"],
        nombre=sample_tipo_opcion_data["nombre"],
        descripcion=sample_tipo_opcion_data["descripcion"],
        activo=sample_tipo_opcion_data["activo"],
        orden=sample_tipo_opcion_data["orden"]
    )
    mock_repository.create.return_value = TipoOpcionModel(**sample_tipo_opcion_data)

    # Act
    result = await tipo_opcion_service.create_tipo_opcion(tipo_opcion_create)

    # Assert
    assert result.id == sample_tipo_opcion_data["id"]
    assert result.codigo == sample_tipo_opcion_data["codigo"]
    assert result.nombre == sample_tipo_opcion_data["nombre"]
    assert result.descripcion == sample_tipo_opcion_data["descripcion"]
    assert result.activo == sample_tipo_opcion_data["activo"]
    assert result.orden == sample_tipo_opcion_data["orden"]
    mock_repository.create.assert_called_once()

    # Verificar que se pasó un objeto TipoOpcionModel al repositorio
    args, _ = mock_repository.create.call_args
    assert isinstance(args[0], TipoOpcionModel)
    assert args[0].codigo == sample_tipo_opcion_data["codigo"]
    assert args[0].nombre == sample_tipo_opcion_data["nombre"]
    assert args[0].descripcion == sample_tipo_opcion_data["descripcion"]
    assert args[0].activo == sample_tipo_opcion_data["activo"]
    assert args[0].orden == sample_tipo_opcion_data["orden"]


@pytest.mark.asyncio
async def test_create_tipo_opcion_duplicate_codigo(tipo_opcion_service, mock_repository, sample_tipo_opcion_data):
    """
    Prueba el manejo de errores al intentar crear un tipo de opción con código duplicado.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método create_tipo_opcion con un código duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar TipoOpcionConflictError.
    """
    # Arrange
    tipo_opcion_create = TipoOpcionCreate(
        codigo=sample_tipo_opcion_data["codigo"],
        nombre=sample_tipo_opcion_data["nombre"]
    )
    mock_repository.create.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(TipoOpcionConflictError) as excinfo:
        await tipo_opcion_service.create_tipo_opcion(tipo_opcion_create)

    assert "Ya existe un tipo de opción con el código" in str(excinfo.value)
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_tipo_opcion_by_id_success(tipo_opcion_service, mock_repository, sample_tipo_opcion_data):
    """
    Prueba la obtención exitosa de un tipo de opción por su ID.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia del tipo de opción.
        - Llama al método get_tipo_opcion_by_id con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar el tipo de opción correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    tipo_opcion_id = sample_tipo_opcion_data["id"]
    mock_repository.get_by_id.return_value = TipoOpcionModel(**sample_tipo_opcion_data)

    # Act
    result = await tipo_opcion_service.get_tipo_opcion_by_id(tipo_opcion_id)

    # Assert
    assert result.id == tipo_opcion_id
    assert result.codigo == sample_tipo_opcion_data["codigo"]
    assert result.nombre == sample_tipo_opcion_data["nombre"]
    assert result.descripcion == sample_tipo_opcion_data["descripcion"]
    assert result.activo == sample_tipo_opcion_data["activo"]
    assert result.orden == sample_tipo_opcion_data["orden"]
    mock_repository.get_by_id.assert_called_once_with(tipo_opcion_id)


@pytest.mark.asyncio
async def test_get_tipo_opcion_by_id_not_found(tipo_opcion_service, mock_repository):
    """
    Prueba el manejo de errores al intentar obtener un tipo de opción que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el tipo de opción no existe.
        - Llama al método get_tipo_opcion_by_id con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar TipoOpcionNotFoundError.
    """
    # Arrange
    tipo_opcion_id = str(ULID())
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(TipoOpcionNotFoundError) as excinfo:
        await tipo_opcion_service.get_tipo_opcion_by_id(tipo_opcion_id)

    assert f"No se encontró el tipo de opción con ID {tipo_opcion_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(tipo_opcion_id)


@pytest.mark.asyncio
async def test_delete_tipo_opcion_success(tipo_opcion_service, mock_repository, sample_tipo_opcion_data):
    """
    Prueba la eliminación exitosa de un tipo de opción.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia y eliminación exitosa del tipo de opción.
        - Llama al método delete_tipo_opcion con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe eliminar el tipo de opción correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    tipo_opcion_id = sample_tipo_opcion_data["id"]
    mock_repository.get_by_id.return_value = TipoOpcionModel(**sample_tipo_opcion_data)
    mock_repository.delete.return_value = True

    # Act
    result = await tipo_opcion_service.delete_tipo_opcion(tipo_opcion_id)

    # Assert
    assert result is True
    mock_repository.get_by_id.assert_called_once_with(tipo_opcion_id)
    mock_repository.delete.assert_called_once_with(tipo_opcion_id)


@pytest.mark.asyncio
async def test_delete_tipo_opcion_not_found(tipo_opcion_service, mock_repository):
    """
    Prueba el manejo de errores al intentar eliminar un tipo de opción que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el tipo de opción no existe.
        - Llama al método delete_tipo_opcion con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar TipoOpcionNotFoundError.
    """
    # Arrange
    tipo_opcion_id = str(ULID())
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(TipoOpcionNotFoundError) as excinfo:
        await tipo_opcion_service.delete_tipo_opcion(tipo_opcion_id)

    assert f"No se encontró el tipo de opción con ID {tipo_opcion_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(tipo_opcion_id)
    mock_repository.delete.assert_not_called()


@pytest.mark.asyncio
async def test_get_tipos_opciones_success(tipo_opcion_service, mock_repository, sample_tipo_opcion_data):
    """
    Prueba la obtención exitosa de una lista paginada de tipos de opciones.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una lista de tipos de opciones.
        - Llama al método get_tipos_opciones con parámetros válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar la lista de tipos de opciones correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    tipos_opciones = [
        TipoOpcionModel(**sample_tipo_opcion_data),
        TipoOpcionModel(
            id=str(ULID()),
            codigo="temperatura",
            nombre="Temperatura",
            descripcion="Nivel de temperatura de la bebida",
            activo=True,
            orden=2
        ),
    ]
    mock_repository.get_all.return_value = (tipos_opciones, len(tipos_opciones))

    # Act
    result = await tipo_opcion_service.get_tipos_opciones(skip=0, limit=10)

    # Assert
    assert result.total == 2
    assert len(result.items) == 2
    assert result.items[0].codigo == sample_tipo_opcion_data["codigo"]
    assert result.items[1].codigo == "temperatura"
    mock_repository.get_all.assert_called_once_with(0, 10)


@pytest.mark.asyncio
async def test_get_tipos_opciones_validation_error(tipo_opcion_service):
    """
    Prueba el manejo de errores al proporcionar parámetros inválidos para obtener tipos de opciones.

    PRECONDICIONES:
        - El servicio debe estar configurado.

    PROCESO:
        - Llama al método get_tipos_opciones con parámetros inválidos.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar TipoOpcionValidationError.
    """
    # Act & Assert - Parámetro skip negativo
    with pytest.raises(TipoOpcionValidationError) as excinfo:
        await tipo_opcion_service.get_tipos_opciones(skip=-1, limit=10)
    assert "El parámetro 'skip' debe ser mayor o igual a cero" in str(excinfo.value)

    # Act & Assert - Parámetro limit no positivo
    with pytest.raises(TipoOpcionValidationError) as excinfo:
        await tipo_opcion_service.get_tipos_opciones(skip=0, limit=0)
    assert "El parámetro 'limit' debe ser mayor a cero" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_tipo_opcion_success(tipo_opcion_service, mock_repository, sample_tipo_opcion_data):
    """
    Prueba la actualización exitosa de un tipo de opción.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la actualización exitosa de un tipo de opción.
        - Llama al método update_tipo_opcion con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe actualizar el tipo de opción correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    tipo_opcion_id = sample_tipo_opcion_data["id"]
    update_data = TipoOpcionUpdate(
        nombre="Nivel de Ají Actualizado",
        descripcion="Descripción actualizada",
        orden=5
    )

    updated_tipo_opcion = TipoOpcionModel(
        **{
            **sample_tipo_opcion_data,
            "nombre": "Nivel de Ají Actualizado",
            "descripcion": "Descripción actualizada",
            "orden": 5,
        }
    )
    mock_repository.update.return_value = updated_tipo_opcion

    # Act
    result = await tipo_opcion_service.update_tipo_opcion(tipo_opcion_id, update_data)

    # Assert
    assert result.id == tipo_opcion_id
    assert result.nombre == "Nivel de Ají Actualizado"
    assert result.descripcion == "Descripción actualizada"
    assert result.orden == 5
    mock_repository.update.assert_called_once_with(
        tipo_opcion_id,
        nombre="Nivel de Ají Actualizado",
        descripcion="Descripción actualizada",
        orden=5
    )


@pytest.mark.asyncio
async def test_update_tipo_opcion_not_found(tipo_opcion_service, mock_repository):
    """
    Prueba el manejo de errores al intentar actualizar un tipo de opción que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el tipo de opción no existe.
        - Llama al método update_tipo_opcion con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar TipoOpcionNotFoundError.
    """
    # Arrange
    tipo_opcion_id = str(ULID())
    update_data = TipoOpcionUpdate(nombre="Tipo de Opción Actualizado")
    mock_repository.update.return_value = None

    # Act & Assert
    with pytest.raises(TipoOpcionNotFoundError) as excinfo:
        await tipo_opcion_service.update_tipo_opcion(tipo_opcion_id, update_data)

    assert f"No se encontró el tipo de opción con ID {tipo_opcion_id}" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(tipo_opcion_id, nombre="Tipo de Opción Actualizado")


@pytest.mark.asyncio
async def test_update_tipo_opcion_duplicate_codigo(tipo_opcion_service, mock_repository, sample_tipo_opcion_data):
    """
    Prueba el manejo de errores al intentar actualizar un tipo de opción con un código duplicado.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método update_tipo_opcion con un código duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar TipoOpcionConflictError.
    """
    # Arrange
    tipo_opcion_id = sample_tipo_opcion_data["id"]
    update_data = TipoOpcionUpdate(codigo="codigo_duplicado")
    mock_repository.update.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(TipoOpcionConflictError) as excinfo:
        await tipo_opcion_service.update_tipo_opcion(tipo_opcion_id, update_data)

    assert "Ya existe un tipo de opción con el código" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(tipo_opcion_id, codigo="codigo_duplicado")


@pytest.mark.asyncio
async def test_update_tipo_opcion_no_changes(tipo_opcion_service, mock_repository, sample_tipo_opcion_data):
    """
    Prueba la actualización de un tipo de opción cuando no se proporcionan cambios.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia del tipo de opción.
        - Llama al método update_tipo_opcion sin proporcionar campos para actualizar.
        - Verifica que se recupere el tipo de opción existente sin cambios.

    POSTCONDICIONES:
        - El servicio debe retornar el tipo de opción existente sin modificaciones.
        - El método update del repositorio no debe ser llamado.
    """
    # Arrange
    tipo_opcion_id = sample_tipo_opcion_data["id"]
    update_data = TipoOpcionUpdate()  # Sin datos para actualizar
    mock_repository.get_by_id.return_value = TipoOpcionModel(**sample_tipo_opcion_data)

    # Act
    result = await tipo_opcion_service.update_tipo_opcion(tipo_opcion_id, update_data)

    # Assert
    assert result.id == tipo_opcion_id
    assert result.codigo == sample_tipo_opcion_data["codigo"]
    mock_repository.get_by_id.assert_called_once_with(tipo_opcion_id)
    mock_repository.update.assert_not_called()

