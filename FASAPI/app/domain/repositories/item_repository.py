"""Repository interface for Item domain entity."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.item import Item
from app.domain.value_objects.etiqueta_item import EtiquetaItem


class ItemRepositoryPort(ABC):
    """Repository interface for Item operations.
    
    This interface defines the contract for Item data access operations.
    All methods work with Item domain entities and value objects, ensuring
    the domain layer remains independent of infrastructure concerns.
    """
    
    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> Optional[Item]:
        """Get item by ID.
        
        Args:
            item_id: Unique identifier of the item
            
        Returns:
            Item domain entity if found, None otherwise
            
        Raises:
            ItemNotFoundError: If item with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def get_available_items(self) -> List[Item]:
        """Get all available items.
        
        Returns items that are active, have stock above minimum,
        and are ready for ordering.
        
        Returns:
            List of available Item domain entities
        """
        pass
    
    @abstractmethod
    async def get_by_category(self, etiqueta: EtiquetaItem) -> List[Item]:
        """Get items by category/label.
        
        Args:
            etiqueta: Item label to filter by
            
        Returns:
            List of Item domain entities with the specified label
        """
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Item]:
        """Get all items regardless of availability.
        
        Returns:
            List of all Item domain entities
        """
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Item]:
        """Get item by name.
        
        Args:
            name: Name of the item to search for
            
        Returns:
            Item domain entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_low_stock_items(self) -> List[Item]:
        """Get items with low stock (at or below minimum).
        
        Returns:
            List of Item domain entities that need restocking
        """
        pass
    
    @abstractmethod
    async def get_by_price_range(self, min_price: float, max_price: float) -> List[Item]:
        """Get items within price range.
        
        Args:
            min_price: Minimum price (inclusive)
            max_price: Maximum price (inclusive)
            
        Returns:
            List of Item domain entities within the price range
        """
        pass
    
    @abstractmethod
    async def save(self, item: Item) -> Item:
        """Save item (create or update).
        
        Args:
            item: Item domain entity to save
            
        Returns:
            Saved Item domain entity with updated metadata
            
        Raises:
            ItemAlreadyExistsError: If creating item with existing name
            InvalidItemDataError: If item data is invalid
        """
        pass
    
    @abstractmethod
    async def delete(self, item_id: UUID) -> bool:
        """Delete item by ID.
        
        Args:
            item_id: Unique identifier of the item to delete
            
        Returns:
            True if item was deleted, False if not found
            
        Raises:
            ItemNotFoundError: If item with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def exists_by_id(self, item_id: UUID) -> bool:
        """Check if item exists by ID.
        
        Args:
            item_id: Unique identifier to check
            
        Returns:
            True if item exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        """Check if item exists by name.
        
        Args:
            name: Name to check for uniqueness
            
        Returns:
            True if item with name exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def count_total(self) -> int:
        """Count total number of items.
        
        Returns:
            Total count of items in the repository
        """
        pass
    
    @abstractmethod
    async def count_available(self) -> int:
        """Count available items.
        
        Returns:
            Count of items that are available for ordering
        """
        pass