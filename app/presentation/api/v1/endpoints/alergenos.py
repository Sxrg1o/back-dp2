"""
Endpoints para gestión de alérgenos.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_database_session
from app.business.services.menu.alergeno_service import AlergenoService
from app.presentation.schemas.alergeno_schemas import (
    AlergenoCreate,
    AlergenoResponse,
    AlergenoUpdate,
    AlergenoSummary,
    AlergenoOrdenUpdate
)
from app.business.exceptions.base_exceptions import ValidationError, NotFoundError

router = APIRouter(prefix="/alergenos", tags=["alergenos"])

# Service instance
alergeno_service = AlergenoService()


@router.post("/", response_model=AlergenoResponse, status_code=status.HTTP_201_CREATED)
async def create_alergeno(
    alergeno_data: AlergenoCreate,
    db: AsyncSession = Depends(get_database_session)
):
    """Crear un nuevo alérgeno."""
    try:
        new_alergeno = await alergeno_service.create_alergeno(
            db=db,
            nombre=alergeno_data.nombre,
            descripcion=alergeno_data.descripcion,
            icono=alergeno_data.icono,
            nivel_riesgo=alergeno_data.nivel_riesgo,
            activo=alergeno_data.activo,
            orden=alergeno_data.orden
        )
        return AlergenoResponse.from_orm(new_alergeno)

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating alergeno: {str(e)}"
        )


@router.get("/{alergeno_id}", response_model=AlergenoResponse)
async def get_alergeno(
    alergeno_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener alérgeno por ID."""
    try:
        alergeno = await alergeno_service.get_alergeno_by_id(db, alergeno_id)
        return AlergenoResponse.from_orm(alergeno)

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/", response_model=List[AlergenoResponse])
async def list_alergenos(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum records to return"),
    activo_only: bool = Query(False, description="Show only active allergens"),
    order_by_orden: bool = Query(True, description="Order by display order"),
    db: AsyncSession = Depends(get_database_session)
):
    """Listar alérgenos con paginación."""
    alergenos = await alergeno_service.list_alergenos(
        db=db,
        skip=skip,
        limit=limit,
        activo_only=activo_only,
        order_by_orden=order_by_orden
    )
    return [AlergenoResponse.from_orm(alergeno) for alergeno in alergenos]


@router.get("/nivel-riesgo/{nivel_riesgo}", response_model=List[AlergenoResponse])
async def get_alergenos_by_risk_level(
    nivel_riesgo: str,
    activo_only: bool = Query(True, description="Show only active allergens"),
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener alérgenos por nivel de riesgo."""
    try:
        alergenos = await alergeno_service.list_by_risk_level(
            db=db,
            nivel_riesgo=nivel_riesgo,
            activo_only=activo_only
        )
        return [AlergenoResponse.from_orm(alergeno) for alergeno in alergenos]

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{alergeno_id}", response_model=AlergenoResponse)
async def update_alergeno(
    alergeno_id: int,
    alergeno_data: AlergenoUpdate,
    db: AsyncSession = Depends(get_database_session)
):
    """Actualizar alérgeno."""
    try:
        updated_alergeno = await alergeno_service.update_alergeno(
            db=db,
            alergeno_id=alergeno_id,
            nombre=alergeno_data.nombre,
            descripcion=alergeno_data.descripcion,
            icono=alergeno_data.icono,
            nivel_riesgo=alergeno_data.nivel_riesgo,
            activo=alergeno_data.activo,
            orden=alergeno_data.orden
        )
        return AlergenoResponse.from_orm(updated_alergeno)

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


@router.delete("/{alergeno_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alergeno(
    alergeno_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Eliminar alérgeno."""
    try:
        await alergeno_service.delete_alergeno(db, alergeno_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{alergeno_id}/deactivate", response_model=AlergenoResponse)
async def deactivate_alergeno(
    alergeno_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Desactivar alérgeno (soft delete)."""
    try:
        alergeno = await alergeno_service.deactivate_alergeno(db, alergeno_id)
        return AlergenoResponse.from_orm(alergeno)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{alergeno_id}/orden", response_model=AlergenoResponse)
async def update_orden(
    alergeno_id: int,
    orden_data: AlergenoOrdenUpdate,
    db: AsyncSession = Depends(get_database_session)
):
    """Actualizar orden de visualización del alérgeno."""
    try:
        alergeno = await alergeno_service.update_orden(
            db, alergeno_id, orden_data.nuevo_orden
        )
        return AlergenoResponse.from_orm(alergeno)
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


@router.get("/nombre/{nombre}", response_model=AlergenoResponse)
async def get_alergeno_by_nombre(
    nombre: str,
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener alérgeno por nombre."""
    try:
        alergeno = await alergeno_service.get_alergeno_by_nombre(db, nombre)
        return AlergenoResponse.from_orm(alergeno)

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/summary/all", response_model=List[AlergenoSummary])
async def get_alergenos_summary(
    activo_only: bool = Query(True, description="Show only active allergens"),
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener resumen de todos los alérgenos (datos mínimos)."""
    alergenos = await alergeno_service.list_alergenos(
        db, skip=0, limit=1000, activo_only=activo_only, order_by_orden=True
    )
    return [AlergenoSummary.from_orm(alergeno) for alergeno in alergenos]


@router.get("/count/total")
async def count_alergenos(
    activo_only: bool = Query(False, description="Count only active allergens"),
    db: AsyncSession = Depends(get_database_session)
):
    """Contar total de alérgenos."""
    count = await alergeno_service.get_alergenos_count(db, activo_only)
    return {"total_alergenos": count}


@router.post("/initialize", response_model=List[AlergenoResponse])
async def initialize_default_alergenos(
    db: AsyncSession = Depends(get_database_session)
):
    """Inicializar alérgenos por defecto del sistema."""
    try:
        alergenos = await alergeno_service.initialize_default_alergenos(db)
        return [AlergenoResponse.from_orm(alergeno) for alergeno in alergenos]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing default alergenos: {str(e)}"
        )