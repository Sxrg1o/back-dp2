"""
Pruebas unitarias para el servicio de pedidos.
"""

import pytest
from decimal import Decimal
from datetime import datetime
from unittest.mock import AsyncMock
from ulid import ULID

from src.business_logic.pedidos.pedido_service import PedidoService
from src.models.pedidos.pedido_model import PedidoModel
from src.models.pedidos.pedido_producto_model import PedidoProductoModel
from src.models.mesas.mesa_model import MesaModel
from src.models.menu.producto_model import ProductoModel
from src.api.schemas.pedido_schema import (
    PedidoCreate,
    PedidoUpdate,
    PedidoEstadoUpdate,
    PedidoCompletoCreate,
    PedidoItemCreate,
)
from src.business_logic.exceptions.pedido_exceptions import (
    PedidoValidationError,
    PedidoNotFoundError,
    PedidoConflictError,
    PedidoStateTransitionError,
)
from src.core.enums.pedido_enums import EstadoPedido
from src.core.enums.mesa_enums import EstadoMesa
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def mock_repository():
    """
    Fixture que proporciona un mock del repositorio de pedidos.
    """
    repository = AsyncMock()
    return repository


@pytest.fixture
def mock_mesa_repository():
    """
    Fixture que proporciona un mock del repositorio de mesas.
    """
    repository = AsyncMock()
    return repository


@pytest.fixture
def pedido_service(mock_repository, mock_mesa_repository):
    """
    Fixture que proporciona una instancia del servicio de pedidos con repositorios mockeados.
    """
    service = PedidoService(AsyncMock())
    service.repository = mock_repository
    service.mesa_repository = mock_mesa_repository
    return service


@pytest.fixture
def sample_pedido_data():
    """
    Fixture que proporciona datos de muestra para un pedido.
    """
    return {
        "id": str(ULID()),
        "id_mesa": str(ULID()),
        "numero_pedido": "20251026-M001-001",
        "estado": EstadoPedido.PENDIENTE,
        "subtotal": Decimal("100.00"),
        "impuestos": Decimal("10.00"),
        "descuentos": Decimal("5.00"),
        "total": Decimal("105.00"),
        "notas_cliente": "Sin cebolla",
        "notas_cocina": "Urgente",
        "fecha_creacion": datetime.now(),
        "fecha_modificacion": datetime.now(),
    }


@pytest.fixture
def sample_mesa_data():
    """
    Fixture que proporciona datos de muestra para una mesa.
    """
    return {
        "id": str(ULID()),
        "numero": "001",
        "capacidad": 4,
        "zona": "A",
        "activo": True,
        "estado": EstadoMesa.DISPONIBLE,
    }


