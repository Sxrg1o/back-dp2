"""
Servicio de aplicación para gestión de ítems del menú.
"""

from typing import List, Optional, Union
from decimal import Decimal
from domain.entities import Item, Plato, Bebida
from domain.entities.enums import EtiquetaItem, EtiquetaPlato
from domain.repositories import ItemRepository, PlatoRepository, BebidaRepository
from domain.use_cases import (
    CreateItemUseCase,
    GetItemUseCase,
    GetAllItemsUseCase,
    UpdateItemUseCase,
    DeleteItemUseCase
)


class ItemService:
    """
    Servicio de aplicación para gestión de ítems del menú.
    """
    
    def __init__(
        self,
        item_repository: ItemRepository,
        plato_repository: PlatoRepository,
        bebida_repository: BebidaRepository
    ):
        """
        Inicializa el servicio con los repositorios necesarios.
        
        Args:
            item_repository: Repositorio de ítems
            plato_repository: Repositorio de platos
            bebida_repository: Repositorio de bebidas
        """
        self.item_repository = item_repository
        self.plato_repository = plato_repository
        self.bebida_repository = bebida_repository
        
        # Inicializar casos de uso
        self.create_item_use_case = CreateItemUseCase(item_repository)
        self.get_item_use_case = GetItemUseCase(item_repository)
        self.get_all_items_use_case = GetAllItemsUseCase(item_repository)
        self.update_item_use_case = UpdateItemUseCase(item_repository)
        self.delete_item_use_case = DeleteItemUseCase(item_repository)
    
    def create_item(self, item: Union[Plato, Bebida]) -> Union[Plato, Bebida]:
        """
        Crea un nuevo ítem del menú.
        
        Args:
            item: Ítem a crear (Plato o Bebida)
            
        Returns:
            Union[Plato, Bebida]: Ítem creado con ID asignado
        """
        return self.create_item_use_case.execute(item)
    
    def get_item(self, item_id: int) -> Optional[Item]:
        """
        Obtiene un ítem por su ID.
        
        Args:
            item_id: ID del ítem
            
        Returns:
            Optional[Item]: Ítem encontrado o None si no existe
        """
        return self.get_item_use_case.execute(item_id)
    
    def get_all_items(self, only_available: bool = False) -> List[Item]:
        """
        Obtiene todos los ítems del menú.
        
        Args:
            only_available: Si True, solo retorna ítems disponibles
            
        Returns:
            List[Item]: Lista de ítems
        """
        return self.get_all_items_use_case.execute(only_available)
    
    def get_all_items_with_ingredientes(self) -> List[dict]:
        """
        Obtiene todos los ítems del menú con sus ingredientes asociados.
        
        Returns:
            List[dict]: Lista de ítems con ingredientes
        """
        return self.item_repository.get_all_with_ingredientes()
    
    def get_items_by_price_range(
        self, 
        min_price: Decimal, 
        max_price: Decimal
    ) -> List[Item]:
        """
        Obtiene ítems por rango de precios.
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo
            
        Returns:
            List[Item]: Lista de ítems en el rango de precios
        """
        return self.get_all_items_use_case.execute_by_price_range(min_price, max_price)
    
    def get_items_by_etiqueta(self, etiqueta: EtiquetaItem) -> List[Item]:
        """
        Obtiene ítems por etiqueta.
        
        Args:
            etiqueta: Etiqueta a buscar
            
        Returns:
            List[Item]: Lista de ítems con la etiqueta
        """
        return self.get_all_items_use_case.execute_by_etiqueta(etiqueta)
    
    def search_items(self, search_term: str) -> List[Item]:
        """
        Busca ítems por nombre o descripción.
        
        Args:
            search_term: Término de búsqueda
            
        Returns:
            List[Item]: Lista de ítems que coinciden con la búsqueda
        """
        return self.get_all_items_use_case.execute_search(search_term)
    
    def update_item(self, item: Union[Plato, Bebida]) -> Union[Plato, Bebida]:
        """
        Actualiza un ítem existente.
        
        Args:
            item: Ítem a actualizar
            
        Returns:
            Union[Plato, Bebida]: Ítem actualizado
        """
        return self.update_item_use_case.execute(item)
    
    def update_item_stock(self, item_id: int, new_stock: int) -> bool:
        """
        Actualiza el stock de un ítem.
        
        Args:
            item_id: ID del ítem
            new_stock: Nuevo stock
            
        Returns:
            bool: True si se actualizó correctamente
        """
        return self.update_item_use_case.execute_stock_update(item_id, new_stock)
    
    def delete_item(self, item_id: int) -> bool:
        """
        Elimina un ítem del menú.
        
        Args:
            item_id: ID del ítem a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return self.delete_item_use_case.execute(item_id)
    
    # Métodos específicos para platos
    def get_platos_by_tipo(self, tipo: EtiquetaPlato) -> List[Plato]:
        """
        Obtiene platos por tipo.
        
        Args:
            tipo: Tipo de plato
            
        Returns:
            List[Plato]: Lista de platos del tipo especificado
        """
        return self.plato_repository.get_by_tipo(tipo)
    
    def get_entradas(self) -> List[Plato]:
        """
        Obtiene todos los platos de entrada.
        
        Returns:
            List[Plato]: Lista de platos de entrada
        """
        return self.plato_repository.get_entradas()
    
    def get_platos_principales(self) -> List[Plato]:
        """
        Obtiene todos los platos principales.
        
        Returns:
            List[Plato]: Lista de platos principales
        """
        return self.plato_repository.get_platos_principales()
    
    def get_postres(self) -> List[Plato]:
        """
        Obtiene todos los postres.
        
        Returns:
            List[Plato]: Lista de postres
        """
        return self.plato_repository.get_postres()
    
    # Métodos específicos para bebidas
    def get_bebidas_alcoholicas(self) -> List[Bebida]:
        """
        Obtiene todas las bebidas alcohólicas.
        
        Returns:
            List[Bebida]: Lista de bebidas alcohólicas
        """
        return self.bebida_repository.get_alcoholicas()
    
    def get_bebidas_no_alcoholicas(self) -> List[Bebida]:
        """
        Obtiene todas las bebidas no alcohólicas.
        
        Returns:
            List[Bebida]: Lista de bebidas no alcohólicas
        """
        return self.bebida_repository.get_no_alcoholicas()
    
    def get_bebidas_by_volume_range(
        self, 
        min_volume: Decimal, 
        max_volume: Decimal
    ) -> List[Bebida]:
        """
        Obtiene bebidas por rango de volumen.
        
        Args:
            min_volume: Volumen mínimo en litros
            max_volume: Volumen máximo en litros
            
        Returns:
            List[Bebida]: Lista de bebidas en el rango de volumen
        """
        return self.bebida_repository.get_by_volume_range(min_volume, max_volume)
