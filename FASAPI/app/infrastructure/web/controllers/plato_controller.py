"""
Plato controller for dish management.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.services.plato_service import PlatoApplicationService
from app.infrastructure.web.dependencies.menu_dependencies import get_plato_service
from app.infrastructure.web.schemas.plato_schemas import (
    PlatoCreateSchema,
    PlatoUpdateSchema,
    PlatoResponseSchema,
    PlatoListResponseSchema,
    AgregarIngredienteRecetaSchema,
    ActualizarIngredienteRecetaSchema
)
from app.infrastructure.web.schemas.mappers.menu_schema_mapper import PlatoSchemaMapper
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.domain.exceptions.menu_exceptions import (
    PlatoNotFoundError,
    PlatoAlreadyExistsError,
    IngredienteNotFoundError,
    MenuDomainException
)


router = APIRouter(prefix="/platos", tags=["platos"])


@router.post("/", response_model=PlatoResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_plato(
    plato_data: PlatoCreateSchema,
    plato_service: PlatoApplicationService = Depends(get_plato_service)
) -> PlatoResponseSchema:
    """Create a new dish."""
    try:
        create_dto = PlatoSchemaMapper.plato_create_schema_to_dto(plato_data)
        plato_dto = await plato_service.create_plato(create_dto)
        return PlatoSchemaMapper.plato_dto_to_response_schema(plato_dto)
    except PlatoAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=List[PlatoListResponseSchema])
async def get_platos(
    available_only: bool = Query(True),
    tipo_plato: EtiquetaPlato = Query(None),
    dificultad: str = Query(None),
    chef: str = Query(None),
    plato_service: PlatoApplicationService = Depends(get_plato_service)
) -> List[PlatoListResponseSchema]:
    """Get all dishes with optional filtering."""
    try:
        if tipo_plato:
            platos_dto = await plato_service.get_platos_by_dish_type(tipo_plato)
        elif dificultad:
            platos_dto = await plato_service.get_platos_by_difficulty(dificultad)
        elif chef:
            platos_dto = await plato_service.get_platos_by_chef(chef)
        elif available_only:
            platos_dto = await plato_service.get_available_platos()
        else:
            platos_dto = await plato_service.get_all_platos()
        
        return [PlatoSchemaMapper.plato_dto_to_list_response_schema(plato) for plato in platos_dto]
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{plato_id}", response_model=PlatoResponseSchema)
async def get_plato_by_id(
    plato_id: UUID,
    plato_service: PlatoApplicationService = Depends(get_plato_service)
) -> PlatoResponseSchema:
    """Get dish by ID."""
    try:
        plato_dto = await plato_service.get_plato_by_id(plato_id)
        return PlatoSchemaMapper.plato_dto_to_response_schema(plato_dto)
    except PlatoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{plato_id}", response_model=PlatoResponseSchema)
async def update_plato(
    plato_id: UUID,
    plato_data: PlatoUpdateSchema,
    plato_service: PlatoApplicationService = Depends(get_plato_service)
) -> PlatoResponseSchema:
    """Update an existing dish."""
    try:
        update_dto = PlatoSchemaMapper.plato_update_schema_to_dto(plato_data)
        plato_dto = await plato_service.update_plato(plato_id, update_dto)
        return PlatoSchemaMapper.plato_dto_to_response_schema(plato_dto)
    except PlatoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PlatoAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{plato_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plato(
    plato_id: UUID,
    plato_service: PlatoApplicationService = Depends(get_plato_service)
):
    """Delete a dish."""
    try:
        deleted = await plato_service.delete_plato(plato_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dish with ID {plato_id} not found")
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/{plato_id}/ingredientes", response_model=PlatoResponseSchema)
async def agregar_ingrediente_receta(
    plato_id: UUID,
    ingrediente_data: AgregarIngredienteRecetaSchema,
    plato_service: PlatoApplicationService = Depends(get_plato_service)
) -> PlatoResponseSchema:
    """Add ingredient to dish recipe."""
    try:
        agregar_dto = PlatoSchemaMapper.agregar_ingrediente_schema_to_dto(ingrediente_data)
        plato_dto = await plato_service.agregar_ingrediente_receta(
            plato_id, agregar_dto.ingrediente_id, agregar_dto.cantidad
        )
        return PlatoSchemaMapper.plato_dto_to_response_schema(plato_dto)
    except (PlatoNotFoundError, IngredienteNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{plato_id}/ingredientes/{ingrediente_id}", response_model=PlatoResponseSchema)
async def remover_ingrediente_receta(
    plato_id: UUID,
    ingrediente_id: UUID,
    plato_service: PlatoApplicationService = Depends(get_plato_service)
) -> PlatoResponseSchema:
    """Remove ingredient from dish recipe."""
    try:
        plato_dto = await plato_service.remover_ingrediente_receta(plato_id, ingrediente_id)
        return PlatoSchemaMapper.plato_dto_to_response_schema(plato_dto)
    except (PlatoNotFoundError, IngredienteNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.patch("/{plato_id}/ingredientes/{ingrediente_id}", response_model=PlatoResponseSchema)
async def actualizar_ingrediente_receta(
    plato_id: UUID,
    ingrediente_id: UUID,
    update_data: ActualizarIngredienteRecetaSchema,
    plato_service: PlatoApplicationService = Depends(get_plato_service)
) -> PlatoResponseSchema:
    """Update ingredient quantity in dish recipe."""
    try:
        update_dto = PlatoSchemaMapper.actualizar_ingrediente_schema_to_dto(update_data)
        plato_dto = await plato_service.actualizar_ingrediente_receta(
            plato_id, ingrediente_id, update_dto.nueva_cantidad
        )
        return PlatoSchemaMapper.plato_dto_to_response_schema(plato_dto)
    except (PlatoNotFoundError, IngredienteNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{plato_id}/disponibilidad", response_model=bool)
async def verificar_disponibilidad_ingredientes(
    plato_id: UUID,
    plato_service: PlatoApplicationService = Depends(get_plato_service)
) -> bool:
    """Check if all ingredients for a dish are available."""
    try:
        return await plato_service.verificar_disponibilidad_ingredientes(plato_id)
    except PlatoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{plato_id}/costo", response_model=float)
async def calcular_costo_ingredientes(
    plato_id: UUID,
    plato_service: PlatoApplicationService = Depends(get_plato_service)
) -> float:
    """Calculate total cost of ingredients for a dish."""
    try:
        return await plato_service.calcular_costo_ingredientes(plato_id)
    except PlatoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")