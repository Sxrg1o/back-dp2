"""
Handler para endpoints de ítems del menú.
"""

from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from ...domain.entities import Item, Plato, Bebida
from ...domain.entities.enums import EtiquetaItem, EtiquetaPlato
from ...application.services import ItemService
from ..db import get_db
from .dtos import (
    PlatoCreateDTO, PlatoUpdateDTO, PlatoResponseDTO,
    BebidaCreateDTO, BebidaUpdateDTO, BebidaResponseDTO,
    ItemResponseDTO, StockUpdateDTO, ItemSearchDTO, PriceRangeDTO,
    MessageResponseDTO, ErrorResponseDTO
)

router = APIRouter(prefix="/items", tags=["items"])


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    """
    Obtiene el servicio de ítems con las dependencias inyectadas.
    """
    from ..repositories import ItemRepositoryImpl, PlatoRepositoryImpl, BebidaRepositoryImpl
    
    item_repository = ItemRepositoryImpl(db)
    plato_repository = PlatoRepositoryImpl(db)
    bebida_repository = BebidaRepositoryImpl(db)
    
    return ItemService(item_repository, plato_repository, bebida_repository)


@router.post("/platos", response_model=PlatoResponseDTO, status_code=201)
def create_plato(
    plato_data: PlatoCreateDTO,
    service: ItemService = Depends(get_item_service)
):
    """
    Crea un nuevo plato en el menú.
    """
    try:
        from ...domain.entities import Plato
        
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
        
        created_plato = service.create_item(plato)
        return PlatoResponseDTO.model_validate(created_plato)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.post("/bebidas", response_model=BebidaResponseDTO, status_code=201)
def create_bebida(
    bebida_data: BebidaCreateDTO,
    service: ItemService = Depends(get_item_service)
):
    """
    Crea una nueva bebida en el menú.
    """
    try:
        from ...domain.entities import Bebida
        
        bebida = Bebida(
            valor_nutricional=bebida_data.valor_nutricional,
            precio=bebida_data.precio,
            tiempo_preparacion=bebida_data.tiempo_preparacion,
            comentarios=bebida_data.comentarios,
            receta=bebida_data.receta,
            disponible=bebida_data.disponible,
            unidades_disponibles=bebida_data.unidades_disponibles,
            num_ingredientes=bebida_data.num_ingredientes,
            kcal=bebida_data.kcal,
            calorias=bebida_data.calorias,
            proteinas=bebida_data.proteinas,
            azucares=bebida_data.azucares,
            descripcion=bebida_data.descripcion,
            etiquetas=bebida_data.etiquetas,
            litros=bebida_data.litros,
            alcoholico=bebida_data.alcoholico
        )
        
        created_bebida = service.create_item(bebida)
        return BebidaResponseDTO.model_validate(created_bebida)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[ItemResponseDTO])
