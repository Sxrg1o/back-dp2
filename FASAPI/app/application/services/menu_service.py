"""Menu application service for general menu management operations."""

from typing import Dict, List, Optional
from uuid import UUID

from app.domain.entities.item import Item
from app.domain.entities.ingrediente import Ingrediente
from app.domain.entities.plato import Plato
from app.domain.entities.bebida import Bebida
from app.domain.repositories.item_repository import ItemRepositoryPort
from app.domain.repositories.ingrediente_repository import IngredienteRepositoryPort
from app.domain.repositories.plato_repository import PlatoRepositoryPort
from app.domain.repositories.bebida_repository import BebidaRepositoryPort
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.domain.exceptions.menu_exceptions import (
    ItemNotFoundError,
    IngredienteNotFoundError,
    PlatoNotFoundError,
    BebidaNotFoundError
)
from app.application.dto.item_dto import ItemResponseDTO
from app.application.dto.ingrediente_dto import IngredienteResponseDTO
from app.application.dto.plato_dto import PlatoResponseDTO
from app.application.dto.bebida_dto import BebidaResponseDTO


class MenuApplicationService:
    """Application service for general menu management operations."""
    
    def __init__(
        self,
        item_repository: ItemRepositoryPort,
        ingrediente_repository: IngredienteRepositoryPort,
        plato_repository: PlatoRepositoryPort,
        bebida_repository: BebidaRepositoryPort
    ):
        """Initialize service with repository dependencies.
        
        Args:
            item_repository: Repository port for item data access
            ingrediente_repository: Repository port for ingredient data access
            plato_repository: Repository port for dish data access
            bebida_repository: Repository port for beverage data access
        """
        self._item_repository = item_repository
        self._ingrediente_repository = ingrediente_repository
        self._plato_repository = plato_repository
        self._bebida_repository = bebida_repository
    
    async def get_full_menu(self) -> Dict[str, List]:
        """Get complete menu with all available items.
        
        Returns:
            Dictionary with categorized menu items:
            - items: All available base items
            - ingredientes: All available ingredients
            - platos: All available dishes
            - bebidas: All available beverages
        """
        # Get all available items from each category
        items = await self._item_repository.get_available_items()
        ingredientes = await self._ingrediente_repository.get_available()
        platos = await self._plato_repository.get_available()
        bebidas = await self._bebida_repository.get_available()
        
        return {
            "items": [self._item_to_response_dto(item) for item in items],
            "ingredientes": [self._ingrediente_to_response_dto(ing) for ing in ingredientes],
            "platos": [self._plato_to_response_dto(plato) for plato in platos],
            "bebidas": [self._bebida_to_response_dto(bebida) for bebida in bebidas]
        }
    
    async def get_menu_by_categories(self) -> Dict[str, Dict[str, List]]:
        """Get menu organized by categories and subcategories.
        
        Returns:
            Dictionary with menu items organized by categories
        """
        # Get items by categories
        vegan_items = await self._item_repository.get_by_category(EtiquetaItem.VEGANO)
        gluten_free_items = await self._item_repository.get_by_category(EtiquetaItem.SIN_GLUTEN)
        spicy_items = await self._item_repository.get_by_category(EtiquetaItem.PICANTE)
        
        # Get ingredients by type
        vegetables = await self._ingrediente_repository.get_by_type(EtiquetaIngrediente.VERDURA)
        meats = await self._ingrediente_repository.get_by_type(EtiquetaIngrediente.CARNE)
        fruits = await self._ingrediente_repository.get_by_type(EtiquetaIngrediente.FRUTA)
        
        # Get dishes by type
        appetizers = await self._plato_repository.get_by_dish_type(EtiquetaPlato.ENTRADA)
        main_courses = await self._plato_repository.get_by_dish_type(EtiquetaPlato.FONDO)
        desserts = await self._plato_repository.get_by_dish_type(EtiquetaPlato.POSTRE)
        
        # Get beverages by type
        alcoholic_beverages = await self._bebida_repository.get_alcoholic()
        non_alcoholic_beverages = await self._bebida_repository.get_non_alcoholic()
        
        return {
            "dietary_preferences": {
                "vegan": [self._item_to_response_dto(item) for item in vegan_items],
                "gluten_free": [self._item_to_response_dto(item) for item in gluten_free_items],
                "spicy": [self._item_to_response_dto(item) for item in spicy_items]
            },
            "ingredients": {
                "vegetables": [self._ingrediente_to_response_dto(ing) for ing in vegetables],
                "meats": [self._ingrediente_to_response_dto(ing) for ing in meats],
                "fruits": [self._ingrediente_to_response_dto(ing) for ing in fruits]
            },
            "dishes": {
                "appetizers": [self._plato_to_response_dto(plato) for plato in appetizers],
                "main_courses": [self._plato_to_response_dto(plato) for plato in main_courses],
                "desserts": [self._plato_to_response_dto(plato) for plato in desserts]
            },
            "beverages": {
                "alcoholic": [self._bebida_to_response_dto(bebida) for bebida in alcoholic_beverages],
                "non_alcoholic": [self._bebida_to_response_dto(bebida) for bebida in non_alcoholic_beverages]
            }
        }
    
    async def search_menu_items(self, query: str) -> Dict[str, List]:
        """Search menu items by name across all categories.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary with search results from all categories
        """
        # Get all items and filter by name containing query
        all_items = await self._item_repository.get_all()
        all_ingredientes = await self._ingrediente_repository.get_all()
        all_platos = await self._plato_repository.get_all()
        all_bebidas = await self._bebida_repository.get_all()
        
        query_lower = query.lower()
        
        # Filter items by name
        matching_items = [item for item in all_items if query_lower in item.nombre.lower()]
        matching_ingredientes = [ing for ing in all_ingredientes if query_lower in ing.nombre.lower()]
        matching_platos = [plato for plato in all_platos if query_lower in plato.nombre.lower()]
        matching_bebidas = [bebida for bebida in all_bebidas if query_lower in bebida.nombre.lower()]
        
        return {
            "items": [self._item_to_response_dto(item) for item in matching_items],
            "ingredientes": [self._ingrediente_to_response_dto(ing) for ing in matching_ingredientes],
            "platos": [self._plato_to_response_dto(plato) for plato in matching_platos],
            "bebidas": [self._bebida_to_response_dto(bebida) for bebida in matching_bebidas]
        }
    
    async def get_menu_statistics(self) -> Dict[str, int]:
        """Get menu statistics.
        
        Returns:
            Dictionary with menu statistics
        """
        # Count items by category
        total_items = await self._item_repository.count_total()
        available_items = await self._item_repository.count_available()
        
        # Count ingredients by type
        vegetables_count = len(await self._ingrediente_repository.get_by_type(EtiquetaIngrediente.VERDURA))
        meats_count = len(await self._ingrediente_repository.get_by_type(EtiquetaIngrediente.CARNE))
        fruits_count = len(await self._ingrediente_repository.get_by_type(EtiquetaIngrediente.FRUTA))
        
        # Count dishes by type
        appetizers_count = len(await self._plato_repository.get_by_dish_type(EtiquetaPlato.ENTRADA))
        main_courses_count = len(await self._plato_repository.get_by_dish_type(EtiquetaPlato.FONDO))
        desserts_count = len(await self._plato_repository.get_by_dish_type(EtiquetaPlato.POSTRE))
        
        # Count beverages
        alcoholic_count = len(await self._bebida_repository.get_alcoholic())
        non_alcoholic_count = len(await self._bebida_repository.get_non_alcoholic())
        
        # Count low stock items
        low_stock_items = len(await self._item_repository.get_low_stock_items())
        low_stock_ingredientes = len(await self._ingrediente_repository.get_low_stock())
        low_stock_bebidas = len(await self._bebida_repository.get_low_stock())
        
        return {
            "total_items": total_items,
            "available_items": available_items,
            "ingredients": {
                "vegetables": vegetables_count,
                "meats": meats_count,
                "fruits": fruits_count,
                "total": vegetables_count + meats_count + fruits_count
            },
            "dishes": {
                "appetizers": appetizers_count,
                "main_courses": main_courses_count,
                "desserts": desserts_count,
                "total": appetizers_count + main_courses_count + desserts_count
            },
            "beverages": {
                "alcoholic": alcoholic_count,
                "non_alcoholic": non_alcoholic_count,
                "total": alcoholic_count + non_alcoholic_count
            },
            "low_stock": {
                "items": low_stock_items,
                "ingredientes": low_stock_ingredientes,
                "bebidas": low_stock_bebidas,
                "total": low_stock_items + low_stock_ingredientes + low_stock_bebidas
            }
        }
    
    async def get_nutritional_summary(self) -> Dict[str, float]:
        """Get nutritional summary of available menu items.
        
        Returns:
            Dictionary with aggregated nutritional information
        """
        # Get all available items
        items = await self._item_repository.get_available_items()
        ingredientes = await self._ingrediente_repository.get_available()
        platos = await self._plato_repository.get_available()
        bebidas = await self._bebida_repository.get_available()
        
        # Combine all items for nutritional analysis
        all_menu_items = items + ingredientes + platos + bebidas
        
        if not all_menu_items:
            return {
                "total_items": 0,
                "average_calories": 0.0,
                "average_proteins": 0.0,
                "average_sugars": 0.0,
                "high_protein_items": 0,
                "low_sugar_items": 0,
                "vegan_items": 0
            }
        
        # Calculate nutritional statistics
        total_calories = sum(item.informacion_nutricional.calorias for item in all_menu_items)
        total_proteins = sum(item.informacion_nutricional.proteinas for item in all_menu_items)
        total_sugars = sum(item.informacion_nutricional.azucares for item in all_menu_items)
        
        high_protein_count = sum(1 for item in all_menu_items if item.informacion_nutricional.es_alto_en_proteinas())
        low_sugar_count = sum(1 for item in all_menu_items if item.informacion_nutricional.es_bajo_en_azucar())
        vegan_count = sum(1 for item in all_menu_items if item.es_vegano())
        
        item_count = len(all_menu_items)
        
        return {
            "total_items": item_count,
            "average_calories": total_calories / item_count,
            "average_proteins": total_proteins / item_count,
            "average_sugars": total_sugars / item_count,
            "high_protein_items": high_protein_count,
            "low_sugar_items": low_sugar_count,
            "vegan_items": vegan_count
        }
    
    def _item_to_response_dto(self, item: Item) -> ItemResponseDTO:
        """Convert Item domain entity to response DTO."""
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
    
    def _ingrediente_to_response_dto(self, ingrediente: Ingrediente) -> IngredienteResponseDTO:
        """Convert Ingrediente domain entity to response DTO."""
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
    
    def _plato_to_response_dto(self, plato: Plato) -> PlatoResponseDTO:
        """Convert Plato domain entity to response DTO."""
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
    
    def _bebida_to_response_dto(self, bebida: Bebida) -> BebidaResponseDTO:
        """Convert Bebida domain entity to response DTO."""
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