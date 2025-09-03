"""
Request ID middleware for tracing requests.
"""
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware to add request ID for tracing."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add request ID to request state and response headers."""
        
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        
        # Store in request state
        request.state.request_id = request_id
        request.state.trace_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add to response headers
        response.headers["X-Request-Id"] = request_id
        response.headers["X-Trace-Id"] = request_id
        
        return response