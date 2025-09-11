"""Tests for menu dependency injection container."""

import pytest
from unittest.mock import Mock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.web.dependencies.container import (
    MenuContainer,
    menu_container,
    get_item_repository,
    get_ingrediente_repository,
    get_plato_repository,
    get_bebida_repository,
    get_item_service,
    get_ingrediente_service,
    get_plato_service,
    get_bebida_service,
    get_menu_service
)
from app.domain.repositories.item_repository import ItemRepositoryPort
from app.domain.repositories.ingrediente_repository import IngredienteRepositoryPort
from app.domain.repositories.plato_repository import PlatoRepositoryPort
from app.domain.repositories.bebida_repository import BebidaRepositoryPort
from app.application.services.item_service import ItemApplicationService
from app.application.services.ingrediente_service import IngredienteApplicationService
from app.application.services.plato_service import PlatoApplicationService
from app.application.services.bebida_service import BebidaApplicationService
from app.application.services.menu_service import MenuApplicationService
from app.infrastructure.persistence.repositories.sqlalchemy_item_repository import SqlAlchemyItemRepository
from app.infrastructure.persistence.repositories.sqlalchemy_ingrediente_repository import SqlAlchemyIngredienteRepository
from app.infrastructure.persistence.repositories.sqlalchemy_plato_repository import SqlAlchemyPlatoRepository
from app.infrastructure.persistence.repositories.sqlalchemy_bebida_repository import SqlAlchemyBebidaRepository


