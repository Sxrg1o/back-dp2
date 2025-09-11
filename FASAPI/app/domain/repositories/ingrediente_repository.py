"""Repository interface for Ingrediente domain entity."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.domain.entities.ingrediente import Ingrediente
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente


class IngredienteRepositoryPort(ABC):
    """Repository interface for Ingrediente operations.
    
    This interface defines the contract for Ingrediente data access operations.
    All methods work with Ingrediente domain entities and value objects, ensuring
    the domain layer remains independent of infrastructure concerns.
    """
    
    @abstractmethod
    async def get_by_id(self, ingrediente_id: UUID) -> Optional[Ingrediente]:
        """Get ingredient by ID.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient
            
        Returns:
            Ingrediente domain entity if found, None otherwise
            
        Raises:
            IngredienteNotFoundError: If ingredient with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def get_by_type(self, tipo: EtiquetaIngrediente) -> List[Ingrediente]:
        """Get ingredients by type.
        
        Args:
            tipo: Type of ingredient (VERDURA, CARNE, FRUTA)
            
        Returns:
            List of Ingrediente domain entities of the specified type
        """
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Ingrediente]:
        """Get all ingredients.
        
        Returns:
            List of all Ingrediente domain entities
        """
        pass
    
    @abstractmethod
    async def get_available(self) -> List[Ingrediente]:
        """Get available ingredients.
        
        Returns ingredients that are active, have stock, and are not expired.
        
        Returns:
            List of available Ingrediente domain entities
        """
        pass
    
    @abstractmethod
    async def check_stock(self, ingrediente_id: UUID) -> int:
        """Check current stock of ingredient.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient
            
        Returns:
            Current stock amount
            
        Raises:
            IngredienteNotFoundError: If ingredient with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def update_stock(self, ingrediente_id: UUID, new_stock: int) -> Ingrediente:
        """Update ingredient stock.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient
            new_stock: New stock amount
            
        Returns:
            Updated Ingrediente domain entity
            
        Raises:
            IngredienteNotFoundError: If ingredient with given ID doesn't exist
            InvalidStockError: If new stock amount is invalid
        """
        pass
    
    @abstractmethod
    async def get_by_supplier(self, proveedor: str) -> List[Ingrediente]:
        """Get ingredients by supplier.
        
        Args:
            proveedor: Supplier name
            
        Returns:
            List of Ingrediente domain entities from the specified supplier
        """
        pass
    
    @abstractmethod
    async def get_expiring_soon(self, days_ahead: int = 3) -> List[Ingrediente]:
        """Get ingredients expiring within specified days.
        
        Args:
            days_ahead: Number of days to look ahead for expiration
            
        Returns:
            List of Ingrediente domain entities expiring soon
        """
        pass
    
    @abstractmethod
    async def get_expired(self) -> List[Ingrediente]:
        """Get expired ingredients.
        
        Returns:
            List of expired Ingrediente domain entities
        """
        pass
    
    @abstractmethod
    async def get_low_stock(self) -> List[Ingrediente]:
        """Get ingredients with low stock.
        
        Returns ingredients at or below minimum stock level.
        
        Returns:
            List of Ingrediente domain entities with low stock
        """
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Ingrediente]:
        """Get ingredient by name.
        
        Args:
            name: Name of the ingredient
            
        Returns:
            Ingrediente domain entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_by_unit_measure(self, unidad_medida: str) -> List[Ingrediente]:
        """Get ingredients by unit of measure.
        
        Args:
            unidad_medida: Unit of measure (e.g., "gramos", "litros")
            
        Returns:
            List of Ingrediente domain entities with the specified unit
        """
        pass
    
    @abstractmethod
    async def save(self, ingrediente: Ingrediente) -> Ingrediente:
        """Save ingredient (create or update).
        
        Args:
            ingrediente: Ingrediente domain entity to save
            
        Returns:
            Saved Ingrediente domain entity with updated metadata
            
        Raises:
            IngredienteAlreadyExistsError: If creating ingredient with existing name
            InvalidIngredienteDataError: If ingredient data is invalid
        """
        pass
    
    @abstractmethod
    async def delete(self, ingrediente_id: UUID) -> bool:
        """Delete ingredient by ID.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient to delete
            
        Returns:
            True if ingredient was deleted, False if not found
            
        Raises:
            IngredienteNotFoundError: If ingredient with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def exists_by_id(self, ingrediente_id: UUID) -> bool:
        """Check if ingredient exists by ID.
        
        Args:
            ingrediente_id: Unique identifier to check
            
        Returns:
            True if ingredient exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        """Check if ingredient exists by name.
        
        Args:
            name: Name to check for uniqueness
            
        Returns:
            True if ingredient with name exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def bulk_update_stock(self, stock_updates: dict[UUID, int]) -> List[Ingrediente]:
        """Update stock for multiple ingredients.
        
        Args:
            stock_updates: Dictionary mapping ingredient IDs to new stock amounts
            
        Returns:
            List of updated Ingrediente domain entities
            
        Raises:
            IngredienteNotFoundError: If any ingredient ID doesn't exist
            InvalidStockError: If any stock amount is invalid
        """
        pass
    
    @abstractmethod
    async def get_total_weight_by_type(self, tipo: EtiquetaIngrediente) -> float:
        """Get total weight of ingredients by type.
        
        Args:
            tipo: Type of ingredient
            
        Returns:
            Total weight in grams of all ingredients of the specified type
        """
        pass