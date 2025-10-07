"""
Endpoints para gestión de alérgenos.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.business_logic.menu.alergeno_service import AlergenoService
from src.api.schemas.alergeno_schema import (
    AlergenoCreate,
    AlergenoResponse,
    AlergenoUpdate,
    AlergenoList,
)
from src.business_logic.exceptions.alergeno_exceptions import (
    AlergenoValidationError,
    AlergenoNotFoundError,
    AlergenoConflictError,
)

router = APIRouter(prefix="/alergenos", tags=["Alérgenos"])


@router.post(
    "",
    response_model=AlergenoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo alérgeno",
    description="Crea un nuevo alérgeno en el sistema con los datos proporcionados.",
)
async def create_alergeno(
    alergeno_data: AlergenoCreate, session: AsyncSession = Depends(get_database_session)
) -> AlergenoResponse:
    """
    Crea un nuevo alérgeno en el sistema.
    
    Args:
        alergeno_data: Datos del alérgeno a crear.
        session: Sesión de base de datos.

    Returns:
        El alérgeno creado con todos sus datos.

    Raises:
        HTTPException:
            - 409: Si ya existe un alérgeno con el mismo nombre.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        alergeno_service = AlergenoService(session)
        return await alergeno_service.create_alergeno(alergeno_data)
    except AlergenoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "/{alergeno_id}",
    response_model=AlergenoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un alérgeno por ID",
    description="Obtiene los detalles de un alérgeno específico por su ID.",
)
async def get_alergeno(
    alergeno_id: UUID, session: AsyncSession = Depends(get_database_session)
) -> AlergenoResponse:
    """
    Obtiene un alérgeno específico por su ID.

    Args:
        alergeno_id: ID del alérgeno a buscar.
        session: Sesión de base de datos.

    Returns:
        El alérgeno encontrado con todos sus datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra el alérgeno.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        alergeno_service = AlergenoService(session)
        return await alergeno_service.get_alergeno_by_id(alergeno_id)
    except AlergenoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "",
    response_model=AlergenoList,
    status_code=status.HTTP_200_OK,
    summary="Listar alérgenos",
    description="Obtiene una lista paginada de alérgenos.",
)
async def list_alergenos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir (paginación)"),
    limit: int = Query(
        100, gt=0, le=500, description="Número máximo de registros a retornar"
    ),
    session: AsyncSession = Depends(get_database_session),
) -> AlergenoList:
    """
    Obtiene una lista paginada de alérgenos.
    
    Args:
        skip: Número de registros a omitir (offset), por defecto 0.
        limit: Número máximo de registros a retornar, por defecto 100.
        session: Sesión de base de datos.

    Returns:
        Lista paginada de alérgenos y el número total de registros.

    Raises:
        HTTPException:
            - 400: Si los parámetros de paginación son inválidos.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        alergeno_service = AlergenoService(session)
        return await alergeno_service.get_alergenos(skip, limit)
    except AlergenoValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.put(
    "/{alergeno_id}",
    response_model=AlergenoResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un alérgeno",
    description="Actualiza los datos de un alérgeno existente.",
)
async def update_alergeno(
    alergeno_id: UUID,
    alergeno_data: AlergenoUpdate,
    session: AsyncSession = Depends(get_database_session),
) -> AlergenoResponse:
    """
    Actualiza un alérgeno existente.

    Args:
        alergeno_id: ID del alérgeno a actualizar.
        alergeno_data: Datos del alérgeno a actualizar.
        session: Sesión de base de datos.

    Returns:
        El alérgeno actualizado con todos sus datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra el alérgeno.
            - 409: Si hay un conflicto (e.g., nombre duplicado).
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        alergeno_service = AlergenoService(session)
        return await alergeno_service.update_alergeno(alergeno_id, alergeno_data)
    except AlergenoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AlergenoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.delete(
    "/{alergeno_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un alérgeno",
    description="Elimina un alérgeno existente del sistema.",
)
async def delete_alergeno(
    alergeno_id: UUID, session: AsyncSession = Depends(get_database_session)
) -> None:
    """
    Elimina un alérgeno existente.

    Args:
        alergeno_id: ID del alérgeno a eliminar.
        session: Sesión de base de datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra el alérgeno.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        alergeno_service = AlergenoService(session)
        result = await alergeno_service.delete_alergeno(alergeno_id)
        # No es necesario verificar el resultado aquí ya que delete_alergeno
        # lanza AlergenoNotFoundError si no encuentra el alérgeno
    except AlergenoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )
