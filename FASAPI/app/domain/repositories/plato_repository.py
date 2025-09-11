"""Repository interface for Plato domain entity."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID

from app.domain.entities.plato import Plato
from app.domain.entities.ingrediente import Ingrediente
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato


class PlatoRepositoryPort(ABC):
    """Repository interface for Plato operations.
    
    This interface defines the contract for Plato data access operations.
    All methods work with Plato domain entities and value objects, ensuring
    the domain layer remains independent of infrastructure concerns.
    """
    
    @abstractmethod
    async def get_by_id(self, plato_id: UUID) -> Optional[Plato]:
        """Get dish by ID.
        
        Args:
            plato_id: Unique identifier of the dish
            
        Returns:
            Plato domain entity if found, None otherwise
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def get_by_dish_type(self, tipo_plato: EtiquetaPlato) -> List[Plato]:
        """Get dishes by type.
        
        Args:
            tipo_plato: Type of dish (ENTRADA, FONDO, POSTRE)
            
        Returns:
            List of Plato domain entities of the specified type
        """
        pass
    
    @abstractmethod
    async def get_with_ingredients(self) -> List[Plato]:
        """Get dishes that have ingredients in their recipe.
        
        Returns:
            List of Plato domain entities that have recipes with ingredients
        """
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Plato]:
        """Get all dishes.
        
        Returns:
            List of all Plato domain entities
        """
        pass
    
    @abstractmethod
    async def get_available(self) -> List[Plato]:
        """Get available dishes.
        
        Returns dishes that are active, have stock, and have available ingredients.
        
        Returns:
            List of available Plato domain entities
        """
        pass
    
    @abstractmethod
    async def get_by_difficulty(self, dificultad: str) -> List[Plato]:
        """Get dishes by difficulty level.
        
        Args:
            dificultad: Difficulty level ("facil", "medio", "dificil")
            
        Returns:
            List of Plato domain entities with the specified difficulty
        """
        pass
    
    @abstractmethod
    async def get_by_chef(self, chef_recomendado: str) -> List[Plato]:
        """Get dishes by recommended chef.
        
        Args:
            chef_recomendado: Name of the recommended chef
            
        Returns:
            List of Plato domain entities recommended for the specified chef
        """
        pass
    
    @abstractmethod
    async def get_by_preparation_time(self, max_minutes: int) -> List[Plato]:
        """Get dishes by maximum preparation time.
        
        Args:
            max_minutes: Maximum preparation time in minutes
            
        Returns:
            List of Plato domain entities that can be prepared within the time limit
        """
        pass
    
    @abstractmethod
    async def get_by_portions(self, min_portions: int, max_portions: int) -> List[Plato]:
        """Get dishes by portion range.
        
        Args:
            min_portions: Minimum number of portions
            max_portions: Maximum number of portions
            
        Returns:
            List of Plato domain entities within the portion range
        """
        pass
    
    @abstractmethod
    async def get_using_ingredient(self, ingrediente_id: UUID) -> List[Plato]:
        """Get dishes that use a specific ingredient.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient
            
        Returns:
            List of Plato domain entities that include the specified ingredient
        """
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Plato]:
        """Get dish by name.
        
        Args:
            name: Name of the dish
            
        Returns:
            Plato domain entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_vegetarian(self) -> List[Plato]:
        """Get vegetarian dishes.
        
        Returns dishes that don't contain meat ingredients.
        
        Returns:
            List of vegetarian Plato domain entities
        """
        pass
    
    @abstractmethod
    async def get_vegan(self) -> List[Plato]:
        """Get vegan dishes.
        
        Returns dishes that are marked as vegan.
        
        Returns:
            List of vegan Plato domain entities
        """
        pass
    
    @abstractmethod
    async def get_gluten_free(self) -> List[Plato]:
        """Get gluten-free dishes.
        
        Returns dishes that are marked as gluten-free.
        
        Returns:
            List of gluten-free Plato domain entities
        """
        pass
    
    @abstractmethod
    async def save(self, plato: Plato) -> Plato:
        """Save dish (create or update).
        
        Args:
            plato: Plato domain entity to save
            
        Returns:
            Saved Plato domain entity with updated metadata
            
        Raises:
            PlatoAlreadyExistsError: If creating dish with existing name
            InvalidPlatoDataError: If dish data is invalid
            IngredienteNotFoundError: If recipe contains non-existent ingredients
        """
        pass
    
    @abstractmethod
    async def delete(self, plato_id: UUID) -> bool:
        """Delete dish by ID.
        
        Args:
            plato_id: Unique identifier of the dish to delete
            
        Returns:
            True if dish was deleted, False if not found
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def exists_by_id(self, plato_id: UUID) -> bool:
        """Check if dish exists by ID.
        
        Args:
            plato_id: Unique identifier to check
            
        Returns:
            True if dish exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        """Check if dish exists by name.
        
        Args:
            name: Name to check for uniqueness
            
        Returns:
            True if dish with name exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def get_recipe_ingredients(self, plato_id: UUID) -> Dict[UUID, float]:
        """Get recipe ingredients and quantities for a dish.
        
        Args:
            plato_id: Unique identifier of the dish
            
        Returns:
            Dictionary mapping ingredient IDs to required quantities
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def check_ingredient_availability(self, plato_id: UUID) -> bool:
        """Check if all ingredients for a dish are available.
        
        Args:
            plato_id: Unique identifier of the dish
            
        Returns:
            True if all ingredients are available in sufficient quantities
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
        """
        pass
    
    @abstractmethod
    async def get_most_popular(self, limit: int = 10) -> List[Plato]:
        """Get most popular dishes.
        
        Args:
            limit: Maximum number of dishes to return
            
        Returns:
            List of most popular Plato domain entities
        """
        pass