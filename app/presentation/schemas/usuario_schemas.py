"""
Pydantic schemas for Usuario (User) entities.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    """Base schema for Usuario."""
    id_rol: int = Field(..., description="Role ID", gt=0)
    email: EmailStr = Field(..., description="User email address")
    nombre: str = Field(..., description="User full name", min_length=1, max_length=255)
    telefono: Optional[str] = Field(None, description="Phone number", max_length=20)
    activo: bool = Field(True, description="User active status")


class UsuarioCreate(UsuarioBase):
    """Schema for creating a new usuario."""
    password_hash: str = Field(..., description="Hashed password", min_length=1)


class UsuarioUpdate(BaseModel):
    """Schema for updating usuario."""
    id_rol: Optional[int] = Field(None, description="Role ID", gt=0)
    email: Optional[EmailStr] = Field(None, description="User email address")
    password_hash: Optional[str] = Field(None, description="Hashed password", min_length=1)
    nombre: Optional[str] = Field(None, description="User full name", min_length=1, max_length=255)
    telefono: Optional[str] = Field(None, description="Phone number", max_length=20)
    activo: Optional[bool] = Field(None, description="User active status")


class UsuarioResponse(UsuarioBase):
    """Schema for usuario responses."""
    id_usuario: int = Field(..., description="User ID")
    ultimo_acceso: Optional[datetime] = Field(None, description="Last access timestamp")
    fecha_creacion: Optional[datetime] = Field(None, description="Creation timestamp")
    fecha_modificacion: Optional[datetime] = Field(None, description="Last modification timestamp")

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password", min_length=1)


class UsuarioProfile(BaseModel):
    """Schema for user profile (without sensitive data)."""
    id_usuario: int = Field(..., description="User ID")
    id_rol: int = Field(..., description="Role ID")
    email: EmailStr = Field(..., description="User email address")
    nombre: str = Field(..., description="User full name")
    telefono: Optional[str] = Field(None, description="Phone number")
    activo: bool = Field(..., description="User active status")
    ultimo_acceso: Optional[datetime] = Field(None, description="Last access timestamp")
    fecha_creacion: Optional[datetime] = Field(None, description="Creation timestamp")

    class Config:
        from_attributes = True