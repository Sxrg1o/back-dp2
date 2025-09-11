"""
Global exception handlers.
"""
import uuid
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import logger
from app.domain.exceptions.menu_exceptions import (
    MenuDomainException,
    ItemNotFoundError,
    ItemNotAvailableError,
    InsufficientStockError,
    InvalidNutritionalDataError,
    InvalidPriceError,
    IngredientExpiredError,
    RecipeValidationError,
    InvalidVolumeError,
    InvalidAlcoholContentError,
    ItemAlreadyExistsError,
    IngredienteNotFoundError,
    IngredienteAlreadyExistsError,
    PlatoNotFoundError,
    PlatoAlreadyExistsError,
    BebidaNotFoundError,
    BebidaAlreadyExistsError,
)


class AppException(Exception):
    """Base application exception."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        code: str = "INTERNAL_ERROR",
        details: Dict[str, Any] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(AppException):
    """Validation error exception."""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            details=details,
        )


class NotFoundError(AppException):
    """Resource not found exception."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
        )


class ConflictError(AppException):
    """Resource conflict exception."""
    
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
        )


def create_error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: Dict[str, Any] = None,
) -> JSONResponse:
    """Create standardized error response."""
    trace_id = getattr(request.state, "trace_id", str(uuid.uuid4()))
    
    error_response = {
        "timestamp": datetime.utcnow().isoformat(),
        "traceId": trace_id,
        "status": status_code,
        "code": code,
        "message": message,
    }
    
    if details:
        error_response["details"] = details
    
    return JSONResponse(
        status_code=status_code,
        content=error_response,
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application exceptions."""
    logger.error(
        "Application exception",
        exc_info=exc,
        extra={
            "status_code": exc.status_code,
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    )
    
    return create_error_response(
        request=request,
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.warning(
        "HTTP exception",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
        },
    )
    
    return create_error_response(
        request=request,
        status_code=exc.status_code,
        code="HTTP_ERROR",
        message=exc.detail,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle validation exceptions."""
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        details.append({
            "field": field,
            "error": error["msg"],
            "type": error["type"],
        })
    
    logger.warning(
        "Validation error",
        extra={
            "errors": exc.errors(),
        },
    )
    
    return create_error_response(
        request=request,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="VALIDATION_ERROR",
        message="Validation failed",
        details=details,
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Handle database integrity errors."""
    logger.error(
        "Database integrity error",
        exc_info=exc,
    )
    
    return create_error_response(
        request=request,
        status_code=status.HTTP_409_CONFLICT,
        code="INTEGRITY_ERROR",
        message="Database constraint violation",
    )


async def menu_domain_exception_handler(
    request: Request, exc: MenuDomainException
) -> JSONResponse:
    """Handle menu domain exceptions."""
    # Map specific menu exceptions to appropriate HTTP status codes
    status_code_mapping = {
        ItemNotFoundError: status.HTTP_404_NOT_FOUND,
        IngredienteNotFoundError: status.HTTP_404_NOT_FOUND,
        PlatoNotFoundError: status.HTTP_404_NOT_FOUND,
        BebidaNotFoundError: status.HTTP_404_NOT_FOUND,
        ItemNotAvailableError: status.HTTP_409_CONFLICT,
        InsufficientStockError: status.HTTP_409_CONFLICT,
        ItemAlreadyExistsError: status.HTTP_409_CONFLICT,
        IngredienteAlreadyExistsError: status.HTTP_409_CONFLICT,
        PlatoAlreadyExistsError: status.HTTP_409_CONFLICT,
        BebidaAlreadyExistsError: status.HTTP_409_CONFLICT,
        IngredientExpiredError: status.HTTP_409_CONFLICT,
        InvalidNutritionalDataError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        InvalidPriceError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        RecipeValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        InvalidVolumeError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        InvalidAlcoholContentError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    }
    
    # Get appropriate status code or default to 400
    status_code = status_code_mapping.get(type(exc), status.HTTP_400_BAD_REQUEST)
    
    logger.warning(
        "Menu domain exception",
        extra={
            "exception_type": type(exc).__name__,
            "message": exc.message,
            "details": exc.details,
            "status_code": status_code,
        },
    )
    
    return create_error_response(
        request=request,
        status_code=status_code,
        code=type(exc).__name__.upper(),
        message=exc.message,
        details=exc.details if exc.details else None,
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    logger.error(
        "Unhandled exception",
        exc_info=exc,
    )
    
    return create_error_response(
        request=request,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="INTERNAL_ERROR",
        message="Internal server error",
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Set up exception handlers for the application."""
    # Add menu domain exception handler first (more specific)
    app.add_exception_handler(MenuDomainException, menu_domain_exception_handler)
    
    # Add general application exception handlers
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)