"""
Idempotency middleware for handling duplicate requests.
"""
import json
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.logging import logger


class IdempotencyMiddleware(BaseHTTPMiddleware):
    """Middleware to handle idempotent requests."""
    
    def __init__(self, app, cache_ttl: int = 3600):
        super().__init__(app)
        self.cache_ttl = cache_ttl
        # TODO: Implement Redis-based cache for production
        self._cache = {}  # Simple in-memory cache for demo
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle idempotent requests using X-Idempotency-Key header."""
        
        # Only handle POST, PUT, PATCH methods
        if request.method not in ["POST", "PUT", "PATCH"]:
            return await call_next(request)
        
        # Check for idempotency key
        idempotency_key = request.headers.get("X-Idempotency-Key")
        if not idempotency_key:
            return await call_next(request)
        
        # Create cache key
        cache_key = f"idempotency:{idempotency_key}:{request.method}:{request.url.path}"
        
        # Check if request was already processed
        if cache_key in self._cache:
            logger.info(
                "Returning cached response for idempotent request",
                idempotency_key=idempotency_key,
                cache_key=cache_key,
            )
            cached_response = self._cache[cache_key]
            return JSONResponse(
                content=cached_response["content"],
                status_code=cached_response["status_code"],
                headers={"X-Idempotency-Replay": "true"},
            )
        
        # Process request
        response = await call_next(request)
        
        # Cache successful responses (2xx status codes)
        if 200 <= response.status_code < 300:
            # Read response body
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            try:
                content = json.loads(response_body.decode())
                self._cache[cache_key] = {
                    "content": content,
                    "status_code": response.status_code,
                }
                
                logger.info(
                    "Cached response for idempotent request",
                    idempotency_key=idempotency_key,
                    cache_key=cache_key,
                )
            except (json.JSONDecodeError, UnicodeDecodeError):
                logger.warning(
                    "Could not cache response - invalid JSON",
                    idempotency_key=idempotency_key,
                )
            
            # Recreate response with body
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
        
        return response