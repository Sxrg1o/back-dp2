"""
Pruebas unitarias para el servicio de usuarios y autenticación.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from ulid import ULID
from datetime import datetime

from src.business_logic.auth.usuario_service import UsuarioService
from src.models.auth.usuario_model import UsuarioModel
from src.models.auth.rol_model import RolModel
from src.api.schemas.usuario_schema import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
)
from src.business_logic.exceptions.usuario_exceptions import (
    UsuarioValidationError,
    UsuarioNotFoundError,
    UsuarioConflictError,
    InvalidCredentialsError,
    InactiveUserError,
)
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def mock_repository():
    """Fixture que proporciona un mock del repositorio de usuarios."""
    repository = AsyncMock()
    return repository


@pytest.fixture
def mock_rol_repository():
    """Fixture que proporciona un mock del repositorio de roles."""
    repository = AsyncMock()
    return repository


@pytest.fixture
def usuario_service(mock_repository, mock_rol_repository):
    """Fixture que proporciona una instancia del servicio de usuarios con repositorios mockeados."""
    service = UsuarioService(AsyncMock())
    service.repository = mock_repository
    service.rol_repository = mock_rol_repository
    return service


@pytest.fixture
def sample_rol_data():
    """Fixture que proporciona datos de muestra para un rol."""
    return {
        "id": str(ULID()),
        "nombre": "Admin",
        "descripcion": "Administrador del sistema",
        "activo": True,
        "fecha_creacion": datetime.now(),
        "fecha_modificacion": datetime.now(),
    }


@pytest.fixture
def sample_usuario_data(sample_rol_data):
    """Fixture que proporciona datos de muestra para un usuario."""
    from src.core.security import security
    
    return {
        "id": str(ULID()),
        "email": "test@example.com",
        "password_hash": security.get_password_hash("password123"),
        "nombre": "Usuario Test",
        "telefono": "123456789",
        "activo": True,
        "id_rol": sample_rol_data["id"],
        "ultimo_acceso": None,
        "fecha_creacion": datetime.now(),
        "fecha_modificacion": datetime.now(),
    }


@pytest.mark.asyncio
async def test_login_success(usuario_service, mock_repository, sample_usuario_data, sample_rol_data):
    """Prueba el login exitoso de un usuario."""
    # Arrange
    login_request = LoginRequest(email="test@example.com", password="password123")
    
    rol_model = RolModel(**sample_rol_data)
    usuario_model = UsuarioModel(**sample_usuario_data)
    usuario_model.rol = rol_model
    
    mock_repository.get_by_email.return_value = usuario_model
    mock_repository.update_ultimo_acceso.return_value = usuario_model
    
    # Act
    result = await usuario_service.login(login_request)
    
    # Assert
    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.token_type == "bearer"
    assert result.usuario.email == "test@example.com"
    mock_repository.get_by_email.assert_called_once_with("test@example.com")
    mock_repository.update_ultimo_acceso.assert_called_once()


@pytest.mark.asyncio
async def test_login_invalid_credentials(usuario_service, mock_repository):
    """Prueba el login con credenciales inválidas."""
    # Arrange
    login_request = LoginRequest(email="test@example.com", password="wrongpassword")
    mock_repository.get_by_email.return_value = None
    
    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await usuario_service.login(login_request)


@pytest.mark.asyncio
async def test_login_inactive_user(usuario_service, mock_repository, sample_usuario_data):
    """Prueba el login de un usuario inactivo."""
    # Arrange
    login_request = LoginRequest(email="test@example.com", password="password123")
    sample_usuario_data["activo"] = False
    usuario_model = UsuarioModel(**sample_usuario_data)
    mock_repository.get_by_email.return_value = usuario_model
    
    # Act & Assert
    with pytest.raises(InactiveUserError):
        await usuario_service.login(login_request)


@pytest.mark.asyncio
async def test_register_success(usuario_service, mock_repository, mock_rol_repository, sample_rol_data):
    """Prueba el registro exitoso de un usuario."""
    # Arrange
    register_request = RegisterRequest(
        email="newuser@example.com",
        password="password123",
        nombre="Nuevo Usuario",
        telefono="987654321",
        id_rol=sample_rol_data["id"],
    )
    
    rol_model = RolModel(**sample_rol_data)
    mock_rol_repository.get_by_id.return_value = rol_model
    mock_repository.get_by_email.return_value = None
    
    new_usuario_data = {
        "id": str(ULID()),
        "email": register_request.email,
        "password_hash": "hashed_password",
        "nombre": register_request.nombre,
        "telefono": register_request.telefono,
        "activo": True,
        "id_rol": register_request.id_rol,
        "ultimo_acceso": None,
        "fecha_creacion": datetime.now(),
        "fecha_modificacion": datetime.now(),
    }
    new_usuario = UsuarioModel(**new_usuario_data)
    new_usuario.rol = rol_model
    mock_repository.create.return_value = new_usuario
    
    # Act
    result = await usuario_service.register(register_request)
    
    # Assert
    assert result.usuario.email == register_request.email
    assert result.message == "Usuario registrado exitosamente"
    mock_rol_repository.get_by_id.assert_called_once_with(sample_rol_data["id"])
    mock_repository.get_by_email.assert_called_once_with(register_request.email)


@pytest.mark.asyncio
async def test_register_email_exists(usuario_service, mock_repository, sample_usuario_data):
    """Prueba el registro con email duplicado."""
    # Arrange
    register_request = RegisterRequest(
        email="test@example.com",
        password="password123",
        nombre="Usuario",
        id_rol=str(ULID()),
    )
    
    usuario_model = UsuarioModel(**sample_usuario_data)
    mock_repository.get_by_email.return_value = usuario_model
    
    # Act & Assert
    with pytest.raises(UsuarioConflictError):
        await usuario_service.register(register_request)


@pytest.mark.asyncio
async def test_refresh_token_success(usuario_service, mock_repository, sample_usuario_data, sample_rol_data):
    """Prueba la renovación exitosa del token."""
    # Arrange
    from src.core.security import security
    
    token_data = {"sub": sample_usuario_data["id"], "email": sample_usuario_data["email"], "rol_id": sample_usuario_data["id_rol"]}
    refresh_token = security.create_refresh_token(token_data)
    refresh_request = RefreshTokenRequest(refresh_token=refresh_token)
    
    rol_model = RolModel(**sample_rol_data)
    usuario_model = UsuarioModel(**sample_usuario_data)
    usuario_model.rol = rol_model
    mock_repository.get_by_id.return_value = usuario_model
    
    # Act
    result = await usuario_service.refresh_token(refresh_request)
    
    # Assert
    assert result.access_token is not None
    assert result.token_type == "bearer"
    mock_repository.get_by_id.assert_called_once_with(sample_usuario_data["id"])


@pytest.mark.asyncio
async def test_refresh_token_invalid(usuario_service):
    """Prueba la renovación con token inválido."""
    # Arrange
    refresh_request = RefreshTokenRequest(refresh_token="invalid_token")
    
    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await usuario_service.refresh_token(refresh_request)

