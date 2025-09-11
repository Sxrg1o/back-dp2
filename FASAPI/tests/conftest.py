"""
Pytest configuration and fixtures.
"""
import asyncio
import pytest
try:
    import pytest_asyncio
    PYTEST_ASYNCIO_AVAILABLE = True
except ImportError:
    PYTEST_ASYNCIO_AVAILABLE = False

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.config import settings
from app.core.dependencies import get_db
from app.models.base import Base


# Test database engine
test_engine = create_async_engine(
    settings.DATABASE_TEST_URL,
    echo=False,
)

# Test session maker
TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


if PYTEST_ASYNCIO_AVAILABLE:
    @pytest_asyncio.fixture
    async def db_session():
        """Create a test database session."""
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        async with TestSessionLocal() as session:
            yield session
        
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


    @pytest_asyncio.fixture
    async def client(db_session: AsyncSession):
        """Create a test client with database dependency override."""
        
        async def override_get_db():
            return db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
        
        app.dependency_overrides.clear()
else:
    # Fallback fixtures for when pytest-asyncio is not available
    @pytest.fixture
    def db_session():
        """Placeholder for db_session when pytest-asyncio is not available."""
        return None
    
    @pytest.fixture
    def client():
        """Placeholder for client when pytest-asyncio is not available."""
        return None


@pytest.fixture
def sample_mesa_data():
    """Sample mesa data for testing."""
    return {
        "numero": 1,
        "nombre": "Mesa Principal",
        "capacidad": 4,
        "ubicacion": "Terraza",
        "descripcion": "Mesa con vista al jardín",
        "activa": True,
    }


@pytest.fixture
def sample_mesa_update_data():
    """Sample mesa update data for testing."""
    return {
        "nombre": "Mesa Actualizada",
        "capacidad": 6,
        "ubicacion": "Interior",
        "descripcion": "Mesa renovada",
        "activa": True,
    }


def override_get_db(session: AsyncSession):
    """Helper function to override database dependency for synchronous tests."""
    async def _override():
        return session
    return _override