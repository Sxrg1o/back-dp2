"""Tests for EtiquetaItem enum."""

import pytest
from app.domain.value_objects.etiqueta_item import EtiquetaItem


class TestEtiquetaItem:
    """Test cases for EtiquetaItem enum."""
    
    def test_enum_values(self):
        """Test that all expected enum values exist."""
        expected_values = {
            "SIN_GLUTEN": "sin_gluten",
            "PICANTE": "picante", 
            "SALADO": "salado",
            "CALIENTE": "caliente",
            "FRIO": "frio",
            "ACIDO": "acido",
            "AGRIO": "agrio",
            "CON_GLUTEN": "con_gluten",
            "VEGANO": "vegano"
        }
        
        for name, value in expected_values.items():
            enum_member = getattr(EtiquetaItem, name)
            assert enum_member.value == value
    
    def test_string_representation(self):
        """Test string representation of enum values."""
        assert str(EtiquetaItem.SIN_GLUTEN) == "sin_gluten"
        assert str(EtiquetaItem.VEGANO) == "vegano"
        assert str(EtiquetaItem.PICANTE) == "picante"
    
    def test_enum_immutability(self):
        """Test that enum values are immutable."""
        with pytest.raises(AttributeError):
            EtiquetaItem.SIN_GLUTEN.value = "modified"
    
    def test_enum_comparison(self):
        """Test enum comparison operations."""
        assert EtiquetaItem.SIN_GLUTEN == EtiquetaItem.SIN_GLUTEN
        assert EtiquetaItem.SIN_GLUTEN != EtiquetaItem.VEGANO
    
    def test_enum_membership(self):
        """Test enum membership operations."""
        all_labels = list(EtiquetaItem)
        assert EtiquetaItem.SIN_GLUTEN in all_labels
        assert EtiquetaItem.VEGANO in all_labels
        assert len(all_labels) == 9