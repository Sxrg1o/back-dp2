"""EtiquetaIngrediente enum for ingredient classification."""

from enum import Enum


class EtiquetaIngrediente(Enum):
    """Enumeration for ingredient type classification."""
    
    VERDURA = "verdura"
    CARNE = "carne"
    FRUTA = "fruta"
    
    def __str__(self) -> str:
        return self.value