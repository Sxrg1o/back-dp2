"""Item application service for menu management."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from app.domain.entities.item import Item
from app.domain.repositories.item_repository import ItemRepositoryPort
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.exceptions.menu_exceptions import (
    ItemNotFoundError,
    ItemAlreadyExistsError,
    InsufficientStockError
)
from app.application.dto.item_dto import (
    CreateItemDTO,
    UpdateItemDTO,
    ItemResponseDTO
)


class ItemApplicationService:
    """Application service for Item use cases."""
    
    def __init__(self, item_repository: ItemRepositoryPort):
        """Initialize service with repository dependency.
        
        Args:
            item_repository: Repository port for item data access
        """
        self._item_repository = item_repository
    
    async def create_item(self, create_dto: CreateItemDTO) -> ItemResponseDTO:
        """Create a new menu item.
        
        Args:
            create_dto: Data transfer object with item creation data
            
        Returns:
            ItemResponseDTO with created item data
            
        Raises:
            ItemAlreadyExistsError: If item with same name already exists
        """
        # Business rule: Check if item name already exists
        if await self._item_repository.exists_by_name(create_dto.nombre):
            raise ItemAlreadyExistsError(f"Item with name '{create_dto.nombre}' already exists")
        
        # Create domain value objects
        precio = Precio(create_dto.precio)
        informacion_nutricional = InformacionNutricional(
            calorias=create_dto.informacion_nutricional.calorias,
            proteinas=create_dto.informacion_nutricional.proteinas,
            azucares=create_dto.informacion_nutricional.azucares,
            grasas=create_dto.informacion_nutricional.grasas,
            carbohidratos=create_dto.informacion_nutricional.carbohidratos,
            fibra=create_dto.informacion_nutricional.fibra,
            sodio=create_dto.informacion_nutricional.sodio
        )
        
        # Create domain entity
        now = datetime.utcnow()
        item = Item(
            id=uuid4(),
            nombre=create_dto.nombre,
            descripcion=create_dto.descripcion,
            precio=precio,
            informacion_nutricional=informacion_nutricional,
            tiempo_preparacion=create_dto.tiempo_preparacion,
            stock_actual=create_dto.stock_actual,
            stock_minimo=create_dto.stock_minimo,
            etiquetas=create_dto.etiquetas,
            activo=create_dto.activo,
            created_at=now,
            updated_at=now,
            version=1
        )
        
        # Save through repository
        saved_item = await self._item_repository.save(item)
        
        # Convert to response DTO
        return self._to_response_dto(saved_item)
    
    async def update_item(self, item_id: UUID, update_dto: UpdateItemDTO) -> ItemResponseDTO:
        """Update an existing menu item.
        
        Args:
            item_id: Unique identifier of the item to update
            update_dto: Data transfer object with update data
            
        Returns:
            ItemResponseDTO with updated item data
            
        Raises:
            ItemNotFoundError: If item with given ID doesn't exist
            ItemAlreadyExistsError: If updating name to existing name
        """
        # Get existing item
        existing_item = await self._item_repository.get_by_id(item_id)
        if not existing_item:
            raise ItemNotFoundError(f"Item with ID {item_id} not found")
        
        # Check name uniqueness if name is being updated
        if update_dto.nombre and update_dto.nombre != existing_item.nombre:
            if await self._item_repository.exists_by_name(update_dto.nombre):
                raise ItemAlreadyExistsError(f"Item with name '{update_dto.nombre}' already exists")
        
        # Update fields if provided
        if update_dto.nombre is not None:
            existing_item.nombre = update_dto.nombre
        
        if update_dto.descripcion is not None:
            existing_item.descripcion = update_dto.descripcion
        
        if update_dto.precio is not None:
            existing_item.actualizar_precio(Precio(update_dto.precio))
        
        if update_dto.informacion_nutricional is not None:
            existing_item.informacion_nutricional = InformacionNutricional(
                calorias=update_dto.informacion_nutricional.calorias,
                proteinas=update_dto.informacion_nutricional.proteinas,
                azucares=update_dto.informacion_nutricional.azucares,
                grasas=update_dto.informacion_nutricional.grasas,
                carbohidratos=update_dto.informacion_nutricional.carbohidratos,
                fibra=update_dto.informacion_nutricional.fibra,
                sodio=update_dto.informacion_nutricional.sodio
            )
        
        if update_dto.tiempo_preparacion is not None:
            existing_item.tiempo_preparacion = update_dto.tiempo_preparacion
        
        if update_dto.stock_actual is not None:
            # Business rule: Validate stock consistency
            if update_dto.stock_minimo is not None:
                if update_dto.stock_minimo > update_dto.stock_actual:
                    raise ValueError("Minimum stock cannot be greater than current stock")
            elif existing_item.stock_minimo > update_dto.stock_actual:
                raise ValueError("Current stock cannot be less than minimum stock")
            
            existing_item.stock_actual = update_dto.stock_actual
        
        if update_dto.stock_minimo is not None:
            if update_dto.stock_minimo > existing_item.stock_actual:
                raise ValueError("Minimum stock cannot be greater than current stock")
            existing_item.stock_minimo = update_dto.stock_minimo
        
        if update_dto.etiquetas is not None:
            existing_item.etiquetas = update_dto.etiquetas
        
        if update_dto.activo is not None:
            if update_dto.activo:
                existing_item.activar()
            else:
                existing_item.desactivar()
        
        existing_item.updated_at = datetime.utcnow()
        existing_item.version += 1
        
        # Save through repository
        updated_item = await self._item_repository.save(existing_item)
        
        # Convert to response DTO
        return self._to_response_dto(updated_item)
    
    async def get_item_by_id(self, item_id: UUID) -> ItemResponseDTO:
        """Get item by ID.
        
        Args:
            item_id: Unique identifier of the item
            
        Returns:
            ItemResponseDTO with item data
            
        Raises:
            ItemNotFoundError: If item with given ID doesn't exist
        """
        item = await self._item_repository.get_by_id(item_id)
        if not item:
            raise ItemNotFoundError(f"Item with ID {item_id} not found")
        
        return self._to_response_dto(item)
    
    async def get_available_items(self) -> List[ItemResponseDTO]:
        """Get all available items.
        
        Returns:
            List of ItemResponseDTO with available items
        """
        items = await self._item_repository.get_available_items()
        return [self._to_response_dto(item) for item in items]
    
    async def get_items_by_category(self, etiqueta: EtiquetaItem) -> List[ItemResponseDTO]:
        """Get items by category/label.
        
        Args:
            etiqueta: Item label to filter by
            
        Returns:
            List of ItemResponseDTO with items of the specified category
        """
        items = await self._item_repository.get_by_category(etiqueta)
        return [self._to_response_dto(item) for item in items]
    
    async def check_stock(self, item_id: UUID) -> int:
        """Check current stock of an item.
        
        Args:
            item_id: Unique identifier of the item
            
        Returns:
            Current stock amount
            
        Raises:
            ItemNotFoundError: If item with given ID doesn't exist
        """
        item = await self._item_repository.get_by_id(item_id)
        if not item:
            raise ItemNotFoundError(f"Item with ID {item_id} not found")
        
        return item.stock_actual
    
    async def update_stock(self, item_id: UUID, cantidad: int, operacion: str) -> ItemResponseDTO:
        """Update item stock.
        
        Args:
            item_id: Unique identifier of the item
            cantidad: Amount to add or subtract
            operacion: Operation type ("aumentar" or "reducir")
            
        Returns:
            ItemResponseDTO with updated item data
            
        Raises:
            ItemNotFoundError: If item with given ID doesn't exist
            InsufficientStockError: If trying to reduce more stock than available
        """
        item = await self._item_repository.get_by_id(item_id)
        if not item:
            raise ItemNotFoundError(f"Item with ID {item_id} not found")
        
        if operacion == "aumentar":
            item.aumentar_stock(cantidad)
        elif operacion == "reducir":
            if cantidad > item.stock_actual:
                raise InsufficientStockError(
                    f"Cannot reduce {cantidad} units. Only {item.stock_actual} units available"
                )
            item.reducir_stock(cantidad)
        else:
            raise ValueError("Operation must be 'aumentar' or 'reducir'")
        
        # Save updated item
        updated_item = await self._item_repository.save(item)
        
        return self._to_response_dto(updated_item)
    
    async def get_low_stock_items(self) -> List[ItemResponseDTO]:
        """Get items with low stock.
        
        Returns:
            List of ItemResponseDTO with items that need restocking
        """
        items = await self._item_repository.get_low_stock_items()
        return [self._to_response_dto(item) for item in items]
    
    async def get_items_by_price_range(self, min_price: float, max_price: float) -> List[ItemResponseDTO]:
        """Get items within price range.
        
        Args:
            min_price: Minimum price (inclusive)
            max_price: Maximum price (inclusive)
            
        Returns:
            List of ItemResponseDTO with items within the price range
        """
        items = await self._item_repository.get_by_price_range(min_price, max_price)
        return [self._to_response_dto(item) for item in items]
    
    async def activate_item(self, item_id: UUID) -> ItemResponseDTO:
        """Activate an item.
        
        Args:
            item_id: Unique identifier of the item
            
        Returns:
            ItemResponseDTO with updated item data
            
        Raises:
            ItemNotFoundError: If item with given ID doesn't exist
        """
        item = await self._item_repository.get_by_id(item_id)
        if not item:
            raise ItemNotFoundError(f"Item with ID {item_id} not found")
        
        item.activar()
        updated_item = await self._item_repository.save(item)
        
        return self._to_response_dto(updated_item)
    
    async def deactivate_item(self, item_id: UUID) -> ItemResponseDTO:
        """Deactivate an item.
        
        Args:
            item_id: Unique identifier of the item
            
        Returns:
            ItemResponseDTO with updated item data
            
        Raises:
            ItemNotFoundError: If item with given ID doesn't exist
        """
        item = await self._item_repository.get_by_id(item_id)
        if not item:
            raise ItemNotFoundError(f"Item with ID {item_id} not found")
        
        item.desactivar()
        updated_item = await self._item_repository.save(item)
        
        return self._to_response_dto(updated_item)
    
    async def delete_item(self, item_id: UUID) -> bool:
        """Delete an item.
        
        Args:
            item_id: Unique identifier of the item to delete
            
        Returns:
            True if item was deleted, False if not found
        """
        return await self._item_repository.delete(item_id)
    
    async def get_all_items(self) -> List[ItemResponseDTO]:
        """Get all items regardless of availability.
        
        Returns:
            List of ItemResponseDTO with all items
        """
        items = await self._item_repository.get_all()
        return [self._to_response_dto(item) for item in items]
    
    def _to_response_dto(self, item: Item) -> ItemResponseDTO:
        """Convert Item domain entity to response DTO.
        
        Args:
            item: Item domain entity
            
        Returns:
            ItemResponseDTO with item data
        """
        from app.application.dto.item_dto import InformacionNutricionalDTO
        
        nutritional_dto = InformacionNutricionalDTO(
            calorias=item.informacion_nutricional.calorias,
            proteinas=item.informacion_nutricional.proteinas,
            azucares=item.informacion_nutricional.azucares,
            grasas=item.informacion_nutricional.grasas,
            carbohidratos=item.informacion_nutricional.carbohidratos,
            fibra=item.informacion_nutricional.fibra,
            sodio=item.informacion_nutricional.sodio
        )
        
        return ItemResponseDTO(
            id=item.id,
            nombre=item.nombre,
            descripcion=item.descripcion,
            precio=item.precio.value,
            informacion_nutricional=nutritional_dto,
            tiempo_preparacion=item.tiempo_preparacion,
            stock_actual=item.stock_actual,
            stock_minimo=item.stock_minimo,
            etiquetas=item.etiquetas,
            activo=item.activo
        )