@pytest.mark.asyncio
async def test_create_pedido_success(
    pedido_service, mock_repository, mock_mesa_repository, sample_pedido_data, sample_mesa_data
):
    """
    Prueba la creación exitosa de un pedido.

    PRECONDICIONES:
        - El servicio y repositorios mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una creación exitosa.
        - Llama al método create_pedido con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe crear el pedido correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
        - El numero_pedido debe generarse automáticamente.
    """
    # Arrange
    pedido_create = PedidoCreate(
        id_mesa=sample_pedido_data["id_mesa"],
        subtotal=sample_pedido_data["subtotal"],
        total=sample_pedido_data["total"],
    )

    # Mock mesa repository
    mock_mesa_repository.get_by_id.return_value = MesaModel(**sample_mesa_data)

    # Mock get_last_sequence
    mock_repository.get_last_sequence_for_date_and_mesa.return_value = 0

    # Mock create
    created_pedido = PedidoModel(**sample_pedido_data)
    mock_repository.create.return_value = created_pedido

    # Act
    result = await pedido_service.create_pedido(pedido_create)

    # Assert
    assert result.id == sample_pedido_data["id"]
    assert result.numero_pedido == sample_pedido_data["numero_pedido"]
    assert result.estado == EstadoPedido.PENDIENTE
    mock_mesa_repository.get_by_id.assert_called_once()
    mock_repository.get_last_sequence_for_date_and_mesa.assert_called_once()
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_pedido_mesa_not_found(
    pedido_service, mock_mesa_repository
):
    """
    Prueba el manejo de errores cuando la mesa no existe.

    PRECONDICIONES:
        - El servicio debe estar configurado.

    PROCESO:
        - Configura el mock para simular que la mesa no existe.
        - Llama al método create_pedido.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar PedidoValidationError.
    """
    # Arrange
    pedido_create = PedidoCreate(
        id_mesa=str(ULID()),
        total=Decimal("100.00"),
    )
    mock_mesa_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(PedidoValidationError) as excinfo:
        await pedido_service.create_pedido(pedido_create)

    assert "No se encontró la mesa" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_pedido_by_id_success(
    pedido_service, mock_repository, sample_pedido_data
):
    """
    Prueba la obtención exitosa de un pedido por su ID.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia del pedido.
        - Llama al método get_pedido_by_id con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar el pedido correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    pedido_id = sample_pedido_data["id"]
    mock_repository.get_by_id.return_value = PedidoModel(**sample_pedido_data)

    # Act
    result = await pedido_service.get_pedido_by_id(pedido_id)

    # Assert
    assert result.id == pedido_id
    assert result.numero_pedido == sample_pedido_data["numero_pedido"]
    mock_repository.get_by_id.assert_called_once_with(pedido_id)


@pytest.mark.asyncio
async def test_get_pedido_by_id_not_found(pedido_service, mock_repository):
    """
    Prueba el manejo de errores al intentar obtener un pedido que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el pedido no existe.
        - Llama al método get_pedido_by_id con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar PedidoNotFoundError.
    """
    # Arrange
    pedido_id = str(ULID())
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(PedidoNotFoundError) as excinfo:
        await pedido_service.get_pedido_by_id(pedido_id)

    assert f"No se encontró el pedido con ID {pedido_id}" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_pedido_by_numero_success(
    pedido_service, mock_repository, sample_pedido_data
):
    """
    Prueba la obtención exitosa de un pedido por su número.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia del pedido.
        - Llama al método get_pedido_by_numero con un número válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar el pedido correctamente.
    """
    # Arrange
    numero_pedido = sample_pedido_data["numero_pedido"]
    mock_repository.get_by_numero_pedido.return_value = PedidoModel(**sample_pedido_data)

    # Act
    result = await pedido_service.get_pedido_by_numero(numero_pedido)

    # Assert
    assert result.numero_pedido == numero_pedido
    mock_repository.get_by_numero_pedido.assert_called_once_with(numero_pedido)


@pytest.mark.asyncio
async def test_delete_pedido_success(
    pedido_service, mock_repository, sample_pedido_data
):
    """
    Prueba la eliminación exitosa de un pedido.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia y eliminación exitosa del pedido.
        - Llama al método delete_pedido con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe eliminar el pedido correctamente.
    """
    # Arrange
    pedido_id = sample_pedido_data["id"]
    mock_repository.get_by_id.return_value = PedidoModel(**sample_pedido_data)
    mock_repository.delete.return_value = True

    # Act
    result = await pedido_service.delete_pedido(pedido_id)

    # Assert
    assert result is True
    mock_repository.get_by_id.assert_called_once_with(pedido_id)
    mock_repository.delete.assert_called_once_with(pedido_id)


@pytest.mark.asyncio
async def test_get_pedidos_success(
    pedido_service, mock_repository, sample_pedido_data
):
    """
    Prueba la obtención exitosa de una lista paginada de pedidos.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una lista de pedidos.
        - Llama al método get_pedidos con parámetros válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar la lista de pedidos correctamente.
    """
    # Arrange
    pedidos = [
        PedidoModel(**sample_pedido_data),
        PedidoModel(
            id=str(ULID()),
            id_mesa=str(ULID()),
            numero_pedido="20251026-M002-001",
            estado=EstadoPedido.CONFIRMADO,
            total=Decimal("200.00"),
        ),
    ]
    mock_repository.get_all.return_value = (pedidos, len(pedidos))

    # Act
    result = await pedido_service.get_pedidos(skip=0, limit=10)

    # Assert
    assert result.total == 2
    assert len(result.items) == 2
    mock_repository.get_all.assert_called_once_with(0, 10, None, None)


@pytest.mark.asyncio
async def test_update_pedido_success(
    pedido_service, mock_repository, sample_pedido_data
):
    """
    Prueba la actualización exitosa de un pedido.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la actualización exitosa.
        - Llama al método update_pedido con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe actualizar el pedido correctamente.
    """
    # Arrange
    pedido_id = sample_pedido_data["id"]
    update_data = PedidoUpdate(total=Decimal("150.00"))

    updated_pedido = PedidoModel(
        **{**sample_pedido_data, "total": Decimal("150.00")}
    )
    mock_repository.update.return_value = updated_pedido

    # Act
    result = await pedido_service.update_pedido(pedido_id, update_data)

    # Assert
    assert result.id == pedido_id
    assert result.total == Decimal("150.00")
    mock_repository.update.assert_called_once_with(pedido_id, total=Decimal("150.00"))


@pytest.mark.asyncio
async def test_cambiar_estado_success(
    pedido_service, mock_repository, sample_pedido_data
):
    """
    Prueba el cambio exitoso de estado de un pedido.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular el cambio de estado exitoso.
        - Llama al método cambiar_estado con un estado válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe cambiar el estado correctamente.
        - El timestamp correspondiente debe actualizarse.
    """
    # Arrange
    pedido_id = sample_pedido_data["id"]
    pedido_actual = PedidoModel(**sample_pedido_data)
    estado_data = PedidoEstadoUpdate(estado=EstadoPedido.CONFIRMADO)

    mock_repository.get_by_id.return_value = pedido_actual

    updated_pedido = PedidoModel(
        **{**sample_pedido_data, "estado": EstadoPedido.CONFIRMADO}
    )
    mock_repository.update.return_value = updated_pedido

    # Act
    result = await pedido_service.cambiar_estado(pedido_id, estado_data)

    # Assert
    assert result.estado == EstadoPedido.CONFIRMADO
    mock_repository.get_by_id.assert_called_once_with(pedido_id)
    mock_repository.update.assert_called_once()
    # Verificar que se pasó fecha_confirmado
    call_kwargs = mock_repository.update.call_args.kwargs
    assert "fecha_confirmado" in call_kwargs
    assert "estado" in call_kwargs
    assert call_kwargs["estado"] == EstadoPedido.CONFIRMADO


@pytest.mark.asyncio
async def test_cambiar_estado_invalid_transition(
    pedido_service, mock_repository, sample_pedido_data
):
    """
    Prueba el manejo de errores al intentar una transición de estado inválida.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un pedido en un estado específico.
        - Llama al método cambiar_estado con un estado inválido.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar PedidoStateTransitionError.
    """
    # Arrange
    pedido_id = sample_pedido_data["id"]
    pedido_entregado = PedidoModel(
        **{**sample_pedido_data, "estado": EstadoPedido.ENTREGADO}
    )
    estado_data = PedidoEstadoUpdate(estado=EstadoPedido.PENDIENTE)

    mock_repository.get_by_id.return_value = pedido_entregado

    # Act & Assert
    with pytest.raises(PedidoStateTransitionError) as excinfo:
        await pedido_service.cambiar_estado(pedido_id, estado_data)

    assert "Transición de estado inválida" in str(excinfo.value)
    mock_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_update_pedido_negative_amount(pedido_service):
    """
    Prueba el manejo de errores al intentar actualizar con valores negativos.

    PRECONDICIONES:
        - El servicio debe estar configurado.

    PROCESO:
        - Intenta crear un PedidoUpdate con valores negativos.
        - Verifica que Pydantic lance una excepción de validación.

    POSTCONDICIONES:
        - Pydantic debe rechazar valores negativos antes de llegar al servicio.
    """
    # Arrange
    from pydantic import ValidationError

    # Act & Assert
    # Pydantic valida en la creación del schema, no en el servicio
    with pytest.raises(ValidationError) as excinfo:
        update_data = PedidoUpdate(total=Decimal("-50.00"))

    # Verificar que el error es por el valor negativo
    assert "greater_than_equal" in str(excinfo.value)


@pytest.fixture
def mock_pedido_producto_repository():
    """
    Fixture que proporciona un mock del repositorio de pedido_producto.
    """
    repository = AsyncMock()
    return repository


@pytest.fixture
def mock_producto_repository():
    """
    Fixture que proporciona un mock del repositorio de productos.
    """
    repository = AsyncMock()
    return repository


@pytest.fixture
def mock_session():
    """
    Fixture que proporciona un mock de la sesión de base de datos.
    """
    session = AsyncMock()
    return session


@pytest.fixture
def pedido_service_completo(
    mock_repository,
    mock_mesa_repository,
    mock_pedido_producto_repository,
    mock_producto_repository,
    mock_session,
):
    """
    Fixture que proporciona una instancia del servicio con todos los repositorios mockeados.
    """
    service = PedidoService(mock_session)
    service.repository = mock_repository
    service.mesa_repository = mock_mesa_repository
    service.pedido_producto_repository = mock_pedido_producto_repository
    service.producto_repository = mock_producto_repository
    return service


@pytest.fixture
def sample_producto_mock():
    """
    Fixture que proporciona un mock de producto.
    """
    from unittest.mock import MagicMock
    producto = MagicMock()
    producto.id = str(ULID())
    producto.nombre = "Hamburguesa Clásica"
    producto.descripcion = "Hamburguesa con queso"
    producto.precio_base = Decimal("25.50")
    producto.disponible = True
    return producto


@pytest.mark.asyncio
async def test_create_pedido_completo_success(
    pedido_service_completo,
    mock_repository,
    mock_mesa_repository,
    mock_pedido_producto_repository,
    mock_producto_repository,
    mock_session,
    sample_mesa_data,
    sample_pedido_data,
    sample_producto_mock,
):
    """
    Prueba la creación exitosa de un pedido completo con items.

    PRECONDICIONES:
        - El servicio y todos los repositorios mock deben estar configurados.
        - Los datos de muestra deben ser válidos.

    PROCESO:
        - Configura los mocks para simular la existencia de mesa y productos.
        - Llama al método create_pedido_completo con datos válidos.
        - Verifica que el pedido y sus items se creen correctamente.

    POSTCONDICIONES:
        - Se debe crear un pedido con numero_pedido generado.
        - Se deben crear todos los items del pedido.
        - Los totales deben calcularse correctamente.
    """
    # Arrange
    mesa = MesaModel(**sample_mesa_data)
    producto = sample_producto_mock

    items = [
        PedidoItemCreate(
            id_producto=producto.id,
            cantidad=2,
            precio_unitario=Decimal("25.50"),
            precio_opciones=Decimal("3.00"),
            notas_personalizacion="Sin cebolla",
        )
    ]

    pedido_completo_data = PedidoCompletoCreate(
        id_mesa=mesa.id,
        items=items,
        notas_cliente="Mesa para evento",
        notas_cocina="Urgente",
    )

    # Mock de mesa
    mock_mesa_repository.get_by_id.return_value = mesa

    # Mock de producto
    mock_producto_repository.get_by_id.return_value = producto

    # Mock de get_last_sequence
    mock_repository.get_last_sequence_for_date_and_mesa.return_value = 0

    # Mock de create pedido
    created_pedido = PedidoModel(
        id=str(ULID()),
        id_mesa=mesa.id,
        numero_pedido="20251026-M001-001",
        estado=EstadoPedido.PENDIENTE,
        subtotal=Decimal("57.00"),  # (25.50 + 3.00) * 2
        impuestos=Decimal("0.00"),
        descuentos=Decimal("0.00"),
        total=Decimal("57.00"),
        notas_cliente="Mesa para evento",
        notas_cocina="Urgente",
    )
    mock_repository.create.return_value = created_pedido

    # Mock de create pedido_producto
    created_item = PedidoProductoModel(
        id=str(ULID()),
        id_pedido=created_pedido.id,
        id_producto=producto.id,
        cantidad=2,
        precio_unitario=Decimal("25.50"),
        precio_opciones=Decimal("3.00"),
        subtotal=Decimal("57.00"),
        notas_personalizacion="Sin cebolla",
    )
    mock_pedido_producto_repository.create.return_value = created_item

    # Act
    result = await pedido_service_completo.create_pedido_completo(pedido_completo_data)

    # Assert
    assert result.id == created_pedido.id
    assert result.numero_pedido == "20251026-M001-001"
    assert result.estado == EstadoPedido.PENDIENTE
    assert result.subtotal == Decimal("57.00")
    assert result.total == Decimal("57.00")
    assert len(result.items) == 1
    assert result.items[0].cantidad == 2

    # Mesa repository is called twice: once for validation, once for _generate_numero_pedido
    assert mock_mesa_repository.get_by_id.call_count == 2
    mock_producto_repository.get_by_id.assert_called_once_with(producto.id)
    mock_repository.create.assert_called_once()
    mock_pedido_producto_repository.create.assert_called_once()
    mock_session.flush.assert_called_once()


@pytest.mark.asyncio
async def test_create_pedido_completo_mesa_not_found(
    pedido_service_completo, mock_mesa_repository, sample_producto_mock
):
    """
    Prueba el manejo de errores cuando la mesa no existe.

    PRECONDICIONES:
        - El servicio debe estar configurado.
        - La mesa especificada no debe existir.

    PROCESO:
        - Configura el mock para simular que la mesa no existe.
        - Llama al método create_pedido_completo.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar PedidoValidationError.
    """
    # Arrange
    items = [
        PedidoItemCreate(
            id_producto=str(ULID()),
            cantidad=1,
            precio_unitario=Decimal("25.50"),
            precio_opciones=Decimal("0.00"),
        )
    ]

    pedido_completo_data = PedidoCompletoCreate(
        id_mesa=str(ULID()), items=items
    )

    mock_mesa_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(PedidoValidationError) as excinfo:
        await pedido_service_completo.create_pedido_completo(pedido_completo_data)

    assert "No se encontró la mesa" in str(excinfo.value)


@pytest.mark.asyncio
async def test_create_pedido_completo_producto_not_found(
    pedido_service_completo,
    mock_mesa_repository,
    mock_producto_repository,
    sample_mesa_data,
):
    """
    Prueba el manejo de errores cuando un producto no existe.

    PRECONDICIONES:
        - El servicio debe estar configurado.
        - La mesa debe existir.
        - El producto especificado no debe existir.

    PROCESO:
        - Configura los mocks para simular que el producto no existe.
        - Llama al método create_pedido_completo.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar PedidoValidationError.
    """
    # Arrange
    mesa = MesaModel(**sample_mesa_data)

    items = [
        PedidoItemCreate(
            id_producto=str(ULID()),
            cantidad=1,
            precio_unitario=Decimal("25.50"),
            precio_opciones=Decimal("0.00"),
        )
    ]

    pedido_completo_data = PedidoCompletoCreate(
        id_mesa=mesa.id, items=items
    )

    mock_mesa_repository.get_by_id.return_value = mesa
    mock_producto_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(PedidoValidationError) as excinfo:
        await pedido_service_completo.create_pedido_completo(pedido_completo_data)

    assert "No se encontró el producto" in str(excinfo.value)


@pytest.mark.asyncio
async def test_create_pedido_completo_producto_not_available(
    pedido_service_completo,
    mock_mesa_repository,
    mock_producto_repository,
    sample_mesa_data,
    sample_producto_mock,
):
    """
    Prueba el manejo de errores cuando un producto no está disponible.

    PRECONDICIONES:
        - El servicio debe estar configurado.
        - La mesa y producto deben existir.
        - El producto debe estar marcado como no disponible.

    PROCESO:
        - Configura los mocks para simular un producto no disponible.
        - Llama al método create_pedido_completo.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar PedidoValidationError.
    """
    # Arrange
    from unittest.mock import MagicMock
    mesa = MesaModel(**sample_mesa_data)
    producto = MagicMock()
    producto.id = sample_producto_mock.id
    producto.nombre = sample_producto_mock.nombre
    producto.disponible = False

    items = [
        PedidoItemCreate(
            id_producto=producto.id,
            cantidad=1,
            precio_unitario=Decimal("25.50"),
            precio_opciones=Decimal("0.00"),
        )
    ]

    pedido_completo_data = PedidoCompletoCreate(
        id_mesa=mesa.id, items=items
    )

    mock_mesa_repository.get_by_id.return_value = mesa
    mock_producto_repository.get_by_id.return_value = producto

    # Act & Assert
    with pytest.raises(PedidoValidationError) as excinfo:
        await pedido_service_completo.create_pedido_completo(pedido_completo_data)

    assert "no está disponible" in str(excinfo.value)
