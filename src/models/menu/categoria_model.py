"""
Modelo de categorías para la gestión del menú del restaurante.

Implementa la estructura de datos para las categorías de productos en el sistema,
adaptado para coincidir con el esquema de MySQL restaurant_dp2.categoria.
"""

from typing import Any, Dict, Optional, Type, TypeVar
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Text, inspect
from src.models.base_model import BaseModel
from src.models.mixins.audit_mixin import AuditMixin

# Definimos un TypeVar para el tipado genérico
T = TypeVar("T", bound="CategoriaModel")


class CategoriaModel(BaseModel, AuditMixin):
    """Modelo para representar categorías de productos en el sistema.

    Define las categorías que organizan los productos del menú del restaurante
    para facilitar la navegación y gestión de la carta digital.

    Attributes
    ----------
    nombre : str
        Nombre de la categoría, debe ser único en el sistema.
    descripcion : str, optional
        Descripción detallada de la categoría y sus productos.
    activo : bool
        Indica si la categoría está activa en el sistema.
    fecha_creacion : datetime
        Fecha y hora de creación del registro (heredado de AuditableModel).
    fecha_modificacion : datetime
        Fecha y hora de última modificación (heredado de AuditableModel).
    creado_por : str, optional
        Usuario que creó el registro (heredado de AuditableModel).
    modificado_por : str, optional
        Usuario que realizó la última modificación (heredado de AuditableModel).
    """

    __tablename__ = "categoria"

    # Columnas específicas del modelo de categoría
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")

    # Métodos comunes para todos los modelos
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la instancia del modelo a un diccionario.

        Transforma todos los atributos del modelo en un diccionario para
        facilitar su serialización y uso en APIs.

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
