from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from app.models.menu_y_carta.domain import Item, Plato, Bebida, Ingrediente
from app.models.menu_y_carta.enums import EtiquetaPlato, TipoAlergeno

class IMenuRepository(ABC):
    """Interfaz abstracta para repositorio de menú"""
    
    @abstractmethod
    def obtener_todos_los_items(self) -> Dict[int, Item]:
        """Obtiene todos los items del menú"""
        pass
    
    @abstractmethod
    def obtener_item_por_id(self, item_id: int) -> Optional[Item]:
        """Obtiene un item específico por ID"""
        pass
    
    @abstractmethod
    def obtener_platos(self) -> List[Plato]:
        """Obtiene todos los platos"""
        pass
    
    @abstractmethod
    def obtener_platos_por_tipo(self, tipo: EtiquetaPlato) -> List[Plato]:
        """Obtiene platos filtrados por tipo"""
        pass
    
    @abstractmethod
    def obtener_bebidas(self) -> List[Bebida]:
        """Obtiene todas las bebidas"""
        pass
    
    @abstractmethod
    def obtener_bebidas_sin_alcohol(self) -> List[Bebida]:
        """Obtiene bebidas sin alcohol"""
        pass
    
    @abstractmethod
    def obtener_bebidas_con_alcohol(self) -> List[Bebida]:
        """Obtiene bebidas con alcohol"""
        pass
    
    @abstractmethod
    def buscar_items_por_nombre(self, nombre: str) -> List[Item]:
        """Busca items por nombre"""
        pass
    
    @abstractmethod
    def filtrar_por_categoria(self, categoria: str) -> List[Item]:
        """Filtra items por categoría"""
        pass
    
    @abstractmethod
    def filtrar_por_alergenos(self, alergenos: List[TipoAlergeno]) -> List[Item]:
        """Filtra items que contengan los alérgenos especificados"""
        pass
    
    @abstractmethod
    def filtrar_sin_alergenos(self, alergenos: List[TipoAlergeno]) -> List[Item]:
        """Filtra items que NO contengan los alérgenos especificados"""
        pass
    
    @abstractmethod
    def obtener_items_disponibles(self) -> List[Item]:
        """Obtiene solo items que están disponibles y tienen stock"""
        pass
    
    @abstractmethod
    def obtener_ingredientes(self) -> List[Ingrediente]:
        """Obtiene todos los ingredientes"""
        pass
    
    @abstractmethod
    def obtener_ingrediente_por_id(self, ingrediente_id: int) -> Optional[Ingrediente]:
        """Obtiene un ingrediente por ID"""
        pass
    
    @abstractmethod
    def buscar_ingredientes_por_nombre(self, nombre: str) -> List[Ingrediente]:
        """Busca ingredientes por nombre"""
        pass
    
    @abstractmethod
    def obtener_items_por_ingrediente(self, ingrediente_id: int) -> List[Item]:
        """Obtiene items que contengan un ingrediente específico"""
        pass
    
    @abstractmethod
    def verificar_disponibilidad_item(self, item_id: int, cantidad: int = 1) -> Tuple[bool, str]:
        """Verifica si un item está disponible en la cantidad solicitada"""
        pass

