"""
Entidad base Item para el dominio del menú y carta.
Representa cualquier elemento del menú con sus características comunes.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal
from .enums import EtiquetaItem


class Item(ABC):
    """
    Clase base abstracta que representa cualquier elemento del menú.
    Define las características comunes de todos los productos.
    """
    
    def __init__(
        self,
        id: Optional[int] = None,
        valor_nutricional: str = "",
        precio: Decimal = Decimal('0.0'),
        tiempo_preparacion: Decimal = Decimal('0.0'),
        comentarios: str = "",
        receta: str = "",
        disponible: bool = True,
        unidades_disponibles: int = 0,
        num_ingredientes: int = 0,
        kcal: int = 0,
        calorias: Decimal = Decimal('0.0'),
        proteinas: Decimal = Decimal('0.0'),
        azucares: Decimal = Decimal('0.0'),
        descripcion: str = "",
        etiquetas: List[EtiquetaItem] = None
    ):
        """
        Inicializa un ítem del menú.
        
        Args:
            id: Identificador único del ítem
            valor_nutricional: Información nutricional completa
            precio: Precio del ítem en el menú
            tiempo_preparacion: Tiempo promedio de preparación en minutos
            comentarios: Notas adicionales sobre el ítem
            receta: Receta asociada para preparación
            disponible: Disponibilidad actual en carta
            unidades_disponibles: Stock disponible del ítem
            num_ingredientes: Número total de ingredientes
            kcal: Calorías por porción
            calorias: Energía total en calorías (detallado)
            proteinas: Contenido de proteínas en gramos
            azucares: Contenido de azúcares en gramos
            descripcion: Descripción detallada del ítem
            etiquetas: Lista de etiquetas del ítem
        """
        self.id = id
        self.valor_nutricional = valor_nutricional
        self.precio = precio
        self.tiempo_preparacion = tiempo_preparacion
        self.comentarios = comentarios
        self.receta = receta
        self.disponible = disponible
        self.unidades_disponibles = unidades_disponibles
        self.num_ingredientes = num_ingredientes
        self.kcal = kcal
        self.calorias = calorias
        self.proteinas = proteinas
        self.azucares = azucares
        self.descripcion = descripcion
        self.etiquetas = etiquetas or []
    
    def verificar_stock(self) -> bool:
        """
        Verifica si hay stock disponible del ítem.
        
        Returns:
            bool: True si hay stock disponible, False en caso contrario
        """
        return self.disponible and self.unidades_disponibles > 0
    
    def reducir_stock(self, cantidad: int) -> bool:
        """
        Reduce el stock del ítem en la cantidad especificada.
        
        Args:
            cantidad: Cantidad a reducir del stock
            
        Returns:
            bool: True si se pudo reducir el stock, False en caso contrario
        """
        if self.unidades_disponibles >= cantidad:
            self.unidades_disponibles -= cantidad
            if self.unidades_disponibles == 0:
                self.disponible = False
            return True
        return False
    
    def aumentar_stock(self, cantidad: int) -> None:
        """
        Aumenta el stock del ítem en la cantidad especificada.
        
        Args:
            cantidad: Cantidad a aumentar del stock
        """
        self.unidades_disponibles += cantidad
        if not self.disponible and self.unidades_disponibles > 0:
            self.disponible = True
    
    def agregar_etiqueta(self, etiqueta: EtiquetaItem) -> None:
        """
        Agrega una etiqueta al ítem.
        
        Args:
            etiqueta: Etiqueta a agregar
        """
        if etiqueta not in self.etiquetas:
            self.etiquetas.append(etiqueta)
    
    def remover_etiqueta(self, etiqueta: EtiquetaItem) -> None:
        """
        Remueve una etiqueta del ítem.
        
        Args:
            etiqueta: Etiqueta a remover
        """
        if etiqueta in self.etiquetas:
            self.etiquetas.remove(etiqueta)
    
    def tiene_etiqueta(self, etiqueta: EtiquetaItem) -> bool:
        """
        Verifica si el ítem tiene una etiqueta específica.
        
        Args:
            etiqueta: Etiqueta a verificar
            
        Returns:
            bool: True si tiene la etiqueta, False en caso contrario
        """
        return etiqueta in self.etiquetas
    
    @abstractmethod
    def get_tipo(self) -> str:
        """
        Retorna el tipo específico del ítem.
        Debe ser implementado por las clases hijas.
        
        Returns:
            str: Tipo del ítem
        """
        pass
    
    def __str__(self) -> str:
        return f"{self.get_tipo()}(id={self.id}, descripcion='{self.descripcion}', precio={self.precio})"
    
    def __repr__(self) -> str:
        return self.__str__()
