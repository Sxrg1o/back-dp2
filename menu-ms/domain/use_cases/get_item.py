"""
Caso de uso para obtener un ítem del menú.
"""

from typing import Optional
from ..entities import Item
from ..repositories import ItemRepository


class GetItemUseCase:
    """
    Caso de uso para obtener un ítem del menú por ID.
    """
    
    def __init__(self, item_repository: ItemRepository):
        """
        Inicializa el caso de uso con el repositorio de ítems.
        
        Args:
            item_repository: Repositorio de ítems
        """
        self.item_repository = item_repository
    
    def execute(self, item_id: int) -> Optional[Item]:
        """
        Ejecuta la obtención de un ítem por ID.
        
        Args:
            item_id: ID del ítem a obtener
            
        Returns:
            Optional[Item]: Ítem encontrado o None si no existe
        """
        if item_id <= 0:
            raise ValueError("El ID del ítem debe ser mayor a 0")
        
        return self.item_repository.get_by_id(item_id)
