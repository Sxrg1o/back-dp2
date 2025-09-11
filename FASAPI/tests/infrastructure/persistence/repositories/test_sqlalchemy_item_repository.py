"""Integration tests for SqlAlchemyItemRepository."""

import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.domain.entities.item import Item
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.infrastructure.persistence.models.base import Base
from app.infrastructure.persistence.repositories.sqlalchemy_item_repository import SqlAlchemyItemRepository


@pytest.fixture
async def async_session():
    """Create async session for testing."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session
    
    await engine.dispose()


@pytest.fixture
def sample_item():
    """Create sample item for testing."""
    return Item(
        id=uuid4(),
        nombre="Test Item",
        descripcion="Test description",
        precio=Precio(Decimal("15.99")),
        informacion_nutricional=InformacionNutricional(
            calorias=250,
            proteinas=12.5,
            azucares=5.0
        ),
        tiempo_preparacion=10,
        stock_actual=50,
        stock_minimo=10,
        etiquetas={EtiquetaItem.SIN_GLUTEN, EtiquetaItem.VEGANO},
        activo=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        version=1
    )


class TestSqlAlchemyItemRepository:
    """Test cases for SqlAlchemyItemRepository."""
    
    async def test_save_and_get_by_id(self, async_session: AsyncSession, sample_item: Item):
        """Test saving and retrieving item by ID."""
        # Arrange
        repository = SqlAlchemyItemRepository(async_session)
        
        # Act
        saved_item = await repository.save(sample_item)
        retrieved_item = await repository.get_by_id(saved_item.id)
        
        # Assert
        assert retrieved_item is not None
        assert retrieved_item.id == sample_item.id
        assert retrieved_item.nombre == sample_item.nombre
        assert retrieved_item.precio == sample_item.precio
        assert retrieved_item.etiquetas == sample_item.etiquetas
    
    async def test_get_available_items(self, async_session: AsyncSession, sample_item: Item):
        """Test getting available items."""
        # Arrange
        repository = SqlAlchemyItemRepository(async_session)
        await repository.save(sample_item)
        
        # Act
        available_items = await repository.get_available_items()
        
        # Assert
        assert len(available_items) == 1
        assert available_items[0].id == sample_item.id
    
    async def test_get_by_category(self, async_session: AsyncSession, sample_item: Item):
        """Test getting items by category."""
        # Arrange
        repository = SqlAlchemyItemRepository(async_session)
        await repository.save(sample_item)
        
        # Act
        vegan_items = await repository.get_by_category(EtiquetaItem.VEGANO)
        
        # Assert
        assert len(vegan_items) == 1
        assert vegan_items[0].id == sample_item.id
    
    async def test_exists_by_name(self, async_session: AsyncSession, sample_item: Item):
        """Test checking if item exists by name."""
        # Arrange
        repository = SqlAlchemyItemRepository(async_session)
        await repository.save(sample_item)
        
        # Act & Assert
        assert await repository.exists_by_name(sample_item.nombre) is True
        assert await repository.exists_by_name("Non-existent Item") is False
    
    async def test_delete(self, async_session: AsyncSession, sample_item: Item):
        """Test deleting item."""
        # Arrange
        repository = SqlAlchemyItemRepository(async_session)
        saved_item = await repository.save(sample_item)
        
        # Act
        deleted = await repository.delete(saved_item.id)
        retrieved_item = await repository.get_by_id(saved_item.id)
        
        # Assert
        assert deleted is True
        assert retrieved_item is None