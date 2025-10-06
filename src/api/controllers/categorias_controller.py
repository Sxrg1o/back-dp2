"""
Endpoints para gestión de categorías.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.business_logic.menu.categoria_service import CategoriaService
from src.api.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
    CategoriaSummary
)
from src.business_logic.exceptions.base_exceptions import ValidationError, NotFoundError

router = APIRouter(prefix="/categorias", tags=["categorias"])

# Service instance
categoria_service = CategoriaService()


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
async def create_categoria(
    categoria_data: CategoriaCreate,
    db: AsyncSession = Depends(get_database_session)
):
    """Crear una nueva categoría."""
    try:
        new_categoria = await categoria_service.create_categoria(
            db=db,
            nombre=categoria_data.nombre,
            descripcion=categoria_data.descripcion,
            orden=categoria_data.orden,
            activo=categoria_data.activo,
            imagen_path=categoria_data.imagen_path
        )
        return CategoriaResponse.from_orm(new_categoria)

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def get_categoria(
    categoria_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener categoría por ID."""
    try:
        categoria = await categoria_service.get_categoria_by_id(db, categoria_id)
        return CategoriaResponse.from_orm(categoria)

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/", response_model=List[CategoriaResponse])
async def list_categorias(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum records to return"),
    activo_only: bool = Query(False, description="Show only active categories"),
    order_by_orden: bool = Query(True, description="Order by display order"),
    db: AsyncSession = Depends(get_database_session)
):
    """Listar categorías con paginación."""
    categorias = await categoria_service.list_categorias(
        db=db,
        skip=skip,
        limit=limit,
        activo_only=activo_only,
        order_by_orden=order_by_orden
    )
    return [CategoriaResponse.from_orm(categoria) for categoria in categorias]


@router.put("/{categoria_id}", response_model=CategoriaResponse)
async def update_categoria(
    categoria_id: int,
    categoria_data: CategoriaUpdate,
    db: AsyncSession = Depends(get_database_session)
):
    """Actualizar categoría."""
    try:
        updated_categoria = await categoria_service.update_categoria(
            db=db,
            categoria_id=categoria_id,
            nombre=categoria_data.nombre,
            descripcion=categoria_data.descripcion,
            orden=categoria_data.orden,
            activo=categoria_data.activo,
            imagen_path=categoria_data.imagen_path
        )
        return CategoriaResponse.from_orm(updated_categoria)

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


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(
    categoria_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Eliminar categoría."""
    try:
        await categoria_service.delete_categoria(db, categoria_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/summary/all", response_model=List[CategoriaSummary])
async def get_categorias_summary(
    activo_only: bool = Query(True, description="Show only active categories"),
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener resumen de todas las categorías."""
    categorias = await categoria_service.list_categorias(
        db, skip=0, limit=1000, activo_only=activo_only, order_by_orden=True
    )
    return [CategoriaSummary.from_orm(categoria) for categoria in categorias]


@router.post("/initialize", response_model=List[CategoriaResponse])
async def initialize_default_categorias(
    db: AsyncSession = Depends(get_database_session)
):
    """Inicializar categorías por defecto del sistema."""
    try:
        categorias = await categoria_service.initialize_default_categorias(db)
        return [CategoriaResponse.from_orm(categoria) for categoria in categorias]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing default categorias: {str(e)}"
        )