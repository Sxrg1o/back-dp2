"""
Servicio para la gestión de productos en el sistema.
"""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.menu.producto_repository import ProductoRepository
from src.models.menu.producto_model import ProductoModel
from src.api.schemas.producto_schema import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
    ProductoSummary,
    ProductoList,
    ProductoCard,
    ProductoCardList,
    ProductoConOpcionesResponse,
)
from src.business_logic.exceptions.producto_exceptions import (
    ProductoValidationError,
    ProductoNotFoundError,
    ProductoConflictError,
)


class ProductoService:
    """Servicio para la gestión de productos en el sistema.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con productos, incluyendo validaciones, transformaciones y manejo de excepciones.

    Attributes
    ----------
    repository : ProductoRepository
        Repositorio para acceso a datos de productos.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el servicio con una sesión de base de datos.

        Parameters
        ----------
        session : AsyncSession
            Sesión asíncrona de SQLAlchemy para realizar operaciones en la base de datos.
        """
        self.repository = ProductoRepository(session)

    async def create_producto(self, producto_data: ProductoCreate) -> ProductoResponse:
        """
        Crea un nuevo producto en el sistema.
        
        Parameters
        ----------
        producto_data : ProductoCreate
            Datos para crear el nuevo producto.

        Returns
        -------
        ProductoResponse
            Esquema de respuesta con los datos del producto creado.

        Raises
        ------
        ProductoConflictError
            Si ya existe un producto con el mismo nombre.
        """
        try:
            # Crear modelo de producto desde los datos
            producto = ProductoModel(
                id_categoria=producto_data.id_categoria,
                nombre=producto_data.nombre,
                descripcion=producto_data.descripcion,
                precio_base=producto_data.precio_base,
                imagen_path=producto_data.imagen_path,
                imagen_alt_text=producto_data.imagen_alt_text,
            )

            # Persistir en la base de datos
            created_producto = await self.repository.create(producto)

            # Convertir y retornar como esquema de respuesta
            return ProductoResponse.model_validate(created_producto)
        except IntegrityError:
            # Capturar errores de integridad (nombre duplicado)
            raise ProductoConflictError(
                f"Ya existe un producto con el nombre '{producto_data.nombre}'"
            )

    async def get_producto_by_id(self, producto_id: UUID) -> ProductoResponse:
        """
        Obtiene un producto por su ID.

        Parameters
        ----------
        producto_id : UUID
            Identificador único del producto a buscar.

        Returns
        -------
        ProductoResponse
            Esquema de respuesta con los datos del producto.

        Raises
        ------
        ProductoNotFoundError
            Si no se encuentra un producto con el ID proporcionado.
        """
        # Buscar el producto por su ID
        producto = await self.repository.get_by_id(producto_id)

        # Verificar si existe
        if not producto:
            raise ProductoNotFoundError(f"No se encontró el producto con ID {producto_id}")

        # Convertir y retornar como esquema de respuesta
        return ProductoResponse.model_validate(producto)

    async def get_producto_con_opciones(self, producto_id: UUID) -> "ProductoConOpcionesResponse":
        """
        Obtiene un producto por su ID con todas sus opciones.
        
        Parameters
        ----------
        producto_id : UUID
            Identificador único del producto a buscar.
            
        Returns
        -------
        ProductoConOpcionesResponse
            Esquema de respuesta con el producto y todas sus opciones.
            
        Raises
        ------
        ProductoNotFoundError
            Si no se encuentra un producto con el ID proporcionado.
        """
        from src.api.schemas.producto_schema import ProductoConOpcionesResponse
        
        # Buscar el producto con opciones (eager loading)
        producto = await self.repository.get_by_id_with_opciones(producto_id)
        
        # Verificar si existe
        if not producto:
            raise ProductoNotFoundError(f"No se encontró el producto con ID {producto_id}")
        
        # Convertir y retornar como esquema de respuesta
        return ProductoConOpcionesResponse.model_validate(producto)

    async def delete_producto(self, producto_id: UUID) -> bool:
        """
        Elimina un producto por su ID.
        
        Parameters
        ----------
        producto_id : UUID
            Identificador único del producto a eliminar.

        Returns
        -------
        bool
            True si el producto fue eliminado correctamente.

        Raises
        ------
        ProductoNotFoundError
            Si no se encuentra un producto con el ID proporcionado.
        """
        # Verificar primero si el producto existe
        producto = await self.repository.get_by_id(producto_id)
        if not producto:
            raise ProductoNotFoundError(f"No se encontró el producto con ID {producto_id}")

        # Eliminar el producto
        result = await self.repository.delete(producto_id)
        return result

    async def get_productos(    
        self, 
        skip: int = 0, 
        limit: int = 100,
        id_categoria: UUID | None = None
    ) -> ProductoList:
        """
        Obtiene una lista paginada de productos.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        ProductoList
            Esquema con la lista de productos y el total.
        """
        # Validar parámetros de entrada
        if skip < 0:
            raise ProductoValidationError(
                "El parámetro 'skip' debe ser mayor o igual a cero"
            )
        if limit < 1:
            raise ProductoValidationError("El parámetro 'limit' debe ser mayor a cero")

        # Obtener productos desde el repositorio
        productos, total = await self.repository.get_all(skip, limit, id_categoria)

        # Convertir modelos a esquemas de resumen
        producto_summaries = [ProductoSummary.model_validate(producto) for producto in productos]

        # Retornar esquema de lista
        return ProductoList(items=producto_summaries, total=total)

    async def update_producto(self, producto_id: UUID, producto_data: ProductoUpdate) -> ProductoResponse:
        """
        Actualiza un producto existente.

        Parameters
        ----------
        producto_id : UUID
            Identificador único del producto a actualizar.
        producto_data : ProductoUpdate
            Datos para actualizar el producto.

        Returns
        -------
        ProductoResponse
            Esquema de respuesta con los datos del producto actualizado.

        Raises
        ------
        ProductoNotFoundError
            Si no se encuentra un producto con el ID proporcionado.
        ProductoConflictError
            Si ya existe otro producto con el mismo nombre.
        """
        # Convertir el esquema de actualización a un diccionario,
        # excluyendo valores None (campos no proporcionados para actualizar)
        update_data = producto_data.model_dump(exclude_none=True)

        if not update_data:
            # Si no hay datos para actualizar, simplemente retornar el producto actual
            return await self.get_producto_by_id(producto_id)

        try:
            # Actualizar el producto
            updated_producto = await self.repository.update(producto_id, **update_data)

            # Verificar si el producto fue encontrado
            if not updated_producto:
                raise ProductoNotFoundError(f"No se encontró el producto con ID {producto_id}")

            # Convertir y retornar como esquema de respuesta
            return ProductoResponse.model_validate(updated_producto)
        except IntegrityError:
            # Capturar errores de integridad (nombre duplicado)
            if "nombre" in update_data:
                raise ProductoConflictError(
                    f"Ya existe un producto con el nombre '{update_data['nombre']}'"
                )
            # Si no es por nombre, reenviar la excepción original
            raise

    async def get_productos_cards_by_categoria(
        self, 
        categoria_id: UUID | None = None,
        skip: int = 0, 
        limit: int = 100
    ) -> ProductoCardList:
        """
        Obtiene una lista paginada de productos en formato card (nombre, imagen, categoría).

        Parameters
        ----------
        categoria_id : UUID | None, optional
            ID de la categoría para filtrar productos. Si es None, retorna todos los productos.
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        ProductoCardList
            Esquema con la lista de productos en formato card y el total.
        
        Raises
        ------
        ProductoValidationError
            Si los parámetros de paginación son inválidos.
        """
        # Validar parámetros de entrada
        if skip < 0:
            raise ProductoValidationError(
                "El parámetro 'skip' debe ser mayor o igual a cero"
            )
        if limit < 1:
            raise ProductoValidationError("El parámetro 'limit' debe ser mayor a cero")

        # Obtener productos desde el repositorio (con o sin filtro de categoría)
        productos, total = await self.repository.get_all(skip, limit, categoria_id)

        # Convertir modelos a esquemas de card
        # Necesitamos incluir la información de la categoría para cada producto
        producto_cards = []
        for producto in productos:
            # Construir el objeto ProductoCard con información de categoría
            card_data = {
                "id": producto.id,
                "nombre": producto.nombre,
                "imagen_path": producto.imagen_path,
                "precio_base": producto.precio_base,
                "categoria": {
                    "id": producto.categoria.id,
                    "nombre": producto.categoria.nombre,
                    "imagen_path": producto.categoria.imagen_path,
                }
            }
            producto_cards.append(ProductoCard.model_validate(card_data))

        # Retornar esquema de lista
        return ProductoCardList(items=producto_cards, total=total)
