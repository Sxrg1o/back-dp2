"""
Integration tests for menu module routing and middleware.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestMenuIntegration:
    """Integration tests for menu module."""
    
    def test_menu_routes_registered(self):
        """Test that menu routes are properly registered."""
        client = TestClient(app)
        
        # Test that menu endpoints exist (they may return errors due to missing DB, but should not return 404)
        menu_endpoints = [
            "/api/v1/menu/menu/statistics",
            "/api/v1/menu/items/",
            "/api/v1/menu/ingredientes/",
            "/api/v1/menu/platos/",
            "/api/v1/menu/bebidas/"
        ]
        
        for endpoint in menu_endpoints:
            response = client.get(endpoint)
            # Should not return 404 (route not found)
            assert response.status_code != 404, f"Route {endpoint} not found"
            # May return 500 due to missing database, but route should exist
            assert response.status_code in [200, 422, 500], f"Unexpected status for {endpoint}: {response.status_code}"
    
    def test_menu_openapi_schema(self):
        """Test that menu endpoints are included in OpenAPI schema."""
        client = TestClient(app)
        
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        
        openapi_schema = response.json()
        paths = openapi_schema.get("paths", {})
        
        # Check that menu paths are in the schema
        menu_paths = [path for path in paths.keys() if "/menu/" in path]
        assert len(menu_paths) > 0, "No menu paths found in OpenAPI schema"
        
        # Verify some key menu endpoints
        expected_paths = [
            "/api/v1/menu/menu/statistics",
            "/api/v1/menu/items/",
            "/api/v1/menu/ingredientes/",
            "/api/v1/menu/platos/",
            "/api/v1/menu/bebidas/"
        ]
        
        for expected_path in expected_paths:
            assert expected_path in paths, f"Expected path {expected_path} not found in OpenAPI schema"
    
    def test_menu_tags_in_openapi(self):
        """Test that menu operations are properly documented in OpenAPI schema."""
        client = TestClient(app)
        
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        
        openapi_schema = response.json()
        paths = openapi_schema.get("paths", {})
        
        # Check that menu paths have proper tags in their operations
        menu_paths = [path for path in paths.keys() if "/menu/" in path]
        assert len(menu_paths) > 0, "No menu paths found in OpenAPI schema"
        
        # Check that at least some menu operations have tags
        has_menu_tags = False
        for path, operations in paths.items():
            if "/menu/" in path:
                for method, operation in operations.items():
                    if isinstance(operation, dict) and "tags" in operation:
                        tags = operation["tags"]
                        if any(tag in ["menu", "items", "ingredientes", "platos", "bebidas"] for tag in tags):
                            has_menu_tags = True
                            break
        
        assert has_menu_tags, "Menu operations should have appropriate tags"
    
    def test_health_endpoint_still_works(self):
        """Test that existing endpoints still work after menu integration."""
        client = TestClient(app)
        
        response = client.get("/health")
        assert response.status_code == 200
        
        health_data = response.json()
        assert "status" in health_data
        assert health_data["status"] == "healthy"
    
    def test_middleware_works_with_menu_endpoints(self):
        """Test that middleware is properly applied to menu endpoints."""
        client = TestClient(app)
        
        # Test a menu endpoint to ensure middleware is applied
        response = client.get("/api/v1/menu/menu/statistics")
        
        # Should have CORS headers (if configured)
        # Should have proper error handling from exception middleware
        # May return 500 due to missing database, but should be properly handled
        if response.status_code >= 400:
            # Should have proper error response format from exception handlers
            error_data = response.json()
            # Should have either 'detail' (FastAPI default) or structured error format
            assert "detail" in error_data or "message" in error_data or "timestamp" in error_data
    
    def test_dependency_injection_setup(self):
        """Test that dependency injection is properly configured."""
        # This test verifies that the application can start without DI errors
        # If there were DI configuration issues, the app wouldn't start properly
        
        client = TestClient(app)
        
        # Test multiple menu endpoints to ensure services are properly injected
        endpoints = [
            "/api/v1/menu/items/",
            "/api/v1/menu/ingredientes/",
            "/api/v1/menu/platos/",
            "/api/v1/menu/bebidas/"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # Should not fail with dependency injection errors
            # May fail with business logic errors (500) but not DI errors (which would be different)
            assert response.status_code != 422, f"Validation error on GET {endpoint} suggests DI issues"
            
            if response.status_code >= 500:
                error_data = response.json()
                error_message = str(error_data.get("detail", "")).lower()
                # Should not contain dependency injection related errors
                assert "dependency" not in error_message
                assert "injection" not in error_message
                assert "container" not in error_message