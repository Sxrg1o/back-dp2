"""
Caso de uso para crear un ingrediente.
"""

from decimal import Decimal
from ..entities import Ingrediente
from ..repositories import IngredienteRepository


class CreateIngredienteUseCase:
    """
    Caso de uso para crear un ingrediente.
    """
    
    def __init__(self, ingrediente_repository: IngredienteRepository):
        """
        Inicializa el caso de uso con el repositorio de ingredientes.
        
        Args:
            ingrediente_repository: Repositorio de ingredientes
        """
        self.ingrediente_repository = ingrediente_repository
    
    def execute(self, ingrediente: Ingrediente) -> Ingrediente:
        """
        Ejecuta la creación de un ingrediente.
        
        Args:
            ingrediente: Ingrediente a crear
            
        Returns:
            Ingrediente: Ingrediente creado con ID asignado
            
        Raises:
            ValueError: Si el ingrediente no es válido
        """
        # Validaciones de negocio
        if not ingrediente.nombre or ingrediente.nombre.strip() == "":
            raise ValueError("El nombre del ingrediente es obligatorio")
        
        if ingrediente.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        if ingrediente.peso <= 0:
            raise ValueError("El peso del ingrediente debe ser mayor a 0")
        
        # Crear el ingrediente
        return self.ingrediente_repository.create(ingrediente)
