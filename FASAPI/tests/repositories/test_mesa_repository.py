"""
Mesa repository tests.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.mesa_repository import mesa_repository
from app.schemas.mesa import MesaCreate


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_mesa(db_session: AsyncSession, sample_mesa_data):
    """Test creating a mesa in repository."""
    
    mesa_create = MesaCreate(**sample_mesa_data)
    mesa = await mesa_repository.create(db_session, obj_in=mesa_create)
    
    assert mesa.numero == sample_mesa_data["numero"]
    assert mesa.nombre == sample_mesa_data["nombre"]
    assert mesa.id is not None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_mesa_by_numero(db_session: AsyncSession, sample_mesa_data):
    """Test getting mesa by number."""
    
    # Create mesa
    mesa_create = MesaCreate(**sample_mesa_data)
    created_mesa = await mesa_repository.create(db_session, obj_in=mesa_create)
    
    # Get by number
    retrieved_mesa = await mesa_repository.get_by_numero(
        db_session, sample_mesa_data["numero"]
    )
    
    assert retrieved_mesa is not None
    assert retrieved_mesa.id == created_mesa.id
    assert retrieved_mesa.numero == sample_mesa_data["numero"]


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_active_mesas(db_session: AsyncSession):
    """Test getting active mesas."""
    
    # Create active mesa
    active_mesa_data = {
        "numero": 1,
        "nombre": "Mesa Activa",
        "capacidad": 4,
        "activa": True,
    }
    mesa_create = MesaCreate(**active_mesa_data)
    await mesa_repository.create(db_session, obj_in=mesa_create)
    
    # Create inactive mesa
    inactive_mesa_data = {
        "numero": 2,
        "nombre": "Mesa Inactiva",
        "capacidad": 4,
        "activa": False,
    }
    mesa_create = MesaCreate(**inactive_mesa_data)
    await mesa_repository.create(db_session, obj_in=mesa_create)
    
    # Get active mesas
    active_mesas = await mesa_repository.get_active_mesas(db_session)
    
    assert len(active_mesas) == 1
    assert active_mesas[0].activa is True
    assert active_mesas[0].numero == 1


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_by_capacidad_range(db_session: AsyncSession):
    """Test getting mesas by capacity range."""
    
    # Create mesas with different capacities
    capacities = [2, 4, 6, 8]
    for i, capacity in enumerate(capacities):
        mesa_data = {
            "numero": i + 1,
            "nombre": f"Mesa {capacity} personas",
            "capacidad": capacity,
            "activa": True,
        }
        mesa_create = MesaCreate(**mesa_data)
        await mesa_repository.create(db_session, obj_in=mesa_create)
    
    # Get mesas with capacity between 4 and 6
    mesas = await mesa_repository.get_by_capacidad_range(db_session, 4, 6)
    
    assert len(mesas) == 2
    capacities_found = [mesa.capacidad for mesa in mesas]
    assert 4 in capacities_found
    assert 6 in capacities_found
    assert 2 not in capacities_found
    assert 8 not in capacities_found