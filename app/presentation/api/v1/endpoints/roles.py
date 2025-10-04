"""
Endpoints para gestión de roles.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_database_session
from app.business.services.auth.rol_service import RolService
from app.presentation.schemas.rol_schemas import (
    RolCreate,
    RolResponse,
    RolUpdate,
    RolSummary
)
from app.business.exceptions.base_exceptions import ValidationError, NotFoundError

router = APIRouter(prefix="/roles", tags=["roles"])

# Service instance
rol_service = RolService()


@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
async def create_rol(
    rol_data: RolCreate,
    db: AsyncSession = Depends(get_database_session)
):
    """Crear un nuevo rol."""
    try:
        new_rol = await rol_service.create_rol(
            db=db,
            nombre=rol_data.nombre,
            descripcion=rol_data.descripcion
        )
        return RolResponse.from_orm(new_rol)

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating rol: {str(e)}"
        )


@router.get("/{rol_id}", response_model=RolResponse)
async def get_rol(
    rol_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener rol por ID."""
    try:
        rol = await rol_service.get_rol_by_id(db, rol_id)
        return RolResponse.from_orm(rol)

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/", response_model=List[RolResponse])
async def list_roles(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_database_session)
):
    """Listar roles con paginación."""
    roles = await rol_service.list_roles(
        db=db,
        skip=skip,
        limit=limit
    )
    return [RolResponse.from_orm(rol) for rol in roles]


@router.put("/{rol_id}", response_model=RolResponse)
async def update_rol(
    rol_id: int,
    rol_data: RolUpdate,
    db: AsyncSession = Depends(get_database_session)
):
    """Actualizar rol."""
    try:
        updated_rol = await rol_service.update_rol(
            db=db,
            rol_id=rol_id,
            nombre=rol_data.nombre,
            descripcion=rol_data.descripcion
        )
        return RolResponse.from_orm(updated_rol)

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rol(
    rol_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Eliminar rol."""
    try:
        await rol_service.delete_rol(db, rol_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/nombre/{nombre}", response_model=RolResponse)
async def get_rol_by_nombre(
    nombre: str,
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener rol por nombre."""
    try:
        rol = await rol_service.get_rol_by_nombre(db, nombre)
        return RolResponse.from_orm(rol)

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/summary/all", response_model=List[RolSummary])
async def get_roles_summary(
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener resumen de todos los roles (solo ID y nombre)."""
    roles = await rol_service.list_roles(db, skip=0, limit=1000)
    return [RolSummary.from_orm(rol) for rol in roles]


@router.get("/count/total")
async def count_roles(
    db: AsyncSession = Depends(get_database_session)
):
    """Contar total de roles."""
    count = await rol_service.get_roles_count(db)
    return {"total_roles": count}


@router.post("/initialize", response_model=List[RolResponse])
async def initialize_default_roles(
    db: AsyncSession = Depends(get_database_session)
):
    """Inicializar roles por defecto del sistema."""
    try:
        roles = await rol_service.initialize_default_roles(db)
        return [RolResponse.from_orm(rol) for rol in roles]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing default roles: {str(e)}"
        )