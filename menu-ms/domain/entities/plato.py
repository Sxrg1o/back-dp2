"""
Entidad Plato para el dominio del menú y carta.
Representa los platos principales, entradas y postres del menú.
"""

from decimal import Decimal
from typing import Optional
from .item import Item
from .enums import EtiquetaPlato


class Plato(Item):
    """
    Representa los platos principales, entradas y postres del menú.
    Especializado para comidas sólidas con información de peso y tipo específico.
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
        peso: Decimal = Decimal('0.0'),
        tipo: EtiquetaPlato = EtiquetaPlato.FONDO
    ):
        """
        Inicializa un plato.
        
        Args:
            id: Identificador único del plato
            valor_nutricional: Información nutricional completa
            precio: Precio del plato en el menú
            tiempo_preparacion: Tiempo promedio de preparación en minutos
            comentarios: Notas adicionales sobre el plato
            receta: Receta específica de preparación del plato
            disponible: Disponibilidad actual en carta
            unidades_disponibles: Stock disponible del plato
            num_ingredientes: Número total de ingredientes
            kcal: Calorías por porción
            calorias: Energía total en calorías (detallado)
            proteinas: Contenido de proteínas en gramos
            azucares: Contenido de azúcares en gramos
            descripcion: Descripción detallada del plato
            etiquetas: Lista de etiquetas del plato
            peso: Peso total del plato en gramos
            tipo: Clasificación del plato (ENTRADA, FONDO, POSTRE)
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
        self.peso = peso
        self.tipo = tipo
    
    def get_tipo(self) -> str:
        """
        Retorna el tipo específico del plato.
        
        Returns:
            str: Tipo del plato
        """
        return "PLATO"
    
    def get_tipo_plato(self) -> EtiquetaPlato:
        """
        Retorna la clasificación específica del plato.
        
        Returns:
            EtiquetaPlato: Clasificación del plato
        """
        return self.tipo
    
    def calcular_densidad_calorica(self) -> Decimal:
        """
        Calcula la densidad calórica del plato (calorías por gramo).
        
        Returns:
            Decimal: Densidad calórica del plato
        """
        if self.peso > 0:
            return self.calorias / self.peso
        return Decimal('0.0')
    
    def es_entrada(self) -> bool:
        """
        Verifica si el plato es una entrada.
        
        Returns:
            bool: True si es entrada, False en caso contrario
        """
        return self.tipo == EtiquetaPlato.ENTRADA
    
    def es_plato_principal(self) -> bool:
        """
        Verifica si el plato es un plato principal.
        
        Returns:
            bool: True si es plato principal, False en caso contrario
        """
        return self.tipo == EtiquetaPlato.FONDO
    
    def es_postre(self) -> bool:
        """
        Verifica si el plato es un postre.
        
        Returns:
            bool: True si es postre, False en caso contrario
        """
        return self.tipo == EtiquetaPlato.POSTRE
    
    def __str__(self) -> str:
        return f"Plato(id={self.id}, descripcion='{self.descripcion}', precio={self.precio}, tipo={self.tipo.value}, peso={self.peso}g)"
    
    def __repr__(self) -> str:
        return self.__str__()
