"""
Mesa (Table) API endpoints.
"""
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.security import get_current_active_user, require_staff
from app.mappers.mesa_mapper import mesa_mapper
from app.schemas.auth import TokenPayload
from app.schemas.base import PaginatedResponse, PaginationParams
from app.schemas.mesa import (
    MesaCreate,
    MesaResponse,
    MesaUpdate,
    MesaListResponse,
)
from app.services.mesa_service import mesa_service

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse,
    summary="Get mesas with pagination",
    description="Retrieve a paginated list of mesas with optional filtering",
)
async def get_mesas(
    pagination: PaginationParams = Depends(),
    activa: Optional[bool] = Query(None, description="Filter by active status"),
    min_capacidad: Optional[int] = Query(None, ge=1, description="Minimum capacity"),
    max_capacidad: Optional[int] = Query(None, ge=1, description="Maximum capacity"),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_active_user),
):
    """Get paginated list of mesas."""
    
    result = await mesa_service.get_mesas(
        db=db,
        pagination=pagination,
        activa=activa,
        min_capacidad=min_capacidad,
        max_capacidad=max_capacidad,
    )
    
    # Convert models to list response schemas
    result.content = mesa_mapper.to_list_response_list(result.content)
    
    return result


@router.get(
    "/active",
    response_model=List[MesaListResponse],
    summary="Get active mesas",
    description="Retrieve all active mesas",
)
async def get_active_mesas(
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_active_user),
):
    """Get all active mesas."""
    
    mesas = await mesa_service.get_active_mesas(db)
    return mesa_mapper.to_list_response_list(mesas)


@router.get(
    "/{mesa_id}",
    response_model=MesaResponse,
    summary="Get mesa by ID",
    description="Retrieve a specific mesa by its ID",
)
async def get_mesa(
    mesa_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_active_user),
):
    """Get mesa by ID."""
    
    mesa = await mesa_service.get_mesa(db, mesa_id)
    return mesa_mapper.to_response(mesa)


@router.get(
    "/numero/{numero}",
    response_model=MesaResponse,
    summary="Get mesa by number",
    description="Retrieve a specific mesa by its table number",
)
async def get_mesa_by_numero(
    numero: int,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_active_user),
):
    """Get mesa by table number."""
    
    mesa = await mesa_service.get_mesa_by_numero(db, numero)
    return mesa_mapper.to_response(mesa)


@router.post(
    "/",
    response_model=MesaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new mesa",
    description="Create a new mesa/table",
)
async def create_mesa(
    mesa_data: MesaCreate,
    db: AsyncSession = Depends(get_db),
    # current_user: TokenPayload = Depends(require_staff),  # Temporarily disabled for testing
):
    """Create a new mesa."""
    
    mesa = await mesa_service.create_mesa(db, mesa_data)
    return mesa_mapper.to_response(mesa)


@router.put(
    "/{mesa_id}",
    response_model=MesaResponse,
    summary="Update mesa",
    description="Update an existing mesa",
)
async def update_mesa(
    mesa_id: uuid.UUID,
    mesa_data: MesaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_staff),
):
    """Update an existing mesa."""
    
    mesa = await mesa_service.update_mesa(db, mesa_id, mesa_data)
    return mesa_mapper.to_response(mesa)


@router.delete(
    "/{mesa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete mesa",
    description="Delete a mesa",
)
async def delete_mesa(
    mesa_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_staff),
):
    """Delete a mesa."""
    
    await mesa_service.delete_mesa(db, mesa_id)
    return None