"""
Servicio para la gestión de opciones de productos por tipo en el sistema.
"""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.pedidos.producto_tipo_opcion_repository import ProductoTipoOpcionRepository
from src.models.pedidos.producto_tipo_opcion_model import ProductoTipoOpcionModel
from src.api.schemas.producto_tipo_opcion_schema import (
    ProductoTipoOpcionCreate,
    ProductoTipoOpcionUpdate,
    ProductoTipoOpcionResponse,
    ProductoTipoOpcionSummary,
    ProductoTipoOpcionList,
)
from src.business_logic.exceptions.producto_tipo_opcion_exceptions import (
    ProductoTipoOpcionValidationError,
    ProductoTipoOpcionNotFoundError,
    ProductoTipoOpcionConflictError,
)


class ProductoTipoOpcionService:
    """Servicio para la gestión de opciones de productos por tipo en el sistema.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con opciones de productos por tipo, incluyendo validaciones, transformaciones y manejo de excepciones.

    Attributes
    ----------
    repository : ProductoTipoOpcionRepository
        Repositorio para acceso a datos de opciones de productos por tipo.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el servicio con una sesión de base de datos.

        Parameters
        ----------
        session : AsyncSession
            Sesión asíncrona de SQLAlchemy para realizar operaciones en la base de datos.
        """
        self.repository = ProductoTipoOpcionRepository(session)

    async def create_producto_tipo_opcion(self, producto_tipo_opcion_data: ProductoTipoOpcionCreate) -> ProductoTipoOpcionResponse:
        """
        Crea una nueva opción de producto en el sistema.
        
        Parameters
        ----------
        producto_tipo_opcion_data : ProductoTipoOpcionCreate
            Datos para crear la nueva opción de producto por tipo.

        Returns
        -------
        ProductoTipoOpcionResponse
            Esquema de respuesta con los datos de la opción de producto por tipo creada.

        Raises
        ------
        ProductoTipoOpcionConflictError
            Si ya existe una opción de producto por tipo con la misma combinación de datos.
        """
        try:
            # Crear modelo de opción de producto por tipo desde los datos
            producto_tipo_opcion = ProductoTipoOpcionModel(
                id_producto=producto_tipo_opcion_data.id_producto,
                id_tipo_opcion=producto_tipo_opcion_data.id_tipo_opcion,
                nombre=producto_tipo_opcion_data.nombre,
                precio_adicional=producto_tipo_opcion_data.precio_adicional,
                activo=producto_tipo_opcion_data.activo,
                orden=producto_tipo_opcion_data.orden
            )

            # Persistir en la base de datos
            created_producto_tipo_opcion = await self.repository.create(producto_tipo_opcion)

            # Convertir y retornar como esquema de respuesta
            return ProductoTipoOpcionResponse.model_validate(created_producto_tipo_opcion)
        except IntegrityError:
            # Capturar errores de integridad
            raise ProductoTipoOpcionConflictError(
                f"Ya existe una opción de producto por tipo con el nombre '{producto_tipo_opcion_data.nombre}'"
            )

    async def get_producto_tipo_opcion_by_id(self, producto_tipo_opcion_id: UUID) -> ProductoTipoOpcionResponse:
        """
        Obtiene una opción de producto por su ID.

        Parameters
        ----------
        producto_tipo_opcion_id : UUID
            Identificador único de la opción de producto por tipo a buscar.

        Returns
        -------
        ProductoTipoOpcionResponse
            Esquema de respuesta con los datos de la opción de producto por tipo.

        Raises
        ------
        ProductoTipoOpcionNotFoundError
            Si no se encuentra una opción de producto por tipo con el ID proporcionado.
        """
        # Buscar la opción de producto por tipo por su ID
        producto_tipo_opcion = await self.repository.get_by_id(producto_tipo_opcion_id)

        # Verificar si existe
        if not producto_tipo_opcion:
            raise ProductoTipoOpcionNotFoundError(f"No se encontró la opción de producto por tipo con ID {producto_tipo_opcion_id}")

        # Convertir y retornar como esquema de respuesta
        return ProductoTipoOpcionResponse.model_validate(producto_tipo_opcion)

    async def delete_producto_tipo_opcion(self, producto_tipo_opcion_id: UUID) -> bool:
        """
        Elimina una opción de producto por su ID.
        
        Parameters
        ----------
        producto_tipo_opcion_id : UUID
            Identificador único de la opción de producto por tipo a eliminar.

        Returns
        -------
        bool
            True si la opción de producto por tipo fue eliminada correctamente.

        Raises
        ------
        ProductoTipoOpcionNotFoundError
            Si no se encuentra una opción de producto por tipo con el ID proporcionado.
        """
        # Verificar primero si la opción de producto por tipo existe
        producto_tipo_opcion = await self.repository.get_by_id(producto_tipo_opcion_id)
        if not producto_tipo_opcion:
            raise ProductoTipoOpcionNotFoundError(f"No se encontró la opción de producto por tipo con ID {producto_tipo_opcion_id}")

        # Eliminar la opción de producto por tipo
        result = await self.repository.delete(producto_tipo_opcion_id)
        return result

    async def get_producto_tipo_opciones(self, skip: int = 0, limit: int = 100) -> ProductoTipoOpcionList:
        """
        Obtiene una lista paginada de opciones de productos.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        ProductoTipoOpcionList
            Esquema con la lista de opciones de productos por tipo y el total.
        """
        # Validar parámetros de entrada
        if skip < 0:
            raise ProductoTipoOpcionValidationError(
                "El parámetro 'skip' debe ser mayor o igual a cero"
            )
        if limit < 1:
            raise ProductoTipoOpcionValidationError("El parámetro 'limit' debe ser mayor a cero")

        # Obtener opciones de productos por tipo desde el repositorio
        producto_tipo_opciones, total = await self.repository.get_all(skip, limit)

        # Convertir modelos a esquemas de resumen
        producto_tipo_opcion_summaries = [ProductoTipoOpcionSummary.model_validate(pto) for pto in producto_tipo_opciones]

        # Retornar esquema de lista
        return ProductoTipoOpcionList(items=producto_tipo_opcion_summaries, total=total)

    async def update_producto_tipo_opcion(self, producto_tipo_opcion_id: UUID, producto_tipo_opcion_data: ProductoTipoOpcionUpdate) -> ProductoTipoOpcionResponse:
        """
        Actualiza una opción de producto existente.

        Parameters
        ----------
        producto_tipo_opcion_id : UUID
            Identificador único de la opción de producto por tipo a actualizar.
        producto_tipo_opcion_data : ProductoTipoOpcionUpdate
            Datos para actualizar la opción de producto por tipo.

        Returns
        -------
        ProductoTipoOpcionResponse
            Esquema de respuesta con los datos de la opción de producto por tipo actualizada.

        Raises
        ------
        ProductoTipoOpcionNotFoundError
            Si no se encuentra una opción de producto por tipo con el ID proporcionado.
        ProductoTipoOpcionConflictError
            Si ya existe otra opción de producto por tipo con el mismo nombre.
        """
        # Convertir el esquema de actualización a un diccionario,
        # excluyendo valores None (campos no proporcionados para actualizar)
        update_data = producto_tipo_opcion_data.model_dump(exclude_none=True)

        if not update_data:
            # Si no hay datos para actualizar, simplemente retornar la opción de producto por tipo actual
            return await self.get_producto_tipo_opcion_by_id(producto_tipo_opcion_id)

        try:
            # Actualizar la opción de producto por tipo
            updated_producto_tipo_opcion = await self.repository.update(producto_tipo_opcion_id, **update_data)

            # Verificar si la opción de producto por tipo fue encontrada
            if not updated_producto_tipo_opcion:
                raise ProductoTipoOpcionNotFoundError(f"No se encontró la opción de producto por tipo con ID {producto_tipo_opcion_id}")

            # Convertir y retornar como esquema de respuesta
            return ProductoTipoOpcionResponse.model_validate(updated_producto_tipo_opcion)
        except IntegrityError:
            # Capturar errores de integridad
            if "nombre" in update_data:
                raise ProductoTipoOpcionConflictError(
                    f"Ya existe una opción de producto por tipo con el nombre '{update_data['nombre']}'"
                )
            # Si no es por nombre, reenviar la excepción original
            raise
