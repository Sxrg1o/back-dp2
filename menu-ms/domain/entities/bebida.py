"""
Entidad Bebida para el dominio del menú y carta.
Representa las bebidas disponibles en el menú.
"""

from decimal import Decimal
from typing import Optional
from .item import Item


class Bebida(Item):
    """
    Representa las bebidas disponibles en el menú.
    Especializado para líquidos con diferenciación entre bebidas alcohólicas y no alcohólicas.
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
        etiquetas: list = None,
        litros: Decimal = Decimal('0.0'),
        alcoholico: bool = False
    ):
        """
        Inicializa una bebida.
        
        Args:
            id: Identificador único de la bebida
            valor_nutricional: Información nutricional completa
            precio: Precio de la bebida en el menú
            tiempo_preparacion: Tiempo promedio de preparación en minutos
            comentarios: Notas adicionales sobre la bebida
            receta: Receta asociada para preparación
            disponible: Disponibilidad actual en carta
            unidades_disponibles: Stock disponible de la bebida
            num_ingredientes: Número total de ingredientes
            kcal: Calorías por porción
            calorias: Energía total en calorías (detallado)
            proteinas: Contenido de proteínas en gramos
            azucares: Contenido de azúcares en gramos
            descripcion: Descripción detallada de la bebida
            etiquetas: Lista de etiquetas de la bebida
            litros: Cantidad en litros del contenido
            alcoholico: Indica si la bebida contiene alcohol
        """
        super().__init__(
            id=id,
            valor_nutricional=valor_nutricional,
            precio=precio,
            tiempo_preparacion=tiempo_preparacion,
            comentarios=comentarios,
            receta=receta,
            disponible=disponible,
            unidades_disponibles=unidades_disponibles,
            num_ingredientes=num_ingredientes,
            kcal=kcal,
            calorias=calorias,
            proteinas=proteinas,
            azucares=azucares,
            descripcion=descripcion,
            etiquetas=etiquetas or []
        )
        self.litros = litros
        self.alcoholico = alcoholico
    
    def get_tipo(self) -> str:
        """
        Retorna el tipo específico de la bebida.
        
        Returns:
            str: Tipo de la bebida
        """
        return "BEBIDA"
    
    def es_alcoholica(self) -> bool:
        """
        Verifica si la bebida es alcohólica.
        
        Returns:
            bool: True si es alcohólica, False en caso contrario
        """
        return self.alcoholico
    
    def calcular_densidad_calorica(self) -> Decimal:
        """
        Calcula la densidad calórica de la bebida (calorías por litro).
        
        Returns:
            Decimal: Densidad calórica de la bebida
        """
        if self.litros > 0:
            return self.calorias / self.litros
        return Decimal('0.0')
    
    def calcular_calorias_por_ml(self) -> Decimal:
        """
        Calcula las calorías por mililitro de la bebida.
        
        Returns:
            Decimal: Calorías por mililitro
        """
        if self.litros > 0:
            return self.calorias / (self.litros * 1000)  # Convertir litros a ml
        return Decimal('0.0')
    
    def es_apta_para_menores(self) -> bool:
        """
        Verifica si la bebida es apta para menores de edad.
        
        Returns:
            bool: True si es apta para menores, False en caso contrario
        """
        return not self.alcoholico
    
    def __str__(self) -> str:
        return f"Bebida(id={self.id}, descripcion='{self.descripcion}', precio={self.precio}, litros={self.litros}L, alcoholico={self.alcoholico})"
    
    def __repr__(self) -> str:
        return self.__str__()