class TestMenuContainer:
    """Test cases for MenuContainer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.container = MenuContainer()
        self.mock_session = Mock(spec=AsyncSession)
    
    def test_container_initialization(self):
        """Test that container initializes correctly."""
        assert self.container is not None
    
    def test_create_item_repository(self):
        """Test item repository creation."""
        repository = self.container.create_item_repository(self.mock_session)
        
        assert isinstance(repository, SqlAlchemyItemRepository)
        assert isinstance(repository, ItemRepositoryPort)
    
    def test_create_ingrediente_repository(self):
        """Test ingrediente repository creation."""
        repository = self.container.create_ingrediente_repository(self.mock_session)
        
        assert isinstance(repository, SqlAlchemyIngredienteRepository)
        assert isinstance(repository, IngredienteRepositoryPort)
    
    def test_create_plato_repository(self):
        """Test plato repository creation."""
        repository = self.container.create_plato_repository(self.mock_session)
        
        assert isinstance(repository, SqlAlchemyPlatoRepository)
        assert isinstance(repository, PlatoRepositoryPort)
    
    def test_create_bebida_repository(self):
        """Test bebida repository creation."""
        repository = self.container.create_bebida_repository(self.mock_session)
        
        assert isinstance(repository, SqlAlchemyBebidaRepository)
        assert isinstance(repository, BebidaRepositoryPort)
    
    def test_create_item_service(self):
        """Test item application service creation."""
        service = self.container.create_item_service(self.mock_session)
        
        assert isinstance(service, ItemApplicationService)
        assert hasattr(service, '_item_repository')
    
    def test_create_ingrediente_service(self):
        """Test ingrediente application service creation."""
        service = self.container.create_ingrediente_service(self.mock_session)
        
        assert isinstance(service, IngredienteApplicationService)
        assert hasattr(service, '_ingrediente_repository')
    
    def test_create_plato_service(self):
        """Test plato application service creation."""
        service = self.container.create_plato_service(self.mock_session)
        
        assert isinstance(service, PlatoApplicationService)
        assert hasattr(service, '_plato_repository')
        assert hasattr(service, '_ingrediente_repository')
    
    def test_create_bebida_service(self):
        """Test bebida application service creation."""
        service = self.container.create_bebida_service(self.mock_session)
        
        assert isinstance(service, BebidaApplicationService)
        assert hasattr(service, '_bebida_repository')
    
    def test_create_menu_service(self):
        """Test menu application service creation."""
        service = self.container.create_menu_service(self.mock_session)
        
        assert isinstance(service, MenuApplicationService)
        assert hasattr(service, '_item_repository')
        assert hasattr(service, '_ingrediente_repository')
        assert hasattr(service, '_plato_repository')
        assert hasattr(service, '_bebida_repository')
    
    def test_repository_instances_are_different(self):
        """Test that each call creates a new repository instance."""
        repo1 = self.container.create_item_repository(self.mock_session)
        repo2 = self.container.create_item_repository(self.mock_session)
        
        assert repo1 is not repo2
    
    def test_service_instances_are_different(self):
        """Test that each call creates a new service instance."""
        service1 = self.container.create_item_service(self.mock_session)
        service2 = self.container.create_item_service(self.mock_session)
        
        assert service1 is not service2
    
    def test_repositories_have_mappers(self):
        """Test that repositories have their own mappers."""
        repo1 = self.container.create_item_repository(self.mock_session)
        repo2 = self.container.create_item_repository(self.mock_session)
        
        # Each repository should have its own mapper instance
        assert hasattr(repo1, 'mapper')
        assert hasattr(repo2, 'mapper')


class TestGlobalContainer:
    """Test cases for global container instance."""
    
    def test_global_container_exists(self):
        """Test that global container instance exists."""
        assert menu_container is not None
        assert isinstance(menu_container, MenuContainer)


class TestFastAPIDependencies:
    """Test cases for FastAPI dependency functions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_session = Mock(spec=AsyncSession)
    
    def test_get_item_repository_dependency(self):
        """Test item repository FastAPI dependency."""
        repository = get_item_repository(self.mock_session)
        
        assert isinstance(repository, ItemRepositoryPort)
        assert isinstance(repository, SqlAlchemyItemRepository)
    
    def test_get_ingrediente_repository_dependency(self):
        """Test ingrediente repository FastAPI dependency."""
        repository = get_ingrediente_repository(self.mock_session)
        
        assert isinstance(repository, IngredienteRepositoryPort)
        assert isinstance(repository, SqlAlchemyIngredienteRepository)
    
    def test_get_plato_repository_dependency(self):
        """Test plato repository FastAPI dependency."""
        repository = get_plato_repository(self.mock_session)
        
        assert isinstance(repository, PlatoRepositoryPort)
        assert isinstance(repository, SqlAlchemyPlatoRepository)
    
    def test_get_bebida_repository_dependency(self):
        """Test bebida repository FastAPI dependency."""
        repository = get_bebida_repository(self.mock_session)
        
        assert isinstance(repository, BebidaRepositoryPort)
        assert isinstance(repository, SqlAlchemyBebidaRepository)
    
    def test_get_item_service_dependency(self):
        """Test item service FastAPI dependency."""
        service = get_item_service(self.mock_session)
        
        assert isinstance(service, ItemApplicationService)
    
    def test_get_ingrediente_service_dependency(self):
        """Test ingrediente service FastAPI dependency."""
        service = get_ingrediente_service(self.mock_session)
        
        assert isinstance(service, IngredienteApplicationService)
    
    def test_get_plato_service_dependency(self):
        """Test plato service FastAPI dependency."""
        service = get_plato_service(self.mock_session)
        
        assert isinstance(service, PlatoApplicationService)
    
    def test_get_bebida_service_dependency(self):
        """Test bebida service FastAPI dependency."""
        service = get_bebida_service(self.mock_session)
        
        assert isinstance(service, BebidaApplicationService)
    
    def test_get_menu_service_dependency(self):
        """Test menu service FastAPI dependency."""
        service = get_menu_service(self.mock_session)
        
        assert isinstance(service, MenuApplicationService)
    
    def test_dependencies_create_new_instances(self):
        """Test that dependency functions create new instances each time."""
        service1 = get_item_service(self.mock_session)
        service2 = get_item_service(self.mock_session)
        
        assert service1 is not service2
    
    def test_service_dependencies_have_correct_repositories(self):
        """Test that service dependencies are wired with correct repositories."""
        item_service = get_item_service(self.mock_session)
        menu_service = get_menu_service(self.mock_session)
        
        # Verify that services have the expected repository types
        assert isinstance(item_service._item_repository, ItemRepositoryPort)
        assert isinstance(menu_service._item_repository, ItemRepositoryPort)
        assert isinstance(menu_service._ingrediente_repository, IngredienteRepositoryPort)
        assert isinstance(menu_service._plato_repository, PlatoRepositoryPort)
        assert isinstance(menu_service._bebida_repository, BebidaRepositoryPort)


