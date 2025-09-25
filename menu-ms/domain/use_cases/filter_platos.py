"""
Caso de uso para filtrar platos por categoría y disponibilidad.
"""

from typing import List
from domain.entities import Plato
from domain.entities.enums import EtiquetaPlato
from domain.repositories import PlatoRepository


class FilterPlatosUseCase:
    """
    Caso de uso para filtrar platos por categoría y disponibilidad.
    """
    
    def __init__(self, plato_repository: PlatoRepository):
        """
        Inicializa el caso de uso con el repositorio de platos.
        
        Args:
            plato_repository: Repositorio de platos
        """
        self.plato_repository = plato_repository
    
    def execute(self, categoria: EtiquetaPlato = None, disponible: bool = None) -> List[Plato]:
        """
        Ejecuta el filtrado de platos según los criterios especificados.
        
        Args:
            categoria: Categoría de plato (ENTRADA, FONDO, POSTRE) opcional
            disponible: Estado de disponibilidad opcional
            
        Returns:
            List[Plato]: Lista de platos que cumplen con los criterios
        """
        # Obtener todos los platos
        if categoria is None and disponible is None:
            return self.plato_repository.get_all()
        
        # Filtrar por categoría
        if categoria is not None and disponible is None:
            return self.plato_repository.get_by_tipo(categoria)
        
        # Implementar la lógica combinada de filtrado
        platos = self.plato_repository.filter_by_categoria_disponibilidad(categoria, disponible)
        return platos
