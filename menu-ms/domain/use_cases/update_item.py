"""
Caso de uso para actualizar un ítem del menú.
"""

from typing import Union, Optional
from decimal import Decimal
from ..entities import Item, Plato, Bebida
from ..repositories import ItemRepository


class UpdateItemUseCase:
    """
    Caso de uso para actualizar un ítem del menú.
    """
    
    def __init__(self, item_repository: ItemRepository):
        """
        Inicializa el caso de uso con el repositorio de ítems.
        
        Args:
            item_repository: Repositorio de ítems
        """
        self.item_repository = item_repository
    
    def execute(self, item: Union[Plato, Bebida]) -> Union[Plato, Bebida]:
        """
        Ejecuta la actualización de un ítem.
        
        Args:
            item: Ítem a actualizar (Plato o Bebida)
            
        Returns:
            Union[Plato, Bebida]: Ítem actualizado
            
        Raises:
            ValueError: Si el ítem no es válido
        """
        if item.id is None or item.id <= 0:
            raise ValueError("El ID del ítem es obligatorio y debe ser mayor a 0")
        
        # Verificar que el ítem existe
        existing_item = self.item_repository.get_by_id(item.id)
        if existing_item is None:
            raise ValueError(f"No se encontró un ítem con ID {item.id}")
        
        # Validaciones de negocio
        if not item.descripcion or item.descripcion.strip() == "":
            raise ValueError("La descripción del ítem es obligatoria")
        
        if item.precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        
        if item.tiempo_preparacion < 0:
            raise ValueError("El tiempo de preparación no puede ser negativo")
        
        if item.unidades_disponibles < 0:
            raise ValueError("Las unidades disponibles no pueden ser negativas")
        
        if item.kcal < 0:
            raise ValueError("Las calorías no pueden ser negativas")
        
        if item.calorias < 0:
            raise ValueError("Las calorías no pueden ser negativas")
        
        if item.proteinas < 0:
            raise ValueError("Las proteínas no pueden ser negativas")
        
        if item.azucares < 0:
            raise ValueError("Los azúcares no pueden ser negativos")
        
        # Validaciones específicas para Plato
        if isinstance(item, Plato):
            if item.peso <= 0:
                raise ValueError("El peso del plato debe ser mayor a 0")
        
        # Validaciones específicas para Bebida
        if isinstance(item, Bebida):
            if item.litros <= 0:
                raise ValueError("Los litros de la bebida deben ser mayores a 0")
        
        # Actualizar el ítem
        return self.item_repository.update(item)
    
    def execute_stock_update(self, item_id: int, new_stock: int) -> bool:
        """
        Ejecuta la actualización del stock de un ítem.
        
        Args:
            item_id: ID del ítem
            new_stock: Nuevo stock
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        if item_id <= 0:
            raise ValueError("El ID del ítem debe ser mayor a 0")
        
        if new_stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        # Verificar que el ítem existe
        existing_item = self.item_repository.get_by_id(item_id)
        if existing_item is None:
            raise ValueError(f"No se encontró un ítem con ID {item_id}")
        
        return self.item_repository.update_stock(item_id, new_stock)
