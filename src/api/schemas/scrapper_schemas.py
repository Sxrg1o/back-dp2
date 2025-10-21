"""
Esquemas de datos (data schemas) para la API de Domotica Scrapper.

Este módulo define los modelos Pydantic utilizados para la validación,
serialización y documentación de la API.
"""

from typing import Dict, Optional, Any
from pydantic import BaseModel


class ProductoDomotica(BaseModel):
    """
    Modelo que representa un producto en el sistema Domotica INC.

    Este esquema es utilizado para la extracción y presentación de datos
    de productos obtenidos mediante web scraping.
    """

    categoria: str
    """Categoría del producto (ej. 'Entradas', 'Platos Fuertes', 'Postres')"""

    nombre: str
    """Nombre completo del producto"""

    stock: str
    """Stock disponible del producto (puede ser número o texto como 'Agotado')"""

    precio: str
    """Precio del producto en moneda local (formato string desde el scraping)"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "categoria": "Platos Fuertes",
                    "nombre": "Lomo Saltado",
                    "stock": "15",
                    "precio": "25.50",
                }
            ]
        }
    }


class MesaDomotica(BaseModel):
    """
    Modelo que representa una mesa en el sistema Domotica INC.

    Este esquema es utilizado para la extracción y presentación de datos
    de mesas obtenidos mediante web scraping.
    """

    nombre: str
    """Nombre/identificador de la mesa"""

    zona: str
    """Zona o área del restaurante donde se ubica la mesa"""

    nota: str = ""
    """Notas adicionales sobre la mesa"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"nombre": "MESA-01", "zona": "Terraza", "nota": ""}
            ]
        }
    }

    def __str__(self) -> str:
        return f"Mesa {self.nombre} en zona {self.zona}"


class HealthResponse(BaseModel):
    """
    Modelo para la respuesta del endpoint de health check.
    """

    error: Optional[str] = None
    """Mensaje de error, si existe alguno"""

    status: int
    """Código de estado HTTP"""

    data: Dict[str, Any]
    """Datos del estado del servicio"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": None,
                    "status": 200,
                    "data": {"status": "online", "timestamp": "2025-10-08T12:00:00Z"},
                }
            ]
        }
    }


class WebSocketMessage(BaseModel):
    """
    Modelo para los mensajes enviados a través de WebSocket.
    """

    evento: str
    """Tipo de evento WebSocket"""

    payload: Dict[str, Any]
    """Contenido del mensaje"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "evento": "actualizacion_mesa",
                    "payload": {
                        "identificador": "MESA-05",
                        "zona": "Salón Principal",
                        "ocupado": True,
                    },
                }
            ]
        }
    }
