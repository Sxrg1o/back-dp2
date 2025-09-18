"""
Caso de uso para obtener un ingrediente.
"""

from typing import Optional
from ..entities import Ingrediente
from ..repositories import IngredienteRepository


class GetIngredienteUseCase:
    """
    Caso de uso para obtener un ingrediente por ID.
    """
    
    def __init__(self, ingrediente_repository: IngredienteRepository):
        """
        Inicializa el caso de uso con el repositorio de ingredientes.
        
        Args:
            ingrediente_repository: Repositorio de ingredientes
        """
        self.ingrediente_repository = ingrediente_repository
    
    def execute(self, ingrediente_id: int) -> Optional[Ingrediente]:
        """
        Ejecuta la obtención de un ingrediente por ID.
        
        Args:
            ingrediente_id: ID del ingrediente a obtener
            
        Returns:
            Optional[Ingrediente]: Ingrediente encontrado o None si no existe
        """
        if ingrediente_id <= 0:
            raise ValueError("El ID del ingrediente debe ser mayor a 0")
        
        return self.ingrediente_repository.get_by_id(ingrediente_id)
