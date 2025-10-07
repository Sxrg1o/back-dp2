"""
Modelo de opciones para configuración de productos o servicios.

Define las opciones disponibles asociadas a un producto o componente configurable,
incluyendo su etiqueta, precio adicional y estado por defecto. 
Adaptado para coincidir con el esquema existente de MySQL restaurant_dp2.opciones.
"""

from typing import Any, Dict, Optional, Type, TypeVar
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DECIMAL, Boolean, inspect
from src.models.base_model import BaseModel
from src.models.mixins.audit_mixin import AuditMixin

# Definimos un TypeVar para el tipado genérico
T = TypeVar("T", bound="OpcionModel")


class OpcionModel(BaseModel, AuditMixin):
    """Modelo para representar las opciones configurables de un producto.

    Permite definir opciones adicionales o alternativas que pueden afectar
    el precio final de un producto o servicio, con soporte de auditoría y control
    de estado activo.

    Attributes
    ----------
    etiqueta : str
        Nombre o etiqueta visible de la opción.
    precio_adicional : float
        Monto adicional que agrega la opción al precio base.
    es_default : bool
        Indica si la opción es la predeterminada dentro del conjunto.
    activo : bool
        Indica si la opción está activa o deshabilitada.
    fecha_creacion : datetime
        Fecha y hora de creación del registro (heredado de AuditMixin).
    fecha_modificacion : datetime
        Fecha y hora de última modificación (heredado de AuditMixin).
    creado_por : str, optional
        Usuario que creó el registro (heredado de AuditMixin).
    modificado_por : str, optional
        Usuario que modificó por última vez el registro (heredado de AuditMixin).
    """

    __tablename__ = "opciones"

    # Columnas específicas del modelo de opción
    etiqueta: Mapped[str] = mapped_column(String(100), nullable=False)
    precio_adicional: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False, default=0.00)
    es_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Métodos comunes
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la instancia del modelo a un diccionario.

        Returns
        -------
        Dict[str, Any]
            Diccionario con los nombres de columnas como claves y sus valores correspondientes.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Crea una instancia del modelo a partir de un diccionario.

        Parameters
        ----------
        data : Dict[str, Any]
            Diccionario con los datos para crear la instancia.

        Returns
        -------
        T
            Nueva instancia del modelo con los datos proporcionados.
        """
        return cls(
            **{k: v for k, v in data.items() if k in inspect(cls).columns.keys()}
        )

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Actualiza la instancia con datos de un diccionario.

        Parameters
        ----------
        data : Dict[str, Any]
            Diccionario con los datos para actualizar la instancia.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)