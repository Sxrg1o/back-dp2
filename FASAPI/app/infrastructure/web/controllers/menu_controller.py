"""
Menu controller for general menu operations.
"""
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.services.menu_service import MenuApplicationService
from app.infrastructure.web.dependencies.menu_dependencies import get_menu_service
from app.domain.exceptions.menu_exceptions import MenuDomainException


router = APIRouter(tags=["menu"])


@router.get(
    "/",
    response_model=Dict[str, List],
    summary="Get complete menu",
    description="Retrieve the complete menu with all available items categorized by type"
)
async def get_full_menu(
    menu_service: MenuApplicationService = Depends(get_menu_service)
) -> Dict[str, List]:
    """Get complete menu with all available items."""
    try:
        return await menu_service.get_full_menu()
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving menu"
        )


@router.get(
    "/categories",
    response_model=Dict[str, Dict[str, List]],
    summary="Get menu by categories",
    description="Retrieve menu organized by categories and subcategories"
)
async def get_menu_by_categories(
    menu_service: MenuApplicationService = Depends(get_menu_service)
) -> Dict[str, Dict[str, List]]:
    """Get menu organized by categories and subcategories."""
    try:
        return await menu_service.get_menu_by_categories()
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving categorized menu"
        )


@router.get(
    "/search",
    response_model=Dict[str, List],
    summary="Search menu items",
    description="Search menu items by name across all categories"
)
async def search_menu_items(
    query: str = Query(..., min_length=1, description="Search query"),
    menu_service: MenuApplicationService = Depends(get_menu_service)
) -> Dict[str, List]:
    """Search menu items by name across all categories."""
    try:
        return await menu_service.search_menu_items(query)
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while searching menu items"
        )


@router.get(
    "/statistics",
    response_model=Dict[str, int],
    summary="Get menu statistics",
    description="Retrieve statistical information about the menu"
)
async def get_menu_statistics(
    menu_service: MenuApplicationService = Depends(get_menu_service)
) -> Dict[str, int]:
    """Get menu statistics."""
    try:
        return await menu_service.get_menu_statistics()
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving menu statistics"
        )


@router.get(
    "/nutrition",
    response_model=Dict[str, float],
    summary="Get nutritional summary",
    description="Retrieve nutritional summary of available menu items"
)
async def get_nutritional_summary(
    menu_service: MenuApplicationService = Depends(get_menu_service)
) -> Dict[str, float]:
    """Get nutritional summary of available menu items."""
    try:
        return await menu_service.get_nutritional_summary()
    except MenuDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving nutritional summary"
        )