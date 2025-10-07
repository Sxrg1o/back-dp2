"""
Repositorio para la gestión de categorías en el sistema.
"""

from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func

from src.models.menu.categoria_model import CategoriaModel


class CategoriaRepository:
    """Repositorio para gestionar operaciones CRUD del modelo de categorías.

    Proporciona acceso a la capa de persistencia para las operaciones
    relacionadas con las categorías en el sistema, siguiendo el patrón Repository.

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

    async def create(self, categoria: CategoriaModel) -> CategoriaModel:
        """
        Crea una nueva categoría en la base de datos.

        Parameters
        ----------
        categoria : CategoriaModel
            Instancia del modelo de categoría a crear.

        Returns
        -------
        CategoriaModel
            El modelo de categoría creado con su ID asignado.

        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        try:
            self.session.add(categoria)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(categoria)
            return categoria
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_by_id(self, categoria_id: UUID) -> Optional[CategoriaModel]:
        """
        Obtiene una categoría por su identificador único.

        Parameters
        ----------
        categoria_id : UUID
            Identificador único de la categoría a buscar.

        Returns
        -------
        Optional[CategoriaModel]
            La categoría encontrada o None si no existe.
        """
        query = select(CategoriaModel).where(CategoriaModel.id == categoria_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_nombre(self, nombre: str) -> Optional[CategoriaModel]:
        """
        Obtiene una categoría por su nombre.

        Parameters
        ----------
        nombre : str
            Nombre de la categoría a buscar.

        Returns
        -------
        Optional[CategoriaModel]
            La categoría encontrada o None si no existe.
        """
        query = select(CategoriaModel).where(CategoriaModel.nombre == nombre)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def delete(self, categoria_id: UUID) -> bool:
        """
        Elimina una categoría de la base de datos por su ID.

        Parameters
        ----------
        categoria_id : UUID
            Identificador único de la categoría a eliminar.

        Returns
        -------
        bool
            True si la categoría fue eliminada, False si no existía.

        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        try:
            stmt = delete(CategoriaModel).where(CategoriaModel.id == categoria_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def update(self, categoria_id: UUID, **kwargs) -> Optional[CategoriaModel]:
        """
        Actualiza una categoría existente con los valores proporcionados.

        Parameters
        ----------
        categoria_id : UUID
            Identificador único de la categoría a actualizar.
        **kwargs
            Campos y valores a actualizar.

        Returns
        -------
        Optional[CategoriaModel]
            La categoría actualizada o None si no existe.

        Raises
        ------
        SQLAlchemyError
            Si ocurre un error durante la operación en la base de datos.
        """
        try:
            # Filtrar solo los campos que pertenecen al modelo
            valid_fields = {
                k: v for k, v in kwargs.items() if hasattr(CategoriaModel, k) and k != "id"
            }

            if not valid_fields:
                # No hay campos válidos para actualizar
                return await self.get_by_id(categoria_id)

            # Construir y ejecutar la sentencia de actualización
            stmt = (
                update(CategoriaModel)
                .where(CategoriaModel.id == categoria_id)
                .values(**valid_fields)
                .returning(CategoriaModel)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            # Obtener el resultado actualizado
            updated_categoria = result.scalars().first()

            # Si no se encontró la categoría, retornar None
            if not updated_categoria:
                return None

            # Refrescar el objeto desde la base de datos
            await self.session.refresh(updated_categoria)

            return updated_categoria
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        activo: Optional[bool] = None
    ) -> Tuple[List[CategoriaModel], int]:
        """
        Obtiene una lista paginada de categorías y el total de registros.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.
        activo : Optional[bool], optional
            Si se especifica, filtra por estado activo/inactivo.

        Returns
        -------
        Tuple[List[CategoriaModel], int]
            Tupla con la lista de categorías y el número total de registros.
        """
        # Consulta base para obtener las categorías paginadas
        query = select(CategoriaModel)
        count_query = select(func.count(CategoriaModel.id))

        # Aplicar filtro de activo si se especifica
        if activo is not None:
            query = query.where(CategoriaModel.activo == activo)
            count_query = count_query.where(CategoriaModel.activo == activo)

        # Aplicar paginación
        query = query.offset(skip).limit(limit)

        try:
            # Ejecutar ambas consultas
            result = await self.session.execute(query)
            count_result = await self.session.execute(count_query)

            # Obtener los resultados
            categorias = result.scalars().all()
            total = count_result.scalar() or 0

            return list(categorias), total
        except SQLAlchemyError:
            raise
