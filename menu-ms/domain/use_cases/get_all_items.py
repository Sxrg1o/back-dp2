"""
Caso de uso para obtener todos los ítems del menú.
"""

from typing import List
from decimal import Decimal
from ..entities import Item
from ..entities.enums import EtiquetaItem
from ..repositories import ItemRepository


class GetAllItemsUseCase:
    """
    Caso de uso para obtener todos los ítems del menú.
    """
    
    def __init__(self, item_repository: ItemRepository):
        """
        Inicializa el caso de uso con el repositorio de ítems.
        
        Args:
            item_repository: Repositorio de ítems
        """
        self.item_repository = item_repository
    
    def execute(self, only_available: bool = False) -> List[Item]:
        """
        Ejecuta la obtención de todos los ítems.
        
        Args:
            only_available: Si True, solo retorna ítems disponibles
            
        Returns:
            List[Item]: Lista de ítems
        """
        if only_available:
            return self.item_repository.get_available()
        return self.item_repository.get_all()
    
    def execute_by_price_range(
        self, 
        min_price: Decimal, 
        max_price: Decimal
    ) -> List[Item]:
        """
        Ejecuta la obtención de ítems por rango de precios.
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo
            
        Returns:
            List[Item]: Lista de ítems en el rango de precios
        """
        if min_price < 0:
            raise ValueError("El precio mínimo no puede ser negativo")
        
        if max_price < 0:
            raise ValueError("El precio máximo no puede ser negativo")
        
        if min_price > max_price:
            raise ValueError("El precio mínimo no puede ser mayor al precio máximo")
        
        return self.item_repository.get_by_price_range(min_price, max_price)
    
    def execute_by_etiqueta(self, etiqueta: EtiquetaItem) -> List[Item]:
        """
        Ejecuta la obtención de ítems por etiqueta.
        
        Args:
            etiqueta: Etiqueta a buscar
            
        Returns:
            List[Item]: Lista de ítems con la etiqueta
        """
        return self.item_repository.get_by_etiqueta(etiqueta)
    
    def execute_search(self, search_term: str) -> List[Item]:
        """
        Ejecuta la búsqueda de ítems por nombre o descripción.
        
        Args:
            search_term: Término de búsqueda
            
        Returns:
            List[Item]: Lista de ítems que coinciden con la búsqueda
        """
        if not search_term or search_term.strip() == "":
            raise ValueError("El término de búsqueda no puede estar vacío")
        
        return self.item_repository.search_by_name(search_term.strip())
