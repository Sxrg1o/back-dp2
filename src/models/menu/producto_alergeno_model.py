"""
Modelo de relación entre productos y alérgenos.

Implementa la tabla de asociación muchos-a-muchos entre productos y alérgenos,
con campos adicionales para detallar el nivel de presencia del alérgeno en cada producto.
Adaptado para coincidir con el esquema de MySQL restaurant_dp2.producto_alergeno.
"""

from typing import Any, Dict, Optional, Type, TypeVar
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Enum, ForeignKey, Index, inspect
from datetime import datetime
from uuid import UUID
from src.models.base_model import BaseModel
from src.core.enums.alergeno_enums import NivelPresencia

# Definimos un TypeVar para el tipado genérico
T = TypeVar("T", bound="ProductoAlergenoModel")


class ProductoAlergenoModel(BaseModel):
    """Modelo para representar la relación entre productos y alérgenos.

    Tabla de asociación muchos-a-muchos que detalla qué alérgenos están presentes
    en cada producto del menú, con información adicional sobre el nivel de presencia
    (contiene, trazas, puede contener).

    Esta tabla usa clave primaria compuesta (id_producto, id_alergeno), por lo que
    NO hereda el campo 'id' de BaseModel.

    Attributes
    ----------
    id_producto : UUID
        Identificador del producto (parte de la clave primaria compuesta).
    id_alergeno : UUID
        Identificador del alérgeno (parte de la clave primaria compuesta).
    nivel_presencia : NivelPresencia
        Nivel de presencia del alérgeno: contiene, trazas, puede_contener.
    notas : str, optional
        Información adicional sobre el alérgeno en este producto.
    activo : bool
        Indica si esta relación está activa.
    fecha_creacion : datetime
        Fecha y hora de creación del registro.
    fecha_modificacion : datetime
        Fecha y hora de última modificación.
    """

    __tablename__ = "producto_alergeno"

    # Claves foráneas que forman la clave primaria compuesta
    id_producto: Mapped[UUID] = mapped_column(
        ForeignKey("producto.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    id_alergeno: Mapped[UUID] = mapped_column(
        ForeignKey("alergeno.id", ondelete="RESTRICT"),
        primary_key=True,
        nullable=False
    )

    # Columnas específicas del modelo
    nivel_presencia: Mapped[NivelPresencia] = mapped_column(
        Enum(NivelPresencia),
        nullable=False,
        default=NivelPresencia.CONTIENE,
        server_default="contiene"
    )
    notas: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Información adicional sobre el alérgeno en este producto"
    )
    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1"
    )

    # Campos de auditoría (sin AuditMixin ya que BaseModel ya tiene id)
    # Nota: fecha_creacon en MySQL es un typo, debería ser fecha_creacion
    fecha_creacion: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        server_default="CURRENT_TIMESTAMP"
    )
    fecha_modificacion: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        server_default="CURRENT_TIMESTAMP",
        onupdate=datetime.utcnow
    )

    # Índices adicionales para mejorar búsquedas
    __table_args__ = (
        Index('idx_producto', 'id_producto'),
        Index('idx_alergeno', 'id_alergeno'),
    )

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
            if hasattr(self, key) and key not in ('id_producto', 'id_alergeno'):
                setattr(self, key, value)

    def __repr__(self) -> str:
        """Representación string del modelo para debugging.

        Returns
        -------
        str
            Representación string del objeto ProductoAlergenoModel.
        """
        return (
            f"<ProductoAlergenoModel(id_producto={self.id_producto}, "
            f"id_alergeno={self.id_alergeno}, "
            f"nivel_presencia='{self.nivel_presencia.value}', activo={self.activo})>"
        )
