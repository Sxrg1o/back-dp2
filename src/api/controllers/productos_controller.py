"""
Product endpoints for menu management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.business_logic.menu.producto_service import ProductoService
from src.api.schemas.producto_schema import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
    ProductoSearchParams,
    ProductoPriceCalculation,
    ProductoPriceResponse,
    ProductoBulkPriceUpdate
)
from src.api.schemas.response_schema import SuccessResponse
from src.core.utils.pagination_utils import PaginationParams, PaginatedResponse
from src.business_logic.exceptions.menu_exceptions import (
    ProductoNotFoundError,
    CategoriaNotFoundError
)

router = APIRouter()
producto_service = ProductoService()


@router.post("/", response_model=ProductoResponse, status_code=201)
async def create_product(
    product_data: ProductoCreate,
    db: AsyncSession = Depends(get_database_session)
):
    """
    Create a new product.

    - **nombre**: Product name (2-200 characters)
    - **descripcion**: Optional product description
    - **precio_base**: Base price (positive decimal)
    - **id_categoria**: Category ID (must exist)
    - **disponible**: Availability status (default: True)
    - **destacado**: Featured status (default: False)
    """
    try:
        product = await producto_service.create_product(
            db, product_data.model_dump()
        )
        return product
    except CategoriaNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=PaginatedResponse[ProductoResponse])
async def get_products(
    pagination: PaginationParams = Depends(),
    search_params: ProductoSearchParams = Depends(),
    db: AsyncSession = Depends(get_database_session)
):
    """
    Get products with optional search and filtering.

    - **search_term**: Search in product name and description
    - **category_id**: Filter by category
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    - **available_only**: Show only available products
    - **featured_only**: Show only featured products
    """
    search_dict = search_params.model_dump(exclude_none=True)

    return await producto_service.search_products(
        db, search_dict, pagination
    )


@router.get("/featured", response_model=List[ProductoResponse])
async def get_featured_products(
    db: AsyncSession = Depends(get_database_session)
):
    """Get all featured and available products."""
    return await producto_service.get_featured_products(db)


@router.get("/category/{category_id}", response_model=List[ProductoResponse])
async def get_products_by_category(
    category_id: int,
    available_only: bool = Query(True, description="Filter only available products"),
    db: AsyncSession = Depends(get_database_session)
):
    """
    Get products by category.

    - **category_id**: Category ID
    - **available_only**: Filter only available products
    """
    try:
        return await producto_service.get_products_by_category(
            db, category_id, available_only
        )
    except CategoriaNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{product_id}", response_model=ProductoResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Get a specific product by ID with all related data."""
    try:
        return await producto_service.get_product_by_id(db, product_id)
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{product_id}", response_model=ProductoResponse)
async def update_product(
    product_id: int,
    product_data: ProductoUpdate,
    db: AsyncSession = Depends(get_database_session)
):
    """
    Update a product.

    - Only provided fields will be updated
    - **nombre**: Product name (2-200 characters)
    - **descripcion**: Product description
    - **precio_base**: Base price (positive decimal)
    - **id_categoria**: Category ID (must exist)
    - **disponible**: Availability status
    - **destacado**: Featured status
    """
    try:
        update_dict = product_data.model_dump(exclude_none=True)
        return await producto_service.update_product(db, product_id, update_dict)
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CategoriaNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{product_id}/toggle-availability", response_model=ProductoResponse)
async def toggle_product_availability(
    product_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Toggle product availability status."""
    try:
        return await producto_service.toggle_product_availability(db, product_id)
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/calculate-price", response_model=ProductoPriceResponse)
async def calculate_product_price(
    price_calculation: ProductoPriceCalculation,
    db: AsyncSession = Depends(get_database_session)
):
    """
    Calculate final product price including selected options.

    - **product_id**: Product ID
    - **selected_options**: List of selected option IDs
    """
    try:
        final_price = await producto_service.calculate_product_final_price(
            db,
            price_calculation.product_id,
            price_calculation.selected_options
        )

        product = await producto_service.get_product_by_id(
            db, price_calculation.product_id
        )

        # Calculate options price
        options_price = final_price - product.precio_base

        # Get selected option details
        selected_option_details = [
            option for option in product.opciones
            if option.id in price_calculation.selected_options
        ]

        return ProductoPriceResponse(
            product_id=price_calculation.product_id,
            base_price=product.precio_base,
            options_price=options_price,
            final_price=final_price,
            selected_options=selected_option_details
        )
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/bulk-price-update", response_model=SuccessResponse)
async def bulk_update_prices(
    bulk_update: ProductoBulkPriceUpdate,
    db: AsyncSession = Depends(get_database_session)
):
    """
    Bulk update product prices.

    - **updates**: List of objects with 'id' and 'precio_base'
    """
    try:
        updated_count = 0
        for update in bulk_update.updates:
            await producto_service.update_product(
                db, update["id"], {"precio_base": update["precio_base"]}
            )
            updated_count += 1

        return SuccessResponse(
            message=f"Successfully updated prices for {updated_count} products"
        )
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}", response_model=SuccessResponse)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Delete a product. This will permanently remove the product from the database."""
    try:
        success = await producto_service.delete_product(db, product_id)
        if success:
            return SuccessResponse(message="Product deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))