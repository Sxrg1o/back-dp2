"""
End-to-end tests for menu module integration.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app.main import app
from app.core.dependencies import get_db
from tests.conftest import override_get_db


class TestMenuE2E:
    """End-to-end tests for menu module."""
    
    @pytest.fixture
    def client(self, db_session: AsyncSession):
        """Create test client with database override."""
        app.dependency_overrides[get_db] = lambda: override_get_db(db_session)
        with TestClient(app) as client:
            yield client
        app.dependency_overrides.clear()
    
    def test_health_check(self, client: TestClient):
        """Test that health check endpoint works."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_menu_endpoints_integration(self, client: TestClient):
        """Test complete menu endpoints integration."""
        # Test get full menu
        response = client.get("/api/v1/menu/")
        assert response.status_code == 200
        menu_data = response.json()
        assert isinstance(menu_data, dict)
        
        # Test get menu by categories
        response = client.get("/api/v1/menu/categories")
        assert response.status_code == 200
        categories_data = response.json()
        assert isinstance(categories_data, dict)
        
        # Test search menu items
        response = client.get("/api/v1/menu/search?query=test")
        assert response.status_code == 200
        search_data = response.json()
        assert isinstance(search_data, dict)
        
        # Test menu statistics
        response = client.get("/api/v1/menu/statistics")
        assert response.status_code == 200
        stats_data = response.json()
        assert isinstance(stats_data, dict)
        
        # Test nutritional summary
        response = client.get("/api/v1/menu/nutrition")
        assert response.status_code == 200
        nutrition_data = response.json()
        assert isinstance(nutrition_data, dict)
    
    def test_item_crud_integration(self, client: TestClient):
        """Test complete item CRUD operations."""
        # Create item
        item_data = {
            "nombre": "Test Item E2E",
            "descripcion": "Test item for E2E testing",
            "precio": 15.99,
            "informacion_nutricional": {
                "calorias": 250,
                "proteinas": 12.5,
                "azucares": 5.0
            },
            "tiempo_preparacion": 15,
            "stock": 10,
            "disponible": True,
            "etiquetas": ["SIN_GLUTEN", "VEGANO"]
        }
        
        response = client.post("/api/v1/menu/items/", json=item_data)
        assert response.status_code == 201
        created_item = response.json()
        item_id = created_item["id"]
        
        # Get item by ID
        response = client.get(f"/api/v1/menu/items/{item_id}")
        assert response.status_code == 200
        retrieved_item = response.json()
        assert retrieved_item["nombre"] == item_data["nombre"]
        
        # Update item
        update_data = {
            "nombre": "Updated Test Item E2E",
            "precio": 18.99
        }
        response = client.put(f"/api/v1/menu/items/{item_id}", json=update_data)
        assert response.status_code == 200
        updated_item = response.json()
        assert updated_item["nombre"] == update_data["nombre"]
        assert updated_item["precio"] == update_data["precio"]
        
        # Get all items
        response = client.get("/api/v1/menu/items/")
        assert response.status_code == 200
        items_list = response.json()
        assert isinstance(items_list, list)
        
        # Delete item
        response = client.delete(f"/api/v1/menu/items/{item_id}")
        assert response.status_code == 204
        
        # Verify item is deleted
        response = client.get(f"/api/v1/menu/items/{item_id}")
        assert response.status_code == 404
    
    def test_ingrediente_crud_integration(self, client: TestClient):
        """Test complete ingrediente CRUD operations."""
        # Create ingrediente
        ingrediente_data = {
            "nombre": "Test Ingredient E2E",
            "descripcion": "Test ingredient for E2E testing",
            "precio": 5.99,
            "informacion_nutricional": {
                "calorias": 50,
                "proteinas": 2.0,
                "azucares": 1.0
            },
            "tiempo_preparacion": 5,
            "stock": 100,
            "disponible": True,
            "etiquetas": ["VERDURA"],
            "peso": 0.5,
            "tipo": "VERDURA",
            "fecha_vencimiento": "2024-12-31"
        }
        
        response = client.post("/api/v1/menu/ingredientes/", json=ingrediente_data)
        assert response.status_code == 201
        created_ingrediente = response.json()
        ingrediente_id = created_ingrediente["id"]
        
        # Get ingrediente by ID
        response = client.get(f"/api/v1/menu/ingredientes/{ingrediente_id}")
        assert response.status_code == 200
        retrieved_ingrediente = response.json()
        assert retrieved_ingrediente["nombre"] == ingrediente_data["nombre"]
        
        # Update stock
        stock_data = {"cantidad": 50}
        response = client.patch(f"/api/v1/menu/ingredientes/{ingrediente_id}/stock", json=stock_data)
        assert response.status_code == 200
        
        # Get all ingredientes
        response = client.get("/api/v1/menu/ingredientes/")
        assert response.status_code == 200
        ingredientes_list = response.json()
        assert isinstance(ingredientes_list, list)
        
        # Delete ingrediente
        response = client.delete(f"/api/v1/menu/ingredientes/{ingrediente_id}")
        assert response.status_code == 204
    
    def test_plato_crud_integration(self, client: TestClient):
        """Test complete plato CRUD operations."""
        # First create an ingredient for the recipe
        ingrediente_data = {
            "nombre": "Recipe Ingredient",
            "descripcion": "Ingredient for recipe",
            "precio": 3.99,
            "informacion_nutricional": {
                "calorias": 30,
                "proteinas": 1.5,
                "azucares": 0.5
            },
            "tiempo_preparacion": 2,
            "stock": 50,
            "disponible": True,
            "etiquetas": ["VERDURA"],
            "peso": 0.2,
            "tipo": "VERDURA",
            "fecha_vencimiento": "2024-12-31"
        }
        
        response = client.post("/api/v1/menu/ingredientes/", json=ingrediente_data)
        assert response.status_code == 201
        ingrediente = response.json()
        ingrediente_id = ingrediente["id"]
        
        # Create plato
        plato_data = {
            "nombre": "Test Dish E2E",
            "descripcion": "Test dish for E2E testing",
            "precio": 25.99,
            "informacion_nutricional": {
                "calorias": 400,
                "proteinas": 20.0,
                "azucares": 8.0
            },
            "tiempo_preparacion": 25,
            "stock": 5,
            "disponible": True,
            "etiquetas": ["ENTRADA"],
            "receta": {
                "ingredientes": [
                    {
                        "ingrediente_id": ingrediente_id,
                        "cantidad": 2.0
                    }
                ],
                "instrucciones": "Test cooking instructions",
                "tiempo_coccion": 20
            },
            "tipo_plato": "ENTRADA"
        }
        
        response = client.post("/api/v1/menu/platos/", json=plato_data)
        assert response.status_code == 201
        created_plato = response.json()
        plato_id = created_plato["id"]
        
        # Get plato by ID
        response = client.get(f"/api/v1/menu/platos/{plato_id}")
        assert response.status_code == 200
        retrieved_plato = response.json()
        assert retrieved_plato["nombre"] == plato_data["nombre"]
        
        # Get all platos
        response = client.get("/api/v1/menu/platos/")
        assert response.status_code == 200
        platos_list = response.json()
        assert isinstance(platos_list, list)
        
        # Delete plato
        response = client.delete(f"/api/v1/menu/platos/{plato_id}")
        assert response.status_code == 204
        
        # Clean up ingredient
        response = client.delete(f"/api/v1/menu/ingredientes/{ingrediente_id}")
        assert response.status_code == 204
    
    def test_bebida_crud_integration(self, client: TestClient):
        """Test complete bebida CRUD operations."""
        # Create bebida
        bebida_data = {
            "nombre": "Test Beverage E2E",
            "descripcion": "Test beverage for E2E testing",
            "precio": 8.99,
            "informacion_nutricional": {
                "calorias": 150,
                "proteinas": 0.0,
                "azucares": 35.0
            },
            "tiempo_preparacion": 3,
            "stock": 20,
            "disponible": True,
            "etiquetas": ["FRIO"],
            "volumen": 0.5,
            "contenido_alcohol": 0.0
        }
        
        response = client.post("/api/v1/menu/bebidas/", json=bebida_data)
        assert response.status_code == 201
        created_bebida = response.json()
        bebida_id = created_bebida["id"]
        
        # Get bebida by ID
        response = client.get(f"/api/v1/menu/bebidas/{bebida_id}")
        assert response.status_code == 200
        retrieved_bebida = response.json()
        assert retrieved_bebida["nombre"] == bebida_data["nombre"]
        
        # Get all bebidas
        response = client.get("/api/v1/menu/bebidas/")
        assert response.status_code == 200
        bebidas_list = response.json()
        assert isinstance(bebidas_list, list)
        
        # Delete bebida
        response = client.delete(f"/api/v1/menu/bebidas/{bebida_id}")
        assert response.status_code == 204
    
    def test_error_handling_integration(self, client: TestClient):
        """Test error handling across menu endpoints."""
        # Test 404 for non-existent item
        non_existent_id = str(uuid4())
        response = client.get(f"/api/v1/menu/items/{non_existent_id}")
        assert response.status_code == 404
        error_data = response.json()
        assert "traceId" in error_data
        assert error_data["status"] == 404
        assert "ITEMNOTFOUNDERROR" in error_data["code"]
        
        # Test validation error
        invalid_item_data = {
            "nombre": "",  # Invalid empty name
            "precio": -5.0  # Invalid negative price
        }
        response = client.post("/api/v1/menu/items/", json=invalid_item_data)
        assert response.status_code == 422
        error_data = response.json()
        assert error_data["status"] == 422
        assert "VALIDATION_ERROR" in error_data["code"]
        
        # Test search with empty query
        response = client.get("/api/v1/menu/search")
        assert response.status_code == 422  # Missing required query parameter
    
    def test_middleware_integration(self, client: TestClient):
        """Test that middleware works correctly with menu endpoints."""
        # Test request ID middleware
        response = client.get("/api/v1/menu/")
        assert response.status_code == 200
        # Request ID should be added by middleware (check in logs or headers if exposed)
        
        # Test CORS middleware (if configured)
        response = client.options("/api/v1/menu/")
        # Should handle OPTIONS request properly
        
        # Test that all menu endpoints work with middleware
        endpoints_to_test = [
            "/api/v1/menu/",
            "/api/v1/menu/categories",
            "/api/v1/menu/statistics",
            "/api/v1/menu/nutrition",
            "/api/v1/menu/items/",
            "/api/v1/menu/ingredientes/",
            "/api/v1/menu/platos/",
            "/api/v1/menu/bebidas/"
        ]
        
        for endpoint in endpoints_to_test:
            response = client.get(endpoint)
            # Should not fail due to middleware issues
            assert response.status_code in [200, 422]  # 422 for missing query params
    
    def test_database_session_management(self, client: TestClient):
        """Test that database sessions are properly managed."""
        # Create multiple concurrent requests to test session handling
        responses = []
        
        # Make multiple requests
        for i in range(5):
            response = client.get("/api/v1/menu/statistics")
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Test that sessions are properly closed (no connection leaks)
        # This is more of a smoke test - real testing would require monitoring connections
        response = client.get("/api/v1/menu/")
        assert response.status_code == 200
    
    def test_dependency_injection_integration(self, client: TestClient):
        """Test that dependency injection works correctly."""
        # Test that services are properly injected and work
        response = client.get("/api/v1/menu/statistics")
        assert response.status_code == 200
        
        # Test that repositories are properly injected
        response = client.get("/api/v1/menu/items/")
        assert response.status_code == 200
        
        # Test that all controllers can access their dependencies
        controllers_endpoints = [
            "/api/v1/menu/",  # MenuController
            "/api/v1/menu/items/",  # ItemController
            "/api/v1/menu/ingredientes/",  # IngredienteController
            "/api/v1/menu/platos/",  # PlatoController
            "/api/v1/menu/bebidas/"  # BebidaController
        ]
        
        for endpoint in controllers_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200