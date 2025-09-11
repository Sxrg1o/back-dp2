# Implementation Plan - Menu and Carta Module

- [x] 1. Create menu domain layer foundation





  - Create directory structure for menu domain layer
  - Implement menu value objects with validation logic
  - Create pure menu domain entities without infrastructure dependencies
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 1.1 Create menu domain directory structure and value objects



  - Create app/domain/value_objects directory and **init**.py files
  - Implement EtiquetaItem enum (SIN_GLUTEN, PICANTE, SALADO, CALIENTE, FRIO, ACIDO, AGRIO, CON_GLUTEN, VEGANO)
  - Implement EtiquetaIngrediente enum (VERDURA, CARNE, FRUTA)
  - Implement EtiquetaPlato enum (ENTRADA, FONDO, POSTRE)
  - Implement Precio value object with validation for positive values
  - Implement InformacionNutricional value object with calories, proteins, sugars
  - Write unit tests for value objects validation and immutability
  - _Requirements: 1.1, 1.2, 1.3_


- [x] 1.2 Implement menu domain entities


  - Create app/domain/entities directory with menu entity classes
  - Implement Item base entity with nutritional info, price, preparation time, stock verification
  - Implement Ingrediente entity with stock management and type classification
  - Implement Plato entity extending Item with recipe and dish type
  - Implement Bebida entity extending Item with volume and alcohol content
  - Add business methods: verificarStock(), calcularCalorias(), isDisponible()
  - Write unit tests for menu entity business logic
  - _Requirements: 1.1, 1.2, 1.3_



- [-] 1.3 Create menu domain exceptions




  - Create app/domain/exceptions directory with menu-specific exceptions
  - Implement MenuDomainException, ItemNotFoundError, ItemNotAvailableError
  - Implement InsufficientStockError, InvalidNutritionalDataError, InvalidPriceError
  - Write unit tests for exception handling
  - _Requirements: 6.1, 6.2, 6.3_

- [ ] 2. Define menu repository ports (interfaces)

  - Create menu repository interfaces in domain layer
  - Define abstract methods for menu data access operations
  - Ensure interfaces return menu domain entities, not ORM objects
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 2.1 Implement menu repository port interfaces

  - Create app/domain/repositories directory with menu repository interfaces
  - Implement ItemRepositoryPort with methods: get_by_id, get_available_items, get_by_category, save, delete
  - Implement IngredienteRepositoryPort with methods: get_by_id, get_by_type, check_stock, update_stock
  - Implement PlatoRepositoryPort with methods: get_by_id, get_by_dish_type, get_with_ingredients
  - Implement BebidaRepositoryPort with methods: get_by_id, get_alcoholic, get_non_alcoholic
  - Ensure all methods work with menu domain entities and value objects
  - Write interface documentation with expected behaviors
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 3. Create menu infrastructure persistence layer

  - Implement SQLAlchemy models separate from menu domain entities
  - Create menu entity-model mappers for conversion
  - Implement menu repository adapters that implement domain ports
  - _Requirements: 3.1, 3.2, 3.3_

- [ ] 3.1 Create menu SQLAlchemy models in infrastructure layer

  - Create app/infrastructure/persistence/models directory structure
  - Implement BaseModel for common audit fields (id, created_at, updated_at, version)
  - Implement ItemModel with SQLAlchemy annotations for nutritional data, price, stock
  - Implement IngredienteModel with stock, weight, type fields
  - Implement PlatoModel extending ItemModel with recipe and dish type
  - Implement BebidaModel extending ItemModel with volume and alcohol content
  - Write database migration scripts for menu model structure
  - _Requirements: 3.1, 3.2_

- [ ] 3.2 Implement menu entity-model mappers

  - Create app/infrastructure/persistence/mappers directory with menu mapper classes
  - Implement ItemMapper with to_entity and to_model methods for Item domain entity
  - Implement IngredienteMapper for Ingrediente entity conversion
  - Implement PlatoMapper for Plato entity conversion with recipe handling
  - Implement BebidaMapper for Bebida entity conversion
  - Handle enum conversion for EtiquetaItem, EtiquetaIngrediente, EtiquetaPlato
  - Write unit tests for bidirectional mapping accuracy
  - _Requirements: 3.2, 3.3_

- [ ] 3.3 Create menu SQLAlchemy repository adapters

  - Create app/infrastructure/persistence/repositories directory
  - Implement SqlAlchemyItemRepository that implements ItemRepositoryPort
  - Implement SqlAlchemyIngredienteRepository that implements IngredienteRepositoryPort
  - Implement SqlAlchemyPlatoRepository that implements PlatoRepositoryPort
  - Implement SqlAlchemyBebidaRepository that implements BebidaRepositoryPort
  - Use mappers for entity-model conversion in all operations
  - Implement complex queries for menu operations (available items, stock checks)
  - Write integration tests with test database
  - _Requirements: 3.1, 3.2, 3.3_

