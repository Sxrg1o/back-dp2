"""Ingrediente application service for menu management."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from app.domain.entities.ingrediente import Ingrediente
from app.domain.repositories.ingrediente_repository import IngredienteRepositoryPort
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.domain.exceptions.menu_exceptions import (
    IngredienteNotFoundError,
    IngredienteAlreadyExistsError,
    InsufficientStockError
)
from app.application.dto.ingrediente_dto import (
    CreateIngredienteDTO,
    UpdateIngredienteDTO,
    IngredienteResponseDTO,
    StockUpdateDTO
)


class IngredienteApplicationService:
    """Application service for Ingrediente use cases."""
    
    def __init__(self, ingrediente_repository: IngredienteRepositoryPort):
        """Initialize service with repository dependency.
        
        Args:
            ingrediente_repository: Repository port for ingredient data access
        """
        self._ingrediente_repository = ingrediente_repository
    
    async def create_ingrediente(self, create_dto: CreateIngredienteDTO) -> IngredienteResponseDTO:
        """Create a new ingredient.
        
        Args:
            create_dto: Data transfer object with ingredient creation data
            
        Returns:
            IngredienteResponseDTO with created ingredient data
            
        Raises:
            IngredienteAlreadyExistsError: If ingredient with same name already exists
        """
        # Business rule: Check if ingredient name already exists
        if await self._ingrediente_repository.exists_by_name(create_dto.nombre):
            raise IngredienteAlreadyExistsError(f"Ingredient with name '{create_dto.nombre}' already exists")
        
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
        ingrediente = Ingrediente(
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
            version=1,
            tipo=create_dto.tipo,
            peso_unitario=create_dto.peso_unitario,
            unidad_medida=create_dto.unidad_medida,
            fecha_vencimiento=create_dto.fecha_vencimiento,
            proveedor=create_dto.proveedor
        )
        
        # Save through repository
        saved_ingrediente = await self._ingrediente_repository.save(ingrediente)
        
        # Convert to response DTO
        return self._to_response_dto(saved_ingrediente)
    
    async def update_ingrediente(self, ingrediente_id: UUID, update_dto: UpdateIngredienteDTO) -> IngredienteResponseDTO:
        """Update an existing ingredient.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient to update
            update_dto: Data transfer object with update data
            
        Returns:
            IngredienteResponseDTO with updated ingredient data
            
        Raises:
            IngredienteNotFoundError: If ingredient with given ID doesn't exist
            IngredienteAlreadyExistsError: If updating name to existing name
        """
        # Get existing ingredient
        existing_ingrediente = await self._ingrediente_repository.get_by_id(ingrediente_id)
        if not existing_ingrediente:
            raise IngredienteNotFoundError(f"Ingredient with ID {ingrediente_id} not found")
        
        # Check name uniqueness if name is being updated
        if update_dto.nombre and update_dto.nombre != existing_ingrediente.nombre:
            if await self._ingrediente_repository.exists_by_name(update_dto.nombre):
                raise IngredienteAlreadyExistsError(f"Ingredient with name '{update_dto.nombre}' already exists")
        
        # Update base Item fields
        if update_dto.nombre is not None:
            existing_ingrediente.nombre = update_dto.nombre
        
        if update_dto.descripcion is not None:
            existing_ingrediente.descripcion = update_dto.descripcion
        
        if update_dto.precio is not None:
            existing_ingrediente.actualizar_precio(Precio(update_dto.precio))
        
        if update_dto.informacion_nutricional is not None:
            existing_ingrediente.informacion_nutricional = InformacionNutricional(
                calorias=update_dto.informacion_nutricional.calorias,
                proteinas=update_dto.informacion_nutricional.proteinas,
                azucares=update_dto.informacion_nutricional.azucares,
                grasas=update_dto.informacion_nutricional.grasas,
                carbohidratos=update_dto.informacion_nutricional.carbohidratos,
                fibra=update_dto.informacion_nutricional.fibra,
                sodio=update_dto.informacion_nutricional.sodio
            )
        
        if update_dto.tiempo_preparacion is not None:
            existing_ingrediente.tiempo_preparacion = update_dto.tiempo_preparacion
        
        if update_dto.stock_actual is not None:
            # Business rule: Validate stock consistency
            if update_dto.stock_minimo is not None:
                if update_dto.stock_minimo > update_dto.stock_actual:
                    raise ValueError("Minimum stock cannot be greater than current stock")
            elif existing_ingrediente.stock_minimo > update_dto.stock_actual:
                raise ValueError("Current stock cannot be less than minimum stock")
            
            existing_ingrediente.stock_actual = update_dto.stock_actual
        
        if update_dto.stock_minimo is not None:
            if update_dto.stock_minimo > existing_ingrediente.stock_actual:
                raise ValueError("Minimum stock cannot be greater than current stock")
            existing_ingrediente.stock_minimo = update_dto.stock_minimo
        
        if update_dto.etiquetas is not None:
            existing_ingrediente.etiquetas = update_dto.etiquetas
        
        if update_dto.activo is not None:
            if update_dto.activo:
                existing_ingrediente.activar()
            else:
                existing_ingrediente.desactivar()
        
        # Update Ingrediente-specific fields
        if update_dto.tipo is not None:
            existing_ingrediente.tipo = update_dto.tipo
        
        if update_dto.peso_unitario is not None:
            existing_ingrediente.peso_unitario = update_dto.peso_unitario
        
        if update_dto.unidad_medida is not None:
            existing_ingrediente.unidad_medida = update_dto.unidad_medida
        
        if update_dto.fecha_vencimiento is not None:
            existing_ingrediente.actualizar_fecha_vencimiento(update_dto.fecha_vencimiento)
        
        if update_dto.proveedor is not None:
            if update_dto.proveedor:
                existing_ingrediente.cambiar_proveedor(update_dto.proveedor)
            else:
                existing_ingrediente.proveedor = None
        
        existing_ingrediente.updated_at = datetime.utcnow()
        existing_ingrediente.version += 1
        
        # Save through repository
        updated_ingrediente = await self._ingrediente_repository.save(existing_ingrediente)
        
        # Convert to response DTO
        return self._to_response_dto(updated_ingrediente)
    
    async def get_ingrediente_by_id(self, ingrediente_id: UUID) -> IngredienteResponseDTO:
        """Get ingredient by ID.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient
            
        Returns:
            IngredienteResponseDTO with ingredient data
            
        Raises:
            IngredienteNotFoundError: If ingredient with given ID doesn't exist
        """
        ingrediente = await self._ingrediente_repository.get_by_id(ingrediente_id)
        if not ingrediente:
            raise IngredienteNotFoundError(f"Ingredient with ID {ingrediente_id} not found")
        
        return self._to_response_dto(ingrediente)
    
    async def get_available_ingredientes(self) -> List[IngredienteResponseDTO]:
        """Get all available ingredients.
        
        Returns:
            List of IngredienteResponseDTO with available ingredients
        """
        ingredientes = await self._ingrediente_repository.get_available()
        return [self._to_response_dto(ingrediente) for ingrediente in ingredientes]
    
    async def get_ingredientes_by_type(self, tipo: EtiquetaIngrediente) -> List[IngredienteResponseDTO]:
        """Get ingredients by type.
        
        Args:
            tipo: Type of ingredient (VERDURA, CARNE, FRUTA)
            
        Returns:
            List of IngredienteResponseDTO with ingredients of the specified type
        """
        ingredientes = await self._ingrediente_repository.get_by_type(tipo)
        return [self._to_response_dto(ingrediente) for ingrediente in ingredientes]
    
    async def check_stock(self, ingrediente_id: UUID) -> int:
        """Check current stock of an ingredient.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient
            
        Returns:
            Current stock amount
            
        Raises:
            IngredienteNotFoundError: If ingredient with given ID doesn't exist
        """
        return await self._ingrediente_repository.check_stock(ingrediente_id)
    
    async def update_stock(self, ingrediente_id: UUID, stock_update_dto: StockUpdateDTO) -> IngredienteResponseDTO:
        """Update ingredient stock.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient
            stock_update_dto: Stock update data
            
        Returns:
            IngredienteResponseDTO with updated ingredient data
            
        Raises:
            IngredienteNotFoundError: If ingredient with given ID doesn't exist
            InsufficientStockError: If trying to reduce more stock than available
        """
        ingrediente = await self._ingrediente_repository.get_by_id(ingrediente_id)
        if not ingrediente:
            raise IngredienteNotFoundError(f"Ingredient with ID {ingrediente_id} not found")
        
        if stock_update_dto.operacion == "aumentar":
            ingrediente.aumentar_stock(stock_update_dto.cantidad)
        elif stock_update_dto.operacion == "reducir":
            if stock_update_dto.cantidad > ingrediente.stock_actual:
                raise InsufficientStockError(
                    f"Cannot reduce {stock_update_dto.cantidad} units. Only {ingrediente.stock_actual} units available"
                )
            ingrediente.reducir_stock(stock_update_dto.cantidad)
        
        # Save updated ingredient
        updated_ingrediente = await self._ingrediente_repository.save(ingrediente)
        
        return self._to_response_dto(updated_ingrediente)
    
    async def get_low_stock_ingredientes(self) -> List[IngredienteResponseDTO]:
        """Get ingredients with low stock.
        
        Returns:
            List of IngredienteResponseDTO with ingredients that need restocking
        """
        ingredientes = await self._ingrediente_repository.get_low_stock()
        return [self._to_response_dto(ingrediente) for ingrediente in ingredientes]
    
    async def get_expiring_soon_ingredientes(self, days_ahead: int = 3) -> List[IngredienteResponseDTO]:
        """Get ingredients expiring within specified days.
        
        Args:
            days_ahead: Number of days to look ahead for expiration
            
        Returns:
            List of IngredienteResponseDTO with ingredients expiring soon
        """
        ingredientes = await self._ingrediente_repository.get_expiring_soon(days_ahead)
        return [self._to_response_dto(ingrediente) for ingrediente in ingredientes]
    
    async def get_expired_ingredientes(self) -> List[IngredienteResponseDTO]:
        """Get expired ingredients.
        
        Returns:
            List of IngredienteResponseDTO with expired ingredients
        """
        ingredientes = await self._ingrediente_repository.get_expired()
        return [self._to_response_dto(ingrediente) for ingrediente in ingredientes]
    
    async def get_ingredientes_by_supplier(self, proveedor: str) -> List[IngredienteResponseDTO]:
        """Get ingredients by supplier.
        
        Args:
            proveedor: Supplier name
            
        Returns:
            List of IngredienteResponseDTO from the specified supplier
        """
        ingredientes = await self._ingrediente_repository.get_by_supplier(proveedor)
        return [self._to_response_dto(ingrediente) for ingrediente in ingredientes]
    
    async def verify_stock_availability(self, ingrediente_id: UUID, required_quantity: float) -> bool:
        """Verify if ingredient has sufficient stock for required quantity.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient
            required_quantity: Required quantity to check
            
        Returns:
            True if sufficient stock is available, False otherwise
            
        Raises:
            IngredienteNotFoundError: If ingredient with given ID doesn't exist
        """
        ingrediente = await self._ingrediente_repository.get_by_id(ingrediente_id)
        if not ingrediente:
            raise IngredienteNotFoundError(f"Ingredient with ID {ingrediente_id} not found")
        
        return ingrediente.stock_actual >= required_quantity and ingrediente.is_disponible()
    
    async def calculate_total_weight_by_type(self, tipo: EtiquetaIngrediente) -> float:
        """Calculate total weight of ingredients by type.
        
        Args:
            tipo: Type of ingredient
            
        Returns:
            Total weight in grams of all ingredients of the specified type
        """
        return await self._ingrediente_repository.get_total_weight_by_type(tipo)
    
    async def delete_ingrediente(self, ingrediente_id: UUID) -> bool:
        """Delete an ingredient.
        
        Args:
            ingrediente_id: Unique identifier of the ingredient to delete
            
        Returns:
            True if ingredient was deleted, False if not found
        """
        return await self._ingrediente_repository.delete(ingrediente_id)
    
    async def get_all_ingredientes(self) -> List[IngredienteResponseDTO]:
        """Get all ingredients regardless of availability.
        
        Returns:
            List of IngredienteResponseDTO with all ingredients
        """
        ingredientes = await self._ingrediente_repository.get_all()
        return [self._to_response_dto(ingrediente) for ingrediente in ingredientes]
    
    def _to_response_dto(self, ingrediente: Ingrediente) -> IngredienteResponseDTO:
        """Convert Ingrediente domain entity to response DTO.
        
        Args:
            ingrediente: Ingrediente domain entity
            
        Returns:
            IngredienteResponseDTO with ingredient data
        """
        from app.application.dto.item_dto import InformacionNutricionalDTO
        
        nutritional_dto = InformacionNutricionalDTO(
            calorias=ingrediente.informacion_nutricional.calorias,
            proteinas=ingrediente.informacion_nutricional.proteinas,
            azucares=ingrediente.informacion_nutricional.azucares,
            grasas=ingrediente.informacion_nutricional.grasas,
            carbohidratos=ingrediente.informacion_nutricional.carbohidratos,
            fibra=ingrediente.informacion_nutricional.fibra,
            sodio=ingrediente.informacion_nutricional.sodio
        )
        
        return IngredienteResponseDTO(
            id=ingrediente.id,
            nombre=ingrediente.nombre,
            descripcion=ingrediente.descripcion,
            precio=ingrediente.precio.value,
            informacion_nutricional=nutritional_dto,
            tiempo_preparacion=ingrediente.tiempo_preparacion,
            stock_actual=ingrediente.stock_actual,
            stock_minimo=ingrediente.stock_minimo,
            etiquetas=ingrediente.etiquetas,
            activo=ingrediente.activo,
            tipo=ingrediente.tipo,
            peso_unitario=ingrediente.peso_unitario,
            unidad_medida=ingrediente.unidad_medida,
            fecha_vencimiento=ingrediente.fecha_vencimiento,
            proveedor=ingrediente.proveedor
        )