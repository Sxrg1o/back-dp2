"""Repository interface for Bebida domain entity."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.bebida import Bebida


class BebidaRepositoryPort(ABC):
    """Repository interface for Bebida operations.
    
    This interface defines the contract for Bebida data access operations.
    All methods work with Bebida domain entities and value objects, ensuring
    the domain layer remains independent of infrastructure concerns.
    """
    
    @abstractmethod
    async def get_by_id(self, bebida_id: UUID) -> Optional[Bebida]:
        """Get beverage by ID.
        
        Args:
            bebida_id: Unique identifier of the beverage
            
        Returns:
            Bebida domain entity if found, None otherwise
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def get_alcoholic(self) -> List[Bebida]:
        """Get alcoholic beverages.
        
        Returns beverages with alcohol content > 0.
        
        Returns:
            List of alcoholic Bebida domain entities
        """
        pass
    
    @abstractmethod
    async def get_non_alcoholic(self) -> List[Bebida]:
        """Get non-alcoholic beverages.
        
        Returns beverages with alcohol content = 0.
        
        Returns:
            List of non-alcoholic Bebida domain entities
        """
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Bebida]:
        """Get all beverages.
        
        Returns:
            List of all Bebida domain entities
        """
        pass
    
    @abstractmethod
    async def get_available(self) -> List[Bebida]:
        """Get available beverages.
        
        Returns beverages that are active and have stock.
        
        Returns:
            List of available Bebida domain entities
        """
        pass
    
    @abstractmethod
    async def get_by_type(self, tipo_bebida: str) -> List[Bebida]:
        """Get beverages by type.
        
        Args:
            tipo_bebida: Type of beverage (e.g., "gaseosa", "jugo", "cerveza", "vino")
            
        Returns:
            List of Bebida domain entities of the specified type
        """
        pass
    
    @abstractmethod
    async def get_by_temperature(self, temperatura_servicio: str) -> List[Bebida]:
        """Get beverages by service temperature.
        
        Args:
            temperatura_servicio: Service temperature ("fria", "caliente", "ambiente")
            
        Returns:
            List of Bebida domain entities with the specified service temperature
        """
        pass
    
    @abstractmethod
    async def get_by_volume_range(self, min_volume: float, max_volume: float) -> List[Bebida]:
        """Get beverages by volume range.
        
        Args:
            min_volume: Minimum volume in milliliters (inclusive)
            max_volume: Maximum volume in milliliters (inclusive)
            
        Returns:
            List of Bebida domain entities within the volume range
        """
        pass
    
    @abstractmethod
    async def get_by_alcohol_range(self, min_alcohol: float, max_alcohol: float) -> List[Bebida]:
        """Get beverages by alcohol content range.
        
        Args:
            min_alcohol: Minimum alcohol percentage (inclusive)
            max_alcohol: Maximum alcohol percentage (inclusive)
            
        Returns:
            List of Bebida domain entities within the alcohol range
        """
        pass
    
    @abstractmethod
    async def get_by_brand(self, marca: str) -> List[Bebida]:
        """Get beverages by brand.
        
        Args:
            marca: Brand name
            
        Returns:
            List of Bebida domain entities from the specified brand
        """
        pass
    
    @abstractmethod
    async def get_by_origin(self, origen: str) -> List[Bebida]:
        """Get beverages by origin.
        
        Args:
            origen: Origin/country of the beverage
            
        Returns:
            List of Bebida domain entities from the specified origin
        """
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Bebida]:
        """Get beverage by name.
        
        Args:
            name: Name of the beverage
            
        Returns:
            Bebida domain entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_cold_beverages(self) -> List[Bebida]:
        """Get cold beverages.
        
        Returns beverages served cold.
        
        Returns:
            List of cold Bebida domain entities
        """
        pass
    
    @abstractmethod
    async def get_hot_beverages(self) -> List[Bebida]:
        """Get hot beverages.
        
        Returns beverages served hot.
        
        Returns:
            List of hot Bebida domain entities
        """
        pass
    
    @abstractmethod
    async def get_standard_volumes(self) -> List[Bebida]:
        """Get beverages with standard volumes.
        
        Returns beverages with standard volumes (200ml, 250ml, 330ml, etc.).
        
        Returns:
            List of Bebida domain entities with standard volumes
        """
        pass
    
    @abstractmethod
    async def get_suitable_for_minors(self) -> List[Bebida]:
        """Get beverages suitable for minors.
        
        Returns non-alcoholic beverages.
        
        Returns:
            List of Bebida domain entities suitable for minors
        """
        pass
    
    @abstractmethod
    async def get_by_volume_category(self, categoria: str) -> List[Bebida]:
        """Get beverages by volume category.
        
        Args:
            categoria: Volume category ("pequeño", "mediano", "grande", "extra_grande")
            
        Returns:
            List of Bebida domain entities in the specified volume category
        """
        pass
    
    @abstractmethod
    async def save(self, bebida: Bebida) -> Bebida:
        """Save beverage (create or update).
        
        Args:
            bebida: Bebida domain entity to save
            
        Returns:
            Saved Bebida domain entity with updated metadata
            
        Raises:
            BebidaAlreadyExistsError: If creating beverage with existing name
            InvalidBebidaDataError: If beverage data is invalid
        """
        pass
    
    @abstractmethod
    async def delete(self, bebida_id: UUID) -> bool:
        """Delete beverage by ID.
        
        Args:
            bebida_id: Unique identifier of the beverage to delete
            
        Returns:
            True if beverage was deleted, False if not found
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def exists_by_id(self, bebida_id: UUID) -> bool:
        """Check if beverage exists by ID.
        
        Args:
            bebida_id: Unique identifier to check
            
        Returns:
            True if beverage exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        """Check if beverage exists by name.
        
        Args:
            name: Name to check for uniqueness
            
        Returns:
            True if beverage with name exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def get_most_popular(self, limit: int = 10) -> List[Bebida]:
        """Get most popular beverages.
        
        Args:
            limit: Maximum number of beverages to return
            
        Returns:
            List of most popular Bebida domain entities
        """
        pass
    
    @abstractmethod
    async def get_low_stock(self) -> List[Bebida]:
        """Get beverages with low stock.
        
        Returns beverages at or below minimum stock level.
        
        Returns:
            List of Bebida domain entities with low stock
        """
        pass