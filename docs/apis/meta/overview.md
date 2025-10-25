# Overview — Arquitectura del Sistema

[⬅ Volver al Índice](../README.md)

## Arquitectura General

El **Restaurant Backend API** sigue una arquitectura en capas basada en **FastAPI** (Python) con separación de responsabilidades:

```
┌─────────────────────────────────────┐
│      API Layer (Controllers)        │  ← FastAPI Routers
├─────────────────────────────────────┤
│   Business Logic (Services)         │  ← Lógica de negocio
├─────────────────────────────────────┤
│      Data Access (Repositories)     │  ← Acceso a datos
├─────────────────────────────────────┤
│         Database (PostgreSQL)       │  ← Persistencia
└─────────────────────────────────────┘
```

## Componentes Principales

### 1. API Layer (`src/api/controllers/`)
- Define los **endpoints REST** usando FastAPI routers
- Maneja validación de entrada con **Pydantic schemas**
- Transforma excepciones de negocio a respuestas HTTP
- Documentación automática con OpenAPI 3.1

### 2. Business Logic (`src/business_logic/`)
- Contiene la **lógica de negocio**
- Servicios por dominio (menu, pedidos, auth, etc.)
- Validaciones de reglas de negocio
- Excepciones personalizadas por módulo

### 3. Data Access (`src/models/`)
- Modelos **SQLAlchemy** (ORM)
- Definición de relaciones entre entidades
- Configuración de índices y constraints

### 4. Core (`src/core/`)
- Configuración global (`config.py`)
- Gestión de base de datos (`database.py`)
- Logging (`logging.py`)
- Dependencias compartidas (`dependencies.py`)

## Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Framework | FastAPI | 0.100+ |
| ORM | SQLAlchemy | 2.0+ |
| Base de Datos | PostgreSQL | 14+ |
| Validación | Pydantic | 2.0+ |
| ASGI Server | Uvicorn | Latest |
| Migraciones | Alembic | 1.11+ |

## Patrones de Diseño

- **Repository Pattern** — Abstracción de acceso a datos
- **Service Layer** — Encapsulación de lógica de negocio
- **Dependency Injection** — Inyección de dependencias con FastAPI
- **DTO Pattern** — Schemas Pydantic como Data Transfer Objects

## Flujo de Request

```
1. Cliente → HTTP Request
2. FastAPI Router → Valida entrada (Pydantic)
3. Controller → Delega a Service
4. Service → Ejecuta lógica de negocio
5. Service → Consulta/modifica datos (ORM)
6. Database → Retorna resultados
7. Service → Transforma a DTO (Pydantic)
8. Controller → Retorna HTTP Response
```

## Convenciones de Código

- **Async/Await** — Todas las operaciones son asíncronas
- **Type Hints** — Tipado estricto en Python
- **Docstrings** — Documentación estilo Google
- **Logging** — Logs estructurados con niveles INFO/WARNING/ERROR
