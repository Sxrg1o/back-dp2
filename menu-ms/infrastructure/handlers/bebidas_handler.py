"""
Handler para endpoints específicos de bebidas del menú.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from domain.entities import Bebida
from domain.entities.enums import EtiquetaItem
from application.services import ItemService
from infrastructure.db import get_db
from .dtos import (
    BebidaCreateDTO, BebidaUpdateDTO, BebidaResponseDTO,
    ItemResponseDTO, MessageResponseDTO, ErrorResponseDTO
)

router = APIRouter(prefix="/bebidas", tags=["bebidas"])


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    """
    Obtiene el servicio de ítems con las dependencias inyectadas.
    """
    from infrastructure.repositories import ItemRepositoryImpl, PlatoRepositoryImpl, BebidaRepositoryImpl
    
    item_repository = ItemRepositoryImpl(db)
    plato_repository = PlatoRepositoryImpl(db)
    bebida_repository = BebidaRepositoryImpl(db)
    
    return ItemService(item_repository, plato_repository, bebida_repository)


@router.post("/", response_model=BebidaResponseDTO, status_code=201)
def create_bebida(
    bebida_data: BebidaCreateDTO,
    service: ItemService = Depends(get_item_service)
):
    """
    Crea una nueva bebida en el menú.
    """
    try:
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
        
        if getattr(bebida_data, 'ingredientes_ids', None):
            from domain.entities import Ingrediente
            bebida.ingredientes = [Ingrediente(id=i) for i in bebida_data.ingredientes_ids]
        
        created_bebida = service.create_item(bebida)
        return BebidaResponseDTO.model_validate(created_bebida)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[BebidaResponseDTO])
def get_all_bebidas(
    only_available: bool = Query(False, description="Solo bebidas disponibles"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene todas las bebidas del menú.
    """
    try:
        # Obtener todos los ítems y filtrar solo bebidas
        all_items = service.get_all_items(only_available)
        bebidas = [item for item in all_items if isinstance(item, Bebida)]
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/{bebida_id}", response_model=BebidaResponseDTO)
def get_bebida(
    bebida_id: int,
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene una bebida específica por su ID.
    """
    try:
        item = service.get_item(bebida_id)
        if not item:
            raise HTTPException(status_code=404, detail="Bebida no encontrada")
        
        if not isinstance(item, Bebida):
            raise HTTPException(status_code=400, detail="El ítem no es una bebida")
        
        return BebidaResponseDTO.model_validate(item)
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put("/{bebida_id}", response_model=BebidaResponseDTO)
def update_bebida(
    bebida_id: int,
    bebida_data: BebidaUpdateDTO,
    service: ItemService = Depends(get_item_service)
):
    """
    Actualiza una bebida existente.
    """
    try:
        # Verificar que el ítem existe y es una bebida
        existing_item = service.get_item(bebida_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Bebida no encontrada")
        
        if not isinstance(existing_item, Bebida):
            raise HTTPException(status_code=400, detail="El ítem no es una bebida")
        
        bebida = Bebida(
            id=bebida_id,
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


@router.patch("/{bebida_id}/stock", response_model=MessageResponseDTO)
def update_bebida_stock(
    bebida_id: int,
    stock_data: dict,
    service: ItemService = Depends(get_item_service)
):
    """
    Actualiza el stock de una bebida.
    """
    try:
        success = service.update_item_stock(bebida_id, stock_data["unidades_disponibles"])
        if not success:
            raise HTTPException(status_code=404, detail="Bebida no encontrada")
        
        return MessageResponseDTO(message="Stock de la bebida actualizado correctamente")
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{bebida_id}", response_model=MessageResponseDTO)
def delete_bebida(
    bebida_id: int,
    service: ItemService = Depends(get_item_service)
):
    """
    Elimina una bebida del menú.
    """
    try:
        success = service.delete_item(bebida_id)
        if not success:
            raise HTTPException(status_code=404, detail="Bebida no encontrada")
        
        return MessageResponseDTO(message="Bebida eliminada correctamente")
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints de búsqueda y filtros específicos para bebidas
@router.get("/search", response_model=List[BebidaResponseDTO])
def search_bebidas(
    q: str = Query(..., description="Término de búsqueda"),
    service: ItemService = Depends(get_item_service)
):
    """
    Busca bebidas por nombre o descripción.
    """
    try:
        items = service.search_items(q)
        bebidas = [item for item in items if isinstance(item, Bebida)]
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/filter/price", response_model=List[BebidaResponseDTO])
def get_bebidas_by_price_range(
    min_price: Decimal = Query(..., ge=0, description="Precio mínimo"),
    max_price: Decimal = Query(..., ge=0, description="Precio máximo"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene bebidas por rango de precios.
    """
    try:
        items = service.get_items_by_price_range(min_price, max_price)
        bebidas = [item for item in items if isinstance(item, Bebida)]
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/filter/etiqueta/{etiqueta}", response_model=List[BebidaResponseDTO])
def get_bebidas_by_etiqueta(
    etiqueta: EtiquetaItem,
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene bebidas por etiqueta.
    """
    try:
        items = service.get_items_by_etiqueta(etiqueta)
        bebidas = [item for item in items if isinstance(item, Bebida)]
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints específicos por tipo de bebida
@router.get("/alcoholicas", response_model=List[BebidaResponseDTO])
def get_bebidas_alcoholicas(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todas las bebidas alcohólicas.
    """
    try:
        bebidas = service.get_bebidas_alcoholicas()
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/no-alcoholicas", response_model=List[BebidaResponseDTO])
def get_bebidas_no_alcoholicas(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todas las bebidas no alcohólicas.
    """
    try:
        bebidas = service.get_bebidas_no_alcoholicas()
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/filter/alcoholico", response_model=List[BebidaResponseDTO])
def get_bebidas_by_alcoholico(
    alcoholico: bool = Query(..., description="Filtrar por bebidas alcohólicas (true) o no alcohólicas (false)"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene bebidas filtradas por contenido alcohólico.
    """
    try:
        if alcoholico:
            bebidas = service.get_bebidas_alcoholicas()
        else:
            bebidas = service.get_bebidas_no_alcoholicas()
        
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints específicos por volumen
@router.get("/filter/volume", response_model=List[BebidaResponseDTO])
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


# Endpoints específicos por densidad calórica
@router.get("/filter/caloric-density", response_model=List[BebidaResponseDTO])
def get_bebidas_by_caloric_density(
    min_density: Decimal = Query(..., ge=0, description="Densidad calórica mínima (cal/L)"),
    max_density: Decimal = Query(..., ge=0, description="Densidad calórica máxima (cal/L)"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene bebidas por rango de densidad calórica.
    """
    try:
        # Obtener todas las bebidas y filtrar por densidad calórica
        all_items = service.get_all_items()
        bebidas = []
        for item in all_items:
            if isinstance(item, Bebida):
                density = item.calcular_densidad_calorica()
                if min_density <= density <= max_density:
                    bebidas.append(item)
        
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints específicos por calorías por mililitro
@router.get("/filter/calories-per-ml", response_model=List[BebidaResponseDTO])
def get_bebidas_by_calories_per_ml(
    min_calories_per_ml: Decimal = Query(..., ge=0, description="Calorías por ml mínimas"),
    max_calories_per_ml: Decimal = Query(..., ge=0, description="Calorías por ml máximas"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene bebidas por rango de calorías por mililitro.
    """
    try:
        # Obtener todas las bebidas y filtrar por calorías por ml
        all_items = service.get_all_items()
        bebidas = []
        for item in all_items:
            if isinstance(item, Bebida):
                calories_per_ml = item.calcular_calorias_por_ml()
                if min_calories_per_ml <= calories_per_ml <= max_calories_per_ml:
                    bebidas.append(item)
        
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints específicos para bebidas aptas para menores
@router.get("/aptas-para-menores", response_model=List[BebidaResponseDTO])
def get_bebidas_aptas_para_menores(service: ItemService = Depends(get_item_service)):
    """
    Obtiene todas las bebidas aptas para menores de edad (no alcohólicas).
    """
    try:
        bebidas = service.get_bebidas_no_alcoholicas()
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Endpoints específicos por rango de litros (categorías)
@router.get("/filter/volume-category", response_model=List[BebidaResponseDTO])
def get_bebidas_by_volume_category(
    category: str = Query(..., description="Categoría de volumen: 'pequena' (<0.5L), 'mediana' (0.5-1L), 'grande' (>1L)"),
    service: ItemService = Depends(get_item_service)
):
    """
    Obtiene bebidas por categoría de volumen.
    """
    try:
        all_items = service.get_all_items()
        bebidas = []
        
        for item in all_items:
            if isinstance(item, Bebida):
                if category == "pequena" and item.litros < 0.5:
                    bebidas.append(item)
                elif category == "mediana" and 0.5 <= item.litros <= 1.0:
                    bebidas.append(item)
                elif category == "grande" and item.litros > 1.0:
                    bebidas.append(item)
        
        return [BebidaResponseDTO.model_validate(bebida) for bebida in bebidas]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
