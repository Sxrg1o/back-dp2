"""
Repositorio para la gestión de productos en el sistema.
"""

from typing import Optional, List, Tuple, Dict, Any
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload

from src.models.menu.producto_model import ProductoModel


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

    async def get_by_id(self, producto_id: UUID) -> Optional[ProductoModel]:
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

    async def get_by_id_with_opciones(self, producto_id: UUID) -> Optional[ProductoModel]:
        """
        Obtiene un producto por su ID con todas sus opciones (eager loading).
        
        Parameters
        ----------
        producto_id : UUID
            Identificador único del producto a buscar.
            
        Returns
        -------
        Optional[ProductoModel]
            El producto encontrado con sus opciones cargadas, o None si no existe.
        """
        query = (
            select(ProductoModel)
            .where(ProductoModel.id == producto_id)
            .options(selectinload(ProductoModel.opciones))
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def delete(self, producto_id: UUID) -> bool:
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

    async def update(self, producto_id: UUID, **kwargs) -> Optional[ProductoModel]:
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
            )

            result = await self.session.execute(stmt)
            await self.session.commit()
            
            # Consultar el producto actualizado
            updated_producto = await self.get_by_id(producto_id)
            
            # Si no se encontró el producto, retornar None
            if not updated_producto:
                return None

            return updated_producto
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_all(
            self, 
            skip: int = 0, 
            limit: int = 100,
            id_categoria: UUID | None = None 
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

    async def batch_insert(self, productos: List[ProductoModel]) -> List[ProductoModel]:
        """
        Inserta múltiples productos en la base de datos en una sola operación.
        
        Parameters
        ----------
        productos : List[ProductoModel]
            Lista de instancias de productos a insertar.
            
        Returns
        -------
        List[ProductoModel]
            Lista de los productos insertados con sus IDs asignados.
            
        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        if not productos:
            return []
            
        try:
            # Agregar todos los productos a la sesión
            self.session.add_all(productos)
            
            # Flush para generar los IDs y otras columnas generadas automáticamente
            await self.session.flush()
            
            # Commit para confirmar la transacción
            await self.session.commit()
            
            # Refrescar todos los productos para asegurar que tengan sus datos actualizados
            for producto in productos:
                await self.session.refresh(producto)
                
            return productos
        except SQLAlchemyError:
            await self.session.rollback()
            raise
            
    async def batch_update(self, updates: List[Tuple[UUID, Dict[str, Any]]]) -> List[ProductoModel]:
        """
        Actualiza múltiples productos en la base de datos en una operación eficiente.
        
        Parameters
        ----------
        updates : List[Tuple[UUID, Dict[str, Any]]]
            Lista de tuplas donde cada tupla contiene el ID del producto y un diccionario
            con los campos a actualizar y sus nuevos valores.
            
        Returns
        -------
        List[ProductoModel]
            Lista de los productos actualizados.
            
        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        if not updates:
            return []
            
        try:
            # Recolectar todos los IDs de productos que se actualizarán
            product_ids = [product_id for product_id, _ in updates]
            
            # Realizar actualizaciones utilizando un enfoque más eficiente
            # que minimiza el número de consultas SQL
            from sqlalchemy import bindparam
            
            # Agrupar actualizaciones por conjuntos de campos a actualizar
            updates_by_fields = {}
            
            for producto_id, update_data in updates:
                # Filtrar solo los campos válidos
                valid_fields = {
                    k: v for k, v in update_data.items() 
                    if hasattr(ProductoModel, k) and k != "id"
                }
                
                if not valid_fields:
                    continue
                    
                # Crear una clave basada en los nombres de los campos
                fields_key = frozenset(valid_fields.keys())
                
                if fields_key not in updates_by_fields:
                    updates_by_fields[fields_key] = []
                    
                # Añadir esta actualización al grupo correspondiente
                update_with_id = valid_fields.copy()
                update_with_id['id'] = producto_id
                updates_by_fields[fields_key].append(update_with_id)
                
            # Para cada grupo de actualizaciones con el mismo conjunto de campos
            for fields, field_updates in updates_by_fields.items():
                if not field_updates:
                    continue
                    
                # Construir una actualización parametrizada
                update_stmt = update(ProductoModel).where(
                    ProductoModel.id == bindparam('id')
                )
                
                # Añadir los campos a actualizar
                update_values = {}
                for field in fields:
                    update_values[field] = bindparam(field)
                    
                update_stmt = update_stmt.values(**update_values)
                
                # Ejecutar la actualización para este grupo
                await self.session.execute(update_stmt, field_updates)
                
            # Confirmar todas las actualizaciones
            await self.session.commit()
            
            # Recuperar todos los productos actualizados en una sola consulta
            query = select(ProductoModel).where(ProductoModel.id.in_(product_ids))
            result = await self.session.execute(query)
            updated_productos = result.scalars().all()
            
            return list(updated_productos)
        except SQLAlchemyError:
            await self.session.rollback()
            raise
