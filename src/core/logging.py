# ...existing code...
"""
Logging configuration for the application.
Produces structured JSON logs with request_id and other context.
"""
import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Dict, Any

import structlog

from src.core.config import get_settings

def configure_logging() -> None:
    """
    Configuración de logging para la aplicación.
    Produce logs estructurados en JSON con request_id y contexto adicional.
    """
    """Configura los handlers de la librería logging y structlog."""
    
    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # build log dir
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # ProcessorFormatter will run structlog processors and render JSON
    processor_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),
        foreign_pre_chain=[
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
        ],
    )

    # Console handler (JSON)
    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(level)
    console.setFormatter(processor_formatter)

    # File handlers (Timed rotating)
    app_file = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        when="midnight",
        backupCount=14,
        utc=True,
    )
    app_file.setLevel(level)
    app_file.setFormatter(processor_formatter)

    access_file = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "access.log"),
        when="midnight",
        backupCount=14,
        utc=True,
    )
    access_file.setLevel(level)
    access_file.setFormatter(processor_formatter)

    error_file = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "error.log"),
        when="midnight",
        backupCount=30,
        utc=True,
    )
    error_file.setLevel(logging.ERROR)
    error_file.setFormatter(processor_formatter)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    # Remove existing handlers to avoid duplicates (safe on startup)
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)
    root_logger.addHandler(console)
    root_logger.addHandler(app_file)

    # Specific loggers for categories
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.setLevel(level)
    uvicorn_access.propagate = False
    # remove handlers to avoid duplicates
    for h in list(uvicorn_access.handlers):
        uvicorn_access.removeHandler(h)
    uvicorn_access.addHandler(access_file)
    uvicorn_access.addHandler(console)

    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.setLevel(level)
    uvicorn_error.propagate = False
    for h in list(uvicorn_error.handlers):
        uvicorn_error.removeHandler(h)
    uvicorn_error.addHandler(error_file)
    uvicorn_error.addHandler(console)

    # SQLAlchemy errors go to error_file (and console)
    sa_logger = logging.getLogger("sqlalchemy")
    sa_logger.setLevel(logging.ERROR)
    sa_logger.propagate = False
    for h in list(sa_logger.handlers):
        sa_logger.removeHandler(h)
    sa_logger.addHandler(error_file)
    sa_logger.addHandler(console)

    # Configure structlog (processors do NOT include JSONRenderer here,
    # ProcessorFormatter will call JSONRenderer)
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name: str):
    """Devuelve un logger estructurado (structlog) con el nombre indicado."""
    return structlog.get_logger(name)
