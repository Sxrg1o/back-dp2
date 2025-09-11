"""Tests for repository interfaces."""

import pytest
from abc import ABC
from uuid import UUID
from typing import get_type_hints

from app.domain.repositories.item_repository import ItemRepositoryPort
from app.domain.repositories.ingrediente_repository import IngredienteRepositoryPort
from app.domain.repositories.plato_repository import PlatoRepositoryPort
from app.domain.repositories.bebida_repository import BebidaRepositoryPort


class TestRepositoryInterfaces:
    """Test repository interface definitions."""
    
    def test_item_repository_is_abstract(self):
        """Test that ItemRepositoryPort is an abstract base class."""
        assert issubclass(ItemRepositoryPort, ABC)
        
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            ItemRepositoryPort()
    
    def test_ingrediente_repository_is_abstract(self):
        """Test that IngredienteRepositoryPort is an abstract base class."""
        assert issubclass(IngredienteRepositoryPort, ABC)
        
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            IngredienteRepositoryPort()
    
    def test_plato_repository_is_abstract(self):
        """Test that PlatoRepositoryPort is an abstract base class."""
        assert issubclass(PlatoRepositoryPort, ABC)
        
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            PlatoRepositoryPort()
    
    def test_bebida_repository_is_abstract(self):
        """Test that BebidaRepositoryPort is an abstract base class."""
        assert issubclass(BebidaRepositoryPort, ABC)
        
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            BebidaRepositoryPort()
    
    def test_item_repository_has_required_methods(self):
        """Test that ItemRepositoryPort has all required methods."""
        required_methods = [
            'get_by_id', 'get_available_items', 'get_by_category', 'get_all',
            'get_by_name', 'get_low_stock_items', 'get_by_price_range',
            'save', 'delete', 'exists_by_id', 'exists_by_name',
            'count_total', 'count_available'
        ]
        
        for method_name in required_methods:
            assert hasattr(ItemRepositoryPort, method_name)
            method = getattr(ItemRepositoryPort, method_name)
            assert callable(method)
    
    def test_ingrediente_repository_has_required_methods(self):
        """Test that IngredienteRepositoryPort has all required methods."""
        required_methods = [
            'get_by_id', 'get_by_type', 'get_all', 'get_available',
            'check_stock', 'update_stock', 'get_by_supplier',
            'get_expiring_soon', 'get_expired', 'get_low_stock',
            'get_by_name', 'get_by_unit_measure', 'save', 'delete',
            'exists_by_id', 'exists_by_name', 'bulk_update_stock',
            'get_total_weight_by_type'
        ]
        
        for method_name in required_methods:
            assert hasattr(IngredienteRepositoryPort, method_name)
            method = getattr(IngredienteRepositoryPort, method_name)
            assert callable(method)
    
    def test_plato_repository_has_required_methods(self):
        """Test that PlatoRepositoryPort has all required methods."""
        required_methods = [
            'get_by_id', 'get_by_dish_type', 'get_with_ingredients',
            'get_all', 'get_available', 'get_by_difficulty', 'get_by_chef',
            'get_by_preparation_time', 'get_by_portions', 'get_using_ingredient',
            'get_by_name', 'get_vegetarian', 'get_vegan', 'get_gluten_free',
            'save', 'delete', 'exists_by_id', 'exists_by_name',
            'get_recipe_ingredients', 'check_ingredient_availability',
            'get_most_popular'
        ]
        
        for method_name in required_methods:
            assert hasattr(PlatoRepositoryPort, method_name)
            method = getattr(PlatoRepositoryPort, method_name)
            assert callable(method)
    
    def test_bebida_repository_has_required_methods(self):
        """Test that BebidaRepositoryPort has all required methods."""
        required_methods = [
            'get_by_id', 'get_alcoholic', 'get_non_alcoholic', 'get_all',
            'get_available', 'get_by_type', 'get_by_temperature',
            'get_by_volume_range', 'get_by_alcohol_range', 'get_by_brand',
            'get_by_origin', 'get_by_name', 'get_cold_beverages',
            'get_hot_beverages', 'get_standard_volumes', 'get_suitable_for_minors',
            'get_by_volume_category', 'save', 'delete', 'exists_by_id',
            'exists_by_name', 'get_most_popular', 'get_low_stock'
        ]
        
        for method_name in required_methods:
            assert hasattr(BebidaRepositoryPort, method_name)
            method = getattr(BebidaRepositoryPort, method_name)
            assert callable(method)
    
    def test_repositories_can_be_imported_from_package(self):
        """Test that all repositories can be imported from the package."""
        from app.domain.repositories import (
            ItemRepositoryPort,
            IngredienteRepositoryPort,
            PlatoRepositoryPort,
            BebidaRepositoryPort
        )
        
        assert ItemRepositoryPort is not None
        assert IngredienteRepositoryPort is not None
        assert PlatoRepositoryPort is not None
        assert BebidaRepositoryPort is not None