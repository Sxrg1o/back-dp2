"""
Handler para endpoints de ingredientes.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from domain.entities import Ingrediente
from domain.entities.enums import EtiquetaIngrediente
from application.services import IngredienteService
from infrastructure.db import get_db
from .dtos import (
    IngredienteCreateDTO, IngredienteUpdateDTO, IngredienteResponseDTO,
    IngredienteStockUpdateDTO, MessageResponseDTO, LowStockDTO
)

router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])


def get_ingrediente_service(db: Session = Depends(get_db)) -> IngredienteService:
    """
    Obtiene el servicio de ingredientes con las dependencias inyectadas.
    """
    from infrastructure.repositories import IngredienteRepositoryImpl
    
    ingrediente_repository = IngredienteRepositoryImpl(db)
    return IngredienteService(ingrediente_repository)


@router.post("/", response_model=IngredienteResponseDTO, status_code=201)
def create_ingrediente(
    ingrediente_data: IngredienteCreateDTO,
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Crea un nuevo ingrediente.
    """
    try:
        ingrediente = Ingrediente(
            nombre=ingrediente_data.nombre,
            stock=ingrediente_data.stock,
            peso=ingrediente_data.peso,
            tipo=ingrediente_data.tipo
        )
        
        created_ingrediente = service.create_ingrediente(ingrediente)
        return IngredienteResponseDTO.model_validate(created_ingrediente)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[IngredienteResponseDTO])
def get_all_ingredientes(
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Obtiene todos los ingredientes.
    """
    try:
        ingredientes = service.get_all_ingredientes()
        return [IngredienteResponseDTO.model_validate(ingrediente) for ingrediente in ingredientes]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/{ingrediente_id}", response_model=IngredienteResponseDTO)
def get_ingrediente(
    ingrediente_id: int,
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Obtiene un ingrediente específico por su ID.
    """
    try:
        ingrediente = service.get_ingrediente(ingrediente_id)
        if not ingrediente:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        
        return IngredienteResponseDTO.model_validate(ingrediente)
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put("/{ingrediente_id}", response_model=IngredienteResponseDTO)
def update_ingrediente(
    ingrediente_id: int,
    ingrediente_data: IngredienteUpdateDTO,
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Actualiza un ingrediente existente.
    """
    try:
        ingrediente = Ingrediente(
            id=ingrediente_id,
            nombre=ingrediente_data.nombre,
            stock=ingrediente_data.stock,
            peso=ingrediente_data.peso,
            tipo=ingrediente_data.tipo
        )
        
        updated_ingrediente = service.update_ingrediente(ingrediente)
        return IngredienteResponseDTO.model_validate(updated_ingrediente)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.patch("/{ingrediente_id}/stock", response_model=MessageResponseDTO)
def update_ingrediente_stock(
    ingrediente_id: int,
    stock_data: IngredienteStockUpdateDTO,
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Actualiza el stock de un ingrediente.
    """
    try:
        success = service.update_ingrediente_stock(ingrediente_id, stock_data.stock)
        if not success:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        
        return MessageResponseDTO(message="Stock actualizado correctamente")
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.patch("/{ingrediente_id}/reduce-stock", response_model=MessageResponseDTO)
def reduce_ingrediente_stock(
    ingrediente_id: int,
    cantidad: Decimal = Query(..., gt=0, description="Cantidad a reducir"),
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Reduce el stock de un ingrediente.
    """
    try:
        success = service.reduce_ingrediente_stock(ingrediente_id, cantidad)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo reducir el stock")
        
        return MessageResponseDTO(message="Stock reducido correctamente")
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{ingrediente_id}", response_model=MessageResponseDTO)
def delete_ingrediente(
    ingrediente_id: int,
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Elimina un ingrediente.
    """
    try:
        success = service.delete_ingrediente(ingrediente_id)
        if not success:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        
        return MessageResponseDTO(message="Ingrediente eliminado correctamente")
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints de búsqueda y filtros
@router.get("/search", response_model=List[IngredienteResponseDTO])
def search_ingredientes(
    q: str = Query(..., description="Término de búsqueda"),
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Busca ingredientes por nombre.
    """
    try:
        ingredientes = service.search_ingredientes(q)
        return [IngredienteResponseDTO.model_validate(ingrediente) for ingrediente in ingredientes]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/filter/tipo/{tipo}", response_model=List[IngredienteResponseDTO])
def get_ingredientes_by_tipo(
    tipo: EtiquetaIngrediente,
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Obtiene ingredientes por tipo.
    """
    try:
        ingredientes = service.get_ingredientes_by_tipo(tipo)
        return [IngredienteResponseDTO.model_validate(ingrediente) for ingrediente in ingredientes]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/verduras", response_model=List[IngredienteResponseDTO])
def get_verduras(service: IngredienteService = Depends(get_ingrediente_service)):
    """
    Obtiene todas las verduras.
    """
    try:
        ingredientes = service.get_verduras()
        return [IngredienteResponseDTO.model_validate(ingrediente) for ingrediente in ingredientes]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/carnes", response_model=List[IngredienteResponseDTO])
def get_carnes(service: IngredienteService = Depends(get_ingrediente_service)):
    """
    Obtiene todas las carnes.
    """
    try:
        ingredientes = service.get_carnes()
        return [IngredienteResponseDTO.model_validate(ingrediente) for ingrediente in ingredientes]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/frutas", response_model=List[IngredienteResponseDTO])
def get_frutas(service: IngredienteService = Depends(get_ingrediente_service)):
    """
    Obtiene todas las frutas.
    """
    try:
        ingredientes = service.get_frutas()
        return [IngredienteResponseDTO.model_validate(ingrediente) for ingrediente in ingredientes]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/low-stock", response_model=List[IngredienteResponseDTO])
def get_ingredientes_low_stock(
    threshold: Decimal = Query(10.0, ge=0, description="Umbral de stock bajo"),
    service: IngredienteService = Depends(get_ingrediente_service)
):
    """
    Obtiene ingredientes con stock bajo.
    """
    try:
        ingredientes = service.get_ingredientes_low_stock(threshold)
        return [IngredienteResponseDTO.model_validate(ingrediente) for ingrediente in ingredientes]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
