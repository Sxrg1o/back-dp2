from enum import Enum

class EtiquetaPlato(Enum):
    """Enumeración para tipos de platos"""
    ENTRADA = "ENTRADA"
    FONDO = "FONDO"
    POSTRE = "POSTRE"

class TipoAlergeno(Enum):
    """Enumeración para tipos de alérgenos"""
    GLUTEN = "GLUTEN"
    LACTEOS = "LACTEOS"
    FRUTOS_SECOS = "FRUTOS_SECOS"
    MARISCOS = "MARISCOS"
    HUEVOS = "HUEVOS"
    SOJA = "SOJA"
    PESCADO = "PESCADO"
    SESAMO = "SESAMO"
    MOSTAZA = "MOSTAZA"
    APIO = "APIO"
    SULFITOS = "SULFITOS"
    LUPINO = "LUPINO"
    MOLUSCOS = "MOLUSCOS"
