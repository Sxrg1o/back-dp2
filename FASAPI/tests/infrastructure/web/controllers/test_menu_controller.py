"""
Tests for menu controller.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.infrastructure.web.controllers.menu_controller import router
from app.application.services.menu_service import MenuApplicationService
from app.infrastructure.web.dependencies.menu_dependencies import get_menu_service


@pytest.fixture
def mock_menu_service():
    """Mock menu service."""
    service = AsyncMock(spec=MenuApplicationService)
    return service


@pytest.fixture
def app(mock_menu_service):
    """Create test FastAPI app."""
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    
    # Override dependency
    app.dependency_overrides[get_menu_service] = lambda: mock_menu_service
    
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    with patch('app.core.config.settings.SCHEDULER_ENABLED', False):
        return TestClient(app)


class TestMenuController:
    """Test menu controller endpoints."""
    
    def test_get_full_menu_success(self, client, mock_menu_service):
        """Test successful full menu retrieval."""
        # Arrange
        expected_menu = {
            "items": [],
            "ingredientes": [],
            "platos": [],
            "bebidas": []
        }
        mock_menu_service.get_full_menu.return_value = expected_menu
        
        # Act
        response = client.get("/api/v1/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == expected_menu
        mock_menu_service.get_full_menu.assert_called_once()
    
    def test_get_menu_by_categories_success(self, client, mock_menu_service):
        """Test successful categorized menu retrieval."""
        # Arrange
        expected_menu = {
            "dietary_preferences": {"vegan": [], "gluten_free": [], "spicy": []},
            "ingredients": {"vegetables": [], "meats": [], "fruits": []},
            "dishes": {"appetizers": [], "main_courses": [], "desserts": []},
            "beverages": {"alcoholic": [], "non_alcoholic": []}
        }
        mock_menu_service.get_menu_by_categories.return_value = expected_menu
        
        # Act
        response = client.get("/api/v1/categories")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == expected_menu
        mock_menu_service.get_menu_by_categories.assert_called_once()
    
    def test_search_menu_items_success(self, client, mock_menu_service):
        """Test successful menu search."""
        # Arrange
        query = "pizza"
        expected_results = {
            "items": [],
            "ingredientes": [],
            "platos": [],
            "bebidas": []
        }
        mock_menu_service.search_menu_items.return_value = expected_results
        
        # Act
        response = client.get(f"/api/v1/search?query={query}")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == expected_results
        mock_menu_service.search_menu_items.assert_called_once_with(query)
    
    def test_search_menu_items_empty_query(self, client, mock_menu_service):
        """Test menu search with empty query."""
        # Act
        response = client.get("/api/v1/search?query=")
        
        # Assert
        assert response.status_code == 422  # Validation error
    
    def test_get_menu_statistics_success(self, client, mock_menu_service):
        """Test successful menu statistics retrieval."""
        # Arrange
        expected_stats = {
            "total_items": 100,
            "available_items": 85,
            "ingredients": 50,
            "dishes": 30,
            "beverages": 20,
            "low_stock": 5
        }
        mock_menu_service.get_menu_statistics.return_value = expected_stats
        
        # Act
        response = client.get("/api/v1/statistics")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == expected_stats
        mock_menu_service.get_menu_statistics.assert_called_once()
    
    def test_get_nutritional_summary_success(self, client, mock_menu_service):
        """Test successful nutritional summary retrieval."""
        # Arrange
        expected_summary = {
            "total_items": 100,
            "average_calories": 250.5,
            "average_proteins": 15.2,
            "average_sugars": 8.1,
            "high_protein_items": 25,
            "low_sugar_items": 40,
            "vegan_items": 30
        }
        mock_menu_service.get_nutritional_summary.return_value = expected_summary
        
        # Act
        response = client.get("/api/v1/nutrition")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == expected_summary
        mock_menu_service.get_nutritional_summary.assert_called_once()
    
    def test_menu_service_error_handling(self, client, mock_menu_service):
        """Test error handling when service raises exception."""
        # Arrange
        mock_menu_service.get_full_menu.side_effect = Exception("Service error")
        
        # Act
        response = client.get("/api/v1/")
        
        # Assert
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]