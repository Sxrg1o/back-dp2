from typing import Any, Dict, Optional, Type, TypeVar
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Index
from src.models.base_model import BaseModel
from src.models.mixins.audit_mixin import AuditMixin

T = TypeVar("T", bound="UsuarioModel")

class UsuarioModel(BaseModel, AuditMixin):
    """
    User model for authentication and user management.
    Adapted to match existing MySQL schema restaurant_dp2.usuario
    """

    __tablename__ = "usuarios"
    __table_args__ = (
        Index("idx_email", "email"),
        Index("idx_rol", "id_rol"),
        Index("idx_activo", "activo"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Usuarios del sistema (staff y clientes registrados)'
        }
    )

    # Campos específicos del usuario
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    nombre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    id_rol: Mapped[str] = mapped_column(String(36), nullable=False)  # ULID de rol

    # Métodos comunes heredados de BaseModel y AuditMixin
    # Si necesitas métodos personalizados, agrégalos aquí

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        # Puedes agregar campos adicionales si lo necesitas
        return result

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return super().from_dict(data)

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        super().update_from_dict(data)