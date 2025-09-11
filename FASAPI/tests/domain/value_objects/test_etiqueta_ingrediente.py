"""Tests for EtiquetaIngrediente enum."""

import pytest
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente


class TestEtiquetaIngrediente:
    """Test cases for EtiquetaIngrediente enum."""
    
    def test_enum_values(self):
        """Test that all expected enum values exist."""
        expected_values = {
            "VERDURA": "verdura",
            "CARNE": "carne",
            "FRUTA": "fruta"
        }
        
        for name, value in expected_values.items():
            enum_member = getattr(EtiquetaIngrediente, name)
            assert enum_member.value == value
    
    def test_string_representation(self):
        """Test string representation of enum values."""
        assert str(EtiquetaIngrediente.VERDURA) == "verdura"
        assert str(EtiquetaIngrediente.CARNE) == "carne"
        assert str(EtiquetaIngrediente.FRUTA) == "fruta"
    
    def test_enum_immutability(self):
        """Test that enum values are immutable."""
        with pytest.raises(AttributeError):
            EtiquetaIngrediente.VERDURA.value = "modified"
    
    def test_enum_comparison(self):
        """Test enum comparison operations."""
        assert EtiquetaIngrediente.VERDURA == EtiquetaIngrediente.VERDURA
        assert EtiquetaIngrediente.VERDURA != EtiquetaIngrediente.CARNE
    
    def test_enum_membership(self):
        """Test enum membership operations."""
        all_types = list(EtiquetaIngrediente)
        assert EtiquetaIngrediente.VERDURA in all_types
        assert EtiquetaIngrediente.CARNE in all_types
        assert EtiquetaIngrediente.FRUTA in all_types
        assert len(all_types) == 3