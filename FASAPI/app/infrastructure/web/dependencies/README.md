# Menu Dependency Injection Container

This module provides dependency injection configuration for the menu module, implementing the hexagonal architecture pattern.

## Overview

The dependency injection container manages the creation and wiring of:
- Repository implementations (infrastructure layer)
- Application services (application layer)
- Proper lifecycle management for database connections

## Components

### MenuContainer

The main container class that creates instances of repositories and services:

```python
from app.infrastructure.web.dependencies.container import MenuContainer

container = MenuContainer()
session = get_database_session()

# Create repositories
item_repo = container.create_item_repository(session)
menu_service = container.create_menu_service(session)
```

### FastAPI Dependencies

For FastAPI integration, use the dependency functions that automatically inject database sessions:

```python
from app.infrastructure.web.dependencies.menu_dependencies import (
    get_item_service,
    get_menu_service
)

@app.get("/items")
async def get_items(
    item_service: ItemApplicationService = Depends(get_item_service)
):
    return await item_service.get_available_items()
```

## Architecture Benefits

1. **Dependency Inversion**: Application services depend on interfaces, not implementations
2. **Testability**: Easy to mock dependencies for unit testing
3. **Flexibility**: Can swap implementations without changing application code
4. **Lifecycle Management**: Proper database session management
5. **Single Responsibility**: Each component has a clear purpose

## Usage in Controllers

```python
from fastapi import APIRouter, Depends
from app.infrastructure.web.dependencies.menu_dependencies import get_menu_service
from app.application.services.menu_service import MenuApplicationService

router = APIRouter()

@router.get("/menu")
async def get_full_menu(
    menu_service: MenuApplicationService = Depends(get_menu_service)
):
    return await menu_service.get_full_menu()
```

## Testing

The container supports easy testing by allowing mock dependencies:

```python
from unittest.mock import Mock
from app.infrastructure.web.dependencies.container import MenuContainer

def test_menu_service():
    container = MenuContainer()
    mock_session = Mock()
    
    service = container.create_menu_service(mock_session)
    # Test service logic...
```

## Directory Structure

```
app/infrastructure/web/dependencies/
├── __init__.py
├── container.py           # Core dependency injection container
├── menu_dependencies.py   # FastAPI integration with database
└── README.md             # This documentation
```