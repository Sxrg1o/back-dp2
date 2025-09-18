"""
Interfaz del repositorio de ítems del menú.
Define el contrato para la persistencia de ítems.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal
from domain.entities import Item, Plato, Bebida
from domain.entities.enums import EtiquetaItem, EtiquetaPlato


class ItemRepository(ABC):
    """
    Interfaz abstracta para el repositorio de ítems del menú.
    Define las operaciones de persistencia para ítems.
    """
    
    @abstractmethod
    def create(self, item: Item) -> Item:
        """
        Crea un nuevo ítem en el repositorio.
        
        Args:
            item: Ítem a crear
            
        Returns:
            Item: Ítem creado con ID asignado
        """
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[Item]:
        """
        Obtiene un ítem por su ID.
        
        Args:
            item_id: ID del ítem
            
        Returns:
            Optional[Item]: Ítem encontrado o None si no existe
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Item]:
        """
        Obtiene todos los ítems del repositorio.
        
        Returns:
            List[Item]: Lista de todos los ítems
        """
        pass
    
    @abstractmethod
    def get_available(self) -> List[Item]:
        """
        Obtiene todos los ítems disponibles en el menú.
        
        Returns:
            List[Item]: Lista de ítems disponibles
        """
        pass
    
    @abstractmethod
    def get_by_price_range(self, min_price: Decimal, max_price: Decimal) -> List[Item]:
        """
        Obtiene ítems dentro de un rango de precios.
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo
            
        Returns:
            List[Item]: Lista de ítems en el rango de precios
        """
        pass
    
    @abstractmethod
    def get_by_etiqueta(self, etiqueta: EtiquetaItem) -> List[Item]:
        """
        Obtiene ítems que tienen una etiqueta específica.
        
        Args:
            etiqueta: Etiqueta a buscar
            
        Returns:
            List[Item]: Lista de ítems con la etiqueta
        """
        pass
    
    @abstractmethod
    def search_by_name(self, name: str) -> List[Item]:
        """
        Busca ítems por nombre o descripción.
        
        Args:
            name: Término de búsqueda
            
        Returns:
            List[Item]: Lista de ítems que coinciden con la búsqueda
        """
        pass
    
    @abstractmethod
    def update(self, item: Item) -> Item:
        """
        Actualiza un ítem existente.
        
        Args:
            item: Ítem a actualizar
            
        Returns:
            Item: Ítem actualizado
        """
        pass
    
    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """
        Elimina un ítem por su ID.
        
        Args:
            item_id: ID del ítem a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def update_stock(self, item_id: int, new_stock: int) -> bool:
        """
        Actualiza el stock de un ítem.
        
        Args:
            item_id: ID del ítem
            new_stock: Nuevo stock
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        pass


class PlatoRepository(ABC):
    """
    Interfaz abstracta para el repositorio de platos.
    Define operaciones específicas para platos.
    """
    
    @abstractmethod
    def create(self, plato: Plato) -> Plato:
        """
        Crea un nuevo plato en el repositorio.
        
        Args:
            plato: Plato a crear
            
        Returns:
            Plato: Plato creado con ID asignado
        """
        pass
    
    @abstractmethod
    def get_by_tipo(self, tipo: EtiquetaPlato) -> List[Plato]:
        """
        Obtiene platos por tipo (ENTRADA, FONDO, POSTRE).
        
        Args:
            tipo: Tipo de plato
            
        Returns:
            List[Plato]: Lista de platos del tipo especificado
        """
        pass
    
    @abstractmethod
    def get_entradas(self) -> List[Plato]:
        """
        Obtiene todos los platos de entrada.
        
        Returns:
            List[Plato]: Lista de platos de entrada
        """
        pass
    
    @abstractmethod
    def get_platos_principales(self) -> List[Plato]:
        """
        Obtiene todos los platos principales.
        
        Returns:
            List[Plato]: Lista de platos principales
        """
        pass
    
    @abstractmethod
    def get_postres(self) -> List[Plato]:
        """
        Obtiene todos los postres.
        
        Returns:
            List[Plato]: Lista de postres
        """
        pass


class BebidaRepository(ABC):
    """
    Interfaz abstracta para el repositorio de bebidas.
    Define operaciones específicas para bebidas.
    """
    
    @abstractmethod
    def create(self, bebida: Bebida) -> Bebida:
        """
        Crea una nueva bebida en el repositorio.
        
        Args:
            bebida: Bebida a crear
            
        Returns:
            Bebida: Bebida creada con ID asignado
        """
        pass
    
    @abstractmethod
    def get_alcoholicas(self) -> List[Bebida]:
        """
        Obtiene todas las bebidas alcohólicas.
        
        Returns:
            List[Bebida]: Lista de bebidas alcohólicas
        """
        pass
    
    @abstractmethod
    def get_no_alcoholicas(self) -> List[Bebida]:
        """
        Obtiene todas las bebidas no alcohólicas.
        
        Returns:
            List[Bebida]: Lista de bebidas no alcohólicas
        """
        pass
    
    @abstractmethod
    def get_by_volume_range(self, min_volume: Decimal, max_volume: Decimal) -> List[Bebida]:
        """
        Obtiene bebidas dentro de un rango de volumen.
        
        Args:
            min_volume: Volumen mínimo en litros
            max_volume: Volumen máximo en litros
            
        Returns:
            List[Bebida]: Lista de bebidas en el rango de volumen
        """
        pass
