"""
Enumeraciones para el dominio del menú y carta.
Define las clasificaciones y etiquetas utilizadas en el sistema.
"""

from enum import Enum


class EtiquetaItem(Enum):
    """
    Clasificación y etiquetado de ítems del menú.
    Utilizado para identificar características especiales de los productos.
    """
    SIN_GLUTEN = "SIN_GLUTEN"
    PICANTE = "PICANTE"
    SALADO = "SALADO"
    CALIENTE = "CALIENTE"
    FRIO = "FRIO"
    ACIDO = "ACIDO"
    AGRIO = "AGRIO"
    CON_GLUTEN = "CON_GLUTEN"
    VEGANO = "VEGANO"


class EtiquetaIngrediente(Enum):
    """
    Clasificación de ingredientes por categoría.
    Utilizado para organizar y filtrar ingredientes por tipo.
    """
    VERDURA = "VERDURA"
    CARNE = "CARNE"
    FRUTA = "FRUTA"


class EtiquetaPlato(Enum):
    """
    Clasificación de platos según su función en el menú.
    Utilizado para organizar platos por su propósito en la comida.
    """
    ENTRADA = "ENTRADA"
    FONDO = "FONDO"
    POSTRE = "POSTRE"


class EtiquetaBebida(Enum):
    """
    Clasificación de bebidas según su tipo.
    Utilizado para organizar bebidas por su categoría.
    """
    ALCOHOLICA = "ALCOHOLICA"
    NO_ALCOHOLICA = "NO_ALCOHOLICA"
    GASEOSA = "GASEOSA"
    NATURAL = "NATURAL"
    CALIENTE = "CALIENTE"
    FRIO = "FRIO"


class TipoItem(Enum):
    """
    Tipo base de ítem del menú.
    Utilizado para distinguir entre platos y bebidas.
    """
    PLATO = "PLATO"
    BEBIDA = "BEBIDA"
