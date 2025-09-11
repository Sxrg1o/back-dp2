"""
Bebida controller for beverage management.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.services.bebida_service import BebidaApplicationService
from app.infrastructure.web.dependencies.menu_dependencies import get_bebida_service
from app.infrastructure.web.schemas.bebida_schemas import (
    BebidaCreateSchema,
    BebidaUpdateSchema,
    BebidaResponseSchema,
    BebidaListResponseSchema
)
from app.infrastructure.web.schemas.mappers.menu_schema_mapper import BebidaSchemaMapper
from app.domain.exceptions.menu_exceptions import (
    BebidaNotFoundError,
    BebidaAlreadyExistsError,
    MenuDomainException
)


router = APIRouter(prefix="/bebidas", tags=["bebidas"])


@router.post("/", response_model=BebidaResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_bebida(
    bebida_data: BebidaCreateSchema,
    bebida_service: BebidaApplicationService = Depends(get_bebida_service)
) -> BebidaResponseSchema:
    """Create a new beverage."""
    try:
        create_dto = BebidaSchemaMapper.bebida_create_schema_to_dto(bebida_data)
        bebida_dto = await bebida_service.create_bebida(create_dto)
        return BebidaSchemaMapper.bebida_dto_to_response_schema(bebida_dto)
    except BebidaAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=List[BebidaListResponseSchema])
async def get_bebidas(
    available_only: bool = Query(True),
    alcoholic: bool = Query(None, description="Filter by alcohol content"),
    temperatura: str = Query(None, description="Filter by service temperature"),
    bebida_service: BebidaApplicationService = Depends(get_bebida_service)
) -> List[BebidaListResponseSchema]:
    """Get all beverages with optional filtering."""
    try:
        if alcoholic is True:
            bebidas_dto = await bebida_service.get_alcoholic_bebidas()
        elif alcoholic is False:
            bebidas_dto = await bebida_service.get_non_alcoholic_bebidas()
        elif available_only:
            bebidas_dto = await bebida_service.get_available_bebidas()
        else:
            bebidas_dto = await bebida_service.get_all_bebidas()
        
        return [BebidaSchemaMapper.bebida_dto_to_list_response_schema(bebida) for bebida in bebidas_dto]
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{bebida_id}", response_model=BebidaResponseSchema)
async def get_bebida_by_id(
    bebida_id: UUID,
    bebida_service: BebidaApplicationService = Depends(get_bebida_service)
) -> BebidaResponseSchema:
    """Get beverage by ID."""
    try:
        bebida_dto = await bebida_service.get_bebida_by_id(bebida_id)
        return BebidaSchemaMapper.bebida_dto_to_response_schema(bebida_dto)
    except BebidaNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{bebida_id}", response_model=BebidaResponseSchema)
async def update_bebida(
    bebida_id: UUID,
    bebida_data: BebidaUpdateSchema,
    bebida_service: BebidaApplicationService = Depends(get_bebida_service)
) -> BebidaResponseSchema:
    """Update an existing beverage."""
    try:
        update_dto = BebidaSchemaMapper.bebida_update_schema_to_dto(bebida_data)
        bebida_dto = await bebida_service.update_bebida(bebida_id, update_dto)
        return BebidaSchemaMapper.bebida_dto_to_response_schema(bebida_dto)
    except BebidaNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BebidaAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{bebida_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bebida(
    bebida_id: UUID,
    bebida_service: BebidaApplicationService = Depends(get_bebida_service)
):
    """Delete a beverage."""
    try:
        deleted = await bebida_service.delete_bebida(bebida_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Beverage with ID {bebida_id} not found")
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{bebida_id}/stock", response_model=int)
async def check_bebida_stock(
    bebida_id: UUID,
    bebida_service: BebidaApplicationService = Depends(get_bebida_service)
) -> int:
    """Check current stock of a beverage."""
    try:
        return await bebida_service.check_stock(bebida_id)
    except BebidaNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/low-stock/", response_model=List[BebidaListResponseSchema])
async def get_low_stock_bebidas(
    bebida_service: BebidaApplicationService = Depends(get_bebida_service)
) -> List[BebidaListResponseSchema]:
    """Get beverages with low stock."""
    try:
        bebidas_dto = await bebida_service.get_low_stock_bebidas()
        return [BebidaSchemaMapper.bebida_dto_to_list_response_schema(bebida) for bebida in bebidas_dto]
    except MenuDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")