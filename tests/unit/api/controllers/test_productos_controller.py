"""
Unit tests for ProductosController
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.main import app
from src.business_logic.menu.producto_service import ProductoService
from src.core.database import get_database_session


# Cliente de prueba
client = TestClient(app)


def test_create_product_success(cleanup_app):
    """
    Verifica que POST /api/v1/productos/ crea un producto correctamente.
    """
    # Mock del servicio
    mock_service = AsyncMock()
    mock_service.create_product = AsyncMock(return_value={
        "id_producto": 1,
        "nombre": "Pizza Margherita",
        "precio_base": 15.0,
        "id_categoria": 1,
        "disponible": True
    })

    # Override de la dependencia del servicio
    # Nota: Necesitamos reemplazar la instancia global producto_service
    with patch('src.api.controllers.productos_controller.producto_service', mock_service):
        # Mock de la sesión de BD
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.post("/api/v1/productos/", json={
            "nombre": "Pizza Margherita",
            "precio_base": 15.0,
            "id_categoria": 1,
            "descripcion": "Pizza clásica"
        })

        # Verificar
        assert response.status_code == 201
        assert response.json()["nombre"] == "Pizza Margherita"


def test_create_product_categoria_not_found(cleanup_app):
    """
    Verifica que POST /api/v1/productos/ retorna 404 si la categoría no existe.
    """
    from src.business_logic.exceptions.menu_exceptions import CategoriaNotFoundError

    # Mock del servicio que lanza excepción
    mock_service = AsyncMock()
    mock_service.create_product = AsyncMock(
        side_effect=CategoriaNotFoundError("Category not found")
    )

    with patch('src.api.controllers.productos_controller.producto_service', mock_service):
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.post("/api/v1/productos/", json={
            "nombre": "Pizza Test",
            "precio_base": 15.0,
            "id_categoria": 999
        })

        # Verificar
        assert response.status_code == 404


def test_get_products(cleanup_app):
    """
    Verifica que GET /api/v1/productos/ lista productos correctamente.
    """
    # Mock del servicio
    mock_service = AsyncMock()
    mock_service.search_products = AsyncMock(return_value={
        "items": [
            {"id_producto": 1, "nombre": "Pizza 1", "precio_base": 10.0},
            {"id_producto": 2, "nombre": "Pizza 2", "precio_base": 12.0}
        ],
        "total": 2,
        "page": 1,
        "per_page": 10
    })

    with patch('src.api.controllers.productos_controller.producto_service', mock_service):
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.get("/api/v1/productos/")

        # Verificar
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 2


def test_get_product_by_id_success(cleanup_app):
    """
    Verifica que GET /api/v1/productos/{id} obtiene un producto correctamente.
    """
    # Mock del servicio
    mock_service = AsyncMock()
    mock_service.get_product_by_id = AsyncMock(return_value={
        "id_producto": 1,
        "nombre": "Pizza Especial",
        "precio_base": 20.0,
        "disponible": True
    })

    with patch('src.api.controllers.productos_controller.producto_service', mock_service):
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.get("/api/v1/productos/1")

        # Verificar
        assert response.status_code == 200
        assert response.json()["id_producto"] == 1
        assert response.json()["nombre"] == "Pizza Especial"


def test_get_product_by_id_not_found(cleanup_app):
    """
    Verifica que GET /api/v1/productos/{id} retorna 404 si no existe.
    """
    from src.business_logic.exceptions.menu_exceptions import ProductoNotFoundError

    # Mock del servicio que lanza excepción
    mock_service = AsyncMock()
    mock_service.get_product_by_id = AsyncMock(
        side_effect=ProductoNotFoundError("Product not found")
    )

    with patch('src.api.controllers.productos_controller.producto_service', mock_service):
        async def mock_db():
            yield AsyncMock()

        app.dependency_overrides[get_database_session] = mock_db

        # Ejecutar
        response = client.get("/api/v1/productos/999")

        # Verificar
        assert response.status_code == 404
