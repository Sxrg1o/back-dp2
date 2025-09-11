# Requirements Document

## Introduction

This specification outlines the refactoring of the Menu and Carta module (Item, Ingrediente, Plato, Bebida) from a traditional layered architecture to a proper hexagonal architecture (also known as Ports and Adapters). The current implementation has domain models tightly coupled to SQLAlchemy ORM, violating the principles of clean architecture. This refactoring will separate business logic from infrastructure concerns for the restaurant's menu management system, making it more testable, maintainable, and technology-agnostic.

## Requirements

### Requirement 1

**User Story:** As a developer, I want menu domain entities (Item, Ingrediente, Plato, Bebida) to be pure business objects without infrastructure dependencies, so that the menu business logic is independent of external frameworks and databases.

#### Acceptance Criteria

1. WHEN creating menu domain entities THEN they SHALL NOT import or depend on SQLAlchemy or any ORM framework
2. WHEN defining menu entities THEN they SHALL contain only business logic and menu-specific domain rules
3. WHEN menu entities are created THEN they SHALL use standard Python data types and menu-specific value objects (EtiquetaItem, EtiquetaIngrediente, EtiquetaPlato)
4. WHEN menu entities need persistence THEN they SHALL be mapped through adapters without modifying the entity itself

### Requirement 2

**User Story:** As a developer, I want to define clear ports (interfaces) for menu data access, so that the menu application core is decoupled from specific database implementations.

#### Acceptance Criteria

1. WHEN defining menu repository interfaces THEN they SHALL be abstract base classes or protocols in the domain layer
2. WHEN menu repository interfaces are created THEN they SHALL define menu-oriented methods (get_available_items, check_stock, get_by_category) without database-specific details
3. WHEN the menu application needs data access THEN it SHALL depend only on the repository interface, not the implementation
4. WHEN menu repository interfaces are defined THEN they SHALL return menu domain entities (Item, Ingrediente, Plato, Bebida), not ORM objects

### Requirement 3

**User Story:** As a developer, I want SQLAlchemy adapters to implement the menu repository interfaces, so that menu database operations are isolated in the infrastructure layer.

#### Acceptance Criteria

1. WHEN implementing menu repository adapters THEN they SHALL implement the menu domain repository interfaces
2. WHEN menu adapters interact with the database THEN they SHALL handle ORM-specific operations for menu entities internally
3. WHEN menu adapters return data THEN they SHALL convert ORM objects to menu domain entities (Item, Ingrediente, Plato, Bebida)
4. WHEN menu adapters receive data THEN they SHALL convert menu domain entities to ORM objects for persistence

### Requirement 4

**User Story:** As a developer, I want proper dependency injection configuration, so that the application can easily switch between different implementations and support testing.

#### Acceptance Criteria

1. WHEN configuring dependencies THEN the application SHALL inject repository implementations through interfaces
2. WHEN running tests THEN the application SHALL be able to use mock implementations of repositories
3. WHEN the application starts THEN dependency injection SHALL wire concrete implementations to interfaces
4. WHEN changing database technology THEN only the adapter implementations need to change, not the core application

### Requirement 5

**User Story:** As a developer, I want the menu application services to work with menu domain entities and repository interfaces, so that menu business logic remains pure and testable.

#### Acceptance Criteria

1. WHEN menu application services are implemented THEN they SHALL depend only on menu repository interfaces
2. WHEN menu services perform business operations THEN they SHALL work with menu domain entities and enforce menu business rules (stock verification, nutritional calculations, recipe management)
3. WHEN menu services need data persistence THEN they SHALL use repository interfaces without knowing the implementation
4. WHEN menu services are tested THEN they SHALL be easily mockable through interface dependencies

### Requirement 6

**User Story:** As a developer, I want proper error handling and menu domain exceptions, so that menu business rule violations are clearly expressed and handled appropriately.

#### Acceptance Criteria

1. WHEN menu domain rules are violated THEN menu-specific exceptions SHALL be raised (ItemNotAvailableError, InsufficientStockError, InvalidNutritionalDataError)
2. WHEN infrastructure errors occur THEN they SHALL be translated to menu domain exceptions at the adapter boundary
3. WHEN menu exceptions are handled THEN they SHALL provide meaningful menu business context
4. WHEN menu errors propagate THEN they SHALL not expose infrastructure implementation details

### Requirement 7

**User Story:** As a developer, I want the existing menu API endpoints to continue working without changes, so that the refactoring is transparent to API consumers.

#### Acceptance Criteria

1. WHEN the menu refactoring is complete THEN all existing menu API endpoints SHALL continue to work identically
2. WHEN menu API responses are generated THEN they SHALL maintain the same structure and format
3. WHEN menu API requests are processed THEN they SHALL follow the same validation and menu business rules
4. WHEN the application is deployed THEN existing menu clients SHALL not require any changes