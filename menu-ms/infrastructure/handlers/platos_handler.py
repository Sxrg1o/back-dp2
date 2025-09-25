"""
Handler para endpoints de platos.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session

from domain.entities import Plato
from domain.entities.enums import EtiquetaPlato
from application.services import ItemService
from infrastructure.db import get_db
from .dtos import (
    PlatoResponseDTO, FilterPlatosDTO, MessageResponseDTO
)

router = APIRouter(prefix="/platos", tags=["platos"])


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    """
    Obtiene el servicio de ítems con las dependencias inyectadas.
    """
    from infrastructure.repositories import ItemRepositoryImpl, PlatoRepositoryImpl, BebidaRepositoryImpl
    
    item_repository = ItemRepositoryImpl(db)
    plato_repository = PlatoRepositoryImpl(db)
    bebida_repository = BebidaRepositoryImpl(db)
    
    return ItemService(item_repository, plato_repository, bebida_repository)


@router.get("/", response_model=List[PlatoResponseDTO])
def get_all_platos(
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene todos los platos.
    """
    try:
        platos = service.plato_repository.get_all()
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.post("/filter", response_model=List[PlatoResponseDTO])
def filter_platos(
    filter_data: FilterPlatosDTO = Body(...),
    service: ItemService = Depends(get_item_service)
):
    """
    Filtra platos por categoría y disponibilidad.
    
    Body:
        - categoria: Categoría de plato (opcional)
        - disponible: Estado de disponibilidad (opcional)
    """
    try:
        platos = service.filter_platos(filter_data.categoria, filter_data.disponible)
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/entradas", response_model=List[PlatoResponseDTO])
def get_entradas(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todos los platos de entrada.
    """
    try:
        platos = service.get_entradas()
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/principales", response_model=List[PlatoResponseDTO])
def get_platos_principales(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todos los platos principales.
    """
    try:
        platos = service.get_platos_principales()
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/postres", response_model=List[PlatoResponseDTO])
def get_postres(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todos los postres.
    """
    try:
        platos = service.get_postres()
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/disponibles", response_model=List[PlatoResponseDTO])
def get_platos_disponibles(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todos los platos disponibles.
    """
    try:
        platos = service.filter_platos(disponible=True)
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")