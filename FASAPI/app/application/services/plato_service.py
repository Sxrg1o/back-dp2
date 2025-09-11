"""Plato application service for menu management."""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from app.domain.entities.plato import Plato
from app.domain.entities.ingrediente import Ingrediente
from app.domain.repositories.plato_repository import PlatoRepositoryPort
from app.domain.repositories.ingrediente_repository import IngredienteRepositoryPort
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.domain.exceptions.menu_exceptions import (
    PlatoNotFoundError,
    PlatoAlreadyExistsError,
    IngredienteNotFoundError,
    InsufficientStockError
)
from app.application.dto.plato_dto import (
    CreatePlatoDTO,
    UpdatePlatoDTO,
    PlatoResponseDTO,
    AgregarIngredienteRecetaDTO,
    ActualizarIngredienteRecetaDTO
)


class PlatoApplicationService:
    """Application service for Plato use cases."""
    
    def __init__(
        self, 
        plato_repository: PlatoRepositoryPort,
        ingrediente_repository: IngredienteRepositoryPort
    ):
        """Initialize service with repository dependencies.
        
        Args:
            plato_repository: Repository port for dish data access
            ingrediente_repository: Repository port for ingredient data access
        """
        self._plato_repository = plato_repository
        self._ingrediente_repository = ingrediente_repository
    
    async def create_plato(self, create_dto: CreatePlatoDTO) -> PlatoResponseDTO:
        """Create a new dish.
        
        Args:
            create_dto: Data transfer object with dish creation data
            
        Returns:
            PlatoResponseDTO with created dish data
            
        Raises:
            PlatoAlreadyExistsError: If dish with same name already exists
            IngredienteNotFoundError: If recipe contains non-existent ingredients
        """
        # Business rule: Check if dish name already exists
        if await self._plato_repository.exists_by_name(create_dto.nombre):
            raise PlatoAlreadyExistsError(f"Dish with name '{create_dto.nombre}' already exists")
        
        # Validate recipe ingredients exist
        if create_dto.receta:
            for ingrediente_id in create_dto.receta.keys():
                ingrediente = await self._ingrediente_repository.get_by_id(ingrediente_id)
                if not ingrediente:
                    raise IngredienteNotFoundError(f"Ingredient with ID {ingrediente_id} not found")
        
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
        plato = Plato(
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
            tipo_plato=create_dto.tipo_plato,
            receta=create_dto.receta,
            instrucciones=create_dto.instrucciones,
            porciones=create_dto.porciones,
            dificultad=create_dto.dificultad,
            chef_recomendado=create_dto.chef_recomendado
        )
        
        # Save through repository
        saved_plato = await self._plato_repository.save(plato)
        
        # Convert to response DTO
        return self._to_response_dto(saved_plato)
    
    async def update_plato(self, plato_id: UUID, update_dto: UpdatePlatoDTO) -> PlatoResponseDTO:
        """Update an existing dish.
        
        Args:
            plato_id: Unique identifier of the dish to update
            update_dto: Data transfer object with update data
            
        Returns:
            PlatoResponseDTO with updated dish data
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
            PlatoAlreadyExistsError: If updating name to existing name
            IngredienteNotFoundError: If recipe contains non-existent ingredients
        """
        # Get existing dish
        existing_plato = await self._plato_repository.get_by_id(plato_id)
        if not existing_plato:
            raise PlatoNotFoundError(f"Dish with ID {plato_id} not found")
        
        # Check name uniqueness if name is being updated
        if update_dto.nombre and update_dto.nombre != existing_plato.nombre:
            if await self._plato_repository.exists_by_name(update_dto.nombre):
                raise PlatoAlreadyExistsError(f"Dish with name '{update_dto.nombre}' already exists")
        
        # Validate recipe ingredients if recipe is being updated
        if update_dto.receta:
            for ingrediente_id in update_dto.receta.keys():
                ingrediente = await self._ingrediente_repository.get_by_id(ingrediente_id)
                if not ingrediente:
                    raise IngredienteNotFoundError(f"Ingredient with ID {ingrediente_id} not found")
        
        # Update base Item fields
        if update_dto.nombre is not None:
            existing_plato.nombre = update_dto.nombre
        
        if update_dto.descripcion is not None:
            existing_plato.descripcion = update_dto.descripcion
        
        if update_dto.precio is not None:
            existing_plato.actualizar_precio(Precio(update_dto.precio))
        
        if update_dto.informacion_nutricional is not None:
            existing_plato.informacion_nutricional = InformacionNutricional(
                calorias=update_dto.informacion_nutricional.calorias,
                proteinas=update_dto.informacion_nutricional.proteinas,
                azucares=update_dto.informacion_nutricional.azucares,
                grasas=update_dto.informacion_nutricional.grasas,
                carbohidratos=update_dto.informacion_nutricional.carbohidratos,
                fibra=update_dto.informacion_nutricional.fibra,
                sodio=update_dto.informacion_nutricional.sodio
            )
        
        if update_dto.tiempo_preparacion is not None:
            existing_plato.tiempo_preparacion = update_dto.tiempo_preparacion
        
        if update_dto.stock_actual is not None:
            # Business rule: Validate stock consistency
            if update_dto.stock_minimo is not None:
                if update_dto.stock_minimo > update_dto.stock_actual:
                    raise ValueError("Minimum stock cannot be greater than current stock")
            elif existing_plato.stock_minimo > update_dto.stock_actual:
                raise ValueError("Current stock cannot be less than minimum stock")
            
            existing_plato.stock_actual = update_dto.stock_actual
        
        if update_dto.stock_minimo is not None:
            if update_dto.stock_minimo > existing_plato.stock_actual:
                raise ValueError("Minimum stock cannot be greater than current stock")
            existing_plato.stock_minimo = update_dto.stock_minimo
        
        if update_dto.etiquetas is not None:
            existing_plato.etiquetas = update_dto.etiquetas
        
        if update_dto.activo is not None:
            if update_dto.activo:
                existing_plato.activar()
            else:
                existing_plato.desactivar()
        
        # Update Plato-specific fields
        if update_dto.tipo_plato is not None:
            existing_plato.tipo_plato = update_dto.tipo_plato
        
        if update_dto.receta is not None:
            existing_plato.receta = update_dto.receta
        
        if update_dto.instrucciones is not None:
            existing_plato.actualizar_instrucciones(update_dto.instrucciones)
        
        if update_dto.porciones is not None:
            existing_plato.porciones = update_dto.porciones
        
        if update_dto.dificultad is not None:
            existing_plato.dificultad = update_dto.dificultad
        
        if update_dto.chef_recomendado is not None:
            if update_dto.chef_recomendado:
                existing_plato.asignar_chef(update_dto.chef_recomendado)
            else:
                existing_plato.chef_recomendado = None
        
        existing_plato.updated_at = datetime.utcnow()
        existing_plato.version += 1
        
        # Save through repository
        updated_plato = await self._plato_repository.save(existing_plato)
        
        # Convert to response DTO
        return self._to_response_dto(updated_plato)
    
    async def get_plato_by_id(self, plato_id: UUID) -> PlatoResponseDTO:
        """Get dish by ID.
        
        Args:
            plato_id: Unique identifier of the dish
            
        Returns:
            PlatoResponseDTO with dish data
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
        """
        plato = await self._plato_repository.get_by_id(plato_id)
        if not plato:
            raise PlatoNotFoundError(f"Dish with ID {plato_id} not found")
        
        return self._to_response_dto(plato)
    
    async def get_available_platos(self) -> List[PlatoResponseDTO]:
        """Get all available dishes.
        
        Returns:
            List of PlatoResponseDTO with available dishes
        """
        platos = await self._plato_repository.get_available()
        return [self._to_response_dto(plato) for plato in platos]
    
    async def get_platos_by_dish_type(self, tipo_plato: EtiquetaPlato) -> List[PlatoResponseDTO]:
        """Get dishes by type.
        
        Args:
            tipo_plato: Type of dish (ENTRADA, FONDO, POSTRE)
            
        Returns:
            List of PlatoResponseDTO with dishes of the specified type
        """
        platos = await self._plato_repository.get_by_dish_type(tipo_plato)
        return [self._to_response_dto(plato) for plato in platos]
    
    async def get_platos_with_ingredients(self) -> List[PlatoResponseDTO]:
        """Get dishes that have ingredients in their recipe.
        
        Returns:
            List of PlatoResponseDTO with dishes that have recipes
        """
        # Get all platos and filter those with ingredients
        all_platos = await self._plato_repository.get_all()
        platos_with_ingredients = [plato for plato in all_platos if plato.receta]
        return [self._to_response_dto(plato) for plato in platos_with_ingredients]
    
    async def agregar_ingrediente_receta(
        self, 
        plato_id: UUID, 
        agregar_dto: AgregarIngredienteRecetaDTO
    ) -> PlatoResponseDTO:
        """Add ingredient to dish recipe.
        
        Args:
            plato_id: Unique identifier of the dish
            agregar_dto: Data with ingredient and quantity to add
            
        Returns:
            PlatoResponseDTO with updated dish data
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
            IngredienteNotFoundError: If ingredient doesn't exist
        """
        plato = await self._plato_repository.get_by_id(plato_id)
        if not plato:
            raise PlatoNotFoundError(f"Dish with ID {plato_id} not found")
        
        # Verify ingredient exists
        ingrediente = await self._ingrediente_repository.get_by_id(agregar_dto.ingrediente_id)
        if not ingrediente:
            raise IngredienteNotFoundError(f"Ingredient with ID {agregar_dto.ingrediente_id} not found")
        
        # Add ingredient to recipe
        plato.agregar_ingrediente(agregar_dto.ingrediente_id, agregar_dto.cantidad)
        
        # Save updated dish
        updated_plato = await self._plato_repository.save(plato)
        
        return self._to_response_dto(updated_plato)
    
    async def remover_ingrediente_receta(self, plato_id: UUID, ingrediente_id: UUID) -> PlatoResponseDTO:
        """Remove ingredient from dish recipe.
        
        Args:
            plato_id: Unique identifier of the dish
            ingrediente_id: Unique identifier of the ingredient to remove
            
        Returns:
            PlatoResponseDTO with updated dish data
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
        """
        plato = await self._plato_repository.get_by_id(plato_id)
        if not plato:
            raise PlatoNotFoundError(f"Dish with ID {plato_id} not found")
        
        # Remove ingredient from recipe
        plato.remover_ingrediente(ingrediente_id)
        
        # Save updated dish
        updated_plato = await self._plato_repository.save(plato)
        
        return self._to_response_dto(updated_plato)
    
    async def actualizar_ingrediente_receta(
        self, 
        plato_id: UUID, 
        ingrediente_id: UUID,
        actualizar_dto: ActualizarIngredienteRecetaDTO
    ) -> PlatoResponseDTO:
        """Update ingredient quantity in dish recipe.
        
        Args:
            plato_id: Unique identifier of the dish
            ingrediente_id: Unique identifier of the ingredient
            actualizar_dto: Data with new quantity
            
        Returns:
            PlatoResponseDTO with updated dish data
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
        """
        plato = await self._plato_repository.get_by_id(plato_id)
        if not plato:
            raise PlatoNotFoundError(f"Dish with ID {plato_id} not found")
        
        # Update ingredient quantity
        plato.actualizar_cantidad_ingrediente(ingrediente_id, actualizar_dto.nueva_cantidad)
        
        # Save updated dish
        updated_plato = await self._plato_repository.save(plato)
        
        return self._to_response_dto(updated_plato)
    
    async def verificar_disponibilidad_ingredientes(self, plato_id: UUID) -> bool:
        """Check if all ingredients for a dish are available.
        
        Args:
            plato_id: Unique identifier of the dish
            
        Returns:
            True if all ingredients are available, False otherwise
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
        """
        plato = await self._plato_repository.get_by_id(plato_id)
        if not plato:
            raise PlatoNotFoundError(f"Dish with ID {plato_id} not found")
        
        # Get all required ingredients
        ingredientes_necesarios = plato.obtener_ingredientes_necesarios()
        if not ingredientes_necesarios:
            return True  # No ingredients needed
        
        # Check availability of each ingredient
        ingredientes_disponibles = {}
        for ingrediente_id in ingredientes_necesarios.keys():
            ingrediente = await self._ingrediente_repository.get_by_id(ingrediente_id)
            if ingrediente:
                ingredientes_disponibles[ingrediente_id] = ingrediente
        
        return plato.verificar_disponibilidad_ingredientes(ingredientes_disponibles)
    
    async def calcular_costo_ingredientes(self, plato_id: UUID) -> float:
        """Calculate total cost of ingredients for a dish.
        
        Args:
            plato_id: Unique identifier of the dish
            
        Returns:
            Total cost of ingredients
            
        Raises:
            PlatoNotFoundError: If dish with given ID doesn't exist
            IngredienteNotFoundError: If any required ingredient is not found
        """
        plato = await self._plato_repository.get_by_id(plato_id)
        if not plato:
            raise PlatoNotFoundError(f"Dish with ID {plato_id} not found")
        
        # Get all required ingredients
        ingredientes_necesarios = plato.obtener_ingredientes_necesarios()
        if not ingredientes_necesarios:
            return 0.0  # No ingredients, no cost
        
        # Get ingredient entities
        ingredientes_disponibles = {}
        for ingrediente_id in ingredientes_necesarios.keys():
            ingrediente = await self._ingrediente_repository.get_by_id(ingrediente_id)
            if not ingrediente:
                raise IngredienteNotFoundError(f"Ingredient with ID {ingrediente_id} not found")
            ingredientes_disponibles[ingrediente_id] = ingrediente
        
        # Calculate cost
        costo_precio = plato.calcular_costo_ingredientes(ingredientes_disponibles)
        return float(costo_precio)
    
    async def get_platos_by_difficulty(self, dificultad: str) -> List[PlatoResponseDTO]:
        """Get dishes by difficulty level.
        
        Args:
            dificultad: Difficulty level ("facil", "medio", "dificil")
            
        Returns:
            List of PlatoResponseDTO with dishes of the specified difficulty
        """
        if dificultad not in ["facil", "medio", "dificil"]:
            raise ValueError("Difficulty must be 'facil', 'medio', or 'dificil'")
        
        platos = await self._plato_repository.get_by_difficulty(dificultad)
        return [self._to_response_dto(plato) for plato in platos]
    
    async def get_platos_by_chef(self, chef: str) -> List[PlatoResponseDTO]:
        """Get dishes by recommended chef.
        
        Args:
            chef: Chef name
            
        Returns:
            List of PlatoResponseDTO recommended by the specified chef
        """
        platos = await self._plato_repository.get_by_chef(chef)
        return [self._to_response_dto(plato) for plato in platos]
    
    async def delete_plato(self, plato_id: UUID) -> bool:
        """Delete a dish.
        
        Args:
            plato_id: Unique identifier of the dish to delete
            
        Returns:
            True if dish was deleted, False if not found
        """
        return await self._plato_repository.delete(plato_id)
    
    async def get_all_platos(self) -> List[PlatoResponseDTO]:
        """Get all dishes regardless of availability.
        
        Returns:
            List of PlatoResponseDTO with all dishes
        """
        platos = await self._plato_repository.get_all()
        return [self._to_response_dto(plato) for plato in platos]
    
    def _to_response_dto(self, plato: Plato) -> PlatoResponseDTO:
        """Convert Plato domain entity to response DTO.
        
        Args:
            plato: Plato domain entity
            
        Returns:
            PlatoResponseDTO with dish data
        """
        from app.application.dto.item_dto import InformacionNutricionalDTO
        
        nutritional_dto = InformacionNutricionalDTO(
            calorias=plato.informacion_nutricional.calorias,
            proteinas=plato.informacion_nutricional.proteinas,
            azucares=plato.informacion_nutricional.azucares,
            grasas=plato.informacion_nutricional.grasas,
            carbohidratos=plato.informacion_nutricional.carbohidratos,
            fibra=plato.informacion_nutricional.fibra,
            sodio=plato.informacion_nutricional.sodio
        )
        
        return PlatoResponseDTO(
            id=plato.id,
            nombre=plato.nombre,
            descripcion=plato.descripcion,
            precio=plato.precio.value,
            informacion_nutricional=nutritional_dto,
            tiempo_preparacion=plato.tiempo_preparacion,
            stock_actual=plato.stock_actual,
            stock_minimo=plato.stock_minimo,
            etiquetas=plato.etiquetas,
            activo=plato.activo,
            tipo_plato=plato.tipo_plato,
            receta=plato.receta,
            instrucciones=plato.instrucciones,
            porciones=plato.porciones,
            dificultad=plato.dificultad,
            chef_recomendado=plato.chef_recomendado
        )