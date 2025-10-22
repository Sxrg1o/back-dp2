"""
Pruebas unitarias para el servicio de categorías.
"""

import pytest
from unittest.mock import AsyncMock
from ulid import ULID
from datetime import datetime


from src.business_logic.menu.categoria_service import CategoriaService
from src.models.menu.categoria_model import CategoriaModel
from src.api.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate
from src.business_logic.exceptions.categoria_exceptions import (
    CategoriaValidationError,
    CategoriaNotFoundError,
    CategoriaConflictError,
)
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def mock_repository():
    """
    Fixture que proporciona un mock del repositorio de categorías.
    """
    repository = AsyncMock()
    return repository


@pytest.fixture
def categoria_service(mock_repository):
    """
    Fixture que proporciona una instancia del servicio de categorías con un repositorio mockeado.
    """
    service = CategoriaService(AsyncMock())
    service.repository = mock_repository
    return service


@pytest.fixture
def sample_categoria_data():
    """
    Fixture que proporciona datos de muestra para una categoría.
    """
    return {
        "id": str(ULID()),
        "nombre": "Test Categoría",
        "descripcion": "Categoría para pruebas",
        "imagen_path": "/images/test.jpg",
        "activo": True,
        "fecha_creacion": datetime.now(),
        "fecha_modificacion": datetime.now(),
    }


@pytest.mark.asyncio
async def test_create_categoria_success(categoria_service, mock_repository, sample_categoria_data):
    """
    Prueba la creación exitosa de una categoría.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una creación exitosa.
        - Llama al método create_categoria con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe crear la categoría correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    categoria_create = CategoriaCreate(
        nombre=sample_categoria_data["nombre"],
        descripcion=sample_categoria_data["descripcion"],
        imagen_path=sample_categoria_data["imagen_path"]
    )
    mock_repository.create.return_value = CategoriaModel(**sample_categoria_data)

    # Act
    result = await categoria_service.create_categoria(categoria_create)

    # Assert
    assert result.id == sample_categoria_data["id"]
    assert result.nombre == sample_categoria_data["nombre"]
    assert result.descripcion == sample_categoria_data["descripcion"]
    assert result.imagen_path == sample_categoria_data["imagen_path"]
    mock_repository.create.assert_called_once()

    # Verificar que se pasó un objeto CategoriaModel al repositorio
    args, _ = mock_repository.create.call_args
    assert isinstance(args[0], CategoriaModel)
    assert args[0].nombre == sample_categoria_data["nombre"]
    assert args[0].descripcion == sample_categoria_data["descripcion"]
    assert args[0].imagen_path == sample_categoria_data["imagen_path"]


@pytest.mark.asyncio
async def test_create_categoria_duplicate_name(categoria_service, mock_repository, sample_categoria_data):
    """
    Prueba el manejo de errores al intentar crear una categoría con nombre duplicado.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método create_categoria con un nombre duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar CategoriaConflictError.
    """
    # Arrange
    categoria_create = CategoriaCreate(
        nombre=sample_categoria_data["nombre"],
        descripcion=sample_categoria_data["descripcion"]
    )
    mock_repository.create.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(CategoriaConflictError) as excinfo:
        await categoria_service.create_categoria(categoria_create)

    assert "Ya existe una categoría con el nombre" in str(excinfo.value)
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_categoria_by_id_success(categoria_service, mock_repository, sample_categoria_data):
    """
    Prueba la obtención exitosa de una categoría por su ID.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia de la categoría.
        - Llama al método get_categoria_by_id con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar la categoría correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    categoria_id = sample_categoria_data["id"]
    mock_repository.get_by_id.return_value = CategoriaModel(**sample_categoria_data)

    # Act
    result = await categoria_service.get_categoria_by_id(categoria_id)

    # Assert
    assert result.id == categoria_id
    assert result.nombre == sample_categoria_data["nombre"]
    assert result.descripcion == sample_categoria_data["descripcion"]
    assert result.imagen_path == sample_categoria_data["imagen_path"]
    mock_repository.get_by_id.assert_called_once_with(categoria_id)


@pytest.mark.asyncio
async def test_get_categoria_by_id_not_found(categoria_service, mock_repository):
    """
    Prueba el manejo de errores al intentar obtener una categoría que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que la categoría no existe.
        - Llama al método get_categoria_by_id con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar CategoriaNotFoundError.
    """
    # Arrange
    categoria_id = str(ULID())
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(CategoriaNotFoundError) as excinfo:
        await categoria_service.get_categoria_by_id(categoria_id)

    assert f"No se encontró la categoría con ID {categoria_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(categoria_id)


