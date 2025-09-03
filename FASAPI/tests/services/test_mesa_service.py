"""
Mesa service tests.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ConflictError
from app.schemas.base import PaginationParams
from app.schemas.mesa import MesaCreate, MesaUpdate
from app.services.mesa_service import mesa_service


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_mesa(db_session: AsyncSession, sample_mesa_data):
    """Test creating a new mesa."""
    
    mesa_create = MesaCreate(**sample_mesa_data)
    mesa = await mesa_service.create_mesa(db_session, mesa_create)
    
    assert mesa.numero == sample_mesa_data["numero"]
    assert mesa.nombre == sample_mesa_data["nombre"]
    assert mesa.capacidad == sample_mesa_data["capacidad"]
    assert mesa.activa == sample_mesa_data["activa"]


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_mesa_duplicate_number(db_session: AsyncSession, sample_mesa_data):
    """Test creating mesa with duplicate number raises conflict error."""
    
    # Create first mesa
    mesa_create = MesaCreate(**sample_mesa_data)
    await mesa_service.create_mesa(db_session, mesa_create)
    
    # Try to create another mesa with same number
    with pytest.raises(ConflictError):
        await mesa_service.create_mesa(db_session, mesa_create)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_mesa(db_session: AsyncSession, sample_mesa_data):
    """Test getting mesa by ID."""
    
    # Create mesa
    mesa_create = MesaCreate(**sample_mesa_data)
    created_mesa = await mesa_service.create_mesa(db_session, mesa_create)
    
    # Get mesa
    retrieved_mesa = await mesa_service.get_mesa(db_session, created_mesa.id)
    
    assert retrieved_mesa.id == created_mesa.id
    assert retrieved_mesa.numero == sample_mesa_data["numero"]


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_mesa_not_found(db_session: AsyncSession):
    """Test getting non-existent mesa raises not found error."""
    
    import uuid
    fake_id = uuid.uuid4()
    
    with pytest.raises(NotFoundError):
        await mesa_service.get_mesa(db_session, fake_id)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_mesa_by_numero(db_session: AsyncSession, sample_mesa_data):
    """Test getting mesa by number."""
    
    # Create mesa
    mesa_create = MesaCreate(**sample_mesa_data)
    created_mesa = await mesa_service.create_mesa(db_session, mesa_create)
    
    # Get mesa by number
    retrieved_mesa = await mesa_service.get_mesa_by_numero(
        db_session, sample_mesa_data["numero"]
    )
    
    assert retrieved_mesa.id == created_mesa.id
    assert retrieved_mesa.numero == sample_mesa_data["numero"]


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_mesa(db_session: AsyncSession, sample_mesa_data, sample_mesa_update_data):
    """Test updating a mesa."""
    
    # Create mesa
    mesa_create = MesaCreate(**sample_mesa_data)
    created_mesa = await mesa_service.create_mesa(db_session, mesa_create)
    
    # Update mesa
    mesa_update = MesaUpdate(**sample_mesa_update_data)
    updated_mesa = await mesa_service.update_mesa(
        db_session, created_mesa.id, mesa_update
    )
    
    assert updated_mesa.id == created_mesa.id
    assert updated_mesa.nombre == sample_mesa_update_data["nombre"]
    assert updated_mesa.capacidad == sample_mesa_update_data["capacidad"]
    assert updated_mesa.version == created_mesa.version + 1


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_mesas_paginated(db_session: AsyncSession):
    """Test getting paginated mesas."""
    
    # Create multiple mesas
    for i in range(5):
        mesa_data = {
            "numero": i + 1,
            "nombre": f"Mesa {i + 1}",
            "capacidad": 4,
            "activa": True,
        }
        mesa_create = MesaCreate(**mesa_data)
        await mesa_service.create_mesa(db_session, mesa_create)
    
    # Get paginated results
    pagination = PaginationParams(page=0, size=3)
    result = await mesa_service.get_mesas(db_session, pagination)
    
    assert len(result.content) == 3
    assert result.total_elements == 5
    assert result.total_pages == 2
    assert result.page == 0
    assert result.size == 3


@pytest.mark.asyncio
@pytest.mark.unit
async def test_delete_mesa(db_session: AsyncSession, sample_mesa_data):
    """Test deleting a mesa."""
    
    # Create mesa
    mesa_create = MesaCreate(**sample_mesa_data)
    created_mesa = await mesa_service.create_mesa(db_session, mesa_create)
    
    # Delete mesa
    deleted_mesa = await mesa_service.delete_mesa(db_session, created_mesa.id)
    
    assert deleted_mesa.id == created_mesa.id
    
    # Verify mesa is deleted
    with pytest.raises(NotFoundError):
        await mesa_service.get_mesa(db_session, created_mesa.id)