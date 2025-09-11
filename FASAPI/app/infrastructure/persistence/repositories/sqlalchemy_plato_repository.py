"""SQLAlchemy adapter for PlatoRepositoryPort."""

from typing import Dict, List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, text
from sqlalchemy.orm import selectinload

from app.domain.entities.plato import Plato
from app.domain.entities.ingrediente import Ingrediente
from app.domain.repositories.plato_repository import PlatoRepositoryPort
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.infrastructure.persistence.models.plato_model import PlatoModel
from app.infrastructure.persistence.models.ingrediente_model import IngredienteModel
from app.infrastructure.persistence.mappers.plato_mapper import PlatoMapper
from app.infrastructure.persistence.mappers.ingrediente_mapper import IngredienteMapper
from app.infrastructure.persistence.repositories.base_repository import BaseSQLAlchemyRepository


class SqlAlchemyPlatoRepository(BaseSQLAlchemyRepository[Plato, PlatoModel], PlatoRepositoryPort):
    """SQLAlchemy adapter for Plato repository operations."""
    
    def __init__(self, session: AsyncSession):
        """Initialize SQLAlchemy Plato repository.
        
        Args:
            session: SQLAlchemy async session
        """
        super().__init__(session, PlatoModel, PlatoMapper())
        self.ingrediente_mapper = IngredienteMapper()
    
    async def get_by_id(self, plato_id: UUID) -> Optional[Plato]:
        """Get dish by ID."""
        model = await self._get_by_id(plato_id)
        return self.mapper.to_entity(model) if model else None
    
    async def get_by_dish_type(self, tipo_plato: EtiquetaPlato) -> List[Plato]:
        """Get dishes by type."""
        stmt = select(PlatoModel).where(
            PlatoModel.tipo_plato == tipo_plato.value
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_with_ingredients(self, plato_id: UUID) -> Optional[Tuple[Plato, Dict[UUID, Ingrediente]]]:
        """Get dish with its ingredients."""
        plato_model = await self._get_by_id(plato_id)
        if not plato_model:
            return None
        
        plato = self.mapper.to_entity(plato_model)
        
        # Get ingredients used in the recipe
        ingrediente_ids = list(plato.receta.keys())
        if not ingrediente_ids:
            return plato, {}
        
        stmt = select(IngredienteModel).where(
            IngredienteModel.id.in_(ingrediente_ids)
        )
        result = await self.session.execute(stmt)
        ingrediente_models = result.scalars().all()
        
        ingredientes = {
            model.id: self.ingrediente_mapper.to_entity(model)
            for model in ingrediente_models
        }
        
        return plato, ingredientes
    
    async def get_all(self) -> List[Plato]:
        """Get all dishes."""
        models = await self._get_all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_available(self) -> List[Plato]:
        """Get available dishes."""
        stmt = select(PlatoModel).where(
            and_(
                PlatoModel.activo == True,
                PlatoModel.stock_actual > 0
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_difficulty(self, dificultad: str) -> List[Plato]:
        """Get dishes by difficulty level."""
        stmt = select(PlatoModel).where(PlatoModel.dificultad == dificultad)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_chef(self, chef_recomendado: str) -> List[Plato]:
        """Get dishes by recommended chef."""
        stmt = select(PlatoModel).where(PlatoModel.chef_recomendado == chef_recomendado)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_preparation_time(self, max_minutes: int) -> List[Plato]:
        """Get dishes by maximum preparation time."""
        stmt = select(PlatoModel).where(PlatoModel.tiempo_preparacion <= max_minutes)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_portions(self, min_portions: int, max_portions: int) -> List[Plato]:
        """Get dishes by portion range."""
        stmt = select(PlatoModel).where(
            and_(
                PlatoModel.porciones >= min_portions,
                PlatoModel.porciones <= max_portions
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_using_ingredient(self, ingrediente_id: UUID) -> List[Plato]:
        """Get dishes that use a specific ingredient."""
        # Use JSON query to find dishes with the ingredient in their recipe
        stmt = select(PlatoModel).where(
            PlatoModel.receta.has_key(str(ingrediente_id))
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_name(self, name: str) -> Optional[Plato]:
        """Get dish by name."""
        stmt = select(PlatoModel).where(PlatoModel.nombre == name)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model) if model else None
    
    async def get_vegetarian(self) -> List[Plato]:
        """Get vegetarian dishes."""
        # This would require complex logic to check ingredients
        # For now, return dishes that don't have meat-based ingredients
        stmt = select(PlatoModel).where(
            PlatoModel.etiquetas.contains(['vegano'])
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_vegan(self) -> List[Plato]:
        """Get vegan dishes."""
        stmt = select(PlatoModel).where(
            PlatoModel.etiquetas.contains(['vegano'])
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_gluten_free(self) -> List[Plato]:
        """Get gluten-free dishes."""
        stmt = select(PlatoModel).where(
            PlatoModel.etiquetas.contains(['sin_gluten'])
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def save(self, plato: Plato) -> Plato:
        """Save dish (create or update)."""
        model = self.mapper.to_model(plato)
        saved_model = await self._save(model)
        return self.mapper.to_entity(saved_model)
    
    async def delete(self, plato_id: UUID) -> bool:
        """Delete dish by ID."""
        return await self._delete_by_id(plato_id)
    
    async def exists_by_id(self, plato_id: UUID) -> bool:
        """Check if dish exists by ID."""
        return await self._exists_by_id(plato_id)
    
    async def exists_by_name(self, name: str) -> bool:
        """Check if dish exists by name."""
        stmt = select(PlatoModel.id).where(PlatoModel.nombre == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def get_recipe_ingredients(self, plato_id: UUID) -> Dict[UUID, float]:
        """Get recipe ingredients and quantities for a dish."""
        stmt = select(PlatoModel.receta).where(PlatoModel.id == plato_id)
        result = await self.session.execute(stmt)
        receta_json = result.scalar_one_or_none()
        
        if not receta_json:
            return {}
        
        # Convert string keys back to UUIDs
        receta = {}
        for ingrediente_id_str, cantidad in receta_json.items():
            try:
                ingrediente_id = UUID(ingrediente_id_str)
                receta[ingrediente_id] = float(cantidad)
            except (ValueError, TypeError):
                continue
        
        return receta
    
    async def check_ingredient_availability(self, plato_id: UUID) -> bool:
        """Check if all ingredients for a dish are available."""
        plato_with_ingredients = await self.get_with_ingredients(plato_id)
        if not plato_with_ingredients:
            return False
        
        plato, ingredientes = plato_with_ingredients
        
        for ingrediente_id, cantidad_necesaria in plato.receta.items():
            if ingrediente_id not in ingredientes:
                return False
            
            ingrediente = ingredientes[ingrediente_id]
            if not ingrediente.is_disponible() or ingrediente.stock_actual < cantidad_necesaria:
                return False
        
        return True
    
    async def get_most_popular(self, limit: int = 10) -> List[Plato]:
        """Get most popular dishes."""
        # For now, return active dishes ordered by name
        # In a real implementation, this would use order/sales data
        stmt = select(PlatoModel).where(
            PlatoModel.activo == True
        ).order_by(PlatoModel.nombre).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]