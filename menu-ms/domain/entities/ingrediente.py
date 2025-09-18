"""
Entidad Ingrediente para el dominio del menú y carta.
Representa los ingredientes individuales utilizados en la preparación de ítems.
"""

from decimal import Decimal
from typing import Optional
from .enums import EtiquetaIngrediente


class Ingrediente:
    """
    Representa los ingredientes individuales utilizados en la preparación de ítems.
    Controla el inventario a nivel de ingrediente.
    """
    
    def __init__(
        self,
        id: Optional[int] = None,
        nombre: str = "",
        stock: Decimal = Decimal('0.0'),
        peso: Decimal = Decimal('0.0'),
        tipo: EtiquetaIngrediente = EtiquetaIngrediente.VERDURA
    ):
        """
        Inicializa un ingrediente.
        
        Args:
            id: Identificador único del ingrediente
            nombre: Nombre del ingrediente
            stock: Cantidad disponible en inventario
            peso: Peso por unidad del ingrediente
            tipo: Clasificación del ingrediente
        """
        self.id = id
        self.nombre = nombre
        self.stock = stock
        self.peso = peso
        self.tipo = tipo
    
    def verificar_stock(self, cantidad_necesaria: Decimal) -> bool:
        """
        Verifica si hay suficiente stock del ingrediente.
        
        Args:
            cantidad_necesaria: Cantidad necesaria del ingrediente
            
        Returns:
            bool: True si hay suficiente stock, False en caso contrario
        """
        return self.stock >= cantidad_necesaria
    
    def reducir_stock(self, cantidad: Decimal) -> bool:
        """
        Reduce el stock del ingrediente en la cantidad especificada.
        
        Args:
            cantidad: Cantidad a reducir del stock
            
        Returns:
            bool: True si se pudo reducir el stock, False en caso contrario
        """
        if self.stock >= cantidad:
            self.stock -= cantidad
            return True
        return False
    
    def aumentar_stock(self, cantidad: Decimal) -> None:
        """
        Aumenta el stock del ingrediente en la cantidad especificada.
        
        Args:
            cantidad: Cantidad a aumentar del stock
        """
        self.stock += cantidad
    
    def calcular_peso_total(self) -> Decimal:
        """
        Calcula el peso total del ingrediente basado en stock y peso unitario.
        
        Returns:
            Decimal: Peso total del ingrediente
        """
        return self.stock * self.peso
    
    def __str__(self) -> str:
        return f"Ingrediente(id={self.id}, nombre='{self.nombre}', stock={self.stock}, tipo={self.tipo.value})"
    
    def __repr__(self) -> str:
        return self.__str__()
