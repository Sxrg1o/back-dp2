"""
Caso de uso para obtener todos los ingredientes.
"""

from typing import List
from decimal import Decimal
from domain.entities import Ingrediente
from domain.entities.enums import EtiquetaIngrediente
from domain.repositories import IngredienteRepository


class GetAllIngredientesUseCase:
    """
    Caso de uso para obtener todos los ingredientes.
    """
    
    def __init__(self, ingrediente_repository: IngredienteRepository):
        """
        Inicializa el caso de uso con el repositorio de ingredientes.
        
        Args:
            ingrediente_repository: Repositorio de ingredientes
        """
        self.ingrediente_repository = ingrediente_repository
    
    def execute(self) -> List[Ingrediente]:
        """
        Ejecuta la obtención de todos los ingredientes.
        
        Returns:
            List[Ingrediente]: Lista de ingredientes
        """
        return self.ingrediente_repository.get_all()
    
    def execute_by_tipo(self, tipo: EtiquetaIngrediente) -> List[Ingrediente]:
        """
        Ejecuta la obtención de ingredientes por tipo.
        
        Args:
            tipo: Tipo de ingrediente
            
        Returns:
            List[Ingrediente]: Lista de ingredientes del tipo especificado
        """
        return self.ingrediente_repository.get_by_tipo(tipo)
    
    def execute_verduras(self) -> List[Ingrediente]:
        """
        Ejecuta la obtención de todas las verduras.
        
        Returns:
            List[Ingrediente]: Lista de verduras
        """
        return self.ingrediente_repository.get_verduras()
    
    def execute_carnes(self) -> List[Ingrediente]:
        """
        Ejecuta la obtención de todas las carnes.
        
        Returns:
            List[Ingrediente]: Lista de carnes
        """
        return self.ingrediente_repository.get_carnes()
    
    def execute_frutas(self) -> List[Ingrediente]:
        """
        Ejecuta la obtención de todas las frutas.
        
        Returns:
            List[Ingrediente]: Lista de frutas
        """
        return self.ingrediente_repository.get_frutas()
    
    def execute_search(self, search_term: str) -> List[Ingrediente]:
        """
        Ejecuta la búsqueda de ingredientes por nombre.
        
        Args:
            search_term: Término de búsqueda
            
        Returns:
            List[Ingrediente]: Lista de ingredientes que coinciden con la búsqueda
        """
        if not search_term or search_term.strip() == "":
            raise ValueError("El término de búsqueda no puede estar vacío")
        
        return self.ingrediente_repository.search_by_name(search_term.strip())
    
    def execute_low_stock(self, threshold: Decimal = Decimal('10.0')) -> List[Ingrediente]:
        """
        Ejecuta la obtención de ingredientes con stock bajo.
        
        Args:
            threshold: Umbral de stock bajo
            
        Returns:
            List[Ingrediente]: Lista de ingredientes con stock bajo
        """
        if threshold < 0:
            raise ValueError("El umbral de stock no puede ser negativo")
        
        return self.ingrediente_repository.get_low_stock(threshold)
