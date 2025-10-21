"""
Repositorio para la gestión de productos en el sistema.
"""

from typing import Optional, List, Tuple

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload

from src.models.menu.producto_model import ProductoModel
from src.models.pedidos.producto_opcion_model import ProductoOpcionModel


class ProductoRepository:
    """Repositorio para gestionar operaciones CRUD del modelo de productos.

    Proporciona acceso a la capa de persistencia para las operaciones
    relacionadas con los productos en el sistema, siguiendo el patrón Repository.

    Attributes
    ----------
    session : AsyncSession
        Sesión asíncrona de SQLAlchemy para realizar operaciones en la base de datos.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el repositorio con una sesión de base de datos.

        Parameters
        ----------
        session : AsyncSession
            Sesión asíncrona de SQLAlchemy para realizar operaciones en la base de datos.
        """
        self.session = session

    async def create(self, producto: ProductoModel) -> ProductoModel:
        """
        Crea un nuevo producto en la base de datos.

        Parameters
        ----------
        producto : ProductoModel
            Instancia del modelo de producto a crear.

        Returns
        -------
        ProductoModel
            El modelo de producto creado con su ID asignado.

        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        try:
            self.session.add(producto)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(producto)
            return producto
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_by_id(self, producto_id: str) -> Optional[ProductoModel]:
        """
        Obtiene un producto por su identificador único.

        Parameters
        ----------
        producto_id : UUID
            Identificador único del producto a buscar.

        Returns
        -------
        Optional[ProductoModel]
            El producto encontrado o None si no existe.
        """
        query = select(ProductoModel).where(ProductoModel.id == producto_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_id_with_opciones(self, producto_id: str) -> Optional[ProductoModel]:
        """
        Obtiene un producto por su ID con todas sus opciones Y tipos de opciones (eager loading).
        
        Modified: Now includes tipo_opcion relationship for grouping.
        
        Parameters
        ----------
        producto_id : str
            Identificador único del producto a buscar (ULID).
            
        Returns
        -------
        Optional[ProductoModel]
            El producto encontrado con sus opciones y tipos cargados, o None si no existe.
        """
        query = (
            select(ProductoModel)
            .where(ProductoModel.id == producto_id)
            .options(
                selectinload(ProductoModel.opciones)
                .selectinload(ProductoOpcionModel.tipo_opcion)  # Load tipo_opcion for each option
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def delete(self, producto_id: str) -> bool:
        """
        Elimina un producto de la base de datos por su ID.

        Parameters
        ----------
        producto_id : UUID
            Identificador único del producto a eliminar.

        Returns
        -------
        bool
            True si el producto fue eliminado, False si no existía.

        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        try:
            stmt = delete(ProductoModel).where(ProductoModel.id == producto_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def update(self, producto_id: str, **kwargs) -> Optional[ProductoModel]:
        """
        Actualiza un producto existente con los valores proporcionados.

        Parameters
        ----------
        producto_id : UUID
            Identificador único del producto a actualizar.
        **kwargs
            Campos y valores a actualizar.

        Returns
        -------
        Optional[ProductoModel]
            El producto actualizado o None si no existe.

        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        try:
            # Filtrar solo los campos que pertenecen al modelo
            valid_fields = {
                k: v for k, v in kwargs.items() if hasattr(ProductoModel, k) and k != "id"
            }

            if not valid_fields:
                # No hay campos válidos para actualizar
                return await self.get_by_id(producto_id)

            # Construir y ejecutar la sentencia de actualización
            stmt = (
                update(ProductoModel)
                .where(ProductoModel.id == producto_id)
                .values(**valid_fields)
                .returning(ProductoModel)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            # Obtener el resultado actualizado
            updated_producto = result.scalars().first()

            # Si no se encontró el producto, retornar None
            if not updated_producto:
                return None

            # Refrescar el objeto desde la base de datos
            await self.session.refresh(updated_producto)

            return updated_producto
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_all(
            self, 
            skip: int = 0, 
            limit: int = 100,
            id_categoria: str | None = None 
        ) -> Tuple[List[ProductoModel], int]:
        """
        Obtiene todos los productos con paginación y filtro opcional por categoría.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.
        id_categoria : UUID | None, optional
            ID de categoría para filtrar (opcional)

        Returns
        -------
        Tuple[List[ProductoModel], int]
            Tupla con la lista de productos y el número total de registros.
        """
        try:
            # Query base con carga eager de la relación categoria
            query = select(ProductoModel).options(selectinload(ProductoModel.categoria))
            
            # ✅ Aplicar filtro de categoría si se proporciona
            if id_categoria is not None:
                query = query.where(ProductoModel.id_categoria == id_categoria)
            
            # Obtener total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await self.session.execute(count_query)
            total = total_result.scalar() or 0
            
            # Aplicar paginación
            query = query.offset(skip).limit(limit)
            
            # Ejecutar query
            result = await self.session.execute(query)
            productos = result.scalars().all()
            
            return list(productos), total
            
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
