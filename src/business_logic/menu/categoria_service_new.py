"""
Servicio para la gestión de categorías en el sistema.
"""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.menu.categoria_repository import CategoriaRepository
from src.models.menu.categoria_model import CategoriaModel
from src.api.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse,
    CategoriaSummary,
    CategoriaList,
)
from src.business_logic.exceptions.categoria_exceptions import (
    CategoriaValidationError,
    CategoriaNotFoundError,
    CategoriaConflictError,
)


class CategoriaService:
    """Servicio para la gestión de categorías en el sistema.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con categorías, incluyendo validaciones, transformaciones y manejo de excepciones.

    Attributes
    ----------
    repository : CategoriaRepository
        Repositorio para acceso a datos de categorías.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el servicio con una sesión de base de datos.

        Parameters
        ----------
        session : AsyncSession
            Sesión asíncrona de SQLAlchemy para realizar operaciones en la base de datos.
        """
        self.repository = CategoriaRepository(session)

    async def create_categoria(self, categoria_data: CategoriaCreate) -> CategoriaResponse:
        """
        Crea una nueva categoría en el sistema.

        PRECONDICIONES:
            - Los datos de la categoría deben pasar las validaciones de CategoriaCreate.
            - El nombre de la categoría debe ser único.

        PROCESO:
            - Valida que el nombre de la categoría sea único.
            - Crea un nuevo modelo de categoría con los datos proporcionados.
            - Persiste la categoría en la base de datos.
            - Convierte el modelo a un esquema de respuesta.

        POSTCONDICIONES:
            - La categoría es persistida en la base de datos.
            - Se retorna un objeto CategoriaResponse con los datos de la categoría creada.

        Parameters
        ----------
        categoria_data : CategoriaCreate
            Datos para crear la nueva categoría.

        Returns
        -------
        CategoriaResponse
            Esquema de respuesta con los datos de la categoría creada.

        Raises
        ------
        CategoriaConflictError
            Si ya existe una categoría con el mismo nombre.
        """
        try:
            # Crear modelo de categoría desde los datos
            categoria = CategoriaModel(
                nombre=categoria_data.nombre, 
                descripcion=categoria_data.descripcion
            )

            # Persistir en la base de datos
            created_categoria = await self.repository.create(categoria)

            # Convertir y retornar como esquema de respuesta
            return CategoriaResponse.model_validate(created_categoria)
        except IntegrityError:
            # Capturar errores de integridad (nombre duplicado)
            raise CategoriaConflictError(
                f"Ya existe una categoría con el nombre '{categoria_data.nombre}'"
            )

    async def get_categoria_by_id(self, categoria_id: UUID) -> CategoriaResponse:
        """
        Obtiene una categoría por su ID.

        PRECONDICIONES:
            - El ID debe ser un UUID válido.

        PROCESO:
            - Busca la categoría en la base de datos usando el repositorio.
            - Si existe, la convierte a un esquema de respuesta.
            - Si no existe, lanza una excepción.

        POSTCONDICIONES:
            - Se retorna un objeto CategoriaResponse si la categoría existe.
            - Se lanza CategoriaNotFoundError si no existe.

        Parameters
        ----------
        categoria_id : UUID
            Identificador único de la categoría a buscar.

        Returns
        -------
        CategoriaResponse
            Esquema de respuesta con los datos de la categoría.

        Raises
        ------
        CategoriaNotFoundError
            Si no se encuentra una categoría con el ID proporcionado.
        """
        # Buscar la categoría por su ID
        categoria = await self.repository.get_by_id(categoria_id)

        # Verificar si existe
        if not categoria:
            raise CategoriaNotFoundError(f"No se encontró la categoría con ID {categoria_id}")

        # Convertir y retornar como esquema de respuesta
        return CategoriaResponse.model_validate(categoria)

    async def delete_categoria(self, categoria_id: UUID) -> bool:
        """
        Elimina una categoría por su ID.

        PRECONDICIONES:
            - El ID debe ser un UUID válido.

        PROCESO:
            - Verifica que la categoría existe.
            - Elimina la categoría de la base de datos.

        POSTCONDICIONES:
            - La categoría es eliminada si existe.
            - Se lanza CategoriaNotFoundError si no existe.

        Parameters
        ----------
        categoria_id : UUID
            Identificador único de la categoría a eliminar.

        Returns
        -------
        bool
            True si la categoría fue eliminada correctamente.

        Raises
        ------
        CategoriaNotFoundError
            Si no se encuentra una categoría con el ID proporcionado.
        """
        # Verificar primero si la categoría existe
        categoria = await self.repository.get_by_id(categoria_id)
        if not categoria:
            raise CategoriaNotFoundError(f"No se encontró la categoría con ID {categoria_id}")

        # Eliminar la categoría
        result = await self.repository.delete(categoria_id)
        return result

    async def get_categorias(self, skip: int = 0, limit: int = 100) -> CategoriaList:
        """
        Obtiene una lista paginada de categorías.

        PRECONDICIONES:
            - Los parámetros skip y limit deben ser enteros no negativos.

        PROCESO:
            - Recupera las categorías según los parámetros de paginación.
            - Convierte los modelos a esquemas de resumen.

        POSTCONDICIONES:
            - Se retorna un objeto CategoriaList con la lista de categorías y el total.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        CategoriaList
            Esquema con la lista de categorías y el total.
        """
        # Validar parámetros de entrada
        if skip < 0:
            raise CategoriaValidationError(
                "El parámetro 'skip' debe ser mayor o igual a cero"
            )
        if limit < 1:
            raise CategoriaValidationError("El parámetro 'limit' debe ser mayor a cero")

        # Obtener categorías desde el repositorio
        categorias, total = await self.repository.get_all(skip, limit)

        # Convertir modelos a esquemas de resumen
        categoria_summaries = [CategoriaSummary.model_validate(categoria) for categoria in categorias]

        # Retornar esquema de lista
        return CategoriaList(items=categoria_summaries, total=total)

    async def get_categorias_activas(self, skip: int = 0, limit: int = 100) -> CategoriaList:
        """
        Obtiene una lista paginada de categorías activas.

        PRECONDICIONES:
            - Los parámetros skip y limit deben ser enteros no negativos.

        PROCESO:
            - Recupera las categorías activas según los parámetros de paginación.
            - Convierte los modelos a esquemas de resumen.

        POSTCONDICIONES:
            - Se retorna un objeto CategoriaList con la lista de categorías activas y el total.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        CategoriaList
            Esquema con la lista de categorías activas y el total.
        """
        # Validar parámetros de entrada
        if skip < 0:
            raise CategoriaValidationError(
                "El parámetro 'skip' debe ser mayor o igual a cero"
            )
        if limit < 1:
            raise CategoriaValidationError("El parámetro 'limit' debe ser mayor a cero")

        # Obtener categorías activas desde el repositorio
        categorias, total = await self.repository.get_activas(skip, limit)

        # Convertir modelos a esquemas de resumen
        categoria_summaries = [CategoriaSummary.model_validate(categoria) for categoria in categorias]

        # Retornar esquema de lista
        return CategoriaList(items=categoria_summaries, total=total)

    async def update_categoria(self, categoria_id: UUID, categoria_data: CategoriaUpdate) -> CategoriaResponse:
        """
        Actualiza una categoría existente.

        PRECONDICIONES:
            - El ID debe ser un UUID válido.
            - Los datos de actualización deben pasar las validaciones de CategoriaUpdate.
            - La categoría debe existir.

        PROCESO:
            - Verifica que la categoría existe.
            - Actualiza solo los campos proporcionados.
            - Persiste los cambios en la base de datos.

        POSTCONDICIONES:
            - La categoría es actualizada en la base de datos.
            - Se retorna un objeto CategoriaResponse con los datos actualizados.

        Parameters
        ----------
        categoria_id : UUID
            Identificador único de la categoría a actualizar.
        categoria_data : CategoriaUpdate
            Datos para actualizar la categoría.

        Returns
        -------
        CategoriaResponse
            Esquema de respuesta con los datos de la categoría actualizada.

        Raises
        ------
        CategoriaNotFoundError
            Si no se encuentra una categoría con el ID proporcionado.
        CategoriaConflictError
            Si ya existe otra categoría con el mismo nombre.
        """
        # Convertir el esquema de actualización a un diccionario,
        # excluyendo valores None (campos no proporcionados para actualizar)
        update_data = categoria_data.model_dump(exclude_none=True)

        if not update_data:
            # Si no hay datos para actualizar, simplemente retornar la categoría actual
            return await self.get_categoria_by_id(categoria_id)

        try:
            # Actualizar la categoría
            updated_categoria = await self.repository.update(categoria_id, **update_data)

            # Verificar si la categoría fue encontrada
            if not updated_categoria:
                raise CategoriaNotFoundError(f"No se encontró la categoría con ID {categoria_id}")

            # Convertir y retornar como esquema de respuesta
            return CategoriaResponse.model_validate(updated_categoria)
        except IntegrityError:
            # Capturar errores de integridad (nombre duplicado)
            if "nombre" in update_data:
                raise CategoriaConflictError(
                    f"Ya existe una categoría con el nombre '{update_data['nombre']}'"
                )
            # Si no es por nombre, reenviar la excepción original
            raise
