"""
Authentication and authorization schemas.
"""
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """JWT token response."""
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    """JWT token payload."""
    
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None


class LoginRequest(BaseModel):
    """Login request."""
    
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    
    refresh_token: str