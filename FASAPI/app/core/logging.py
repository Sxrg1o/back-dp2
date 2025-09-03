"""
Logging configuration and utilities.
"""
import logging
import sys
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory

from app.core.config import settings


def setup_logging() -> None:
    """Set up structured logging."""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.LOG_FORMAT == "json"
            else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # Silence noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# Create logger instance
logger = structlog.get_logger()


def log_request(
    method: str,
    url: str,
    status_code: int,
    duration: float,
    **kwargs: Any,
) -> None:
    """Log HTTP request."""
    logger.info(
        "HTTP request",
        method=method,
        url=str(url),
        status_code=status_code,
        duration_ms=round(duration * 1000, 2),
        **kwargs,
    )


def log_database_query(
    query: str,
    duration: float,
    **kwargs: Any,
) -> None:
    """Log database query."""
    logger.debug(
        "Database query",
        query=query,
        duration_ms=round(duration * 1000, 2),
        **kwargs,
    )


def log_external_request(
    method: str,
    url: str,
    status_code: int,
    duration: float,
    **kwargs: Any,
) -> None:
    """Log external API request."""
    logger.info(
        "External request",
        method=method,
        url=str(url),
        status_code=status_code,
        duration_ms=round(duration * 1000, 2),
        **kwargs,
    )