"""EtiquetaItem enum for menu item labels."""

from enum import Enum


class EtiquetaItem(Enum):
    """Enumeration for menu item labels."""
    
    SIN_GLUTEN = "sin_gluten"
    PICANTE = "picante"
    SALADO = "salado"
    CALIENTE = "caliente"
    FRIO = "frio"
    ACIDO = "acido"
    AGRIO = "agrio"
    CON_GLUTEN = "con_gluten"
    VEGANO = "vegano"
    
    def __str__(self) -> str:
        return self.value