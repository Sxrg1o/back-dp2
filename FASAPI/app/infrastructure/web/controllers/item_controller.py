"""
Item controller for menu item management.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.services.item_service import ItemApplicationService
from app.infrastructure.web.dependencies.menu_dependencies import get_item_service
from app.infrastructure.web.schemas.menu_schemas import (
    ItemCreateSchema,
    ItemUpdateSchema,
    ItemResponseSchema,
    ItemListResponseSchema
)
from app.infrastructure.web.schemas.mappers.menu_schema_mapper import MenuSchemaMapper
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.exceptions.menu_exceptions import (
    ItemNotFoundError,
    ItemAlreadyExistsError,
    InsufficientStockError,
    MenuDomainException
)


router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "/",
    response_model=ItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create menu item",
    description="Create a new menu item"
)
async def create_item(
    item_data: ItemCreateSchema,
    item_service: ItemApplicationService = Depends(get_item_service)
) -> ItemResponseSchema:
    """Create a new menu item."""
    try:
        # Convert schema to DTO
        create_dto = MenuSchemaMapper.item_create_schema_to_dto(item_data)
        
        # Create item through service
        item_dto = await item_service.create_item(create_dto)
        
        # Convert DTO to response schema
        return MenuSchemaMapper.item_dto_to_response_schema(item_dto)
        
    except ItemAlreadyExistsError as e:
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
            detail="Internal server error while creating item"
        )


@router.get(
    "/",
    response_model=List[ItemListResponseSchema],
    summary="Get all items",
    description="Retrieve all menu items with optional filtering"
)
async def get_items(
    available_only: bool = Query(True, description="Filter by availability"),
    category: EtiquetaItem = Query(None, description="Filter by category"),
    min_price: float = Query(None, ge=0, description="Minimum price filter"),
    max_price: float = Query(None, ge=0, description="Maximum price filter"),
    item_service: ItemApplicationService = Depends(get_item_service)
) -> List[ItemListResponseSchema]:
    """Get all menu items with optional filtering."""
    try:
        if category:
            # Filter by category
            items_dto = await item_service.get_items_by_category(category)
        elif min_price is not None and max_price is not None:
            # Filter by price range
            items_dto = await item_service.get_items_by_price_range(min_price, max_price)
        elif available_only:
            # Get only available items
            items_dto = await item_service.get_available_items()
        else:
            # Get all items
            items_dto = await item_service.get_all_items()
        
        # Convert DTOs to list response schemas
        return [MenuSchemaMapper.item_dto_to_list_response_schema(item) for item in items_dto]
        
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving items"
        )


@router.get(
    "/{item_id}",
    response_model=ItemResponseSchema,
    summary="Get item by ID",
    description="Retrieve a specific menu item by its ID"
)
async def get_item_by_id(
    item_id: UUID,
    item_service: ItemApplicationService = Depends(get_item_service)
) -> ItemResponseSchema:
    """Get item by ID."""
    try:
        # Get item through service
        item_dto = await item_service.get_item_by_id(item_id)
        
        # Convert DTO to response schema
        return MenuSchemaMapper.item_dto_to_response_schema(item_dto)
        
    except ItemNotFoundError as e:
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
            detail="Internal server error while retrieving item"
        )


@router.put(
    "/{item_id}",
    response_model=ItemResponseSchema,
    summary="Update menu item",
    description="Update an existing menu item"
)
async def update_item(
    item_id: UUID,
    item_data: ItemUpdateSchema,
    item_service: ItemApplicationService = Depends(get_item_service)
) -> ItemResponseSchema:
    """Update an existing menu item."""
    try:
        # Convert schema to DTO
        update_dto = MenuSchemaMapper.item_update_schema_to_dto(item_data)
        
        # Update item through service
        item_dto = await item_service.update_item(item_id, update_dto)
        
        # Convert DTO to response schema
        return MenuSchemaMapper.item_dto_to_response_schema(item_dto)
        
    except ItemNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ItemAlreadyExistsError as e:
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
            detail="Internal server error while updating item"
        )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete menu item",
    description="Delete a menu item"
)
async def delete_item(
    item_id: UUID,
    item_service: ItemApplicationService = Depends(get_item_service)
):
    """Delete a menu item."""
    try:
        # Delete item through service
        deleted = await item_service.delete_item(item_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
            
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting item"
        )


@router.get(
    "/{item_id}/stock",
    response_model=int,
    summary="Check item stock",
    description="Check current stock of a menu item"
)
async def check_item_stock(
    item_id: UUID,
    item_service: ItemApplicationService = Depends(get_item_service)
) -> int:
    """Check current stock of a menu item."""
    try:
        return await item_service.check_stock(item_id)
        
    except ItemNotFoundError as e:
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
    "/{item_id}/stock",
    response_model=ItemResponseSchema,
    summary="Update item stock",
    description="Update stock of a menu item"
)
async def update_item_stock(
    item_id: UUID,
    cantidad: int = Query(..., gt=0, description="Quantity to add or remove"),
    operacion: str = Query(..., regex="^(aumentar|reducir)$", description="Operation: 'aumentar' or 'reducir'"),
    item_service: ItemApplicationService = Depends(get_item_service)
) -> ItemResponseSchema:
    """Update stock of a menu item."""
    try:
        # Update stock through service
        item_dto = await item_service.update_stock(item_id, cantidad, operacion)
        
        # Convert DTO to response schema
        return MenuSchemaMapper.item_dto_to_response_schema(item_dto)
        
    except ItemNotFoundError as e:
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


@router.patch(
    "/{item_id}/activate",
    response_model=ItemResponseSchema,
    summary="Activate item",
    description="Activate a menu item"
)
async def activate_item(
    item_id: UUID,
    item_service: ItemApplicationService = Depends(get_item_service)
) -> ItemResponseSchema:
    """Activate a menu item."""
    try:
        # Activate item through service
        item_dto = await item_service.activate_item(item_id)
        
        # Convert DTO to response schema
        return MenuSchemaMapper.item_dto_to_response_schema(item_dto)
        
    except ItemNotFoundError as e:
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
            detail="Internal server error while activating item"
        )


@router.patch(
    "/{item_id}/deactivate",
    response_model=ItemResponseSchema,
    summary="Deactivate item",
    description="Deactivate a menu item"
)
async def deactivate_item(
    item_id: UUID,
    item_service: ItemApplicationService = Depends(get_item_service)
) -> ItemResponseSchema:
    """Deactivate a menu item."""
    try:
        # Deactivate item through service
        item_dto = await item_service.deactivate_item(item_id)
        
        # Convert DTO to response schema
        return MenuSchemaMapper.item_dto_to_response_schema(item_dto)
        
    except ItemNotFoundError as e:
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
            detail="Internal server error while deactivating item"
        )


@router.get(
    "/low-stock/",
    response_model=List[ItemListResponseSchema],
    summary="Get low stock items",
    description="Retrieve items with low stock that need restocking"
)
async def get_low_stock_items(
    item_service: ItemApplicationService = Depends(get_item_service)
) -> List[ItemListResponseSchema]:
    """Get items with low stock."""
    try:
        # Get low stock items through service
        items_dto = await item_service.get_low_stock_items()
        
        # Convert DTOs to list response schemas
        return [MenuSchemaMapper.item_dto_to_list_response_schema(item) for item in items_dto]
        
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving low stock items"
        )