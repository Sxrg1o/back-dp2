"""
Caso de uso para eliminar un ingrediente.
"""

from domain.repositories import IngredienteRepository


class DeleteIngredienteUseCase:
    """
    Caso de uso para eliminar un ingrediente.
    """
    
    def __init__(self, ingrediente_repository: IngredienteRepository):
        """
        Inicializa el caso de uso con el repositorio de ingredientes.
        
        Args:
            ingrediente_repository: Repositorio de ingredientes
        """
        self.ingrediente_repository = ingrediente_repository
    
    def execute(self, ingrediente_id: int) -> bool:
        """
        Ejecuta la eliminación de un ingrediente.
        
        Args:
            ingrediente_id: ID del ingrediente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
            
        Raises:
            ValueError: Si el ID no es válido
        """
        if ingrediente_id <= 0:
            raise ValueError("El ID del ingrediente debe ser mayor a 0")
        
        # Verificar que el ingrediente existe
        existing_ingrediente = self.ingrediente_repository.get_by_id(ingrediente_id)
        if existing_ingrediente is None:
            raise ValueError(f"No se encontró un ingrediente con ID {ingrediente_id}")
        
        return self.ingrediente_repository.delete(ingrediente_id)
