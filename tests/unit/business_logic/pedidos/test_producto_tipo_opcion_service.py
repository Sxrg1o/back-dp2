"""
Pruebas unitarias para el servicio de opciones de productos.
"""

import pytest
from unittest.mock import AsyncMock
import uuid
from datetime import datetime
from decimal import Decimal

from src.business_logic.pedidos.producto_tipo_opcion_service import ProductoTipoOpcionService
from src.models.pedidos.producto_tipo_opcion_model import ProductoTipoOpcionModel
from src.api.schemas.producto_tipo_opcion_schema import ProductoTipoOpcionCreate, ProductoTipoOpcionUpdate
from src.business_logic.exceptions.producto_tipo_opcion_exceptions import (
    ProductoTipoOpcionValidationError,
    ProductoTipoOpcionNotFoundError,
    ProductoTipoOpcionConflictError,
)
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def mock_repository():
    """
    Fixture que proporciona un mock del repositorio de opciones de productos.
    """
    repository = AsyncMock()
    return repository


@pytest.fixture
def producto_opcion_service(mock_repository):
    """
    Fixture que proporciona una instancia del servicio de opciones de productos con un repositorio mockeado.
    """
    service = ProductoTipoOpcionService(AsyncMock())
    service.repository = mock_repository
    return service


@pytest.fixture
def sample_producto_opcion_data():
    """
    Fixture que proporciona datos de muestra para una opción de producto.
    """
    return {
        "id": uuid.uuid4(),
        "id_producto": uuid.uuid4(),
        "id_tipo_opcion": uuid.uuid4(),
        "nombre": "Ají suave",
        "precio_adicional": Decimal("0.00"),
        "activo": True,
        "orden": 1,
        "fecha_creacion": datetime.now(),
        "fecha_modificacion": datetime.now(),
    }


@pytest.mark.asyncio
async def test_create_producto_tipo_opcion_success(producto_opcion_service, mock_repository, sample_producto_opcion_data):
    """
    Prueba la creación exitosa de una opción de producto.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una creación exitosa.
        - Llama al método create_producto_tipo_opcion con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe crear la opción de producto correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    producto_opcion_create = ProductoTipoOpcionCreate(
        id_producto=sample_producto_opcion_data["id_producto"],
        id_tipo_opcion=sample_producto_opcion_data["id_tipo_opcion"],
        nombre=sample_producto_opcion_data["nombre"],
        precio_adicional=sample_producto_opcion_data["precio_adicional"],
        activo=sample_producto_opcion_data["activo"],
        orden=sample_producto_opcion_data["orden"]
    )
    mock_repository.create.return_value = ProductoTipoOpcionModel(**sample_producto_opcion_data)

    # Act
    result = await producto_opcion_service.create_producto_tipo_opcion(producto_opcion_create)

    # Assert
    assert result.id == sample_producto_opcion_data["id"]
    assert result.nombre == sample_producto_opcion_data["nombre"]
    assert result.precio_adicional == sample_producto_opcion_data["precio_adicional"]
    mock_repository.create.assert_called_once()

    # Verificar que se pasó un objeto ProductoTipoOpcionModel al repositorio
    args, _ = mock_repository.create.call_args
    assert isinstance(args[0], ProductoTipoOpcionModel)
    assert args[0].nombre == sample_producto_opcion_data["nombre"]
    assert args[0].id_producto == sample_producto_opcion_data["id_producto"]


@pytest.mark.asyncio
async def test_create_producto_tipo_opcion_duplicate(producto_opcion_service, mock_repository, sample_producto_opcion_data):
    """
    Prueba el manejo de errores al intentar crear una opción de producto duplicada.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método create_producto_tipo_opcion con un nombre duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar ProductoTipoOpcionConflictError.
    """
    # Arrange
    producto_opcion_create = ProductoTipoOpcionCreate(
        id_producto=sample_producto_opcion_data["id_producto"],
        id_tipo_opcion=sample_producto_opcion_data["id_tipo_opcion"],
        nombre=sample_producto_opcion_data["nombre"],
        precio_adicional=sample_producto_opcion_data["precio_adicional"],
        activo=sample_producto_opcion_data["activo"],
        orden=sample_producto_opcion_data["orden"]
    )
    mock_repository.create.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(ProductoTipoOpcionConflictError) as excinfo:
        await producto_opcion_service.create_producto_tipo_opcion(producto_opcion_create)

        assert "Ya existe una opción de producto por tipo con el nombre" in str(excinfo.value)
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_producto_tipo_opcion_by_id_success(producto_opcion_service, mock_repository, sample_producto_opcion_data):
    """
    Prueba la obtención exitosa de una opción de producto por su ID.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia de la opción de producto.
        - Llama al método get_producto_tipo_opcion_by_id con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar la opción de producto correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    producto_opcion_id = sample_producto_opcion_data["id"]
    mock_repository.get_by_id.return_value = ProductoTipoOpcionModel(**sample_producto_opcion_data)

    # Act
    result = await producto_opcion_service.get_producto_tipo_opcion_by_id(producto_opcion_id)

    # Assert
    assert result.id == producto_opcion_id
    assert result.nombre == sample_producto_opcion_data["nombre"]
    assert result.precio_adicional == sample_producto_opcion_data["precio_adicional"]
    mock_repository.get_by_id.assert_called_once_with(producto_opcion_id)


