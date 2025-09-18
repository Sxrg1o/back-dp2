"""
Servicio de aplicación para gestión de ingredientes.
"""

from typing import List, Optional
from decimal import Decimal
from domain.entities import Ingrediente
from domain.entities.enums import EtiquetaIngrediente
from domain.repositories import IngredienteRepository
from domain.use_cases import (
    CreateIngredienteUseCase,
    GetIngredienteUseCase,
    GetAllIngredientesUseCase,
    UpdateIngredienteUseCase,
    DeleteIngredienteUseCase
)


class IngredienteService:
    """
    Servicio de aplicación para gestión de ingredientes.
    """
    
    def __init__(self, ingrediente_repository: IngredienteRepository):
        """
        Inicializa el servicio con el repositorio de ingredientes.
        
        Args:
            ingrediente_repository: Repositorio de ingredientes
        """
        self.ingrediente_repository = ingrediente_repository
        
        # Inicializar casos de uso
        self.create_ingrediente_use_case = CreateIngredienteUseCase(ingrediente_repository)
        self.get_ingrediente_use_case = GetIngredienteUseCase(ingrediente_repository)
        self.get_all_ingredientes_use_case = GetAllIngredientesUseCase(ingrediente_repository)
        self.update_ingrediente_use_case = UpdateIngredienteUseCase(ingrediente_repository)
        self.delete_ingrediente_use_case = DeleteIngredienteUseCase(ingrediente_repository)
    
    def create_ingrediente(self, ingrediente: Ingrediente) -> Ingrediente:
        """
        Crea un nuevo ingrediente.
        
        Args:
            ingrediente: Ingrediente a crear
            
        Returns:
            Ingrediente: Ingrediente creado con ID asignado
        """
        return self.create_ingrediente_use_case.execute(ingrediente)
    
    def get_ingrediente(self, ingrediente_id: int) -> Optional[Ingrediente]:
        """
        Obtiene un ingrediente por su ID.
        
        Args:
            ingrediente_id: ID del ingrediente
            
        Returns:
            Optional[Ingrediente]: Ingrediente encontrado o None si no existe
        """
        return self.get_ingrediente_use_case.execute(ingrediente_id)
    
    def get_all_ingredientes(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes.
        
        Returns:
            List[Ingrediente]: Lista de ingredientes
        """
        return self.get_all_ingredientes_use_case.execute()
    
    def get_ingredientes_by_tipo(self, tipo: EtiquetaIngrediente) -> List[Ingrediente]:
        """
        Obtiene ingredientes por tipo.
        
        Args:
            tipo: Tipo de ingrediente
            
        Returns:
            List[Ingrediente]: Lista de ingredientes del tipo especificado
        """
        return self.get_all_ingredientes_use_case.execute_by_tipo(tipo)
    
    def get_verduras(self) -> List[Ingrediente]:
        """
        Obtiene todas las verduras.
        
        Returns:
            List[Ingrediente]: Lista de verduras
        """
        return self.get_all_ingredientes_use_case.execute_verduras()
    
    def get_carnes(self) -> List[Ingrediente]:
        """
        Obtiene todas las carnes.
        
        Returns:
            List[Ingrediente]: Lista de carnes
        """
        return self.get_all_ingredientes_use_case.execute_carnes()
    
    def get_frutas(self) -> List[Ingrediente]:
        """
        Obtiene todas las frutas.
        
        Returns:
            List[Ingrediente]: Lista de frutas
        """
        return self.get_all_ingredientes_use_case.execute_frutas()
    
    def search_ingredientes(self, search_term: str) -> List[Ingrediente]:
        """
        Busca ingredientes por nombre.
        
        Args:
            search_term: Término de búsqueda
            
        Returns:
            List[Ingrediente]: Lista de ingredientes que coinciden con la búsqueda
        """
        return self.get_all_ingredientes_use_case.execute_search(search_term)
    
    def get_ingredientes_low_stock(
        self, 
        threshold: Decimal = Decimal('10.0')
    ) -> List[Ingrediente]:
        """
        Obtiene ingredientes con stock bajo.
        
        Args:
            threshold: Umbral de stock bajo
            
        Returns:
            List[Ingrediente]: Lista de ingredientes con stock bajo
        """
        return self.get_all_ingredientes_use_case.execute_low_stock(threshold)
    
    def update_ingrediente(self, ingrediente: Ingrediente) -> Ingrediente:
        """
        Actualiza un ingrediente existente.
        
        Args:
            ingrediente: Ingrediente a actualizar
            
        Returns:
            Ingrediente: Ingrediente actualizado
        """
        return self.update_ingrediente_use_case.execute(ingrediente)
    
    def update_ingrediente_stock(self, ingrediente_id: int, new_stock: Decimal) -> bool:
        """
        Actualiza el stock de un ingrediente.
        
        Args:
            ingrediente_id: ID del ingrediente
            new_stock: Nuevo stock
            
        Returns:
            bool: True si se actualizó correctamente
        """
        return self.update_ingrediente_use_case.execute_stock_update(ingrediente_id, new_stock)
    
    def reduce_ingrediente_stock(self, ingrediente_id: int, cantidad: Decimal) -> bool:
        """
        Reduce el stock de un ingrediente.
        
        Args:
            ingrediente_id: ID del ingrediente
            cantidad: Cantidad a reducir
            
        Returns:
            bool: True si se pudo reducir el stock
        """
        return self.update_ingrediente_use_case.execute_reduce_stock(ingrediente_id, cantidad)
    
    def delete_ingrediente(self, ingrediente_id: int) -> bool:
        """
        Elimina un ingrediente.
        
        Args:
            ingrediente_id: ID del ingrediente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.delete_ingrediente_use_case.execute(ingrediente_id)
