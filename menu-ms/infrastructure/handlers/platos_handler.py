"""
Handler para endpoints específicos de platos del menú.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from domain.entities import Plato
from domain.entities.enums import EtiquetaPlato, EtiquetaItem
from application.services import ItemService
from infrastructure.db import get_db
from .dtos import (
    PlatoCreateDTO, PlatoUpdateDTO, PlatoResponseDTO,
    ItemResponseDTO, MessageResponseDTO, ErrorResponseDTO
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


@router.post("/", response_model=PlatoResponseDTO, status_code=201)
def create_plato(
    plato_data: PlatoCreateDTO,
    service: ItemService = Depends(get_item_service)
):
    """
    Crea un nuevo plato en el menú.
    """
    try:
        # Construir entidad de dominio
        plato = Plato(
            valor_nutricional=plato_data.valor_nutricional,
            precio=plato_data.precio,
            tiempo_preparacion=plato_data.tiempo_preparacion,
            comentarios=plato_data.comentarios,
            receta=plato_data.receta,
            disponible=plato_data.disponible,
            unidades_disponibles=plato_data.unidades_disponibles,
            num_ingredientes=plato_data.num_ingredientes,
            kcal=plato_data.kcal,
            calorias=plato_data.calorias,
            proteinas=plato_data.proteinas,
            azucares=plato_data.azucares,
            descripcion=plato_data.descripcion,
            etiquetas=plato_data.etiquetas,
            peso=plato_data.peso,
            tipo=plato_data.tipo
        )
        
        # Mapear ingredientes_ids a entidades mínimas (solo id)
        if getattr(plato_data, 'ingredientes_ids', None):
            from domain.entities import Ingrediente
            plato.ingredientes = [Ingrediente(id=i) for i in plato_data.ingredientes_ids]
        
        created_plato = service.create_item(plato)
        return PlatoResponseDTO.model_validate(created_plato)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[PlatoResponseDTO])
def get_all_platos(
    only_available: bool = Query(False, description="Solo platos disponibles"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene todos los platos del menú.
    """
    try:
        # Obtener todos los ítems y filtrar solo platos
        all_items = service.get_all_items(only_available)
        platos = [item for item in all_items if isinstance(item, Plato)]
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/{plato_id}", response_model=PlatoResponseDTO)
def get_plato(
    plato_id: int,
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene un plato específico por su ID.
    """
    try:
        item = service.get_item(plato_id)
        if not item:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        
        if not isinstance(item, Plato):
            raise HTTPException(status_code=400, detail="El ítem no es un plato")
        
        return PlatoResponseDTO.model_validate(item)
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put("/{plato_id}", response_model=PlatoResponseDTO)
def update_plato(
    plato_id: int,
    plato_data: PlatoUpdateDTO,
    service: ItemService = Depends(get_item_service)
):
    """
    Actualiza un plato existente.
    """
    try:
        # Verificar que el ítem existe y es un plato
        existing_item = service.get_item(plato_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        
        if not isinstance(existing_item, Plato):
            raise HTTPException(status_code=400, detail="El ítem no es un plato")
        
        plato = Plato(
            id=plato_id,
            valor_nutricional=plato_data.valor_nutricional,
            precio=plato_data.precio,
            tiempo_preparacion=plato_data.tiempo_preparacion,
            comentarios=plato_data.comentarios,
            receta=plato_data.receta,
            disponible=plato_data.disponible,
            unidades_disponibles=plato_data.unidades_disponibles,
            num_ingredientes=plato_data.num_ingredientes,
            kcal=plato_data.kcal,
            calorias=plato_data.calorias,
            proteinas=plato_data.proteinas,
            azucares=plato_data.azucares,
            descripcion=plato_data.descripcion,
            etiquetas=plato_data.etiquetas,
            peso=plato_data.peso,
            tipo=plato_data.tipo
        )
        
        updated_plato = service.update_item(plato)
        return PlatoResponseDTO.model_validate(updated_plato)
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.patch("/{plato_id}/stock", response_model=MessageResponseDTO)
def update_plato_stock(
    plato_id: int,
    stock_data: dict,
    service: ItemService = Depends(get_item_service)
):
    """
    Actualiza el stock de un plato.
    """
    try:
        success = service.update_item_stock(plato_id, stock_data["unidades_disponibles"])
        if not success:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        
        return MessageResponseDTO(message="Stock del plato actualizado correctamente")
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{plato_id}", response_model=MessageResponseDTO)
def delete_plato(
    plato_id: int,
    service: ItemService = Depends(get_item_service)
):
    """
    Elimina un plato del menú.
    """
    try:
        success = service.delete_item(plato_id)
        if not success:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        
        return MessageResponseDTO(message="Plato eliminado correctamente")
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints de búsqueda y filtros específicos para platos
@router.get("/search", response_model=List[PlatoResponseDTO])
def search_platos(
    q: str = Query(..., description="Término de búsqueda"),
    service: ItemService = Depends(get_item_service)
):
    """
    Busca platos por nombre o descripción.
    """
    try:
        items = service.search_items(q)
        platos = [item for item in items if isinstance(item, Plato)]
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/filter/price", response_model=List[PlatoResponseDTO])
def get_platos_by_price_range(
    min_price: Decimal = Query(..., ge=0, description="Precio mínimo"),
    max_price: Decimal = Query(..., ge=0, description="Precio máximo"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene platos por rango de precios.
    """
    try:
        items = service.get_items_by_price_range(min_price, max_price)
        platos = [item for item in items if isinstance(item, Plato)]
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/filter/etiqueta/{etiqueta}", response_model=List[PlatoResponseDTO])
def get_platos_by_etiqueta(
    etiqueta: EtiquetaItem,
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene platos por etiqueta.
    """
    try:
        items = service.get_items_by_etiqueta(etiqueta)
        platos = [item for item in items if isinstance(item, Plato)]
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints específicos por tipo de plato
@router.get("/filter/tipo/{tipo}", response_model=List[PlatoResponseDTO])
def get_platos_by_tipo(
    tipo: EtiquetaPlato,
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene platos por tipo (ENTRADA, FONDO, POSTRE).
    """
    try:
        platos = service.get_platos_by_tipo(tipo)
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


# Endpoints específicos por peso
@router.get("/filter/weight", response_model=List[PlatoResponseDTO])
def get_platos_by_weight_range(
    min_weight: Decimal = Query(..., ge=0, description="Peso mínimo en gramos"),
    max_weight: Decimal = Query(..., ge=0, description="Peso máximo en gramos"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene platos por rango de peso.
    """
    try:
        # Obtener todos los platos y filtrar por peso
        all_items = service.get_all_items()
        platos = [
            item for item in all_items 
            if isinstance(item, Plato) and min_weight <= item.peso <= max_weight
        ]
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints específicos por densidad calórica
@router.get("/filter/caloric-density", response_model=List[PlatoResponseDTO])
def get_platos_by_caloric_density(
    min_density: Decimal = Query(..., ge=0, description="Densidad calórica mínima (cal/g)"),
    max_density: Decimal = Query(..., ge=0, description="Densidad calórica máxima (cal/g)"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene platos por rango de densidad calórica.
    """
    try:
        # Obtener todos los platos y filtrar por densidad calórica
        all_items = service.get_all_items()
        platos = []
        for item in all_items:
            if isinstance(item, Plato):
                density = item.calcular_densidad_calorica()
                if min_density <= density <= max_density:
                    platos.append(item)
        
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")