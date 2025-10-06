"""
Endpoints para gestión de usuarios.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.repositories.auth.usuario_mysql_repository import UsuarioMySQLRepository
from src.api.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate
)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

# Repository instance
usuario_repo = UsuarioMySQLRepository()


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(
    usuario_data: UsuarioCreate,
    db: AsyncSession = Depends(get_database_session)
):
    """Crear un nuevo usuario."""
    try:
        # Check if email already exists
        existing_user = await usuario_repo.get_by_email(db, usuario_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create user
        new_usuario = await usuario_repo.create_usuario(
            db=db,
            id_rol=usuario_data.id_rol,
            email=usuario_data.email,
            password_hash=usuario_data.password_hash,
            nombre=usuario_data.nombre,
            telefono=usuario_data.telefono,
            activo=usuario_data.activo
        )

        return UsuarioResponse.from_orm(new_usuario)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating usuario: {str(e)}"
        )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener usuario por ID."""
    usuario = await usuario_repo.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario not found"
        )

    return UsuarioResponse.from_orm(usuario)


@router.get("/", response_model=List[UsuarioResponse])
async def list_usuarios(
    skip: int = 0,
    limit: int = 100,
    activo_only: bool = False,
    db: AsyncSession = Depends(get_database_session)
):
    """Listar usuarios con paginación."""
    usuarios = await usuario_repo.get_all(
        db=db,
        skip=skip,
        limit=limit,
        activo_only=activo_only
    )

    return [UsuarioResponse.from_orm(usuario) for usuario in usuarios]


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: AsyncSession = Depends(get_database_session)
):
    """Actualizar usuario."""
    # Check if usuario exists
    existing_usuario = await usuario_repo.get_by_id(db, usuario_id)
    if not existing_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario not found"
        )

    # Check email uniqueness if email is being updated
    if usuario_data.email and usuario_data.email != existing_usuario.email:
        email_exists = await usuario_repo.exists_email(db, usuario_data.email, usuario_id)
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )

    # Update usuario
    updated_usuario = await usuario_repo.update_usuario(
        db=db,
        usuario_id=usuario_id,
        **usuario_data.dict(exclude_unset=True)
    )

    return UsuarioResponse.from_orm(updated_usuario)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Eliminar usuario (hard delete)."""
    deleted = await usuario_repo.delete_usuario(db, usuario_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario not found"
        )


@router.patch("/{usuario_id}/deactivate", response_model=UsuarioResponse)
async def deactivate_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Desactivar usuario (soft delete)."""
    usuario = await usuario_repo.deactivate_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario not found"
        )

    return UsuarioResponse.from_orm(usuario)


@router.get("/email/{email}", response_model=UsuarioResponse)
async def get_usuario_by_email(
    email: str,
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener usuario por email."""
    usuario = await usuario_repo.get_by_email(db, email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario not found"
        )

    return UsuarioResponse.from_orm(usuario)


@router.get("/role/{id_rol}", response_model=List[UsuarioResponse])
async def get_usuarios_by_role(
    id_rol: int,
    db: AsyncSession = Depends(get_database_session)
):
    """Obtener usuarios por rol."""
    usuarios = await usuario_repo.get_by_role(db, id_rol)
    return [UsuarioResponse.from_orm(usuario) for usuario in usuarios]


@router.get("/count/total")
async def count_usuarios(
    activo_only: bool = False,
    db: AsyncSession = Depends(get_database_session)
):
    """Contar total de usuarios."""
    count = await usuario_repo.count_usuarios(db, activo_only)
    return {"total_usuarios": count}