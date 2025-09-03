"""
Pagination utility tests.
"""
import pytest

from app.schemas.base import PaginationParams
from app.util.pagination import PaginationHelper


@pytest.mark.unit
def test_paginate():
    """Test pagination helper."""
    
    # Sample data
    items = [f"item_{i}" for i in range(10)]
    pagination = PaginationParams(page=0, size=3)
    
    # Paginate first 3 items
    result = PaginationHelper.paginate(
        items=items[:3],
        pagination=pagination,
        total_count=10,
    )
    
    assert len(result.content) == 3
    assert result.page == 0
    assert result.size == 3
    assert result.total_elements == 10
    assert result.total_pages == 4


@pytest.mark.unit
def test_get_offset():
    """Test offset calculation."""
    
    pagination = PaginationParams(page=2, size=5)
    offset = PaginationHelper.get_offset(pagination)
    
    assert offset == 10  # page 2 * size 5


@pytest.mark.unit
def test_parse_sort():
    """Test sort parameter parsing."""
    
    # Test ascending sort
    field, direction = PaginationHelper.parse_sort("name,asc")
    assert field == "name"
    assert direction == "asc"
    
    # Test descending sort
    field, direction = PaginationHelper.parse_sort("created_at,desc")
    assert field == "created_at"
    assert direction == "desc"
    
    # Test default direction
    field, direction = PaginationHelper.parse_sort("name")
    assert field == "name"
    assert direction == "asc"
    
    # Test invalid direction
    field, direction = PaginationHelper.parse_sort("name,invalid")
    assert field == "name"
    assert direction == "asc"
    
    # Test empty sort
    field, direction = PaginationHelper.parse_sort("")
    assert field is None
    assert direction is None


@pytest.mark.unit
def test_validate_pagination():
    """Test pagination validation."""
    
    # Test negative page
    pagination = PaginationParams(page=-1, size=20)
    validated = PaginationHelper.validate_pagination(pagination)
    assert validated.page == 0
    
    # Test size too small
    pagination = PaginationParams(page=0, size=0)
    validated = PaginationHelper.validate_pagination(pagination)
    assert validated.size == 20
    
    # Test size too large
    pagination = PaginationParams(page=0, size=500)
    validated = PaginationHelper.validate_pagination(pagination)
    assert validated.size == 200
    
    # Test valid pagination
    pagination = PaginationParams(page=1, size=50)
    validated = PaginationHelper.validate_pagination(pagination)
    assert validated.page == 1
    assert validated.size == 50