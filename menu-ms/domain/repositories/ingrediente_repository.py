"""
Interfaz del repositorio de ingredientes.
Define el contrato para la persistencia de ingredientes.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal
from domain.entities import Ingrediente
from domain.entities.enums import EtiquetaIngrediente


class IngredienteRepository(ABC):
    """
    Interfaz abstracta para el repositorio de ingredientes.
    Define las operaciones de persistencia para ingredientes.
    """
    
    @abstractmethod
    def create(self, ingrediente: Ingrediente) -> Ingrediente:
        """
        Crea un nuevo ingrediente en el repositorio.
        
        Args:
            ingrediente: Ingrediente a crear
            
        Returns:
            Ingrediente: Ingrediente creado con ID asignado
        """
        pass
    
    @abstractmethod
    def get_by_id(self, ingrediente_id: int) -> Optional[Ingrediente]:
        """
        Obtiene un ingrediente por su ID.
        
        Args:
            ingrediente_id: ID del ingrediente
            
        Returns:
            Optional[Ingrediente]: Ingrediente encontrado o None si no existe
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes del repositorio.
        
        Returns:
            List[Ingrediente]: Lista de todos los ingredientes
        """
        pass
    
    @abstractmethod
    def get_by_tipo(self, tipo: EtiquetaIngrediente) -> List[Ingrediente]:
        """
        Obtiene ingredientes por tipo.
        
        Args:
            tipo: Tipo de ingrediente
            
        Returns:
            List[Ingrediente]: Lista de ingredientes del tipo especificado
        """
        pass
    
    @abstractmethod
    def get_verduras(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes de tipo verdura.
        
        Returns:
            List[Ingrediente]: Lista de verduras
        """
        pass
    
    @abstractmethod
    def get_carnes(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes de tipo carne.
        
        Returns:
            List[Ingrediente]: Lista de carnes
        """
        pass
    
    @abstractmethod
    def get_frutas(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes de tipo fruta.
        
        Returns:
            List[Ingrediente]: Lista de frutas
        """
        pass
    
    @abstractmethod
    def search_by_name(self, name: str) -> List[Ingrediente]:
        """
        Busca ingredientes por nombre.
        
        Args:
            name: Término de búsqueda
            
        Returns:
            List[Ingrediente]: Lista de ingredientes que coinciden con la búsqueda
        """
        pass
    
    @abstractmethod
    def get_low_stock(self, threshold: Decimal = Decimal('10.0')) -> List[Ingrediente]:
        """
        Obtiene ingredientes con stock bajo.
        
        Args:
            threshold: Umbral de stock bajo
            
        Returns:
            List[Ingrediente]: Lista de ingredientes con stock bajo
        """
        pass
    
    @abstractmethod
    def update(self, ingrediente: Ingrediente) -> Ingrediente:
        """
        Actualiza un ingrediente existente.
        
        Args:
            ingrediente: Ingrediente a actualizar
            
        Returns:
            Ingrediente: Ingrediente actualizado
        """
        pass
    
    @abstractmethod
    def delete(self, ingrediente_id: int) -> bool:
        """
        Elimina un ingrediente por su ID.
        
        Args:
            ingrediente_id: ID del ingrediente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def update_stock(self, ingrediente_id: int, new_stock: Decimal) -> bool:
        """
        Actualiza el stock de un ingrediente.
        
        Args:
            ingrediente_id: ID del ingrediente
            new_stock: Nuevo stock
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def reduce_stock(self, ingrediente_id: int, cantidad: Decimal) -> bool:
        """
        Reduce el stock de un ingrediente.
        
        Args:
            ingrediente_id: ID del ingrediente
            cantidad: Cantidad a reducir
            
        Returns:
            bool: True si se pudo reducir el stock, False en caso contrario
        """
        pass
