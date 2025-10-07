"""
Servicio para la gestión de alérgenos en el sistema.
"""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.menu.alergeno_repository import AlergenoRepository
from src.models.menu.alergeno_model import AlergenoModel
from src.api.schemas.alergeno_schema import (
    AlergenoCreate,
    AlergenoUpdate,
    AlergenoResponse,
    AlergenoSummary,
    AlergenoList,
)
from src.business_logic.exceptions.alergeno_exceptions import (
    AlergenoValidationError,
    AlergenoNotFoundError,
    AlergenoConflictError,
)


class AlergenoService:
    """Servicio para la gestión de alérgenos en el sistema.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con alérgenos, incluyendo validaciones, transformaciones y manejo de excepciones.

    Attributes
    ----------
    repository : AlergenoRepository
        Repositorio para acceso a datos de alérgenos.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el servicio con una sesión de base de datos.

        Parameters
        ----------
        session : AsyncSession
            Sesión asíncrona de SQLAlchemy para realizar operaciones en la base de datos.
        """
        self.repository = AlergenoRepository(session)

    async def create_alergeno(self, alergeno_data: AlergenoCreate) -> AlergenoResponse:
        """
        Crea un nuevo alérgeno en el sistema.

        PRECONDICIONES:
            - Los datos del alérgeno deben pasar las validaciones de AlergenoCreate.
            - El nombre del alérgeno debe ser único.

        PROCESO:
            - Valida que el nombre del alérgeno sea único.
            - Crea un nuevo modelo de alérgeno con los datos proporcionados.
            - Persiste el alérgeno en la base de datos.
            - Convierte el modelo a un esquema de respuesta.

        POSTCONDICIONES:
            - El alérgeno es persistido en la base de datos.
            - Se retorna un objeto AlergenoResponse con los datos del alérgeno creado.

        Parameters
        ----------
        alergeno_data : AlergenoCreate
            Datos para crear el nuevo alérgeno.

        Returns
        -------
        AlergenoResponse
            Esquema de respuesta con los datos del alérgeno creado.

        Raises
        ------
        AlergenoConflictError
            Si ya existe un alérgeno con el mismo nombre.
        """
        try:
            # Crear modelo de alérgeno desde los datos
            alergeno = AlergenoModel(
                nombre=alergeno_data.nombre,
                descripcion=alergeno_data.descripcion,
                icono=alergeno_data.icono,
                nivel_riesgo=alergeno_data.nivel_riesgo
            )

            # Persistir en la base de datos
            created_alergeno = await self.repository.create(alergeno)

            # Convertir y retornar como esquema de respuesta
            return AlergenoResponse.model_validate(created_alergeno)
        except IntegrityError:
            # Capturar errores de integridad (nombre duplicado)
            raise AlergenoConflictError(
                f"Ya existe un alérgeno con el nombre '{alergeno_data.nombre}'"
            )

    async def get_alergeno_by_id(self, alergeno_id: UUID) -> AlergenoResponse:
        """
        Obtiene un alérgeno por su ID.

        PRECONDICIONES:
            - El ID debe ser un UUID válido.

        PROCESO:
            - Busca el alérgeno en la base de datos usando el repositorio.
            - Si existe, lo convierte a un esquema de respuesta.
            - Si no existe, lanza una excepción.

        POSTCONDICIONES:
            - Se retorna un objeto AlergenoResponse si el alérgeno existe.
            - Se lanza AlergenoNotFoundError si no existe.

        Parameters
        ----------
        alergeno_id : UUID
            Identificador único del alérgeno a buscar.

        Returns
        -------
        AlergenoResponse
            Esquema de respuesta con los datos del alérgeno.

        Raises
        ------
        AlergenoNotFoundError
            Si no se encuentra un alérgeno con el ID proporcionado.
        """
        # Buscar el alérgeno por su ID
        alergeno = await self.repository.get_by_id(alergeno_id)

        # Verificar si existe
        if not alergeno:
            raise AlergenoNotFoundError(f"No se encontró el alérgeno con ID {alergeno_id}")

        # Convertir y retornar como esquema de respuesta
        return AlergenoResponse.model_validate(alergeno)

    async def delete_alergeno(self, alergeno_id: UUID) -> bool:
        """
        Elimina un alérgeno por su ID.

        PRECONDICIONES:
            - El ID debe ser un UUID válido.

        PROCESO:
            - Verifica que el alérgeno existe.
            - Elimina el alérgeno de la base de datos.

        POSTCONDICIONES:
            - El alérgeno es eliminado si existe.
            - Se lanza AlergenoNotFoundError si no existe.

        Parameters
        ----------
        alergeno_id : UUID
            Identificador único del alérgeno a eliminar.

        Returns
        -------
        bool
            True si el alérgeno fue eliminado correctamente.

        Raises
        ------
        AlergenoNotFoundError
            Si no se encuentra un alérgeno con el ID proporcionado.
        """
        # Verificar primero si el alérgeno existe
        alergeno = await self.repository.get_by_id(alergeno_id)
        if not alergeno:
            raise AlergenoNotFoundError(f"No se encontró el alérgeno con ID {alergeno_id}")

        # Eliminar el alérgeno
        result = await self.repository.delete(alergeno_id)
        return result

    async def get_alergenos(self, skip: int = 0, limit: int = 100) -> AlergenoList:
        """
        Obtiene una lista paginada de alérgenos.

        PRECONDICIONES:
            - Los parámetros skip y limit deben ser enteros no negativos.

        PROCESO:
            - Recupera los alérgenos según los parámetros de paginación.
            - Convierte los modelos a esquemas de resumen.

        POSTCONDICIONES:
            - Se retorna un objeto AlergenoList con la lista de alérgenos y el total.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        AlergenoList
            Esquema con la lista de alérgenos y el total.
        """
        # Validar parámetros de entrada
        if skip < 0:
            raise AlergenoValidationError(
                "El parámetro 'skip' debe ser mayor o igual a cero"
            )
        if limit < 1:
            raise AlergenoValidationError("El parámetro 'limit' debe ser mayor a cero")

        # Obtener alérgenos desde el repositorio
        alergenos, total = await self.repository.get_all(skip, limit)

        # Convertir modelos a esquemas de resumen
        alergeno_summaries = [AlergenoSummary.model_validate(alergeno) for alergeno in alergenos]

        # Retornar esquema de lista
        return AlergenoList(items=alergeno_summaries, total=total)

    async def update_alergeno(self, alergeno_id: UUID, alergeno_data: AlergenoUpdate) -> AlergenoResponse:
        """
        Actualiza un alérgeno existente.

        PRECONDICIONES:
            - El ID debe ser un UUID válido.
            - Los datos de actualización deben pasar las validaciones de AlergenoUpdate.
            - El alérgeno debe existir.

        PROCESO:
            - Verifica que el alérgeno existe.
            - Actualiza solo los campos proporcionados.
            - Persiste los cambios en la base de datos.

        POSTCONDICIONES:
            - El alérgeno es actualizado en la base de datos.
            - Se retorna un objeto AlergenoResponse con los datos actualizados.

        Parameters
        ----------
        alergeno_id : UUID
            Identificador único del alérgeno a actualizar.
        alergeno_data : AlergenoUpdate
            Datos para actualizar el alérgeno.

        Returns
        -------
        AlergenoResponse
            Esquema de respuesta con los datos del alérgeno actualizado.

        Raises
        ------
        AlergenoNotFoundError
            Si no se encuentra un alérgeno con el ID proporcionado.
        AlergenoConflictError
            Si ya existe otro alérgeno con el mismo nombre.
        """
        # Convertir el esquema de actualización a un diccionario,
        # excluyendo valores None (campos no proporcionados para actualizar)
        update_data = alergeno_data.model_dump(exclude_none=True)

        if not update_data:
            # Si no hay datos para actualizar, simplemente retornar el alérgeno actual
            return await self.get_alergeno_by_id(alergeno_id)

        try:
            # Actualizar el alérgeno
            updated_alergeno = await self.repository.update(alergeno_id, **update_data)

            # Verificar si el alérgeno fue encontrado
            if not updated_alergeno:
                raise AlergenoNotFoundError(f"No se encontró el alérgeno con ID {alergeno_id}")

            # Convertir y retornar como esquema de respuesta
            return AlergenoResponse.model_validate(updated_alergeno)
        except IntegrityError:
            # Capturar errores de integridad (nombre duplicado)
            if "nombre" in update_data:
                raise AlergenoConflictError(
                    f"Ya existe un alérgeno con el nombre '{update_data['nombre']}'"
                )
            # Si no es por nombre, reenviar la excepción original
            raise