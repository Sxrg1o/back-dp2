"""
Timestamp mixin for automatic created_at and updated_at fields.
"""

from typing import Optional
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    declared_attr,
    declarative_mixin,
)
from sqlalchemy import TIMESTAMP, func
from datetime import datetime


@declarative_mixin
class AuditMixin:
    """Clase mixin para agregar campos de auditoría a los modelos.

    Proporciona campos de seguimiento para la creación y modificación de registros.
    Debe ser incluida en aquellos modelos que requieran seguimiento de cambios
    temporales y de usuario.

    Attributes
    ----------
    activo: bool
        Indica si el registro está soft-deleted o activo.
    fecha_creacion : datetime
        Fecha y hora de creación del registro.
    fecha_modificacion : datetime
        Fecha y hora de última modificación del registro.
    creado_por : str, optional
        Identificador del usuario que creó el registro.
    modificado_por : str, optional
        Identificador del usuario que modificó por última vez el registro.
    """

    # Usando declared_attr para asegurar que las columnas se añaden a la tabla concreta
    @declared_attr
    def fecha_creacion(cls) -> Mapped[datetime]:
        return mapped_column(TIMESTAMP, nullable=False, server_default=func.now())

    @declared_attr
    def fecha_modificacion(cls) -> Mapped[datetime]:
        return mapped_column(
            TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()
        )

    # Seguimiento opcional del usuario que realizó los cambios
    @declared_attr
    def creado_por(cls) -> Mapped[Optional[str]]:
        return mapped_column(default=None)

    @declared_attr
    def modificado_por(cls) -> Mapped[Optional[str]]:
        return mapped_column(default=None)
