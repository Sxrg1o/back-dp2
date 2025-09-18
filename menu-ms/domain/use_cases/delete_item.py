"""
Caso de uso para eliminar un ítem del menú.
"""

from ..repositories import ItemRepository


class DeleteItemUseCase:
    """
    Caso de uso para eliminar un ítem del menú.
    """
    
    def __init__(self, item_repository: ItemRepository):
        """
        Inicializa el caso de uso con el repositorio de ítems.
        
        Args:
            item_repository: Repositorio de ítems
        """
        self.item_repository = item_repository
    
    def execute(self, item_id: int) -> bool:
        """
        Ejecuta la eliminación de un ítem.
        
        Args:
            item_id: ID del ítem a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
            
        Raises:
            ValueError: Si el ID no es válido
        """
        if item_id <= 0:
            raise ValueError("El ID del ítem debe ser mayor a 0")
        
        # Verificar que el ítem existe
        existing_item = self.item_repository.get_by_id(item_id)
        if existing_item is None:
            raise ValueError(f"No se encontró un ítem con ID {item_id}")
        
        return self.item_repository.delete(item_id)