@pytest.mark.asyncio
async def test_get_producto_tipo_opcion_by_id_not_found(producto_opcion_service, mock_repository):
    """
    Prueba el manejo de errores al intentar obtener una opción de producto que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que la opción de producto no existe.
        - Llama al método get_producto_tipo_opcion_by_id con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar ProductoTipoOpcionNotFoundError.
    """
    # Arrange
    producto_opcion_id = uuid.uuid4()
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ProductoTipoOpcionNotFoundError) as excinfo:
        await producto_opcion_service.get_producto_tipo_opcion_by_id(producto_opcion_id)

        assert f"No se encontró la opción de producto por tipo con ID {producto_opcion_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(producto_opcion_id)


@pytest.mark.asyncio
async def test_delete_producto_tipo_opcion_success(producto_opcion_service, mock_repository, sample_producto_opcion_data):
    """
    Prueba la eliminación exitosa de una opción de producto.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia y eliminación exitosa de la opción de producto.
        - Llama al método delete_producto_tipo_opcion con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe eliminar la opción de producto correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    producto_opcion_id = sample_producto_opcion_data["id"]
    mock_repository.get_by_id.return_value = ProductoTipoOpcionModel(**sample_producto_opcion_data)
    mock_repository.delete.return_value = True

    # Act
    result = await producto_opcion_service.delete_producto_tipo_opcion(producto_opcion_id)

    # Assert
    assert result is True
    mock_repository.get_by_id.assert_called_once_with(producto_opcion_id)
    mock_repository.delete.assert_called_once_with(producto_opcion_id)


@pytest.mark.asyncio
async def test_delete_producto_tipo_opcion_not_found(producto_opcion_service, mock_repository):
    """
    Prueba el manejo de errores al intentar eliminar una opción de producto que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que la opción de producto no existe.
        - Llama al método delete_producto_tipo_opcion con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar ProductoTipoOpcionNotFoundError.
    """
    # Arrange
    producto_opcion_id = uuid.uuid4()
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ProductoTipoOpcionNotFoundError) as excinfo:
        await producto_opcion_service.delete_producto_tipo_opcion(producto_opcion_id)

        assert f"No se encontró la opción de producto por tipo con ID {producto_opcion_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(producto_opcion_id)
    mock_repository.delete.assert_not_called()


@pytest.mark.asyncio
async def test_get_producto_tipo_opciones_success(producto_opcion_service, mock_repository, sample_producto_opcion_data):
    """
    Prueba la obtención exitosa de una lista paginada de opciones de productos.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una lista de opciones de productos.
        - Llama al método get_producto_tipo_opciones con parámetros válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar la lista de opciones de productos correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    producto_opciones = [
        ProductoTipoOpcionModel(**sample_producto_opcion_data),
        ProductoTipoOpcionModel(
            id=uuid.uuid4(),
            id_producto=uuid.uuid4(),
            id_tipo_opcion=uuid.uuid4(),
            nombre="Sin ají",
            precio_adicional=Decimal("0.00"),
            activo=True,
            orden=0
        ),
    ]
    mock_repository.get_all.return_value = (producto_opciones, len(producto_opciones))

    # Act
    result = await producto_opcion_service.get_producto_tipo_opciones(skip=0, limit=10)

    # Assert
    assert result.total == 2
    assert len(result.items) == 2
    assert result.items[0].nombre == sample_producto_opcion_data["nombre"]
    assert result.items[1].nombre == "Sin ají"
    mock_repository.get_all.assert_called_once_with(0, 10)


