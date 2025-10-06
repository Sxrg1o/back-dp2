"""
Pydantic schemas for Rol (Role) entities.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class RolBase(BaseModel):
    """Base schema for Rol."""
    nombre: str = Field(..., description="Role name", min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, description="Role description", max_length=255)


class RolCreate(RolBase):
    """Schema for creating a new rol."""
    pass


class RolUpdate(BaseModel):
    """Schema for updating rol."""
    nombre: Optional[str] = Field(None, description="Role name", min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, description="Role description", max_length=255)


class RolResponse(RolBase):
    """Schema for rol responses."""
    id_rol: int = Field(..., description="Role ID")
    fecha_creacion: Optional[datetime] = Field(None, description="Creation timestamp")
    fecha_modificacion: Optional[datetime] = Field(None, description="Last modification timestamp")

    class Config:
        from_attributes = True


class RolSummary(BaseModel):
    """Schema for rol summary (minimal data)."""
    id_rol: int = Field(..., description="Role ID")
    nombre: str = Field(..., description="Role name")

    class Config:
        from_attributes = True