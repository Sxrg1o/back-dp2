"""Bebida application service for menu management."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from app.domain.entities.bebida import Bebida
from app.domain.repositories.bebida_repository import BebidaRepositoryPort
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.exceptions.menu_exceptions import (
    BebidaNotFoundError,
    BebidaAlreadyExistsError,
    InsufficientStockError
)
from app.application.dto.bebida_dto import (
    CreateBebidaDTO,
    UpdateBebidaDTO,
    BebidaResponseDTO
)


class BebidaApplicationService:
    """Application service for Bebida use cases."""
    
    def __init__(self, bebida_repository: BebidaRepositoryPort):
        """Initialize service with repository dependency.
        
        Args:
            bebida_repository: Repository port for beverage data access
        """
        self._bebida_repository = bebida_repository
    
    async def create_bebida(self, create_dto: CreateBebidaDTO) -> BebidaResponseDTO:
        """Create a new beverage.
        
        Args:
            create_dto: Data transfer object with beverage creation data
            
        Returns:
            BebidaResponseDTO with created beverage data
            
        Raises:
            BebidaAlreadyExistsError: If beverage with same name already exists
        """
        # Business rule: Check if beverage name already exists
        if await self._bebida_repository.exists_by_name(create_dto.nombre):
            raise BebidaAlreadyExistsError(f"Beverage with name '{create_dto.nombre}' already exists")
        
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
        bebida = Bebida(
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
            volumen=create_dto.volumen,
            contenido_alcohol=create_dto.contenido_alcohol,
            temperatura_servicio=create_dto.temperatura_servicio,
            tipo_bebida=create_dto.tipo_bebida,
            marca=create_dto.marca,
            origen=create_dto.origen
        )
        
        # Save through repository
        saved_bebida = await self._bebida_repository.save(bebida)
        
        # Convert to response DTO
        return self._to_response_dto(saved_bebida)
    
    async def update_bebida(self, bebida_id: UUID, update_dto: UpdateBebidaDTO) -> BebidaResponseDTO:
        """Update an existing beverage.
        
        Args:
            bebida_id: Unique identifier of the beverage to update
            update_dto: Data transfer object with update data
            
        Returns:
            BebidaResponseDTO with updated beverage data
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
            BebidaAlreadyExistsError: If updating name to existing name
        """
        # Get existing beverage
        existing_bebida = await self._bebida_repository.get_by_id(bebida_id)
        if not existing_bebida:
            raise BebidaNotFoundError(f"Beverage with ID {bebida_id} not found")
        
        # Check name uniqueness if name is being updated
        if update_dto.nombre and update_dto.nombre != existing_bebida.nombre:
            if await self._bebida_repository.exists_by_name(update_dto.nombre):
                raise BebidaAlreadyExistsError(f"Beverage with name '{update_dto.nombre}' already exists")
        
        # Update base Item fields
        if update_dto.nombre is not None:
            existing_bebida.nombre = update_dto.nombre
        
        if update_dto.descripcion is not None:
            existing_bebida.descripcion = update_dto.descripcion
        
        if update_dto.precio is not None:
            existing_bebida.actualizar_precio(Precio(update_dto.precio))
        
        if update_dto.informacion_nutricional is not None:
            existing_bebida.informacion_nutricional = InformacionNutricional(
                calorias=update_dto.informacion_nutricional.calorias,
                proteinas=update_dto.informacion_nutricional.proteinas,
                azucares=update_dto.informacion_nutricional.azucares,
                grasas=update_dto.informacion_nutricional.grasas,
                carbohidratos=update_dto.informacion_nutricional.carbohidratos,
                fibra=update_dto.informacion_nutricional.fibra,
                sodio=update_dto.informacion_nutricional.sodio
            )
        
        if update_dto.tiempo_preparacion is not None:
            existing_bebida.tiempo_preparacion = update_dto.tiempo_preparacion
        
        if update_dto.stock_actual is not None:
            # Business rule: Validate stock consistency
            if update_dto.stock_minimo is not None:
                if update_dto.stock_minimo > update_dto.stock_actual:
                    raise ValueError("Minimum stock cannot be greater than current stock")
            elif existing_bebida.stock_minimo > update_dto.stock_actual:
                raise ValueError("Current stock cannot be less than minimum stock")
            
            existing_bebida.stock_actual = update_dto.stock_actual
        
        if update_dto.stock_minimo is not None:
            if update_dto.stock_minimo > existing_bebida.stock_actual:
                raise ValueError("Minimum stock cannot be greater than current stock")
            existing_bebida.stock_minimo = update_dto.stock_minimo
        
        if update_dto.etiquetas is not None:
            existing_bebida.etiquetas = update_dto.etiquetas
        
        if update_dto.activo is not None:
            if update_dto.activo:
                existing_bebida.activar()
            else:
                existing_bebida.desactivar()
        
        # Update Bebida-specific fields
        if update_dto.volumen is not None:
            existing_bebida.volumen = update_dto.volumen
        
        if update_dto.contenido_alcohol is not None:
            existing_bebida.contenido_alcohol = update_dto.contenido_alcohol
        
        if update_dto.temperatura_servicio is not None:
            existing_bebida.actualizar_temperatura_servicio(update_dto.temperatura_servicio)
        
        if update_dto.tipo_bebida is not None:
            existing_bebida.tipo_bebida = update_dto.tipo_bebida
        
        if update_dto.marca is not None:
            if update_dto.marca:
                existing_bebida.actualizar_marca(update_dto.marca)
            else:
                existing_bebida.marca = None
        
        if update_dto.origen is not None:
            if update_dto.origen:
                existing_bebida.actualizar_origen(update_dto.origen)
            else:
                existing_bebida.origen = None
        
        existing_bebida.updated_at = datetime.utcnow()
        existing_bebida.version += 1
        
        # Save through repository
        updated_bebida = await self._bebida_repository.save(existing_bebida)
        
        # Convert to response DTO
        return self._to_response_dto(updated_bebida)
    
    async def get_bebida_by_id(self, bebida_id: UUID) -> BebidaResponseDTO:
        """Get beverage by ID.
        
        Args:
            bebida_id: Unique identifier of the beverage
            
        Returns:
            BebidaResponseDTO with beverage data
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
        """
        bebida = await self._bebida_repository.get_by_id(bebida_id)
        if not bebida:
            raise BebidaNotFoundError(f"Beverage with ID {bebida_id} not found")
        
        return self._to_response_dto(bebida)
    
    async def get_available_bebidas(self) -> List[BebidaResponseDTO]:
        """Get all available beverages.
        
        Returns:
            List of BebidaResponseDTO with available beverages
        """
        bebidas = await self._bebida_repository.get_available()
        return [self._to_response_dto(bebida) for bebida in bebidas]
    
    async def get_alcoholic_bebidas(self) -> List[BebidaResponseDTO]:
        """Get alcoholic beverages.
        
        Returns:
            List of BebidaResponseDTO with alcoholic beverages
        """
        bebidas = await self._bebida_repository.get_alcoholic()
        return [self._to_response_dto(bebida) for bebida in bebidas]
    
    async def get_non_alcoholic_bebidas(self) -> List[BebidaResponseDTO]:
        """Get non-alcoholic beverages.
        
        Returns:
            List of BebidaResponseDTO with non-alcoholic beverages
        """
        bebidas = await self._bebida_repository.get_non_alcoholic()
        return [self._to_response_dto(bebida) for bebida in bebidas]
    
    async def get_bebidas_by_volume_range(self, min_volume: float, max_volume: float) -> List[BebidaResponseDTO]:
        """Get beverages within volume range.
        
        Args:
            min_volume: Minimum volume in milliliters (inclusive)
            max_volume: Maximum volume in milliliters (inclusive)
            
        Returns:
            List of BebidaResponseDTO with beverages within the volume range
        """
        bebidas = await self._bebida_repository.get_by_volume_range(min_volume, max_volume)
        return [self._to_response_dto(bebida) for bebida in bebidas]
    
    async def get_bebidas_by_temperature(self, temperatura: str) -> List[BebidaResponseDTO]:
        """Get beverages by service temperature.
        
        Args:
            temperatura: Service temperature ("fria", "caliente", "ambiente")
            
        Returns:
            List of BebidaResponseDTO with beverages of the specified temperature
        """
        if temperatura not in ["fria", "caliente", "ambiente"]:
            raise ValueError("Temperature must be 'fria', 'caliente', or 'ambiente'")
        
        bebidas = await self._bebida_repository.get_by_temperature(temperatura)
        return [self._to_response_dto(bebida) for bebida in bebidas]
    
    async def get_bebidas_by_brand(self, marca: str) -> List[BebidaResponseDTO]:
        """Get beverages by brand.
        
        Args:
            marca: Brand name
            
        Returns:
            List of BebidaResponseDTO from the specified brand
        """
        bebidas = await self._bebida_repository.get_by_brand(marca)
        return [self._to_response_dto(bebida) for bebida in bebidas]
    
    async def check_stock(self, bebida_id: UUID) -> int:
        """Check current stock of a beverage.
        
        Args:
            bebida_id: Unique identifier of the beverage
            
        Returns:
            Current stock amount
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
        """
        bebida = await self._bebida_repository.get_by_id(bebida_id)
        if not bebida:
            raise BebidaNotFoundError(f"Beverage with ID {bebida_id} not found")
        
        return bebida.stock_actual
    
    async def update_stock(self, bebida_id: UUID, cantidad: int, operacion: str) -> BebidaResponseDTO:
        """Update beverage stock.
        
        Args:
            bebida_id: Unique identifier of the beverage
            cantidad: Amount to add or subtract
            operacion: Operation type ("aumentar" or "reducir")
            
        Returns:
            BebidaResponseDTO with updated beverage data
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
            InsufficientStockError: If trying to reduce more stock than available
        """
        bebida = await self._bebida_repository.get_by_id(bebida_id)
        if not bebida:
            raise BebidaNotFoundError(f"Beverage with ID {bebida_id} not found")
        
        if operacion == "aumentar":
            bebida.aumentar_stock(cantidad)
        elif operacion == "reducir":
            if cantidad > bebida.stock_actual:
                raise InsufficientStockError(
                    f"Cannot reduce {cantidad} units. Only {bebida.stock_actual} units available"
                )
            bebida.reducir_stock(cantidad)
        else:
            raise ValueError("Operation must be 'aumentar' or 'reducir'")
        
        # Save updated beverage
        updated_bebida = await self._bebida_repository.save(bebida)
        
        return self._to_response_dto(updated_bebida)
    
    async def get_low_stock_bebidas(self) -> List[BebidaResponseDTO]:
        """Get beverages with low stock.
        
        Returns:
            List of BebidaResponseDTO with beverages that need restocking
        """
        bebidas = await self._bebida_repository.get_low_stock()
        return [self._to_response_dto(bebida) for bebida in bebidas]
    
    async def verify_age_restriction(self, bebida_id: UUID) -> bool:
        """Check if beverage requires age verification (alcoholic beverages).
        
        Args:
            bebida_id: Unique identifier of the beverage
            
        Returns:
            True if age verification is required, False otherwise
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
        """
        bebida = await self._bebida_repository.get_by_id(bebida_id)
        if not bebida:
            raise BebidaNotFoundError(f"Beverage with ID {bebida_id} not found")
        
        return bebida.requiere_edad_minima()
    
    async def calculate_alcohol_content(self, bebida_id: UUID) -> float:
        """Calculate total alcohol content in milliliters.
        
        Args:
            bebida_id: Unique identifier of the beverage
            
        Returns:
            Total alcohol content in milliliters
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
        """
        bebida = await self._bebida_repository.get_by_id(bebida_id)
        if not bebida:
            raise BebidaNotFoundError(f"Beverage with ID {bebida_id} not found")
        
        return bebida.calcular_alcohol_total()
    
    async def calculate_price_per_ml(self, bebida_id: UUID) -> float:
        """Calculate price per milliliter.
        
        Args:
            bebida_id: Unique identifier of the beverage
            
        Returns:
            Price per milliliter
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
        """
        bebida = await self._bebida_repository.get_by_id(bebida_id)
        if not bebida:
            raise BebidaNotFoundError(f"Beverage with ID {bebida_id} not found")
        
        return bebida.calcular_precio_por_ml()
    
    async def get_bebidas_suitable_for_minors(self) -> List[BebidaResponseDTO]:
        """Get beverages suitable for minors (non-alcoholic).
        
        Returns:
            List of BebidaResponseDTO with beverages suitable for minors
        """
        bebidas = await self._bebida_repository.get_non_alcoholic()
        return [self._to_response_dto(bebida) for bebida in bebidas]
    
    async def activate_bebida(self, bebida_id: UUID) -> BebidaResponseDTO:
        """Activate a beverage.
        
        Args:
            bebida_id: Unique identifier of the beverage
            
        Returns:
            BebidaResponseDTO with updated beverage data
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
        """
        bebida = await self._bebida_repository.get_by_id(bebida_id)
        if not bebida:
            raise BebidaNotFoundError(f"Beverage with ID {bebida_id} not found")
        
        bebida.activar()
        updated_bebida = await self._bebida_repository.save(bebida)
        
        return self._to_response_dto(updated_bebida)
    
    async def deactivate_bebida(self, bebida_id: UUID) -> BebidaResponseDTO:
        """Deactivate a beverage.
        
        Args:
            bebida_id: Unique identifier of the beverage
            
        Returns:
            BebidaResponseDTO with updated beverage data
            
        Raises:
            BebidaNotFoundError: If beverage with given ID doesn't exist
        """
        bebida = await self._bebida_repository.get_by_id(bebida_id)
        if not bebida:
            raise BebidaNotFoundError(f"Beverage with ID {bebida_id} not found")
        
        bebida.desactivar()
        updated_bebida = await self._bebida_repository.save(bebida)
        
        return self._to_response_dto(updated_bebida)
    
    async def delete_bebida(self, bebida_id: UUID) -> bool:
        """Delete a beverage.
        
        Args:
            bebida_id: Unique identifier of the beverage to delete
            
        Returns:
            True if beverage was deleted, False if not found
        """
        return await self._bebida_repository.delete(bebida_id)
    
    async def get_all_bebidas(self) -> List[BebidaResponseDTO]:
        """Get all beverages regardless of availability.
        
        Returns:
            List of BebidaResponseDTO with all beverages
        """
        bebidas = await self._bebida_repository.get_all()
        return [self._to_response_dto(bebida) for bebida in bebidas]
    
    def _to_response_dto(self, bebida: Bebida) -> BebidaResponseDTO:
        """Convert Bebida domain entity to response DTO.
        
        Args:
            bebida: Bebida domain entity
            
        Returns:
            BebidaResponseDTO with beverage data
        """
        from app.application.dto.item_dto import InformacionNutricionalDTO
        
        nutritional_dto = InformacionNutricionalDTO(
            calorias=bebida.informacion_nutricional.calorias,
            proteinas=bebida.informacion_nutricional.proteinas,
            azucares=bebida.informacion_nutricional.azucares,
            grasas=bebida.informacion_nutricional.grasas,
            carbohidratos=bebida.informacion_nutricional.carbohidratos,
            fibra=bebida.informacion_nutricional.fibra,
            sodio=bebida.informacion_nutricional.sodio
        )
        
        return BebidaResponseDTO(
            id=bebida.id,
            nombre=bebida.nombre,
            descripcion=bebida.descripcion,
            precio=bebida.precio.value,
            informacion_nutricional=nutritional_dto,
            tiempo_preparacion=bebida.tiempo_preparacion,
            stock_actual=bebida.stock_actual,
            stock_minimo=bebida.stock_minimo,
            etiquetas=bebida.etiquetas,
            activo=bebida.activo,
            volumen=bebida.volumen,
            contenido_alcohol=bebida.contenido_alcohol,
            temperatura_servicio=bebida.temperatura_servicio,
            tipo_bebida=bebida.tipo_bebida,
            marca=bebida.marca,
            origen=bebida.origen
        )