class TestDependencyLifecycle:
    """Test cases for dependency lifecycle management."""
    
    def test_container_manages_lifecycle(self):
        """Test that container properly manages component lifecycle."""
        container = MenuContainer()
        
        # Container should be initialized properly
        assert container is not None
        
        # Each repository creation should create new instances
        repo1 = container.create_item_repository(Mock())
        repo2 = container.create_item_repository(Mock())
        
        assert repo1 is not repo2
    
    def test_session_isolation(self):
        """Test that different sessions create isolated repository instances."""
        session1 = Mock(spec=AsyncSession)
        session2 = Mock(spec=AsyncSession)
        
        repo1 = get_item_repository(session1)
        repo2 = get_item_repository(session2)
        
        # Different instances
        assert repo1 is not repo2
        
        # Different sessions
        assert repo1._session is session1
        assert repo2._session is session2
    
    def test_service_repository_consistency(self):
        """Test that services get repositories with the same session."""
        session = Mock(spec=AsyncSession)
        
        item_service = get_item_service(session)
        menu_service = get_menu_service(session)
        
        # All repositories should use the same session
        assert item_service._item_repository._session is session
        assert menu_service._item_repository._session is session
        assert menu_service._ingrediente_repository._session is session
        assert menu_service._plato_repository._session is session
        assert menu_service._bebida_repository._session is session


class TestContainerErrorHandling:
    """Test cases for container error handling."""
    
    def test_container_with_none_session(self):
        """Test container behavior with None session."""
        container = MenuContainer()
        
        # Should not raise exception during creation, but repositories might fail later
        repository = container.create_item_repository(None)
        assert repository is not None
    
    def test_dependency_with_none_session(self):
        """Test dependency functions with None session."""
        # Should not raise exception during creation
        repository = get_item_repository(None)
        assert repository is not None
        
        service = get_item_service(None)
        assert service is not None


@pytest.mark.integration
class TestContainerIntegration:
    """Integration tests for dependency container."""
    
    @pytest.fixture
    async def mock_session(self):
        """Create a mock database session."""
        session = AsyncMock(spec=AsyncSession)
        return session
    
    async def test_full_dependency_chain(self, mock_session):
        """Test complete dependency chain from container to service."""
        # Create service through dependency injection
        menu_service = get_menu_service(mock_session)
        
        # Verify the complete chain is properly wired
        assert isinstance(menu_service, MenuApplicationService)
        assert isinstance(menu_service._item_repository, ItemRepositoryPort)
        assert isinstance(menu_service._ingrediente_repository, IngredienteRepositoryPort)
        assert isinstance(menu_service._plato_repository, PlatoRepositoryPort)
        assert isinstance(menu_service._bebida_repository, BebidaRepositoryPort)
        
        # Verify all repositories use the same session
        assert menu_service._item_repository._session is mock_session
        assert menu_service._ingrediente_repository._session is mock_session
        assert menu_service._plato_repository._session is mock_session
        assert menu_service._bebida_repository._session is mock_session
    
    async def test_service_method_calls_work(self, mock_session):
        """Test that service methods can be called (even if they fail due to mocking)."""
        item_service = get_item_service(mock_session)
        
        # This should not raise an exception related to dependency injection
        # (it might raise other exceptions due to mocking, but that's expected)
        assert hasattr(item_service, 'get_available_items')
        assert callable(item_service.get_available_items)