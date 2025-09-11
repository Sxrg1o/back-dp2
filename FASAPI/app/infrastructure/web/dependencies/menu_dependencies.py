"""FastAPI dependencies for menu module with database integration."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.infrastructure.web.dependencies.container import (
    get_item_repository as _get_item_repository,
    get_ingrediente_repository as _get_ingrediente_repository,
    get_plato_repository as _get_plato_repository,
    get_bebida_repository as _get_bebida_repository,
    get_item_service as _get_item_service,
    get_ingrediente_service as _get_ingrediente_service,
    get_plato_service as _get_plato_service,
    get_bebida_service as _get_bebida_service,
    get_menu_service as _get_menu_service
)

# Domain repositories
from app.domain.repositories.item_repository import ItemRepositoryPort
from app.domain.repositories.ingrediente_repository import IngredienteRepositoryPort
from app.domain.repositories.plato_repository import PlatoRepositoryPort
from app.domain.repositories.bebida_repository import BebidaRepositoryPort

# Application services
from app.application.services.item_service import ItemApplicationService
from app.application.services.ingrediente_service import IngredienteApplicationService
from app.application.services.plato_service import PlatoApplicationService
from app.application.services.bebida_service import BebidaApplicationService
from app.application.services.menu_service import MenuApplicationService


# FastAPI dependencies with database session injection
def get_item_repository(
    session: AsyncSession = Depends(get_db)
) -> ItemRepositoryPort:
    """FastAPI dependency for item repository with database session.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        ItemRepositoryPort implementation
    """
    return _get_item_repository(session)


def get_ingrediente_repository(
    session: AsyncSession = Depends(get_db)
) -> IngredienteRepositoryPort:
    """FastAPI dependency for ingrediente repository with database session.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        IngredienteRepositoryPort implementation
    """
    return _get_ingrediente_repository(session)


def get_plato_repository(
    session: AsyncSession = Depends(get_db)
) -> PlatoRepositoryPort:
    """FastAPI dependency for plato repository with database session.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        PlatoRepositoryPort implementation
    """
    return _get_plato_repository(session)


def get_bebida_repository(
    session: AsyncSession = Depends(get_db)
) -> BebidaRepositoryPort:
    """FastAPI dependency for bebida repository with database session.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        BebidaRepositoryPort implementation
    """
    return _get_bebida_repository(session)


def get_item_service(
    session: AsyncSession = Depends(get_db)
) -> ItemApplicationService:
    """FastAPI dependency for item application service with database session.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        ItemApplicationService instance
    """
    return _get_item_service(session)


def get_ingrediente_service(
    session: AsyncSession = Depends(get_db)
) -> IngredienteApplicationService:
    """FastAPI dependency for ingrediente application service with database session.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        IngredienteApplicationService instance
    """
    return _get_ingrediente_service(session)


def get_plato_service(
    session: AsyncSession = Depends(get_db)
) -> PlatoApplicationService:
    """FastAPI dependency for plato application service with database session.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        PlatoApplicationService instance
    """
    return _get_plato_service(session)


def get_bebida_service(
    session: AsyncSession = Depends(get_db)
) -> BebidaApplicationService:
    """FastAPI dependency for bebida application service with database session.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        BebidaApplicationService instance
    """
    return _get_bebida_service(session)


def get_menu_service(
    session: AsyncSession = Depends(get_db)
) -> MenuApplicationService:
    """FastAPI dependency for menu application service with database session.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        MenuApplicationService instance
    """
    return _get_menu_service(session)