"""
Modelo de productos para la gestión del menú del restaurante.

Implementa la estructura de datos para los productos (platos) disponibles en el menú,
adaptado para coincidir con el esquema de MySQL restaurant_dp2.producto.
"""

from typing import Any, Dict, Optional, Type, TypeVar, TYPE_CHECKING, List
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Text, DECIMAL, ForeignKey, Index
from uuid import UUID
from src.models.base_model import BaseModel
from src.models.mixins.audit_mixin import AuditMixin

if TYPE_CHECKING:
    from src.models.menu.categoria_model import CategoriaModel
    from src.models.pedidos.producto_opcion_model import ProductoOpcionModel

# Definimos un TypeVar para el tipado genérico
T = TypeVar("T", bound="ProductoModel")


class ProductoModel(BaseModel, AuditMixin):
    """Modelo para representar productos (platos) del menú en el sistema.

    Define los productos disponibles en el menú del restaurante, organizados
    por categorías y con toda la información necesaria para su visualización
    y gestión en la carta digital.

    Attributes
    ----------
    id_categoria : UUID
        Identificador de la categoría a la que pertenece el producto.
    nombre : str
        Nombre del producto/plato.
    descripcion : str, optional
        Descripción detallada del producto.
    precio_base : Decimal
        Precio base del producto (debe ser mayor a 0).
    imagen_path : str, optional
        Ruta de la imagen del producto.
    imagen_alt_text : str, optional
        Texto alternativo para la imagen (accesibilidad).
    disponible : bool
        Indica si el producto está disponible actualmente.
    destacado : bool
        Indica si el producto es destacado en el menú.
    fecha_creacion : datetime
        Fecha y hora de creación del registro (heredado de AuditMixin).
    fecha_modificacion : datetime
        Fecha y hora de última modificación (heredado de AuditMixin).
    creado_por : str, optional
        Usuario que creó el registro (heredado de AuditMixin).
    modificado_por : str, optional
        Usuario que realizó la última modificación (heredado de AuditMixin).
    """

    __tablename__ = "producto"

    # Foreign Key - Relación con categoría
    id_categoria: Mapped[UUID] = mapped_column(
        ForeignKey("categoria.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # Columnas específicas del modelo de producto
    nombre: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio_base: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, index=True
    )
    imagen_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    imagen_alt_text: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    disponible: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="1", index=True
    )
    destacado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0", index=True
    )

    # Relación con Categoría
    categoria: Mapped["CategoriaModel"] = relationship(
        "CategoriaModel",
        back_populates="productos",
        lazy="selectin"
    )

    # Relación con ProductoOpcion (opciones disponibles para este producto)
    opciones: Mapped[List["ProductoOpcionModel"]] = relationship(
        "ProductoOpcionModel",
        back_populates="producto",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    # Índices adicionales
    __table_args__ = (
        Index('idx_busqueda', 'nombre', 'descripcion', mysql_prefix='FULLTEXT'),
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
        # Filtrar solo columnas válidas, ignorar relaciones
        valid_columns = [c.name for c in cls.__table__.columns]
        filtered_data = {
            k: v for k, v in data.items() 
            if k in valid_columns
        }
        return cls(**filtered_data)

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Actualiza la instancia con datos de un diccionario.

        Parameters
        ----------
        data : Dict[str, Any]
            Diccionario con los datos para actualizar la instancia.
        """
        for key, value in data.items():
            # Ignorar relaciones, solo actualizar columnas directas
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def __repr__(self) -> str:
        """Representación en string del modelo Producto."""
        return (
            f"<ProductoModel(id={self.id}, nombre='{self.nombre}', "
            f"precio_base={self.precio_base}, disponible={self.disponible})>"
        )