@pytest.mark.asyncio
async def test_delete_categoria_success(categoria_service, mock_repository, sample_categoria_data):
    """
    Prueba la eliminación exitosa de una categoría.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia y eliminación exitosa de la categoría.
        - Llama al método delete_categoria con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe eliminar la categoría correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    categoria_id = sample_categoria_data["id"]
    mock_repository.get_by_id.return_value = CategoriaModel(**sample_categoria_data)
    mock_repository.delete.return_value = True

    # Act
    result = await categoria_service.delete_categoria(categoria_id)

    # Assert
    assert result is True
    mock_repository.get_by_id.assert_called_once_with(categoria_id)
    mock_repository.delete.assert_called_once_with(categoria_id)


@pytest.mark.asyncio
async def test_delete_categoria_not_found(categoria_service, mock_repository):
    """
    Prueba el manejo de errores al intentar eliminar una categoría que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que la categoría no existe.
        - Llama al método delete_categoria con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar CategoriaNotFoundError.
    """
    # Arrange
    categoria_id = str(ULID())
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(CategoriaNotFoundError) as excinfo:
        await categoria_service.delete_categoria(categoria_id)

    assert f"No se encontró la categoría con ID {categoria_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(categoria_id)
    mock_repository.delete.assert_not_called()


@pytest.mark.asyncio
async def test_get_categorias_success(categoria_service, mock_repository, sample_categoria_data):
    """
    Prueba la obtención exitosa de una lista paginada de categorías.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una lista de categorías.
        - Llama al método get_categorias con parámetros válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar la lista de categorías correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    categorias = [
        CategoriaModel(**sample_categoria_data),
        CategoriaModel(
            id=str(ULID()),
            nombre="Otra Categoría",
            descripcion="Otra categoría para pruebas",
            imagen_path="/images/otra.jpg",
            activo=True,
        ),
    ]
    mock_repository.get_all.return_value = (categorias, len(categorias))

    # Act
    result = await categoria_service.get_categorias(skip=0, limit=10)

    # Assert
    assert result.total == 2
    assert len(result.items) == 2
    assert result.items[0].nombre == sample_categoria_data["nombre"]
    assert result.items[1].nombre == "Otra Categoría"
    mock_repository.get_all.assert_called_once_with(0, 10)


@pytest.mark.asyncio
async def test_get_categorias_validation_error(categoria_service):
    """
    Prueba el manejo de errores al proporcionar parámetros inválidos para obtener categorías.

    PRECONDICIONES:
        - El servicio debe estar configurado.

    PROCESO:
        - Llama al método get_categorias con parámetros inválidos.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar CategoriaValidationError.
    """
    # Act & Assert - Parámetro skip negativo
    with pytest.raises(CategoriaValidationError) as excinfo:
        await categoria_service.get_categorias(skip=-1, limit=10)
    assert "El parámetro 'skip' debe ser mayor o igual a cero" in str(excinfo.value)

    # Act & Assert - Parámetro limit no positivo
    with pytest.raises(CategoriaValidationError) as excinfo:
        await categoria_service.get_categorias(skip=0, limit=0)
    assert "El parámetro 'limit' debe ser mayor a cero" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_categoria_success(categoria_service, mock_repository, sample_categoria_data):
    """
    Prueba la actualización exitosa de una categoría.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la actualización exitosa de una categoría.
        - Llama al método update_categoria con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe actualizar la categoría correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    categoria_id = sample_categoria_data["id"]
    update_data = CategoriaUpdate(
        nombre="Categoría Actualizada",
        descripcion="Descripción actualizada",
        imagen_path="/images/updated.jpg"
    )

    updated_categoria = CategoriaModel(
        **{
            **sample_categoria_data,
            "nombre": "Categoría Actualizada",
            "descripcion": "Descripción actualizada",
            "imagen_path": "/images/updated.jpg",
        }
    )
    mock_repository.update.return_value = updated_categoria

    # Act
    result = await categoria_service.update_categoria(categoria_id, update_data)

    # Assert
    assert result.id == categoria_id
    assert result.nombre == "Categoría Actualizada"
    assert result.descripcion == "Descripción actualizada"
    assert result.imagen_path == "/images/updated.jpg"
    mock_repository.update.assert_called_once_with(
        categoria_id,
        nombre="Categoría Actualizada",
        descripcion="Descripción actualizada",
        imagen_path="/images/updated.jpg"
    )


@pytest.mark.asyncio
async def test_update_categoria_not_found(categoria_service, mock_repository):
    """
    Prueba el manejo de errores al intentar actualizar una categoría que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que la categoría no existe.
        - Llama al método update_categoria con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar CategoriaNotFoundError.
    """
    # Arrange
    categoria_id = str(ULID())
    update_data = CategoriaUpdate(nombre="Categoría Actualizada")
    mock_repository.update.return_value = None

    # Act & Assert
    with pytest.raises(CategoriaNotFoundError) as excinfo:
        await categoria_service.update_categoria(categoria_id, update_data)

    assert f"No se encontró la categoría con ID {categoria_id}" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(categoria_id, nombre="Categoría Actualizada")


@pytest.mark.asyncio
async def test_update_categoria_duplicate_name(categoria_service, mock_repository, sample_categoria_data):
    """
    Prueba el manejo de errores al intentar actualizar una categoría con un nombre duplicado.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método update_categoria con un nombre duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar CategoriaConflictError.
    """
    # Arrange
    categoria_id = sample_categoria_data["id"]
    update_data = CategoriaUpdate(nombre="Categoría Duplicada")
    mock_repository.update.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(CategoriaConflictError) as excinfo:
        await categoria_service.update_categoria(categoria_id, update_data)

    assert "Ya existe una categoría con el nombre" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(categoria_id, nombre="Categoría Duplicada")


@pytest.mark.asyncio
async def test_update_categoria_no_changes(categoria_service, mock_repository, sample_categoria_data):
    """
    Prueba la actualización de una categoría cuando no se proporcionan cambios.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia de la categoría.
        - Llama al método update_categoria sin proporcionar campos para actualizar.
        - Verifica que se recupere la categoría existente sin cambios.

    POSTCONDICIONES:
        - El servicio debe retornar la categoría existente sin modificaciones.
        - El método update del repositorio no debe ser llamado.
    """
    # Arrange
    categoria_id = sample_categoria_data["id"]
    update_data = CategoriaUpdate()  # Sin datos para actualizar
    mock_repository.get_by_id.return_value = CategoriaModel(**sample_categoria_data)

    # Act
    result = await categoria_service.update_categoria(categoria_id, update_data)

    # Assert
    assert result.id == categoria_id
    assert result.nombre == sample_categoria_data["nombre"]
    mock_repository.get_by_id.assert_called_once_with(categoria_id)
    mock_repository.update.assert_not_called()
