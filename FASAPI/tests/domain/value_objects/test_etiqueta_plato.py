"""Tests for EtiquetaPlato enum."""

import pytest
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato


class TestEtiquetaPlato:
    """Test cases for EtiquetaPlato enum."""
    
    def test_enum_values(self):
        """Test that all expected enum values exist."""
        expected_values = {
            "ENTRADA": "entrada",
            "FONDO": "fondo",
            "POSTRE": "postre"
        }
        
        for name, value in expected_values.items():
            enum_member = getattr(EtiquetaPlato, name)
            assert enum_member.value == value
    
    def test_string_representation(self):
        """Test string representation of enum values."""
        assert str(EtiquetaPlato.ENTRADA) == "entrada"
        assert str(EtiquetaPlato.FONDO) == "fondo"
        assert str(EtiquetaPlato.POSTRE) == "postre"
    
    def test_enum_immutability(self):
        """Test that enum values are immutable."""
        with pytest.raises(AttributeError):
            EtiquetaPlato.ENTRADA.value = "modified"
    
    def test_enum_comparison(self):
        """Test enum comparison operations."""
        assert EtiquetaPlato.ENTRADA == EtiquetaPlato.ENTRADA
        assert EtiquetaPlato.ENTRADA != EtiquetaPlato.FONDO
    
    def test_enum_membership(self):
        """Test enum membership operations."""
        all_types = list(EtiquetaPlato)
        assert EtiquetaPlato.ENTRADA in all_types
        assert EtiquetaPlato.FONDO in all_types
        assert EtiquetaPlato.POSTRE in all_types
        assert len(all_types) == 3