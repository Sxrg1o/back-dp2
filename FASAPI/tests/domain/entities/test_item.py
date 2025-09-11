"""Tests for Item domain entity."""

import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.item import Item
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem


class TestItem:
    """Test cases for Item domain entity."""
    
    def create_valid_item(self) -> Item:
        """Create a valid item for testing."""
        return Item(
            id=uuid4(),
            nombre="Test Item",
            descripcion="Test description",
            precio=Precio(Decimal("10.50")),
            informacion_nutricional=InformacionNutricional(calorias=200, proteinas=15.0, azucares=5.0),
            tiempo_preparacion=15,
            stock_actual=50,
            stock_minimo=10,
            etiquetas={EtiquetaItem.VEGANO, EtiquetaItem.SIN_GLUTEN},
            activo=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1
        )
    
    def test_valid_item_creation(self):
        """Test creating a valid item."""
        item = self.create_valid_item()
        assert item.nombre == "Test Item"
        assert item.precio.value == Decimal("10.50")
        assert item.stock_actual == 50
        assert item.activo is True
    
    def test_invalid_empty_name(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Item name cannot be empty"):
            Item(
                id=uuid4(),
                nombre="",
                descripcion="Test",
                precio=Precio(Decimal("10.50")),
                informacion_nutricional=InformacionNutricional(calorias=200, proteinas=15.0, azucares=5.0),
                tiempo_preparacion=15,
                stock_actual=50,
                stock_minimo=10,
                etiquetas=set(),
                activo=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1
            )
    
    def test_invalid_negative_preparation_time(self):
        """Test that negative preparation time raises ValueError."""
        with pytest.raises(ValueError, match="Preparation time cannot be negative"):
            Item(
                id=uuid4(),
                nombre="Test Item",
                descripcion="Test",
                precio=Precio(Decimal("10.50")),
                informacion_nutricional=InformacionNutricional(calorias=200, proteinas=15.0, azucares=5.0),
                tiempo_preparacion=-5,
                stock_actual=50,
                stock_minimo=10,
                etiquetas=set(),
                activo=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1
            )
    
    def test_verificar_stock(self):
        """Test stock verification."""
        item = self.create_valid_item()
        assert item.verificar_stock() is True
        
        # Test with zero stock
        item.stock_actual = 0
        assert item.verificar_stock() is False
        
        # Test with inactive item
        item.stock_actual = 50
        item.activo = False
        assert item.verificar_stock() is False
    
    def test_calcular_calorias(self):
        """Test calorie calculation."""
        item = self.create_valid_item()
        assert item.calcular_calorias() == 200
    
    def test_is_disponible(self):
        """Test availability check."""
        item = self.create_valid_item()
        assert item.is_disponible() is True
        
        # Test with stock at minimum level
        item.stock_actual = item.stock_minimo
        assert item.is_disponible() is False
        
        # Test with stock below minimum
        item.stock_actual = item.stock_minimo - 1
        assert item.is_disponible() is False
        
        # Test with inactive item
        item.stock_actual = 50
        item.activo = False
        assert item.is_disponible() is False
    
    def test_reducir_stock(self):
        """Test stock reduction."""
        item = self.create_valid_item()
        initial_stock = item.stock_actual
        
        item.reducir_stock(10)
        assert item.stock_actual == initial_stock - 10
        
        # Test invalid quantity
        with pytest.raises(ValueError, match="Quantity must be positive"):
            item.reducir_stock(0)
        
        # Test insufficient stock
        with pytest.raises(ValueError, match="Insufficient stock available"):
            item.reducir_stock(1000)
    
    def test_aumentar_stock(self):
        """Test stock increase."""
        item = self.create_valid_item()
        initial_stock = item.stock_actual
        
        item.aumentar_stock(20)
        assert item.stock_actual == initial_stock + 20
        
        # Test invalid quantity
        with pytest.raises(ValueError, match="Quantity must be positive"):
            item.aumentar_stock(-5)
    
    def test_actualizar_precio(self):
        """Test price update."""
        item = self.create_valid_item()
        nuevo_precio = Precio(Decimal("15.75"))
        
        item.actualizar_precio(nuevo_precio)
        assert item.precio == nuevo_precio
    
    def test_etiqueta_management(self):
        """Test label management."""
        item = self.create_valid_item()
        
        # Test adding label
        item.agregar_etiqueta(EtiquetaItem.PICANTE)
        assert item.tiene_etiqueta(EtiquetaItem.PICANTE)
        
        # Test removing label
        item.remover_etiqueta(EtiquetaItem.VEGANO)
        assert not item.tiene_etiqueta(EtiquetaItem.VEGANO)
    
    def test_activation_deactivation(self):
        """Test item activation and deactivation."""
        item = self.create_valid_item()
        
        item.desactivar()
        assert item.activo is False
        
        item.activar()
        assert item.activo is True
    
    def test_necesita_restock(self):
        """Test restock need detection."""
        item = self.create_valid_item()
        assert item.necesita_restock() is False
        
        item.stock_actual = item.stock_minimo
        assert item.necesita_restock() is True
        
        item.stock_actual = item.stock_minimo - 1
        assert item.necesita_restock() is True
    
    def test_dietary_checks(self):
        """Test dietary restriction checks."""
        item = self.create_valid_item()
        
        assert item.es_vegano() is True
        assert item.es_sin_gluten() is True
        
        item.remover_etiqueta(EtiquetaItem.VEGANO)
        assert item.es_vegano() is False
    
    def test_string_representation(self):
        """Test string representation."""
        item = self.create_valid_item()
        expected = f"{item.nombre} - {item.precio}"
        assert str(item) == expected