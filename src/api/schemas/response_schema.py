"""
Common response schemas for API endpoints.
"""

from typing import Any, Optional, Dict
from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """Standard success response schema."""

    success: bool = Field(True, description="Operation success flag")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Optional additional data")


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    success: bool = Field(False, description="Operation success flag")
    error: Dict[str, Any] = Field(..., description="Error details")
    path: str = Field(..., description="Request path")
    method: str = Field(..., description="HTTP method")


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    environment: str = Field(..., description="Environment")
    timestamp: str = Field(..., description="Response timestamp")


class MessageResponse(BaseModel):
    """Simple message response schema."""

    message: str = Field(..., description="Response message")