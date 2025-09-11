"""EtiquetaPlato enum for dish type classification."""

from enum import Enum


class EtiquetaPlato(Enum):
    """Enumeration for dish type classification."""
    
    ENTRADA = "entrada"
    FONDO = "fondo"
    POSTRE = "postre"
    
    def __str__(self) -> str:
        return self.value