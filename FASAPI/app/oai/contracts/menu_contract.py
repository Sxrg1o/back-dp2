"""
Menu contract for external menu integrations.
"""
from typing import List, Optional
from decimal import Decimal

from pydantic import BaseModel, Field


class MenuItemContract(BaseModel):
    """Contract for menu item from external sources."""
    
    external_id: str = Field(..., description="External system ID")
    name: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    price: Decimal = Field(..., description="Item price")
    category: str = Field(..., description="Item category")
    image_url: Optional[str] = Field(None, description="Item image URL")
    available: bool = Field(True, description="Item availability")
    ingredients: List[str] = Field(default_factory=list, description="Item ingredients")
    allergens: List[str] = Field(default_factory=list, description="Item allergens")
    
    class Config:
        json_encoders = {
            Decimal: str,
        }


class MenuContract(BaseModel):
    """Contract for complete menu from external sources."""
    
    restaurant_id: str = Field(..., description="Restaurant identifier")
    restaurant_name: str = Field(..., description="Restaurant name")
    items: List[MenuItemContract] = Field(..., description="Menu items")
    last_updated: Optional[str] = Field(None, description="Last update timestamp")
    source: str = Field(..., description="Data source identifier")