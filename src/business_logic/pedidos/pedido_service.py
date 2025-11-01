"""
Servicio para la gestión de pedidos en el sistema.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.pedidos.pedido_repository import PedidoRepository
from src.repositories.mesas.mesa_repository import MesaRepository
from src.repositories.pedidos.pedido_producto_repository import PedidoProductoRepository
from src.repositories.pedidos.pedido_opcion_repository import PedidoOpcionRepository
from src.repositories.menu.producto_repository import ProductoRepository
from src.repositories.pedidos.producto_opcion_repository import ProductoOpcionRepository
from src.models.pedidos.pedido_model import PedidoModel
from src.models.pedidos.pedido_producto_model import PedidoProductoModel
from src.models.pedidos.pedido_opcion_model import PedidoOpcionModel
from src.api.schemas.pedido_schema import (
    PedidoCreate,
    PedidoUpdate,
    PedidoResponse,
    PedidoSummary,
    PedidoList,
    PedidoEstadoUpdate,
    PedidoCompletoCreate,
    PedidoCompletoResponse,
)
from src.api.schemas.pedido_producto_schema import PedidoProductoResponse
from src.api.schemas.pedido_opcion_schema import PedidoOpcionResponse
from src.api.schemas.pedido_schema import PedidoProductoWithOpcionesResponse
from src.business_logic.exceptions.pedido_exceptions import (
    PedidoValidationError,
    PedidoNotFoundError,
    PedidoConflictError,
    PedidoStateTransitionError,
)
from src.core.enums.pedido_enums import EstadoPedido


class PedidoService:
    """Servicio para la gestión de pedidos en el sistema.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con pedidos, incluyendo validaciones, generación de número de pedido,
    gestión de estados y manejo de excepciones.

    Attributes
    ----------
    repository : PedidoRepository
        Repositorio para acceso a datos de pedidos.
    mesa_repository : MesaRepository
        Repositorio para validar mesas.
    """

    # Transiciones de estado válidas
    VALID_TRANSITIONS = {
        EstadoPedido.PENDIENTE: [EstadoPedido.CONFIRMADO, EstadoPedido.CANCELADO],
        EstadoPedido.CONFIRMADO: [EstadoPedido.EN_PREPARACION, EstadoPedido.CANCELADO],
        EstadoPedido.EN_PREPARACION: [EstadoPedido.LISTO, EstadoPedido.CANCELADO],
        EstadoPedido.LISTO: [EstadoPedido.ENTREGADO],
        EstadoPedido.ENTREGADO: [],
        EstadoPedido.CANCELADO: [],
    }

    def __init__(self, session: AsyncSession):
        """
        Inicializa el servicio con una sesión de base de datos.

        Parameters
        ----------
        session : AsyncSession
            Sesión asíncrona de SQLAlchemy para realizar operaciones en la base de datos.
        """
        self.repository = PedidoRepository(session)
        self.mesa_repository = MesaRepository(session)
        self.pedido_producto_repository = PedidoProductoRepository(session)
        self.pedido_opcion_repository = PedidoOpcionRepository(session)
        self.producto_repository = ProductoRepository(session)
        self.producto_opcion_repository = ProductoOpcionRepository(session)
        self.session = session

    async def _generate_numero_pedido(self, id_mesa: str) -> str:
        """
        Genera un número de pedido único con formato YYYYMMDD-M{numero_mesa}-{seq:03d}.

        Parameters
        ----------
        id_mesa : str
            ID de la mesa (ULID).

        Returns
        -------
        str
            Número de pedido generado.

        Raises
        ------
        PedidoValidationError
            Si la mesa no existe.
        """
        # Obtener la mesa para extraer el número
        mesa = await self.mesa_repository.get_by_id(id_mesa)
        if not mesa:
            raise PedidoValidationError(f"No se encontró la mesa con ID {id_mesa}")

        # Obtener la fecha actual
        now = datetime.now()
        date_str = now.strftime("%Y%m%d")

        # Obtener la última secuencia para esta fecha y mesa
        last_seq = await self.repository.get_last_sequence_for_date_and_mesa(
            now, mesa.numero
        )
        new_seq = last_seq + 1

        # Generar el número de pedido
        numero_pedido = f"{date_str}-M{mesa.numero}-{new_seq:03d}"

        return numero_pedido

    async def create_pedido(self, pedido_data: PedidoCreate) -> PedidoResponse:
        """
        Crea un nuevo pedido en el sistema.

        Parameters
        ----------
        pedido_data : PedidoCreate
            Datos para crear el nuevo pedido.

        Returns
        -------
        PedidoResponse
            Esquema de respuesta con los datos del pedido creado.

        Raises
        ------
        PedidoConflictError
            Si ya existe un pedido con el mismo número.
        PedidoValidationError
            Si los datos son inválidos o la mesa no existe.
        """
        try:
            # Generar número de pedido automáticamente
            numero_pedido = await self._generate_numero_pedido(pedido_data.id_mesa)

            # Crear modelo de pedido desde los datos
            pedido = PedidoModel(
                id_mesa=pedido_data.id_mesa,
                numero_pedido=numero_pedido,
                estado=EstadoPedido.PENDIENTE,
                subtotal=pedido_data.subtotal or Decimal("0.00"),
                impuestos=pedido_data.impuestos or Decimal("0.00"),
                descuentos=pedido_data.descuentos or Decimal("0.00"),
                total=pedido_data.total or Decimal("0.00"),
                notas_cliente=pedido_data.notas_cliente,
                notas_cocina=pedido_data.notas_cocina,
            )

            # Persistir en la base de datos
            created_pedido = await self.repository.create(pedido)

            # Convertir y retornar como esquema de respuesta
            return PedidoResponse.model_validate(created_pedido)
        except IntegrityError:
            # Capturar errores de integridad (numero_pedido duplicado, FK inválida)
            raise PedidoConflictError(
                f"Error al crear el pedido. Posible conflicto con numero_pedido o FK inválida"
            )

    async def get_pedido_by_id(self, pedido_id: str) -> PedidoResponse:
        """
        Obtiene un pedido por su ID.

        Parameters
        ----------
        pedido_id : str
            Identificador único del pedido a buscar (ULID).

        Returns
        -------
        PedidoResponse
            Esquema de respuesta con los datos del pedido.

        Raises
        ------
        PedidoNotFoundError
            Si no se encuentra un pedido con el ID proporcionado.
        """
        # Buscar el pedido por su ID
        pedido = await self.repository.get_by_id(pedido_id)

        # Verificar si existe
        if not pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        # Convertir y retornar como esquema de respuesta
        return PedidoResponse.model_validate(pedido)

    async def get_pedido_by_numero(self, numero_pedido: str) -> PedidoResponse:
        """
        Obtiene un pedido por su número único.

        Parameters
        ----------
        numero_pedido : str
            Número único del pedido a buscar.

        Returns
        -------
        PedidoResponse
            Esquema de respuesta con los datos del pedido.

        Raises
        ------
        PedidoNotFoundError
            Si no se encuentra un pedido con el número proporcionado.
        """
        # Buscar el pedido por su número
        pedido = await self.repository.get_by_numero_pedido(numero_pedido)

        # Verificar si existe
        if not pedido:
            raise PedidoNotFoundError(
                f"No se encontró el pedido con número {numero_pedido}"
            )

        # Convertir y retornar como esquema de respuesta
        return PedidoResponse.model_validate(pedido)

    async def delete_pedido(self, pedido_id: str) -> bool:
        """
        Elimina un pedido por su ID.

        Parameters
        ----------
        pedido_id : str
            Identificador único del pedido a eliminar (ULID).

        Returns
        -------
        bool
            True si el pedido fue eliminado correctamente.

        Raises
        ------
        PedidoNotFoundError
            Si no se encuentra un pedido con el ID proporcionado.
        """
        # Verificar primero si el pedido existe
        pedido = await self.repository.get_by_id(pedido_id)
        if not pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        # Eliminar el pedido
        result = await self.repository.delete(pedido_id)
        return result

    async def get_pedidos(
        self,
        skip: int = 0,
        limit: int = 100,
        estado: Optional[EstadoPedido] = None,
        id_mesa: Optional[str] = None,
    ) -> PedidoList:
        """
        Obtiene una lista paginada de pedidos.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.
        estado : EstadoPedido, optional
            Filtrar por estado del pedido.
        id_mesa : str, optional
            Filtrar por ID de mesa.

        Returns
        -------
        PedidoList
            Esquema con la lista de pedidos y el total.
        """
        # Validar parámetros de entrada
        if skip < 0:
            raise PedidoValidationError(
                "El parámetro 'skip' debe ser mayor o igual a cero"
            )
        if limit < 1:
            raise PedidoValidationError("El parámetro 'limit' debe ser mayor a cero")

        # Obtener pedidos desde el repositorio
        pedidos, total = await self.repository.get_all(skip, limit, estado, id_mesa)

        # Convertir modelos a esquemas de resumen
        pedido_summaries = [PedidoSummary.model_validate(pedido) for pedido in pedidos]

        # Retornar esquema de lista
        return PedidoList(items=pedido_summaries, total=total)

    async def update_pedido(
        self, pedido_id: str, pedido_data: PedidoUpdate
    ) -> PedidoResponse:
        """
        Actualiza un pedido existente.

        Parameters
        ----------
        pedido_id : str
            Identificador único del pedido a actualizar (ULID).
        pedido_data : PedidoUpdate
            Datos para actualizar el pedido.

        Returns
        -------
        PedidoResponse
            Esquema de respuesta con los datos del pedido actualizado.

        Raises
        ------
        PedidoNotFoundError
            Si no se encuentra un pedido con el ID proporcionado.
        PedidoValidationError
            Si los datos de actualización son inválidos.
        """
        # Convertir el esquema de actualización a un diccionario,
        # excluyendo valores None (campos no proporcionados para actualizar)
        update_data = pedido_data.model_dump(exclude_none=True)

        if not update_data:
            # Si no hay datos para actualizar, simplemente retornar el pedido actual
            return await self.get_pedido_by_id(pedido_id)

        # Validar que los valores monetarios sean positivos
        for field in ["subtotal", "impuestos", "descuentos", "total"]:
            if field in update_data and update_data[field] < 0:
                raise PedidoValidationError(
                    f"El campo '{field}' debe ser mayor o igual a cero"
                )

        try:
            # Actualizar el pedido
            updated_pedido = await self.repository.update(pedido_id, **update_data)

            # Verificar si el pedido fue encontrado
            if not updated_pedido:
                raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

            # Convertir y retornar como esquema de respuesta
            return PedidoResponse.model_validate(updated_pedido)
        except IntegrityError:
            # Capturar errores de integridad (FK inválida)
            raise PedidoValidationError(
                "Error al actualizar el pedido. Verifique los datos proporcionados"
            )

    async def cambiar_estado(
        self, pedido_id: str, estado_data: PedidoEstadoUpdate
    ) -> PedidoResponse:
        """
        Cambia el estado de un pedido y actualiza el timestamp correspondiente.

        Parameters
        ----------
        pedido_id : str
            Identificador único del pedido.
        estado_data : PedidoEstadoUpdate
            Nuevo estado del pedido.

        Returns
        -------
        PedidoResponse
            Esquema de respuesta con los datos del pedido actualizado.

        Raises
        ------
        PedidoNotFoundError
            Si no se encuentra el pedido.
        PedidoStateTransitionError
            Si la transición de estado no es válida.
        """
        # Obtener el pedido actual
        pedido = await self.repository.get_by_id(pedido_id)
        if not pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        # Validar la transición de estado
        nuevo_estado = estado_data.estado
        if nuevo_estado not in self.VALID_TRANSITIONS.get(pedido.estado, []):
            raise PedidoStateTransitionError(
                f"Transición de estado inválida: {pedido.estado.value} -> {nuevo_estado.value}"
            )

        # Preparar los datos de actualización
        update_fields = {}
        update_fields["estado"] = nuevo_estado

        # Actualizar el timestamp correspondiente al nuevo estado
        now = datetime.now()
        if nuevo_estado == EstadoPedido.CONFIRMADO:
            update_fields["fecha_confirmado"] = now
        elif nuevo_estado == EstadoPedido.EN_PREPARACION:
            update_fields["fecha_en_preparacion"] = now
        elif nuevo_estado == EstadoPedido.LISTO:
            update_fields["fecha_listo"] = now
        elif nuevo_estado == EstadoPedido.ENTREGADO:
            update_fields["fecha_entregado"] = now
        elif nuevo_estado == EstadoPedido.CANCELADO:
            update_fields["fecha_cancelado"] = now

        # Actualizar el pedido
        updated_pedido = await self.repository.update(pedido_id, **update_fields)

        # Convertir y retornar como esquema de respuesta
        return PedidoResponse.model_validate(updated_pedido)

    async def create_pedido_completo(
        self, pedido_data: PedidoCompletoCreate
    ) -> PedidoCompletoResponse:
        """
        Crea un pedido completo con sus items en una sola transacción.

        Este método crea un pedido y todos sus items de forma atómica, calculando
        automáticamente los totales basándose en los items proporcionados.

        Parameters
        ----------
        pedido_data : PedidoCompletoCreate
            Datos del pedido completo con su lista de items.

        Returns
        -------
        PedidoCompletoResponse
            Esquema de respuesta con el pedido y sus items creados.

        Raises
        ------
        PedidoValidationError
            Si los datos son inválidos, la mesa no existe, o algún producto
            no existe o no está disponible.
        PedidoConflictError
            Si hay un conflicto de integridad en la base de datos.
        """
        try:
            # Validar que la mesa existe
            mesa = await self.mesa_repository.get_by_id(pedido_data.id_mesa)
            if not mesa:
                raise PedidoValidationError(
                    f"No se encontró la mesa con ID {pedido_data.id_mesa}"
                )

            # Validar que todos los productos existen y están disponibles
            for item in pedido_data.items:
                producto = await self.producto_repository.get_by_id(item.id_producto)
                if not producto:
                    raise PedidoValidationError(
                        f"No se encontró el producto con ID {item.id_producto}"
                    )
                if not producto.disponible:
                    raise PedidoValidationError(
                        f"El producto '{producto.nombre}' no está disponible actualmente"
                    )

                # Validar que todas las opciones existen
                for opcion in item.opciones:
                    producto_opcion = await self.producto_opcion_repository.get_by_id(opcion.id_producto_opcion)
                    if not producto_opcion:
                        raise PedidoValidationError(
                            f"No se encontró la opción de producto con ID {opcion.id_producto_opcion}"
                        )

            # Generar número de pedido
            numero_pedido = await self._generate_numero_pedido(pedido_data.id_mesa)

            # Calcular subtotal sumando todos los items
            subtotal = Decimal("0.00")
            for item in pedido_data.items:
                # Calcular precio_opciones sumando todas las opciones
                precio_opciones = sum(opcion.precio_adicional for opcion in item.opciones)
                precio_total_unitario = item.precio_unitario + precio_opciones
                item_subtotal = Decimal(str(item.cantidad)) * precio_total_unitario
                subtotal += item_subtotal

            # Por ahora no calculamos impuestos ni descuentos, solo el total = subtotal
            total = subtotal

            # Crear el pedido
            pedido = PedidoModel(
                id_mesa=pedido_data.id_mesa,
                numero_pedido=numero_pedido,
                estado=EstadoPedido.PENDIENTE,
                subtotal=subtotal,
                impuestos=Decimal("0.00"),
                descuentos=Decimal("0.00"),
                total=total,
                notas_cliente=pedido_data.notas_cliente,
                notas_cocina=pedido_data.notas_cocina,
            )

            # Persistir el pedido
            created_pedido = await self.repository.create(pedido)

            # Crear todos los items del pedido con sus opciones
            created_items_with_opciones = []
            for item_data in pedido_data.items:
                # Calcular precio_opciones sumando todas las opciones
                precio_opciones = sum(opcion.precio_adicional for opcion in item_data.opciones)
                precio_total_unitario = item_data.precio_unitario + precio_opciones
                item_subtotal = Decimal(str(item_data.cantidad)) * precio_total_unitario

                # Crear el item
                item = PedidoProductoModel(
                    id_pedido=created_pedido.id,
                    id_producto=item_data.id_producto,
                    cantidad=item_data.cantidad,
                    precio_unitario=item_data.precio_unitario,
                    precio_opciones=precio_opciones,
                    subtotal=item_subtotal,
                    notas_personalizacion=item_data.notas_personalizacion,
                )

                # Persistir el item
                created_item = await self.pedido_producto_repository.create(item)

                # Crear las opciones para este item
                created_opciones = []
                for opcion_data in item_data.opciones:
                    opcion = PedidoOpcionModel(
                        id_pedido_producto=created_item.id,
                        id_producto_opcion=opcion_data.id_producto_opcion,
                        precio_adicional=opcion_data.precio_adicional,
                    )
                    created_opcion = await self.pedido_opcion_repository.create(opcion)
                    created_opciones.append(created_opcion)

                # Guardar item con sus opciones
                created_items_with_opciones.append((created_item, created_opciones))

            # Commit de la transacción (si usamos flush automáticamente)
            await self.session.flush()

            # Construir la respuesta completa con items y opciones
            pedido_response = PedidoResponse.model_validate(created_pedido)

            # Construir items con opciones
            items_with_opciones_response = []
            for item, opciones in created_items_with_opciones:
                # Convertir el item
                item_dict = {
                    "id": item.id,
                    "id_pedido": item.id_pedido,
                    "id_producto": item.id_producto,
                    "cantidad": item.cantidad,
                    "precio_unitario": item.precio_unitario,
                    "precio_opciones": item.precio_opciones,
                    "subtotal": item.subtotal,
                    "notas_personalizacion": item.notas_personalizacion,
                    "fecha_creacion": item.fecha_creacion,
                    "fecha_modificacion": item.fecha_modificacion,
                    "opciones": [PedidoOpcionResponse.model_validate(opcion) for opcion in opciones]
                }
                items_with_opciones_response.append(PedidoProductoWithOpcionesResponse(**item_dict))

            # Crear el objeto de respuesta completo
            response_dict = pedido_response.model_dump()
            response_dict["items"] = items_with_opciones_response

            return PedidoCompletoResponse(**response_dict)

        except IntegrityError as e:
            # Rollback implícito por SQLAlchemy
            raise PedidoConflictError(
                f"Error al crear el pedido completo. Conflicto de integridad: {str(e)}"
            )
