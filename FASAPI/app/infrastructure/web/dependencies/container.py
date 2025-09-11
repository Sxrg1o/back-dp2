"""Dependency injection container for menu module."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

# Domain repositories (interfaces)
from app.domain.repositories.item_repository import ItemRepositoryPort
from app.domain.repositories.ingrediente_repository import IngredienteRepositoryPort
from app.domain.repositories.plato_repository import PlatoRepositoryPort
from app.domain.repositories.bebida_repository import BebidaRepositoryPort

# Infrastructure repository implementations
from app.infrastructure.persistence.repositories.sqlalchemy_item_repository import SqlAlchemyItemRepository
from app.infrastructure.persistence.repositories.sqlalchemy_ingrediente_repository import SqlAlchemyIngredienteRepository
from app.infrastructure.persistence.repositories.sqlalchemy_plato_repository import SqlAlchemyPlatoRepository
from app.infrastructure.persistence.repositories.sqlalchemy_bebida_repository import SqlAlchemyBebidaRepository

# Mappers
from app.infrastructure.persistence.mappers.item_mapper import ItemMapper
from app.infrastructure.persistence.mappers.ingrediente_mapper import IngredienteMapper
from app.infrastructure.persistence.mappers.plato_mapper import PlatoMapper
from app.infrastructure.persistence.mappers.bebida_mapper import BebidaMapper

# Application services
from app.application.services.item_service import ItemApplicationService
from app.application.services.ingrediente_service import IngredienteApplicationService
from app.application.services.plato_service import PlatoApplicationService
from app.application.services.bebida_service import BebidaApplicationService
from app.application.services.menu_service import MenuApplicationService


class MenuContainer:
    """Dependency injection container for menu module."""
    
    def __init__(self):
        """Initialize container."""
        pass
    
    # Repository factory methods
    def create_item_repository(self, session: AsyncSession) -> ItemRepositoryPort:
        """Create item repository instance.
        
        Args:
            session: Database session
            
        Returns:
            ItemRepositoryPort implementation
        """
        return SqlAlchemyItemRepository(session)
    
    def create_ingrediente_repository(self, session: AsyncSession) -> IngredienteRepositoryPort:
        """Create ingrediente repository instance.
        
        Args:
            session: Database session
            
        Returns:
            IngredienteRepositoryPort implementation
        """
        return SqlAlchemyIngredienteRepository(session)
    
    def create_plato_repository(self, session: AsyncSession) -> PlatoRepositoryPort:
        """Create plato repository instance.
        
        Args:
            session: Database session
            
        Returns:
            PlatoRepositoryPort implementation
        """
        return SqlAlchemyPlatoRepository(session)
    
    def create_bebida_repository(self, session: AsyncSession) -> BebidaRepositoryPort:
        """Create bebida repository instance.
        
        Args:
            session: Database session
            
        Returns:
            BebidaRepositoryPort implementation
        """
        return SqlAlchemyBebidaRepository(session)
    
    # Application service factory methods
    def create_item_service(self, session: AsyncSession) -> ItemApplicationService:
        """Create item application service instance.
        
        Args:
            session: Database session
            
        Returns:
            ItemApplicationService instance
        """
        item_repository = self.create_item_repository(session)
        return ItemApplicationService(item_repository)
    
    def create_ingrediente_service(self, session: AsyncSession) -> IngredienteApplicationService:
        """Create ingrediente application service instance.
        
        Args:
            session: Database session
            
        Returns:
            IngredienteApplicationService instance
        """
        ingrediente_repository = self.create_ingrediente_repository(session)
        return IngredienteApplicationService(ingrediente_repository)
    
    def create_plato_service(self, session: AsyncSession) -> PlatoApplicationService:
        """Create plato application service instance.
        
        Args:
            session: Database session
            
        Returns:
            PlatoApplicationService instance
        """
        plato_repository = self.create_plato_repository(session)
        ingrediente_repository = self.create_ingrediente_repository(session)
        return PlatoApplicationService(plato_repository, ingrediente_repository)
    
    def create_bebida_service(self, session: AsyncSession) -> BebidaApplicationService:
        """Create bebida application service instance.
        
        Args:
            session: Database session
            
        Returns:
            BebidaApplicationService instance
        """
        bebida_repository = self.create_bebida_repository(session)
        return BebidaApplicationService(bebida_repository)
    
    def create_menu_service(self, session: AsyncSession) -> MenuApplicationService:
        """Create menu application service instance.
        
        Args:
            session: Database session
            
        Returns:
            MenuApplicationService instance
        """
        item_repository = self.create_item_repository(session)
        ingrediente_repository = self.create_ingrediente_repository(session)
        plato_repository = self.create_plato_repository(session)
        bebida_repository = self.create_bebida_repository(session)
        
        return MenuApplicationService(
            item_repository,
            ingrediente_repository,
            plato_repository,
            bebida_repository
        )


# Global container instance
menu_container = MenuContainer()


# FastAPI dependency functions


def get_item_repository(
    session: AsyncSession
) -> ItemRepositoryPort:
    """FastAPI dependency for item repository.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        ItemRepositoryPort implementation
    """
    return menu_container.create_item_repository(session)


def get_ingrediente_repository(
    session: AsyncSession
) -> IngredienteRepositoryPort:
    """FastAPI dependency for ingrediente repository.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        IngredienteRepositoryPort implementation
    """
    return menu_container.create_ingrediente_repository(session)


def get_plato_repository(
    session: AsyncSession
) -> PlatoRepositoryPort:
    """FastAPI dependency for plato repository.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        PlatoRepositoryPort implementation
    """
    return menu_container.create_plato_repository(session)


def get_bebida_repository(
    session: AsyncSession
) -> BebidaRepositoryPort:
    """FastAPI dependency for bebida repository.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        BebidaRepositoryPort implementation
    """
    return menu_container.create_bebida_repository(session)


def get_item_service(
    session: AsyncSession
) -> ItemApplicationService:
    """FastAPI dependency for item application service.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        ItemApplicationService instance
    """
    return menu_container.create_item_service(session)


def get_ingrediente_service(
    session: AsyncSession
) -> IngredienteApplicationService:
    """FastAPI dependency for ingrediente application service.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        IngredienteApplicationService instance
    """
    return menu_container.create_ingrediente_service(session)


def get_plato_service(
    session: AsyncSession
) -> PlatoApplicationService:
    """FastAPI dependency for plato application service.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        PlatoApplicationService instance
    """
    return menu_container.create_plato_service(session)


def get_bebida_service(
    session: AsyncSession
) -> BebidaApplicationService:
    """FastAPI dependency for bebida application service.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        BebidaApplicationService instance
    """
    return menu_container.create_bebida_service(session)


def get_menu_service(
    session: AsyncSession
) -> MenuApplicationService:
    """FastAPI dependency for menu application service.
    
    Args:
        session: Database session from FastAPI dependency
        
    Returns:
        MenuApplicationService instance
    """
    return menu_container.create_menu_service(session)