@pytest.mark.asyncio
async def test_get_producto_tipo_opciones_validation_error(producto_opcion_service):
    """
    Prueba el manejo de errores al proporcionar parámetros inválidos para obtener opciones de productos.

    PRECONDICIONES:
        - El servicio debe estar configurado.

    PROCESO:
        - Llama al método get_producto_tipo_opciones con parámetros inválidos.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar ProductoTipoOpcionValidationError.
    """
    # Act & Assert - Parámetro skip negativo
    with pytest.raises(ProductoTipoOpcionValidationError) as excinfo:
        await producto_opcion_service.get_producto_tipo_opciones(skip=-1, limit=10)
    assert "El parámetro 'skip' debe ser mayor o igual a cero" in str(excinfo.value)

    # Act & Assert - Parámetro limit no positivo
    with pytest.raises(ProductoTipoOpcionValidationError) as excinfo:
        await producto_opcion_service.get_producto_tipo_opciones(skip=0, limit=0)
    assert "El parámetro 'limit' debe ser mayor a cero" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_producto_tipo_opcion_success(producto_opcion_service, mock_repository, sample_producto_opcion_data):
    """
    Prueba la actualización exitosa de una opción de producto.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la actualización exitosa de una opción de producto.
        - Llama al método update_producto_tipo_opcion con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe actualizar la opción de producto correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    producto_opcion_id = sample_producto_opcion_data["id"]
    update_data = ProductoTipoOpcionUpdate(
        nombre="Ají picante",
        precio_adicional=Decimal("2.50")
    )

    updated_producto_opcion = ProductoTipoOpcionModel(
        **{
            **sample_producto_opcion_data,
            "nombre": "Ají picante",
            "precio_adicional": Decimal("2.50"),
        }
    )
    mock_repository.update.return_value = updated_producto_opcion

    # Act
    result = await producto_opcion_service.update_producto_tipo_opcion(producto_opcion_id, update_data)

    # Assert
    assert result.id == producto_opcion_id
    assert result.nombre == "Ají picante"
    assert result.precio_adicional == Decimal("2.50")
    mock_repository.update.assert_called_once_with(
        producto_opcion_id, nombre="Ají picante", precio_adicional=Decimal("2.50")
    )


@pytest.mark.asyncio
async def test_update_producto_tipo_opcion_not_found(producto_opcion_service, mock_repository):
    """
    Prueba el manejo de errores al intentar actualizar una opción de producto que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que la opción de producto no existe.
        - Llama al método update_producto_tipo_opcion con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar ProductoTipoOpcionNotFoundError.
    """
    # Arrange
    producto_opcion_id = uuid.uuid4()
    update_data = ProductoTipoOpcionUpdate(nombre="Ají picante")
    mock_repository.update.return_value = None

    # Act & Assert
    with pytest.raises(ProductoTipoOpcionNotFoundError) as excinfo:
        await producto_opcion_service.update_producto_tipo_opcion(producto_opcion_id, update_data)

        assert f"No se encontró la opción de producto por tipo con ID {producto_opcion_id}" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(producto_opcion_id, nombre="Ají picante")


@pytest.mark.asyncio
async def test_update_producto_tipo_opcion_duplicate_name(producto_opcion_service, mock_repository, sample_producto_opcion_data):
    """
    Prueba el manejo de errores al intentar actualizar una opción de producto con un nombre duplicado.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método update_producto_tipo_opcion con un nombre duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar ProductoTipoOpcionConflictError.
    """
    # Arrange
    producto_opcion_id = sample_producto_opcion_data["id"]
    update_data = ProductoTipoOpcionUpdate(nombre="Opción Duplicada")
    mock_repository.update.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(ProductoTipoOpcionConflictError) as excinfo:
        await producto_opcion_service.update_producto_tipo_opcion(producto_opcion_id, update_data)

        assert "Ya existe una opción de producto por tipo con el nombre" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(producto_opcion_id, nombre="Opción Duplicada")


@pytest.mark.asyncio
async def test_update_producto_tipo_opcion_no_changes(producto_opcion_service, mock_repository, sample_producto_opcion_data):
    """
    Prueba la actualización de una opción de producto cuando no se proporcionan cambios.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia de la opción de producto.
        - Llama al método update_producto_tipo_opcion sin proporcionar campos para actualizar.
        - Verifica que se recupere la opción de producto existente sin cambios.

    POSTCONDICIONES:
        - El servicio debe retornar la opción de producto existente sin modificaciones.
        - El método update del repositorio no debe ser llamado.
    """
    # Arrange
    producto_opcion_id = sample_producto_opcion_data["id"]
    update_data = ProductoTipoOpcionUpdate()  # Sin datos para actualizar
    mock_repository.get_by_id.return_value = ProductoTipoOpcionModel(**sample_producto_opcion_data)

    # Act
    result = await producto_opcion_service.update_producto_tipo_opcion(producto_opcion_id, update_data)

    # Assert
    assert result.id == producto_opcion_id
    assert result.nombre == sample_producto_opcion_data["nombre"]
    mock_repository.get_by_id.assert_called_once_with(producto_opcion_id)
    mock_repository.update.assert_not_called()
