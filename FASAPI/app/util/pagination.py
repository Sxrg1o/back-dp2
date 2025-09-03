"""
Pagination utilities.
"""
from typing import List, TypeVar, Generic
from math import ceil

from app.schemas.base import PaginatedResponse, PaginationParams

T = TypeVar('T')


class PaginationHelper(Generic[T]):
    """Helper class for pagination operations."""
    
    @staticmethod
    def paginate(
        items: List[T],
        pagination: PaginationParams,
        total_count: int = None,
    ) -> PaginatedResponse:
        """
        Create paginated response from items list.
        
        Args:
            items: List of items for current page
            pagination: Pagination parameters
            total_count: Total number of items (if None, uses len(items))
        
        Returns:
            PaginatedResponse with pagination metadata
        """
        
        if total_count is None:
            total_count = len(items)
        
        total_pages = ceil(total_count / pagination.size) if pagination.size > 0 else 0
        
        sort_info = []
        if pagination.sort:
            sort_info = [pagination.sort]
        
        return PaginatedResponse(
            content=items,
            page=pagination.page,
            size=pagination.size,
            total_elements=total_count,
            total_pages=total_pages,
            sort=sort_info,
        )
    
    @staticmethod
    def get_offset(pagination: PaginationParams) -> int:
        """Get offset for database queries."""
        return pagination.page * pagination.size
    
    @staticmethod
    def parse_sort(sort_param: str) -> tuple[str, str]:
        """
        Parse sort parameter into field and direction.
        
        Args:
            sort_param: Sort parameter in format "field,direction" (e.g., "name,asc")
        
        Returns:
            Tuple of (field, direction)
        """
        
        if not sort_param:
            return None, None
        
        parts = sort_param.split(",")
        field = parts[0].strip()
        direction = parts[1].strip().lower() if len(parts) > 1 else "asc"
        
        # Validate direction
        if direction not in ["asc", "desc"]:
            direction = "asc"
        
        return field, direction
    
    @staticmethod
    def validate_pagination(pagination: PaginationParams) -> PaginationParams:
        """
        Validate and normalize pagination parameters.
        
        Args:
            pagination: Pagination parameters to validate
        
        Returns:
            Validated pagination parameters
        """
        
        # Ensure page is not negative
        if pagination.page < 0:
            pagination.page = 0
        
        # Ensure size is within bounds
        if pagination.size < 1:
            pagination.size = 20
        elif pagination.size > 200:
            pagination.size = 200
        
        return pagination