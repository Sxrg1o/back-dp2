"""Tests for Ingrediente domain entity."""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.ingrediente import Ingrediente
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente


class TestIngrediente:
    """Test cases for Ingrediente domain entity."""
    
    def create_valid_ingrediente(self) -> Ingrediente:
        """Create a valid ingredient for testing."""
        return Ingrediente(
            id=uuid4(),
            nombre="Tomate",
            descripcion="Tomate fresco",
            precio=Precio(Decimal("2.50")),
            informacion_nutricional=InformacionNutricional(calorias=18, proteinas=0.9, azucares=2.6),
            tiempo_preparacion=5,
            stock_actual=100,
            stock_minimo=20,
            etiquetas={EtiquetaItem.VEGANO, EtiquetaItem.SIN_GLUTEN},
            activo=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            tipo=EtiquetaIngrediente.VERDURA,
            peso_unitario=150.0,
            unidad_medida="gramos",
            fecha_vencimiento=datetime.utcnow() + timedelta(days=7),
            proveedor="Proveedor Local"
        )
    
    def test_valid_ingrediente_creation(self):
        """Test creating a valid ingredient."""
        ingrediente = self.create_valid_ingrediente()
        assert ingrediente.nombre == "Tomate"
        assert ingrediente.tipo == EtiquetaIngrediente.VERDURA
        assert ingrediente.peso_unitario == 150.0
        assert ingrediente.unidad_medida == "gramos"
    
    def test_invalid_negative_weight(self):
        """Test that negative unit weight raises ValueError."""
        with pytest.raises(ValueError, match="Unit weight must be positive"):
            Ingrediente(
                id=uuid4(),
                nombre="Test",
                descripcion="Test",
                precio=Precio(Decimal("2.50")),
                informacion_nutricional=InformacionNutricional(calorias=18, proteinas=0.9, azucares=2.6),
                tiempo_preparacion=5,
                stock_actual=100,
                stock_minimo=20,
                etiquetas=set(),
                activo=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                tipo=EtiquetaIngrediente.VERDURA,
                peso_unitario=-10.0,
                unidad_medida="gramos"
            )
    
    def test_invalid_empty_unit_measure(self):
        """Test that empty unit measure raises ValueError."""
        with pytest.raises(ValueError, match="Unit of measure cannot be empty"):
            Ingrediente(
                id=uuid4(),
                nombre="Test",
                descripcion="Test",
                precio=Precio(Decimal("2.50")),
                informacion_nutricional=InformacionNutricional(calorias=18, proteinas=0.9, azucares=2.6),
                tiempo_preparacion=5,
                stock_actual=100,
                stock_minimo=20,
                etiquetas=set(),
                activo=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                tipo=EtiquetaIngrediente.VERDURA,
                peso_unitario=150.0,
                unidad_medida=""
            )
    
    def test_esta_vencido(self):
        """Test expiration check."""
        ingrediente = self.create_valid_ingrediente()
        assert ingrediente.esta_vencido() is False
        
        # Test expired ingredient
        ingrediente.fecha_vencimiento = datetime.utcnow() - timedelta(days=1)
        assert ingrediente.esta_vencido() is True
        
        # Test ingredient without expiration date
        ingrediente.fecha_vencimiento = None
        assert ingrediente.esta_vencido() is False
    
    def test_dias_hasta_vencimiento(self):
        """Test days until expiration calculation."""
        ingrediente = self.create_valid_ingrediente()
        dias = ingrediente.dias_hasta_vencimiento()
        assert dias is not None
        assert dias >= 6  # Should be around 7 days
        
        # Test ingredient without expiration date
        ingrediente.fecha_vencimiento = None
        assert ingrediente.dias_hasta_vencimiento() is None
    
    def test_esta_proximo_a_vencer(self):
        """Test close to expiration check."""
        ingrediente = self.create_valid_ingrediente()
        
        # Test ingredient expiring in 2 days (close to expiration)
        ingrediente.fecha_vencimiento = datetime.utcnow() + timedelta(days=2)
        assert ingrediente.esta_proximo_a_vencer() is True
        
        # Test ingredient expiring in 5 days (not close)
        ingrediente.fecha_vencimiento = datetime.utcnow() + timedelta(days=5)
        assert ingrediente.esta_proximo_a_vencer() is False
    
    def test_calcular_peso_total(self):
        """Test total weight calculation."""
        ingrediente = self.create_valid_ingrediente()
        peso_total = ingrediente.calcular_peso_total()
        expected = ingrediente.stock_actual * ingrediente.peso_unitario
        assert peso_total == expected
    
    def test_tipo_checks(self):
        """Test ingredient type checks."""
        ingrediente = self.create_valid_ingrediente()
        
        assert ingrediente.es_verdura() is True
        assert ingrediente.es_carne() is False
        assert ingrediente.es_fruta() is False
        
        # Test with different type
        ingrediente.tipo = EtiquetaIngrediente.CARNE
        assert ingrediente.es_verdura() is False
        assert ingrediente.es_carne() is True
    
    def test_is_disponible_with_expiration(self):
        """Test availability check including expiration."""
        ingrediente = self.create_valid_ingrediente()
        assert ingrediente.is_disponible() is True
        
        # Test expired ingredient
        ingrediente.fecha_vencimiento = datetime.utcnow() - timedelta(days=1)
        assert ingrediente.is_disponible() is False
    
    def test_actualizar_fecha_vencimiento(self):
        """Test expiration date update."""
        ingrediente = self.create_valid_ingrediente()
        nueva_fecha = datetime.utcnow() + timedelta(days=14)
        
        ingrediente.actualizar_fecha_vencimiento(nueva_fecha)
        assert ingrediente.fecha_vencimiento == nueva_fecha
        
        # Test invalid date (in the past)
        with pytest.raises(ValueError, match="New expiration date must be in the future"):
            ingrediente.actualizar_fecha_vencimiento(datetime.utcnow() - timedelta(days=1))
    
    def test_cambiar_proveedor(self):
        """Test supplier change."""
        ingrediente = self.create_valid_ingrediente()
        nuevo_proveedor = "Nuevo Proveedor"
        
        ingrediente.cambiar_proveedor(nuevo_proveedor)
        assert ingrediente.proveedor == nuevo_proveedor
        
        # Test empty supplier name
        with pytest.raises(ValueError, match="Supplier name cannot be empty"):
            ingrediente.cambiar_proveedor("")
    
    def test_string_representation(self):
        """Test string representation."""
        ingrediente = self.create_valid_ingrediente()
        expected = f"{ingrediente.nombre} ({ingrediente.tipo.value}) - {ingrediente.peso_unitario}g - {ingrediente.precio}"
        assert str(ingrediente) == expected