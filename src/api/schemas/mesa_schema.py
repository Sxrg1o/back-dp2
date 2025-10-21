"""
Schemas de Pydantic para la entidad Mesa.

Este módulo define las estructuras de datos para crear, actualizar y
representar las mesas en la API.
"""


from typing import Optional, ClassVar, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from src.core.enums.mesa_enums import EstadoMesa

class MesaBase(BaseModel):
    """
    Schema base con los campos comunes para una mesa.

    Attributes
    ----------
    numero : str
        Numero de la mesa
    capacidad : Optional[int]
        Capacidad de la mesa.
    zona : Optional[str]
        Zona donde se encuentra la mesa.
    qr_code : Optional[str]
        Código QR asociado a la mesa para identificación rápida.
    estado : EstadoMesa
        Estado actual de la mesa (disponible, ocupada, reservada, mantenimiento).
    """
    numero: str = Field(
        description="Número identificativo de la mesa.",
        min_length=1,
        max_length=20
    )
    capacidad: Optional[int] = Field(
        default=None,
        description="Capacidad de la mesa."
    )
    zona: Optional[str] = Field(
        default=None,
        description="Zona donde se encuentra la mesa."
    )
    qr_code: Optional[str] = Field(
        default=None,
        description="Código QR asociado a la mesa para identificación rápida."
    )
    estado: EstadoMesa = Field(
        default=EstadoMesa.DISPONIBLE,
        description="Estado actual de la mesa (disponible, ocupada, reservada, mantenimiento)."
    )


class MesaCreate(MesaBase):
    """
    Schema para la creación de una nueva mesa.

    Hereda todos los campos de MesaBase y se utiliza como cuerpo
    de la petición (request body) en el endpoint de creación.
    """
    pass


class MesaUpdate(BaseModel):
    """
    Schema para la actualización parcial de una mesa.

    Todos los campos son opcionales para permitir actualizaciones
    parciales (método PATCH).
    """
    numero: Optional[str] = Field(
        default=None,
        description="Nuevo número identificativo de la mesa.",
        min_length=1,
        max_length=20
    )
    capacidad: Optional[int] = Field(
        default=None,
        description="Nueva capacidad de la mesa."
    )
    zona: Optional[str] = Field(
        default=None,
        description="Nueva zona donde se encuentra la mesa."
    )
    qr_code: Optional[str] = Field(
        default=None,
        description="Nuevo código QR asociado a la mesa."
    )
    estado: Optional[EstadoMesa] = Field(
        default=None,
        description="Nuevo estado de la mesa (disponible, ocupada, reservada, mantenimiento)."
    )


class MesaResponse(MesaBase):
    """
    Schema para representar una mesa en las respuestas de la API.

    Incluye campos de auditoría y de solo lectura que no se exponen en
    la creación o actualización.
    """
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Identificador único de la mesa (UUID).")
    activo: bool = Field(description="Indica si la mesa está activa en el sistema.")
    fecha_creacion: Optional[datetime] = Field(
        default=None, description="Fecha y hora de creación del registro."
    )
    fecha_modificacion: Optional[datetime] = Field(
        default=None, description="Fecha y hora de la última modificación."
    )


class MesaSummary(BaseModel):
    """
    Schema con información resumida de una mesa para listas.

    Diseñado para ser ligero y eficiente al devolver múltiples registros.
    """
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Identificador único de la mesa (UUID).")
    numero: str = Field(description="Número de la mesa.")
    capacidad: Optional[int] = Field(description="Capacidad de la mesa.")
    zona: Optional[str] = Field(description="Zona donde se encuentra la mesa.")
    qr_code: Optional[str] = Field(description="Código QR asociado a la mesa.")
    estado: EstadoMesa = Field(description="Estado actual de la mesa.")

class MesaList(BaseModel):
    """Schema para respuestas paginadas que contienen una lista de mesas."""
    items: List[MesaSummary] = Field(description="Lista de mesas en la página actual.")
    total: int = Field(description="Número total de mesas que coinciden con la consulta.")
