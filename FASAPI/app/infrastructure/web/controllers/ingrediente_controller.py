"""
Ingrediente controller for ingredient management.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.services.ingrediente_service import IngredienteApplicationService
from app.infrastructure.web.dependencies.menu_dependencies import get_ingrediente_service
from app.infrastructure.web.schemas.ingrediente_schemas import (
    IngredienteCreateSchema,
    IngredienteUpdateSchema,
    IngredienteResponseSchema,
    IngredienteListResponseSchema,
    StockUpdateSchema
)
from app.infrastructure.web.schemas.mappers.menu_schema_mapper import IngredienteSchemaMapper
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.domain.exceptions.menu_exceptions import (
    IngredienteNotFoundError,
    IngredienteAlreadyExistsError,
    InsufficientStockError,
    MenuDomainException
)


router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])


@router.post(
    "/",
    response_model=IngredienteResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create ingredient",
    description="Create a new ingredient"
)
async def create_ingrediente(
    ingrediente_data: IngredienteCreateSchema,
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
) -> IngredienteResponseSchema:
    """Create a new ingredient."""
    try:
        # Convert schema to DTO
        create_dto = IngredienteSchemaMapper.ingrediente_create_schema_to_dto(ingrediente_data)
        
        # Create ingredient through service
        ingrediente_dto = await ingrediente_service.create_ingrediente(create_dto)
        
        # Convert DTO to response schema
        return IngredienteSchemaMapper.ingrediente_dto_to_response_schema(ingrediente_dto)
        
    except IngredienteAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while creating ingredient"
        )


@router.get(
    "/",
    response_model=List[IngredienteListResponseSchema],
    summary="Get all ingredients",
    description="Retrieve all ingredients with optional filtering"
)
async def get_ingredientes(
    available_only: bool = Query(True, description="Filter by availability"),
    tipo: EtiquetaIngrediente = Query(None, description="Filter by ingredient type"),
    proveedor: str = Query(None, description="Filter by supplier"),
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
) -> List[IngredienteListResponseSchema]:
    """Get all ingredients with optional filtering."""
    try:
        if tipo:
            # Filter by type
            ingredientes_dto = await ingrediente_service.get_ingredientes_by_type(tipo)
        elif proveedor:
            # Filter by supplier
            ingredientes_dto = await ingrediente_service.get_ingredientes_by_supplier(proveedor)
        elif available_only:
            # Get only available ingredients
            ingredientes_dto = await ingrediente_service.get_available_ingredientes()
        else:
            # Get all ingredients
            ingredientes_dto = await ingrediente_service.get_all_ingredientes()
        
        # Convert DTOs to list response schemas
        return [IngredienteSchemaMapper.ingrediente_dto_to_list_response_schema(ing) for ing in ingredientes_dto]
        
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving ingredients"
        )


@router.get(
    "/{ingrediente_id}",
    response_model=IngredienteResponseSchema,
    summary="Get ingredient by ID",
    description="Retrieve a specific ingredient by its ID"
)
async def get_ingrediente_by_id(
    ingrediente_id: UUID,
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
) -> IngredienteResponseSchema:
    """Get ingredient by ID."""
    try:
        # Get ingredient through service
        ingrediente_dto = await ingrediente_service.get_ingrediente_by_id(ingrediente_id)
        
        # Convert DTO to response schema
        return IngredienteSchemaMapper.ingrediente_dto_to_response_schema(ingrediente_dto)
        
    except IngredienteNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving ingredient"
        )


@router.put(
    "/{ingrediente_id}",
    response_model=IngredienteResponseSchema,
    summary="Update ingredient",
    description="Update an existing ingredient"
)
async def update_ingrediente(
    ingrediente_id: UUID,
    ingrediente_data: IngredienteUpdateSchema,
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
) -> IngredienteResponseSchema:
    """Update an existing ingredient."""
    try:
        # Convert schema to DTO
        update_dto = IngredienteSchemaMapper.ingrediente_update_schema_to_dto(ingrediente_data)
        
        # Update ingredient through service
        ingrediente_dto = await ingrediente_service.update_ingrediente(ingrediente_id, update_dto)
        
        # Convert DTO to response schema
        return IngredienteSchemaMapper.ingrediente_dto_to_response_schema(ingrediente_dto)
        
    except IngredienteNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except IngredienteAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating ingredient"
        )


@router.delete(
    "/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete ingredient",
    description="Delete an ingredient"
)
async def delete_ingrediente(
    ingrediente_id: UUID,
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
):
    """Delete an ingredient."""
    try:
        # Delete ingredient through service
        deleted = await ingrediente_service.delete_ingrediente(ingrediente_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingredient with ID {ingrediente_id} not found"
            )
            
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting ingredient"
        )


@router.get(
    "/{ingrediente_id}/stock",
    response_model=int,
    summary="Check ingredient stock",
    description="Check current stock of an ingredient"
)
async def check_ingrediente_stock(
    ingrediente_id: UUID,
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
) -> int:
    """Check current stock of an ingredient."""
    try:
        return await ingrediente_service.check_stock(ingrediente_id)
        
    except IngredienteNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while checking stock"
        )


@router.patch(
    "/{ingrediente_id}/stock",
    response_model=IngredienteResponseSchema,
    summary="Update ingredient stock",
    description="Update stock of an ingredient"
)
async def update_ingrediente_stock(
    ingrediente_id: UUID,
    stock_update: StockUpdateSchema,
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
) -> IngredienteResponseSchema:
    """Update stock of an ingredient."""
    try:
        # Convert schema to DTO
        stock_dto = IngredienteSchemaMapper.stock_update_schema_to_dto(stock_update)
        
        # Update stock through service
        ingrediente_dto = await ingrediente_service.update_stock(ingrediente_id, stock_dto)
        
        # Convert DTO to response schema
        return IngredienteSchemaMapper.ingrediente_dto_to_response_schema(ingrediente_dto)
        
    except IngredienteNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InsufficientStockError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating stock"
        )


@router.get(
    "/low-stock/",
    response_model=List[IngredienteListResponseSchema],
    summary="Get low stock ingredients",
    description="Retrieve ingredients with low stock that need restocking"
)
async def get_low_stock_ingredientes(
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
) -> List[IngredienteListResponseSchema]:
    """Get ingredients with low stock."""
    try:
        # Get low stock ingredients through service
        ingredientes_dto = await ingrediente_service.get_low_stock_ingredientes()
        
        # Convert DTOs to list response schemas
        return [IngredienteSchemaMapper.ingrediente_dto_to_list_response_schema(ing) for ing in ingredientes_dto]
        
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving low stock ingredients"
        )


@router.get(
    "/expiring/",
    response_model=List[IngredienteListResponseSchema],
    summary="Get expiring ingredients",
    description="Retrieve ingredients expiring within specified days"
)
async def get_expiring_ingredientes(
    days_ahead: int = Query(3, ge=1, le=30, description="Days ahead to check for expiration"),
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
) -> List[IngredienteListResponseSchema]:
    """Get ingredients expiring within specified days."""
    try:
        # Get expiring ingredients through service
        ingredientes_dto = await ingrediente_service.get_expiring_soon_ingredientes(days_ahead)
        
        # Convert DTOs to list response schemas
        return [IngredienteSchemaMapper.ingrediente_dto_to_list_response_schema(ing) for ing in ingredientes_dto]
        
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving expiring ingredients"
        )


@router.get(
    "/expired/",
    response_model=List[IngredienteListResponseSchema],
    summary="Get expired ingredients",
    description="Retrieve expired ingredients"
)
async def get_expired_ingredientes(
    ingrediente_service: IngredienteApplicationService = Depends(get_ingrediente_service)
) -> List[IngredienteListResponseSchema]:
    """Get expired ingredients."""
    try:
        # Get expired ingredients through service
        ingredientes_dto = await ingrediente_service.get_expired_ingredientes()
        
        # Convert DTOs to list response schemas
        return [IngredienteSchemaMapper.ingrediente_dto_to_list_response_schema(ing) for ing in ingredientes_dto]
        
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving expired ingredients"
        )