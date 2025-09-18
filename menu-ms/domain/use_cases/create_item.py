"""
Caso de uso para crear un ítem del menú.
"""

from typing import Union
from decimal import Decimal
from ..entities import Item, Plato, Bebida
from ..repositories import ItemRepository


class CreateItemUseCase:
    """
    Caso de uso para crear un ítem del menú.
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
        Ejecuta la creación de un ítem.
        
        Args:
            item: Ítem a crear (Plato o Bebida)
            
        Returns:
            Union[Plato, Bebida]: Ítem creado con ID asignado
            
        Raises:
            ValueError: Si el ítem no es válido
        """
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
        
        # Crear el ítem
        return self.item_repository.create(item)