def get_all_items(
    only_available: bool = Query(False, description="Solo ítems disponibles"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene todos los ítems del menú.
    """
    try:
        items = service.get_all_items(only_available)
        return [ItemResponseDTO.model_validate(item) for item in items]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/{item_id}", response_model=ItemResponseDTO)
def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene un ítem específico por su ID.
    """
    try:
        item = service.get_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Ítem no encontrado")
        
        return ItemResponseDTO.model_validate(item)
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put("/platos/{item_id}", response_model=PlatoResponseDTO)
def update_plato(
    item_id: int,
    plato_data: PlatoUpdateDTO,
    service: ItemService = Depends(get_item_service)
):
    """
    Actualiza un plato existente.
    """
    try:
        from ...domain.entities import Plato
        
        # Verificar que el ítem existe y es un plato
        existing_item = service.get_item(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Plato no encontrado")
        
        if not isinstance(existing_item, Plato):
            raise HTTPException(status_code=400, detail="El ítem no es un plato")
        
        plato = Plato(
            id=item_id,
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


@router.put("/bebidas/{item_id}", response_model=BebidaResponseDTO)
def update_bebida(
    item_id: int,
    bebida_data: BebidaUpdateDTO,
    service: ItemService = Depends(get_item_service)
):
    """
    Actualiza una bebida existente.
    """
    try:
        from ...domain.entities import Bebida
        
        # Verificar que el ítem existe y es una bebida
        existing_item = service.get_item(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Bebida no encontrada")
        
        if not isinstance(existing_item, Bebida):
            raise HTTPException(status_code=400, detail="El ítem no es una bebida")
        
        bebida = Bebida(
            id=item_id,
            valor_nutricional=bebida_data.valor_nutricional,
            precio=bebida_data.precio,
            tiempo_preparacion=bebida_data.tiempo_preparacion,
            comentarios=bebida_data.comentarios,
            receta=bebida_data.receta,
            disponible=bebida_data.disponible,
            unidades_disponibles=bebida_data.unidades_disponibles,
            num_ingredientes=bebida_data.num_ingredientes,
            kcal=bebida_data.kcal,
            calorias=bebida_data.calorias,
            proteinas=bebida_data.proteinas,
            azucares=bebida_data.azucares,
            descripcion=bebida_data.descripcion,
            etiquetas=bebida_data.etiquetas,
            litros=bebida_data.litros,
            alcoholico=bebida_data.alcoholico
        )
        
        updated_bebida = service.update_item(bebida)
        return BebidaResponseDTO.model_validate(updated_bebida)
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.patch("/{item_id}/stock", response_model=MessageResponseDTO)
def update_item_stock(
    item_id: int,
    stock_data: StockUpdateDTO,
    service: ItemService = Depends(get_item_service)
):
    """
    Actualiza el stock de un ítem.
    """
    try:
        success = service.update_item_stock(item_id, stock_data.unidades_disponibles)
        if not success:
            raise HTTPException(status_code=404, detail="Ítem no encontrado")
        
        return MessageResponseDTO(message="Stock actualizado correctamente")
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{item_id}", response_model=MessageResponseDTO)
def delete_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
):
    """
    Elimina un ítem del menú.
    """
    try:
        success = service.delete_item(item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Ítem no encontrado")
        
        return MessageResponseDTO(message="Ítem eliminado correctamente")
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints de búsqueda y filtros
@router.get("/search", response_model=List[ItemResponseDTO])
def search_items(
    q: str = Query(..., description="Término de búsqueda"),
    service: ItemService = Depends(get_item_service)
):
    """
    Busca ítems por nombre o descripción.
    """
    try:
        items = service.search_items(q)
        return [ItemResponseDTO.model_validate(item) for item in items]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/filter/price", response_model=List[ItemResponseDTO])
def get_items_by_price_range(
    min_price: Decimal = Query(..., ge=0, description="Precio mínimo"),
    max_price: Decimal = Query(..., ge=0, description="Precio máximo"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene ítems por rango de precios.
    """
    try:
        items = service.get_items_by_price_range(min_price, max_price)
        return [ItemResponseDTO.model_validate(item) for item in items]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/filter/etiqueta/{etiqueta}", response_model=List[ItemResponseDTO])
def get_items_by_etiqueta(
    etiqueta: EtiquetaItem,
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene ítems por etiqueta.
    """
    try:
        items = service.get_items_by_etiqueta(etiqueta)
        return [ItemResponseDTO.model_validate(item) for item in items]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints específicos para platos
@router.get("/platos/entradas", response_model=List[PlatoResponseDTO])
def get_entradas(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todos los platos de entrada.
    """
    try:
        platos = service.get_entradas()
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/platos/principales", response_model=List[PlatoResponseDTO])
def get_platos_principales(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todos los platos principales.
    """
    try:
        platos = service.get_platos_principales()
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/platos/postres", response_model=List[PlatoResponseDTO])
def get_postres(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todos los postres.
    """
    try:
        platos = service.get_postres()
        return [PlatoResponseDTO.model_validate(plato) for plato in platos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints específicos para bebidas
@router.get("/bebidas/alcoholicas", response_model=List[BebidaResponseDTO])
def get_bebidas_alcoholicas(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todas las bebidas alcohólicas.
    """
    try:
        bebidas = service.get_bebidas_alcoholicas()
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/bebidas/no-alcoholicas", response_model=List[BebidaResponseDTO])
def get_bebidas_no_alcoholicas(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todas las bebidas no alcohólicas.
    """
    try:
        bebidas = service.get_bebidas_no_alcoholicas()
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/bebidas/filter/volume", response_model=List[BebidaResponseDTO])
def get_bebidas_by_volume_range(
    min_volume: Decimal = Query(..., ge=0, description="Volumen mínimo en litros"),
    max_volume: Decimal = Query(..., ge=0, description="Volumen máximo en litros"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene bebidas por rango de volumen.
    """
    try:
        bebidas = service.get_bebidas_by_volume_range(min_volume, max_volume)
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
