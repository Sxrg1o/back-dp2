"""
Unit tests for RolService
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from src.business_logic.auth.rol_service import RolService
from src.business_logic.exceptions.base_exceptions import ValidationError, NotFoundError
from src.models.auth.rol_model import RolModel


@pytest.mark.asyncio
async def test_create_rol_success():
    """
    Verifica que create_rol crea un rol correctamente.
    """
    mock_db = AsyncMock()

    rol_creado = RolModel(
        id_rol=1,
        nombre="Admin",
        descripcion="Administrador del sistema"
    )

    with patch.object(RolService, '__init__', lambda x: None):
        service = RolService()
        service.rol_repo = MagicMock()
        service.rol_repo.get_by_nombre = AsyncMock(return_value=None)  # No existe
        service.rol_repo.create_rol = AsyncMock(return_value=rol_creado)

        # Ejecutar
        resultado = await service.create_rol(
            mock_db,
            nombre="admin",
            descripcion="Administrador del sistema"
        )

        # Verificar
        assert resultado is not None
        assert resultado.nombre == "Admin"  # Se normaliza a Title Case
        service.rol_repo.get_by_nombre.assert_called_once()
        service.rol_repo.create_rol.assert_called_once()


@pytest.mark.asyncio
async def test_create_rol_nombre_vacio():
    """
    Verifica que create_rol lanza excepción si el nombre está vacío.
    """
    mock_db = AsyncMock()

    with patch.object(RolService, '__init__', lambda x: None):
        service = RolService()
        service.rol_repo = MagicMock()

        # Verificar que lanza ValidationError
        with pytest.raises(ValidationError, match="Role name is required"):
            await service.create_rol(mock_db, nombre="   ")


@pytest.mark.asyncio
async def test_create_rol_nombre_muy_largo():
    """
    Verifica que create_rol lanza excepción si el nombre es muy largo.
    """
    mock_db = AsyncMock()

    nombre_largo = "A" * 51  # Más de 50 caracteres

    with patch.object(RolService, '__init__', lambda x: None):
        service = RolService()
        service.rol_repo = MagicMock()

        # Verificar que lanza ValidationError
        with pytest.raises(ValidationError, match="50 characters or less"):
            await service.create_rol(mock_db, nombre=nombre_largo)


@pytest.mark.asyncio
async def test_create_rol_duplicado():
    """
    Verifica que create_rol lanza excepción si el rol ya existe.
    """
    mock_db = AsyncMock()

    # Rol existente
    rol_existente = RolModel(id_rol=1, nombre="Admin")

    with patch.object(RolService, '__init__', lambda x: None):
        service = RolService()
        service.rol_repo = MagicMock()
        service.rol_repo.get_by_nombre = AsyncMock(return_value=rol_existente)

        # Verificar que lanza ValidationError
        with pytest.raises(ValidationError, match="already exists"):
            await service.create_rol(mock_db, nombre="admin")


@pytest.mark.asyncio
async def test_get_rol_by_id_success():
    """
    Verifica que get_rol_by_id obtiene un rol correctamente.
    """
    mock_db = AsyncMock()

    rol_esperado = RolModel(
        id_rol=1,
        nombre="Mesero",
        descripcion="Personal de servicio"
    )

    with patch.object(RolService, '__init__', lambda x: None):
        service = RolService()
        service.rol_repo = MagicMock()
        service.rol_repo.get_by_id = AsyncMock(return_value=rol_esperado)

        # Ejecutar
        resultado = await service.get_rol_by_id(mock_db, 1)

        # Verificar
        assert resultado is not None
        assert resultado.id_rol == 1
        assert resultado.nombre == "Mesero"
        service.rol_repo.get_by_id.assert_called_once_with(mock_db, 1)


@pytest.mark.asyncio
async def test_get_rol_by_id_not_found():
    """
    Verifica que get_rol_by_id lanza excepción cuando no encuentra el rol.
    """
    mock_db = AsyncMock()

    with patch.object(RolService, '__init__', lambda x: None):
        service = RolService()
        service.rol_repo = MagicMock()
        service.rol_repo.get_by_id = AsyncMock(return_value=None)

        # Verificar que lanza NotFoundError
        with pytest.raises(NotFoundError):
            await service.get_rol_by_id(mock_db, 999)
