"""
Schemas para el endpoint de seed de la base de datos.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class SeedResult(BaseModel):
    """Resultado de la ejecución del seed."""
    
    success: bool = Field(..., description="Indica si el seed se ejecutó correctamente")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    data_created: Dict[str, int] = Field(..., description="Cantidad de registros creados por tipo")
    execution_time: float = Field(..., description="Tiempo de ejecución en segundos")


class SeedResponse(BaseModel):
    """Respuesta del endpoint de seed."""
    
    status: str = Field(..., description="Estado de la operación")
    result: SeedResult = Field(..., description="Resultado detallado del seed")
    timestamp: str = Field(..., description="Timestamp de la ejecución")
