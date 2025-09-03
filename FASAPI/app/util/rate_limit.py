"""
Rate limiting utilities.
"""
import time
from typing import Dict, Optional
from collections import defaultdict, deque

from app.core.logging import logger


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in the time window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed for the given identifier.
        
        Args:
            identifier: Unique identifier (e.g., IP address, user ID)
        
        Returns:
            True if request is allowed, False otherwise
        """
        
        current_time = time.time()
        window_start = current_time - self.window_seconds
        
        # Get request history for this identifier
        request_times = self.requests[identifier]
        
        # Remove old requests outside the window
        while request_times and request_times[0] < window_start:
            request_times.popleft()
        
        # Check if we're within the limit
        if len(request_times) >= self.max_requests:
            logger.warning(
                "Rate limit exceeded",
                identifier=identifier,
                requests_count=len(request_times),
                max_requests=self.max_requests,
            )
            return False
        
        # Add current request
        request_times.append(current_time)
        
        return True
    
    def get_remaining_requests(self, identifier: str) -> int:
        """
        Get remaining requests for the identifier.
        
        Args:
            identifier: Unique identifier
        
        Returns:
            Number of remaining requests in current window
        """
        
        current_time = time.time()
        window_start = current_time - self.window_seconds
        
        request_times = self.requests[identifier]
        
        # Remove old requests
        while request_times and request_times[0] < window_start:
            request_times.popleft()
        
        return max(0, self.max_requests - len(request_times))
    
    def get_reset_time(self, identifier: str) -> Optional[float]:
        """
        Get time when rate limit resets for the identifier.
        
        Args:
            identifier: Unique identifier
        
        Returns:
            Unix timestamp when limit resets, or None if no requests
        """
        
        request_times = self.requests[identifier]
        
        if not request_times:
            return None
        
        return request_times[0] + self.window_seconds
    
    def clear_identifier(self, identifier: str):
        """Clear rate limit data for an identifier."""
        if identifier in self.requests:
            del self.requests[identifier]
    
    def clear_all(self):
        """Clear all rate limit data."""
        self.requests.clear()


class CircuitBreaker:
    """Circuit breaker for external service calls."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception,
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before trying again
            expected_exception: Exception type that counts as failure
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def __call__(self, func):
        """Decorator to wrap function with circuit breaker."""
        
        async def wrapper(*args, **kwargs):
            return await self.call(func, *args, **kwargs)
        
        return wrapper
    
    async def call(self, func, *args, **kwargs):
        """
        Call function with circuit breaker protection.
        
        Args:
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
        
        Returns:
            Function result
        
        Raises:
            Exception: If circuit is open or function fails
        """
        
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
                logger.info("Circuit breaker transitioning to HALF_OPEN")
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
            
        except self.expected_exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        
        return time.time() - self.last_failure_time >= self.recovery_timeout
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = "CLOSED"
        
        if self.state == "HALF_OPEN":
            logger.info("Circuit breaker reset to CLOSED")
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(
                "Circuit breaker opened",
                failure_count=self.failure_count,
                threshold=self.failure_threshold,
            )
    
    def reset(self):
        """Manually reset circuit breaker."""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"
        logger.info("Circuit breaker manually reset")
    
    def get_state(self) -> Dict[str, any]:
        """Get current circuit breaker state."""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "failure_threshold": self.failure_threshold,
            "last_failure_time": self.last_failure_time,
            "recovery_timeout": self.recovery_timeout,
        }


# Global instances
default_rate_limiter = RateLimiter(max_requests=100, window_seconds=60)
scraping_rate_limiter = RateLimiter(max_requests=10, window_seconds=60)
external_api_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)