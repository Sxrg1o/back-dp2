"""
Allergen-related enumerations.
"""

from enum import Enum


class NivelRiesgo(str, Enum):
    """Allergen risk levels."""
    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"
    CRITICO = "critico"


class NivelPresencia(str, Enum):
    """Allergen presence levels in products."""
    CONTIENE = "contiene"
    TRAZAS = "trazas"
    PUEDE_CONTENER = "puede_contener"