- [ ] 4. Implement menu application layer services

  - Create menu application services that use repository ports
  - Implement menu DTOs for data transfer between layers
  - Ensure services work only with menu domain entities and interfaces
  - _Requirements: 5.1, 5.2, 5.3_

- [ ] 4.1 Create menu application DTOs

  - Create app/application/dto directory with menu DTOs
  - Implement CreateItemDTO, UpdateItemDTO with nutritional validation
  - Implement CreateIngredienteDTO, UpdateIngredienteDTO with stock validation
  - Implement CreatePlatoDTO with recipe and ingredient validation
  - Implement CreateBebidaDTO with volume and alcohol content validation
  - Use Pydantic for validation with business rules
  - Write unit tests for DTO validation rules
  - _Requirements: 5.1, 5.2_

- [ ] 4.2 Implement menu application services

  - Create app/application/services directory with menu service classes
  - Implement MenuApplicationService for menu management operations
  - Implement ItemApplicationService with use cases: create_item, update_item, get_available_items, check_stock
  - Implement IngredienteApplicationService with stock management and ingredient operations
  - Use dependency injection for repository ports
  - Implement business rules: stock verification, nutritional calculations, availability checks
  - Write unit tests with mocked repository implementations
  - _Requirements: 5.1, 5.2, 5.3_

- [ ] 5. Setup menu dependency injection container

  - Create dependency injection configuration for menu module
  - Wire menu repository implementations to interfaces
  - Configure menu application services with proper dependencies
  - _Requirements: 4.1, 4.2, 4.3_

- [ ] 5.1 Create menu dependency injection container

  - Create app/infrastructure/web/dependencies directory and container module
  - Implement dependency injection for menu repository and service instances
  - Configure FastAPI dependencies to use menu container
  - Setup proper lifecycle management for database connections
  - Write tests for menu dependency resolution
  - _Requirements: 4.1, 4.2, 4.3_

- [ ] 6. Refactor menu API controllers to use new architecture

  - Update FastAPI menu controllers to use application services
  - Maintain existing menu API contract and response formats
  - Ensure backward compatibility with current menu API
  - _Requirements: 7.1, 7.2, 7.3_

- [ ] 6.1 Create new menu API schemas in infrastructure layer

  - Create app/infrastructure/web/schemas directory with menu API request/response schemas
  - Implement ItemSchema, IngredienteSchema, PlatoSchema, BebidaSchema
  - Implement schemas that match existing menu API contract
  - Add mappers between menu DTOs and API schemas
  - Handle enum serialization for menu labels
  - Write unit tests for schema validation
  - _Requirements: 7.1, 7.2_

- [ ] 6.2 Implement new menu controllers

  - Create app/infrastructure/web/controllers directory with menu controller classes
  - Implement MenuController for general menu operations
  - Implement ItemController for item management endpoints
  - Implement all existing menu endpoints using menu application services
  - Maintain exact same API responses and status codes
  - Add proper error handling for menu operations
  - Write integration tests for all menu endpoints
  - _Requirements: 7.1, 7.2, 7.3_

- [ ] 7. Update menu routing and middleware integration

  - Update FastAPI app to use new menu controllers
  - Ensure all middleware continues to work with menu endpoints
  - Maintain existing error handling behavior for menu operations
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 7.1 Update FastAPI application configuration for menu module

  - Modify main.py to use new menu controllers and dependency injection
  - Update router registration to use new MenuController and ItemController
  - Ensure all existing middleware and exception handlers work with menu endpoints
  - Configure proper database session management for menu operations
  - Write end-to-end tests for complete menu request flow
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 8. Remove old menu architecture components

  - Remove old menu models, repositories, and services
  - Clean up unused imports and dependencies
  - Update all menu tests to use new architecture
  - _Requirements: 7.4_

- [ ] 8.1 Clean up legacy menu code

  - Remove old menu-related models from app/models/
  - Remove old menu repositories from app/repositories/
  - Remove old menu services from app/services/
  - Update all import statements throughout the codebase for menu components
  - Remove unused menu dependencies from requirements
  - Ensure no references to old menu architecture remain
  - _Requirements: 7.4_

- [ ] 8.2 Update all menu tests to new architecture
  - Refactor existing menu tests to use new domain entities and services
  - Update test fixtures and mocks for new menu architecture
  - Add comprehensive tests for menu domain layer components:
    - Item, Ingrediente, Plato, Bebida entity tests
    - Menu value object tests (EtiquetaItem, Precio, InformacionNutricional)
    - Menu repository adapter tests
    - Menu application service tests
    - Menu controller integration tests
  - Ensure all menu tests pass with new implementation
  - Add performance tests for menu database operations
  - _Requirements: 7.4_
