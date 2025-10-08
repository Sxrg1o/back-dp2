"""
Servicio para la gestión de tipos de opciones en el sistema.
"""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.pedidos.tipo_opciones_repository import TipoOpcionRepository
from src.models.pedidos.tipo_opciones_model import TipoOpcionModel
from src.api.schemas.tipo_opciones_schema import (
    TipoOpcionCreate,
    TipoOpcionUpdate,
    TipoOpcionResponse,
    TipoOpcionSummary,
    TipoOpcionList,
)
from src.business_logic.exceptions.tipo_opciones_exceptions import (
    TipoOpcionValidationError,
    TipoOpcionNotFoundError,
    TipoOpcionConflictError,
)


class TipoOpcionService:
    """Servicio para la gestión de tipos de opciones en el sistema.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con tipos de opciones, incluyendo validaciones, transformaciones y manejo de excepciones.

    Attributes
    ----------
    repository : TipoOpcionRepository
        Repositorio para acceso a datos de tipos de opciones.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el servicio con una sesión de base de datos.

        Parameters
        ----------
        session : AsyncSession
            Sesión asíncrona de SQLAlchemy para realizar operaciones en la base de datos.
        """
        self.repository = TipoOpcionRepository(session)

    async def create_tipo_opcion(self, tipo_opcion_data: TipoOpcionCreate) -> TipoOpcionResponse:
        """
        Crea un nuevo tipo de opción en el sistema.

        Parameters
        ----------
        tipo_opcion_data : TipoOpcionCreate
            Datos para crear el nuevo tipo de opción.

        Returns
        -------
        TipoOpcionResponse
            Esquema de respuesta con los datos del tipo de opción creado.

        Raises
        ------
        TipoOpcionConflictError
            Si ya existe un tipo de opción con el mismo código.
        """
        try:
            # Crear modelo de tipo de opción desde los datos
            tipo_opcion = TipoOpcionModel(
                codigo=tipo_opcion_data.codigo,
                nombre=tipo_opcion_data.nombre,
                descripcion=tipo_opcion_data.descripcion,
                activo=tipo_opcion_data.activo,
                orden=tipo_opcion_data.orden
            )

            # Persistir en la base de datos
            created_tipo_opcion = await self.repository.create(tipo_opcion)

            # Convertir y retornar como esquema de respuesta
            return TipoOpcionResponse.model_validate(created_tipo_opcion)
        except IntegrityError:
            # Capturar errores de integridad (código duplicado)
            raise TipoOpcionConflictError(
                f"Ya existe un tipo de opción con el código '{tipo_opcion_data.codigo}'"
            )

    async def get_tipo_opcion_by_id(self, tipo_opcion_id: UUID) -> TipoOpcionResponse:
        """
        Obtiene un tipo de opción por su ID.

        Parameters
        ----------
        tipo_opcion_id : UUID
            Identificador único del tipo de opción a buscar.

        Returns
        -------
        TipoOpcionResponse
            Esquema de respuesta con los datos del tipo de opción.

        Raises
        ------
        TipoOpcionNotFoundError
            Si no se encuentra un tipo de opción con el ID proporcionado.
        """
        # Buscar el tipo de opción por su ID
        tipo_opcion = await self.repository.get_by_id(tipo_opcion_id)

        # Verificar si existe
        if not tipo_opcion:
            raise TipoOpcionNotFoundError(f"No se encontró el tipo de opción con ID {tipo_opcion_id}")

        # Convertir y retornar como esquema de respuesta
        return TipoOpcionResponse.model_validate(tipo_opcion)

    async def delete_tipo_opcion(self, tipo_opcion_id: UUID) -> bool:
        """
        Elimina un tipo de opción por su ID.

        Parameters
        ----------
        tipo_opcion_id : UUID
            Identificador único del tipo de opción a eliminar.

        Returns
        -------
        bool
            True si el tipo de opción fue eliminado correctamente.

        Raises
        ------
        TipoOpcionNotFoundError
            Si no se encuentra un tipo de opción con el ID proporcionado.
        """
        # Verificar primero si el tipo de opción existe
        tipo_opcion = await self.repository.get_by_id(tipo_opcion_id)
        if not tipo_opcion:
            raise TipoOpcionNotFoundError(f"No se encontró el tipo de opción con ID {tipo_opcion_id}")

        # Eliminar el tipo de opción
        result = await self.repository.delete(tipo_opcion_id)
        return result

    async def get_tipos_opciones(self, skip: int = 0, limit: int = 100) -> TipoOpcionList:
        """
        Obtiene una lista paginada de tipos de opciones.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        TipoOpcionList
            Esquema con la lista de tipos de opciones y el total.
        """
        # Validar parámetros de entrada
        if skip < 0:
            raise TipoOpcionValidationError(
                "El parámetro 'skip' debe ser mayor o igual a cero"
            )
        if limit < 1:
            raise TipoOpcionValidationError("El parámetro 'limit' debe ser mayor a cero")

        # Obtener tipos de opciones desde el repositorio
        tipos_opciones, total = await self.repository.get_all(skip, limit)

        # Convertir modelos a esquemas de resumen
        tipo_opcion_summaries = [TipoOpcionSummary.model_validate(tipo_opcion) for tipo_opcion in tipos_opciones]

        # Retornar esquema de lista
        return TipoOpcionList(items=tipo_opcion_summaries, total=total)

    async def update_tipo_opcion(self, tipo_opcion_id: UUID, tipo_opcion_data: TipoOpcionUpdate) -> TipoOpcionResponse:
        """
        Actualiza un tipo de opción existente.

        Parameters
        ----------
        tipo_opcion_id : UUID
            Identificador único del tipo de opción a actualizar.
        tipo_opcion_data : TipoOpcionUpdate
            Datos para actualizar el tipo de opción.

        Returns
        -------
        TipoOpcionResponse
            Esquema de respuesta con los datos del tipo de opción actualizado.

        Raises
        ------
        TipoOpcionNotFoundError
            Si no se encuentra un tipo de opción con el ID proporcionado.
        TipoOpcionConflictError
            Si ya existe otro tipo de opción con el mismo código.
        """
        # Convertir el esquema de actualización a un diccionario,
        # excluyendo valores None (campos no proporcionados para actualizar)
        update_data = tipo_opcion_data.model_dump(exclude_none=True)

        if not update_data:
            # Si no hay datos para actualizar, simplemente retornar el tipo de opción actual
            return await self.get_tipo_opcion_by_id(tipo_opcion_id)

        try:
            # Actualizar el tipo de opción
            updated_tipo_opcion = await self.repository.update(tipo_opcion_id, **update_data)

            # Verificar si el tipo de opción fue encontrado
            if not updated_tipo_opcion:
                raise TipoOpcionNotFoundError(f"No se encontró el tipo de opción con ID {tipo_opcion_id}")

            # Convertir y retornar como esquema de respuesta
            return TipoOpcionResponse.model_validate(updated_tipo_opcion)
        except IntegrityError:
            # Capturar errores de integridad (código duplicado)
            if "codigo" in update_data:
                raise TipoOpcionConflictError(
                    f"Ya existe un tipo de opción con el código '{update_data['codigo']}'"
                )
            # Si no es por código, reenviar la excepción original
            raise

