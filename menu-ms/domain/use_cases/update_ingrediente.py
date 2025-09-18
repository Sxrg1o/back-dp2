"""
Caso de uso para actualizar un ingrediente.
"""

from decimal import Decimal
from domain.entities import Ingrediente
from domain.repositories import IngredienteRepository


class UpdateIngredienteUseCase:
    """
    Caso de uso para actualizar un ingrediente.
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
        Ejecuta la actualización de un ingrediente.
        
        Args:
            ingrediente: Ingrediente a actualizar
            
        Returns:
            Ingrediente: Ingrediente actualizado
            
        Raises:
            ValueError: Si el ingrediente no es válido
        """
        if ingrediente.id is None or ingrediente.id <= 0:
            raise ValueError("El ID del ingrediente es obligatorio y debe ser mayor a 0")
        
        # Verificar que el ingrediente existe
        existing_ingrediente = self.ingrediente_repository.get_by_id(ingrediente.id)
        if existing_ingrediente is None:
            raise ValueError(f"No se encontró un ingrediente con ID {ingrediente.id}")
        
        # Validaciones de negocio
        if not ingrediente.nombre or ingrediente.nombre.strip() == "":
            raise ValueError("El nombre del ingrediente es obligatorio")
        
        if ingrediente.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        if ingrediente.peso <= 0:
            raise ValueError("El peso del ingrediente debe ser mayor a 0")
        
        # Actualizar el ingrediente
        return self.ingrediente_repository.update(ingrediente)
    
    def execute_stock_update(self, ingrediente_id: int, new_stock: Decimal) -> bool:
        """
        Ejecuta la actualización del stock de un ingrediente.
        
        Args:
            ingrediente_id: ID del ingrediente
            new_stock: Nuevo stock
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if ingrediente_id <= 0:
            raise ValueError("El ID del ingrediente debe ser mayor a 0")
        
        if new_stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        # Verificar que el ingrediente existe
        existing_ingrediente = self.ingrediente_repository.get_by_id(ingrediente_id)
        if existing_ingrediente is None:
            raise ValueError(f"No se encontró un ingrediente con ID {ingrediente_id}")
        
        return self.ingrediente_repository.update_stock(ingrediente_id, new_stock)
    
    def execute_reduce_stock(self, ingrediente_id: int, cantidad: Decimal) -> bool:
        """
        Ejecuta la reducción del stock de un ingrediente.
        
        Args:
            ingrediente_id: ID del ingrediente
            cantidad: Cantidad a reducir
            
        Returns:
            bool: True si se pudo reducir el stock, False en caso contrario
        """
        if ingrediente_id <= 0:
            raise ValueError("El ID del ingrediente debe ser mayor a 0")
        
        if cantidad <= 0:
            raise ValueError("La cantidad a reducir debe ser mayor a 0")
        
        # Verificar que el ingrediente existe
        existing_ingrediente = self.ingrediente_repository.get_by_id(ingrediente_id)
        if existing_ingrediente is None:
            raise ValueError(f"No se encontró un ingrediente con ID {ingrediente_id}")
        
        return self.ingrediente_repository.reduce_stock(ingrediente_id, cantidad)
