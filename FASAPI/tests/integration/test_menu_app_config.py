"""
Test FastAPI application configuration for menu module.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestMenuAppConfiguration:
    """Test menu module integration with FastAPI application."""
    
    def test_app_creation(self):
        """Test that the FastAPI app can be created successfully."""
        assert app is not None
        assert app.title == "Restaurant Platform API"
    
    def test_health_endpoint(self):
        """Test that health endpoint works."""
        with TestClient(app) as client:
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
    
    def test_menu_routes_registered(self):
        """Test that menu routes are properly registered."""
        with TestClient(app) as client:
            # Test that menu endpoints return proper responses (not 404)
            # Note: These may return 500 due to database issues, but should not be 404 (route not found)
            response = client.get("/api/v1/menu/")
            assert response.status_code != 404, "Menu route not found - routing configuration issue"
            
            response = client.get("/api/v1/menu/items/")
            assert response.status_code != 404, "Items route not found - routing configuration issue"
            
            response = client.get("/api/v1/menu/ingredientes/")
            assert response.status_code != 404, "Ingredientes route not found - routing configuration issue"
            
            response = client.get("/api/v1/menu/platos/")
            assert response.status_code != 404, "Platos route not found - routing configuration issue"
            
            response = client.get("/api/v1/menu/bebidas/")
            assert response.status_code != 404, "Bebidas route not found - routing configuration issue"
    
    def test_exception_handlers_configured(self):
        """Test that exception handlers are properly configured."""
        with TestClient(app) as client:
            # Test 404 handling
            response = client.get("/api/v1/nonexistent")
            assert response.status_code == 404
            data = response.json()
            assert "traceId" in data
            assert "timestamp" in data
            assert data["status"] == 404
    
    def test_middleware_configured(self):
        """Test that middleware is properly configured."""
        with TestClient(app) as client:
            # Test CORS middleware
            response = client.options("/api/v1/menu/")
            # Should handle OPTIONS request
            assert response.status_code in [200, 405]  # 405 if OPTIONS not explicitly handled
            
            # Test that requests go through middleware
            response = client.get("/health")
            assert response.status_code == 200
    
    def test_openapi_schema_generation(self):
        """Test that OpenAPI schema can be generated."""
        with TestClient(app) as client:
            response = client.get("/api/v1/openapi.json")
            assert response.status_code == 200
            schema = response.json()
            assert "openapi" in schema
            assert "paths" in schema
            
            # Check that menu paths are included
            paths = schema["paths"]
            menu_paths = [path for path in paths.keys() if "/menu" in path]
            assert len(menu_paths) > 0
    
    def test_docs_endpoints(self):
        """Test that documentation endpoints work."""
        with TestClient(app) as client:
            # Test Swagger UI
            response = client.get("/docs")
            assert response.status_code == 200
            
            # Test ReDoc
            response = client.get("/redoc")
            assert response.status_code == 200
    
    def test_menu_dependency_injection(self):
        """Test that menu dependencies can be resolved."""
        # This is a basic test to ensure the app starts without dependency injection errors
        with TestClient(app) as client:
            # If dependency injection is broken, these requests would fail with 500 errors
            response = client.get("/api/v1/menu/statistics")
            # Should not be a 500 error (dependency injection failure)
            assert response.status_code != 500
            
            response = client.get("/api/v1/menu/items/")
            assert response.status_code != 500
    
    def test_error_response_format(self):
        """Test that error responses follow the expected format."""
        with TestClient(app) as client:
            # Test validation error format
            response = client.post("/api/v1/menu/items/", json={})
            assert response.status_code == 422
            data = response.json()
            
            # Check error response structure
            assert "timestamp" in data
            assert "traceId" in data
            assert "status" in data
            assert "code" in data
            assert "message" in data
            assert data["status"] == 422
            assert data["code"] == "VALIDATION_ERROR"
    
    def test_menu_controllers_integration(self):
        """Test that all menu controllers are properly integrated."""
        with TestClient(app) as client:
            # Test each controller's main endpoint
            controllers_endpoints = [
                ("/api/v1/menu/", "MenuController"),
                ("/api/v1/menu/items/", "ItemController"),
                ("/api/v1/menu/ingredientes/", "IngredienteController"),
                ("/api/v1/menu/platos/", "PlatoController"),
                ("/api/v1/menu/bebidas/", "BebidaController")
            ]
            
            for endpoint, controller_name in controllers_endpoints:
                response = client.get(endpoint)
                # Should not be 404 (route not found) or 500 (controller error)
                assert response.status_code not in [404, 500], f"{controller_name} not properly integrated"