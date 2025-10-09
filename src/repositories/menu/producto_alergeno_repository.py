"""
Repositorio para la gestión de relaciones producto-alérgeno en el sistema.
"""

from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func

from src.models.menu.producto_alergeno_model import ProductoAlergenoModel


class ProductoAlergenoRepository:
    """Repositorio para gestionar operaciones CRUD de relaciones producto-alérgeno.

    Proporciona acceso a la capa de persistencia para las operaciones
    relacionadas con la asignación de alérgenos a productos del menú,
    siguiendo el patrón Repository.

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

    async def create(self, producto_alergeno: ProductoAlergenoModel) -> ProductoAlergenoModel:
        """
        Crea una nueva relación producto-alérgeno en la base de datos.

        Parameters
        ----------
        producto_alergeno : ProductoAlergenoModel
            Instancia del modelo de relación a crear.

        Returns
        -------
        ProductoAlergenoModel
            El modelo de relación creado.

        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        try:
            self.session.add(producto_alergeno)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(producto_alergeno)
            return producto_alergeno
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_by_id(self, id_producto: UUID, id_alergeno: UUID) -> Optional[ProductoAlergenoModel]:
        """
        Obtiene una relación producto-alérgeno por su clave primaria compuesta.

        Parameters
        ----------
        id_producto : UUID
            Identificador único del producto.
        id_alergeno : UUID
            Identificador único del alérgeno.

        Returns
        -------
        Optional[ProductoAlergenoModel]
            La relación encontrada o None si no existe.
        """
        query = select(ProductoAlergenoModel).where(
            ProductoAlergenoModel.id_producto == id_producto,
            ProductoAlergenoModel.id_alergeno == id_alergeno
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def delete(self, id_producto: UUID, id_alergeno: UUID) -> bool:
        """
        Elimina una relación producto-alérgeno de la base de datos.

        Parameters
        ----------
        id_producto : UUID
            Identificador único del producto.
        id_alergeno : UUID
            Identificador único del alérgeno.

        Returns
        -------
        bool
            True si la relación fue eliminada, False si no existía.

        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        try:
            stmt = delete(ProductoAlergenoModel).where(
                ProductoAlergenoModel.id_producto == id_producto,
                ProductoAlergenoModel.id_alergeno == id_alergeno
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def update(
        self, id_producto: UUID, id_alergeno: UUID, **kwargs
    ) -> Optional[ProductoAlergenoModel]:
        """
        Actualiza una relación producto-alérgeno existente con los valores proporcionados.

        Parameters
        ----------
        id_producto : UUID
            Identificador único del producto.
        id_alergeno : UUID
            Identificador único del alérgeno.
        **kwargs
            Campos y valores a actualizar.

        Returns
        -------
        Optional[ProductoAlergenoModel]
            La relación actualizada o None si no existe.

        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        try:
            # Filtrar solo los campos que pertenecen al modelo
            # Excluir las claves primarias (id_producto, id_alergeno)
            valid_fields = {
                k: v for k, v in kwargs.items()
                if hasattr(ProductoAlergenoModel, k) and k not in ("id_producto", "id_alergeno", "id")
            }

            if not valid_fields:
                # No hay campos válidos para actualizar
                return await self.get_by_id(id_producto, id_alergeno)

            # Construir y ejecutar la sentencia de actualización
            stmt = (
                update(ProductoAlergenoModel)
                .where(
                    ProductoAlergenoModel.id_producto == id_producto,
                    ProductoAlergenoModel.id_alergeno == id_alergeno
                )
                .values(**valid_fields)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            # Consultar la relación actualizada
            updated_producto_alergeno = await self.get_by_id(id_producto, id_alergeno)
            
            # Si no se encontró la relación, retornar None
            if not updated_producto_alergeno:
                return None

            return updated_producto_alergeno
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> Tuple[List[ProductoAlergenoModel], int]:
        """
        Obtiene una lista paginada de relaciones producto-alérgeno y el total de registros.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        Tuple[List[ProductoAlergenoModel], int]
            Tupla con la lista de relaciones y el número total de registros.
        """
        # Consulta para obtener las relaciones paginadas
        query = select(ProductoAlergenoModel).offset(skip).limit(limit)

        # Consulta para obtener el total de registros
        count_query = select(func.count()).select_from(ProductoAlergenoModel)

        try:
            # Ejecutar ambas consultas
            result = await self.session.execute(query)
            count_result = await self.session.execute(count_query)

            # Obtener los resultados
            producto_alergenos = result.scalars().all()
            total = count_result.scalar() or 0

            return list(producto_alergenos), total
        except SQLAlchemyError:
            # En caso de error, no es necesario hacer rollback aquí
            # porque no estamos modificando datos
            raise

    async def get_by_producto(self, id_producto: UUID) -> List[ProductoAlergenoModel]:
        """
        Obtiene todos los alérgenos asociados a un producto específico.

        Parameters
        ----------
        id_producto : UUID
            Identificador único del producto.

        Returns
        -------
        List[ProductoAlergenoModel]
            Lista de relaciones producto-alérgeno para el producto especificado.
        """
        query = select(ProductoAlergenoModel).where(
            ProductoAlergenoModel.id_producto == id_producto
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_alergeno(self, id_alergeno: UUID) -> List[ProductoAlergenoModel]:
        """
        Obtiene todos los productos que contienen un alérgeno específico.

        Parameters
        ----------
        id_alergeno : UUID
            Identificador único del alérgeno.

        Returns
        -------
        List[ProductoAlergenoModel]
            Lista de relaciones producto-alérgeno para el alérgeno especificado.
        """
        query = select(ProductoAlergenoModel).where(
            ProductoAlergenoModel.id_alergeno == id_alergeno
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
