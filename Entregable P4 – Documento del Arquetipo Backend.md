**PONTIFICIA UNIVERSIDAD CATÓLICA DEL PERÚ**

 

**FACULTAD DE CIENCIAS E INGENIERÍA**

 

**INGENIERÍA INFORMÁTICA**

 

 

![Imagen relacionada][image1]

 

 

 

                                                       	

**Documento de Arquetipo del Proyecto**

 

 

 

 

 

**ELABORADO POR:**

 Andree Salazar Ttito

 

 

| Historial de Revisiones |  |  |  |
| ----- | :---- | :---- | :---- |
| **Fecha** | **Versión** | **Descripción** | **Responsable** |
| 15/04/2025 | Versión 1.0 | Arquetipo de Backend | Andree Salazar Ttito  |

# **1\.**  **Introducción**

En este documento se define y estandariza el **arquetipo de backend** para el proyecto de la plataforma de atención de restaurantes. Su propósito es proporcionar una **base reutilizable y consistente** para el desarrollo de servicios en **Python 3.11 \+ FastAPI**, siguiendo principios de separación de capas, desacoplamiento, observabilidad y seguridad.

Este arquetipo tiene como objetivos principales:

* **Estandarizar** la creación de servicios backend en FastAPI con una estructura modular (routers, servicios, repositorios, DTOs, mappers, seguridad, configuración).

* **Asegurar la calidad** mediante componentes integrados para:

  * Seguridad basada en **JWT** y control de roles.

  * **Observabilidad** con logs estructurados, trazabilidad y métricas.

  * **Pruebas** unitarias y de integración automatizadas con pytest.

* **Facilitar la integración con sistemas externos**, en especial en los casos donde **no exista una API oficial expuesta por los proveedores o comercios**.

  * Para fuentes **estáticas** (HTML renderizado servidor) se estandariza el uso de **web scraping con BeautifulSoup** sobre `httpx` y `lxml`.

  * Para fuentes **dinámicas** (SPAs, contenido cargado con JavaScript, formularios con login) se integra un módulo de **RPA** basado en **Playwright** o **Selenium**, lo que permite automatizar interacciones de navegador (login, clicks, descargas de reportes).

# **2\.**  **Objetivos**

Definir un **arquetipo Backend (Python 3.11 \+ FastAPI)** reutilizable para **acelerar la creación de servicios REST** organizados en capas bien definidas (routers, servicios, repositorios, modelos, DTOs, mappers y configuración), con soporte para:

* **Seguridad JWT** y control de accesos por roles.

* **Observabilidad integrada** (logs estructurados, trazabilidad de peticiones, métricas).

* **Tooling de calidad** (pytest, black, ruff, mypy, pre-commit) y pipelines de CI/CD.

* **Plantillas operativas** listas para entornos locales, staging y producción (Docker \+ Alembic para migraciones, Redis para cache/idempotencia, y APScheduler para tareas programadas).

* **Módulos de integración externos** mediante **web scraping con BeautifulSoup** y, cuando sea necesario, **RPA con Playwright/Selenium**, para aquellos proveedores que no dispongan de APIs oficiales.

Este arquetipo está alineado a los **módulos y requisitos del sistema de restaurantes**, entre los que destacan:

* **Gestión de Mesas y Ocupación**

* **Carta Digital Interactiva (vía scraping/RPA de proveedores o fuentes externas)**

* **Personalización de Pedidos**

* **Solicitudes en Mesa**

* **Comandas en Tiempo Real**

* **Identificación de Pedidos por Comensal**

* **Pagos y División de Cuentas**  
     
    

# **3\.**  **Estructura del arquetipo**

El diseño de la estructura del producto,busca reducir el acoplamiento ,mejorar la mantenibilidad y testabilidad y acelerar la integración y el despliegue continuo. Este arquetipo considera el IDE de Visual Studio Code, junto con la extensión de Java para VSCode, el soporte para Spring Boot (Spring Initializr y Spring Tools) y el plugin de Docker. Se eligió este IDE por su ligereza, amplia comunidad y facilidad de integración con contenedores, depuración y herramientas de calidad de código. Además, permite una configuración homogénea en los equipos de desarrollo, garantizando portabilidad y productividad.   
Justificación por carpeta o capa:

## **Principios y patrones aplicados**

**SoC / SRP (Separación de responsabilidades):** cada capa cumple un rol único y aislado.

**Inversión de dependencias:** los *routers* dependen de servicios, y estos de repositorios (interfaces de persistencia).

**DDD ligero \+ Clean/Hexagonal pragmático:**

* `models/` (dominio)

* `services/` (casos de uso)

* `routers/` (adaptadores HTTP)

* `repositories/` (puertos de persistencia)

  **DTOs \+ Mappers:** se evita filtrar entidades de dominio hacia la API. Los *schemas* Pydantic aseguran contratos estables.

  **Convenciones \> configuraciones:** la estructura es repetible y fácilmente entendible para nuevos miembros.

## **Justificación por carpeta/capa**

**routers/**: Endpoints HTTP finos. Traduce HTTP ↔ casos de uso. No contiene reglas de negocio. Facilita versionado de API, validación de entrada y documentación automática (Swagger/ReDoc).

**services/**

* Orquesta la lógica de negocio y reglas de aplicación.

* Contiene interfaces que pueden ser fácilmente *mockeadas* en pruebas.

  **repositories/**: Acceso a datos (SQLAlchemy ORM/Core). Abstrae el motor de base de datos; permite cambiar o mejorar consultas sin alterar la lógica de negocio.

  **models/**: Entidades de dominio coherentes y validadas (SQLAlchemy). Mantienen reglas invariables cercanas a los datos.

  **schemas/**: Contratos de entrada/salida (Pydantic). Mejoran la seguridad (no exponen campos internos) y permiten evolución del API.

  **mappers/**: Conversión explícita entre `models` y `schemas` (manuales o `from_orm`). Reduce código repetitivo y evita errores.

  **core/config.py**: Configuración centralizada (CORS, OpenAPI, logging, conexión a BD, Redis). Evita configuraciones dispersas.

  **core/security.py**: Políticas de autenticación/autorización (JWT/OAuth2, dependencias de seguridad). Mantiene la seguridad separada del negocio.

  **core/exceptions.py**: Manejo global de excepciones (`ExceptionHandler`). Respuestas uniformes, auditables y consistentes.

  **oai/**: Integraciones externas sin API oficial:

* **sources/**: Scraping (BeautifulSoup/httpx) y RPA (Playwright/Selenium).

* **contracts/**: DTOs normalizados de las integraciones.

* **orchestrator.py**: Selección de estrategia HTTP o RPA.

* **cache.py**: cacheo de resultados en Redis.

  **jobs/** y **scheduler/**: Tareas programadas (APScheduler, Celery) para scraping recurrente, limpieza de caché, notificaciones, etc., sin bloquear peticiones HTTP.

  **util/**: Helpers pequeños, genéricos y puros (rate limiting, paginación, circuit breaker). Evitar clases “dios” con lógica extensa y confusa.

  **middlewares/**: Middleware para request-id, idempotencia, logging, rate limiting.

  **tests/**: Espejo de la estructura principal por capas. Mejora cobertura y facilita pruebas unitarias y de integración con `pytest` \+ `httpx`.

  **logs/**: Salida unificada para troubleshooting, auditoría y observabilidad (estructurados con structlog/loguru).

  **alembic/**: Migraciones reproducibles de base de datos (equivalente a Flyway/Liquibase).

  **target/** (build): Artefactos generados (no se versionan) → soporte a pipelines CI/CD y despliegue en contenedores.

## **Beneficios por atributo de calidad**

* **Mantenibilidad**: módulos pequeños y localización clara de cambios.

* **Testabilidad**: interfaces en `service`, mappers explícitos y repos aislados.

* **Seguridad**: DTO \+ validación \+ `security` dedicado disminuyen superficie de ataque.

* **Rendimiento**: repositorios permiten caching/consultas específicas sin invadir el negocio.

* **Observabilidad**: logging estructurado y puntos únicos de manejo de errores.

* **Portabilidad/DevOps**: empaquetado JAR, `Dockerfile`, migraciones automatizadas.

## **Flujo típico (solicitud–respuesta)**

Cliente (frontend / app móvil / integraciones externas)

↓

Router (FastAPI – capa de entrada)

Define el endpoint (APIRouter).

Valida parámetros con Pydantic.

Documenta automáticamente el contrato OpenAPI.

↓

Service (casos de uso / lógica de negocio)

Orquesta reglas de negocio.

Invoca repositorios, mappers o integraciones externas.

Exponible en interfaces para facilitar pruebas unitarias.

↓

Repository (persistencia con SQLAlchemy)

Abstrae acceso a la base de datos.

Implementa consultas específicas, optimizadas y seguras.

↓

Base de Datos (PostgreSQL / MySQL / SQLite)

Estado persistente de entidades de dominio.

↔

Mapper (schemas ⇆ models)

Traducción entre modelos de dominio (SQLAlchemy) y DTOs (Pydantic).

Garantiza contratos limpios y evita exponer campos internos.  
 

| Proyecto/ ├─ .gitignore ├─ .env (opcional, variables de entorno) ├─ Dockerfile (opcional, para contenedores) ├─ pyproject.toml (o requirements.txt, gestor de dependencias) ├─ README.md │ ├─ logs/ │   └─ application.log │ ├─ alembic/                  \# Migraciones de BD (equivalente a Liquibase/Flyway) │   ├─ versions/ │   └─ env.py │ ├─ app/                      \# Código principal │   ├─ main.py               \# Punto de entrada (equivalente a Application.java) │   │ │   ├─ core/                 \# Configuración centralizada │   │   ├─ config.py         \# CORS, OpenAPI, BD, Redis │   │   ├─ security.py       \# Seguridad JWT/OAuth2 │   │   ├─ exceptions.py     \# Manejadores de errores globales │   │   ├─ logging.py        \# Logging estructurado │   │   └─ dependencies.py   \# Dependencias comunes (DB, auth, etc.) │   │ │   ├─ routers/              \# Controladores REST (equivalente a controller/) │   │   ├─ mesas.py │   │   ├─ pedidos.py │   │   └─ pagos.py │   │ │   ├─ services/             \# Casos de uso (equivalente a service/) │   │   ├─ mesa\_service.py │   │   └─ pedido\_service.py │   │ │   ├─ repositories/         \# Persistencia (equivalente a repository/) │   │   ├─ mesa\_repository.py │   │   └─ pedido\_repository.py │   │ │   ├─ models/               \# Entidades de dominio (SQLAlchemy) │   │   ├─ mesa.py │   │   └─ pedido.py │   │ │   ├─ schemas/              \# DTOs de entrada/salida (Pydantic) │   │   ├─ mesa.py │   │   └─ pedido.py │   │ │   ├─ mappers/              \# Conversión model ⇆ schema │   │   └─ mesa\_mapper.py │   │ │   ├─ jobs/                 \# Tareas en background (APScheduler, Celery) │   │   └─ cleaners.py │   │ │   ├─ scheduler/            \# Configuración de jobs │   │   └─ setup.py │   │ │   ├─ oai/                  \# Integraciones externas (scraping/RPA) │   │   ├─ contracts/        \# DTOs de integraciones │   │   ├─ sources/          \# Scrapers/RPA por fuente │   │   ├─ orchestrator.py   \# Selección HTTP vs RPA │   │   └─ cache.py          \# Cache con Redis │   │ │   ├─ util/                 \# Utilidades/helpers │   │   ├─ pagination.py │   │   └─ rate\_limit.py │   │ │   ├─ middlewares/          \# Middlewares (idempotencia, trace, etc.) │   │   ├─ request\_id.py │   │   └─ idempotency.py │   │ │   └─ resources/            \# Archivos de config (equivalente a application.yml) │       ├─ application.yml │       └─ log\_config.yaml │ ├─ tests/                    \# Pruebas (pytest, httpx) │   ├─ conftest.py           \# Configuración global de tests │   ├─ test\_health.py        \# Test de salud │   │ │   ├─ routers/              \# Tests de controladores │   │   └─ test\_mesas.py │   │ │   ├─ services/             \# Tests de servicios │   │   └─ test\_mesa\_service.py │   │ │   ├─ repositories/         \# Tests de repositorios │   │   └─ test\_mesa\_repository.py │   │ │   └─ util/                 \# Tests de helpers │       └─ test\_pagination.py │ ├─ target/                   \# (build/output, similar a Maven target/) │   ├─ app-version.whl       \# paquete compilado │   └─ dist/                 \# distribución final  |
| :---- |

# **3\.**  **Contratos de API**

## **1\) Información General**

* **Sistema:** `<Nombre>`  
* **Base URL:** `https://api.<dominio>.com/api/v1` (prod) · `http://localhost:8085/api/v1` (dev)  
* **Versionado:** por ruta (`/api/v1`; cambios rompientes → `/api/v2`)  
* **Formato:** JSON (UTF-8) · **Fechas:** ISO-8601 (UTC)

## **2\) AuthN/AuthZ**

* **Esquema:** Bearer JWT → `Authorization: Bearer <token>`

* **Roles (ej.):** 

* **Refresh:** `POST /auth/refresh`

* **Errores:** `401` (no auth), `403` (sin permiso)

## **3\) Encabezados Comunes**

* `Content-Type: application/json`

* `Accept: application/json`

* `X-Request-Id` (opcional, UUID)

* `X-Idempotency-Key` (POST/PUT críticos)

* `X-Trace-Id` (devuelto por el server)

## **4\) Paginación y Filtros**

* **Query:** `page` (≥0), `size` (1–200), `sort` (`campo,asc|desc`), `search`

* **Respuesta:**

{"content":\[...\],"page":0,"size":20,"totalElements":153,"totalPages":8,"sort":\["name,asc"\]}

## **5\) Convenciones de Recursos**

* **Rutas:** plural \+ kebab-case (`/users`, `/purchase-orders`)

* **ID en path:** `/users/{id}` · **Subrecursos:** `/orders/{id}/items`

* **Métodos:** GET (leer), POST (crear), PUT (reemplazar), PATCH (parcial), DELETE (eliminar)

* **Idempotencia:** PUT/DELETE; POST \+ `X-Idempotency-Key` si aplica

## **6\) Error Uniforme**

{  
  "timestamp":"\<ISO8601\>",  
  "traceId":"\<uuid\>",  
  "status":400,  
  "code":"VALIDATION\_ERROR",  
  "message":"Datos inválidos",  
  "details":\[{"field":"email","error":"must\_be\_valid\_email"}\]  
}

## **7\) Esquemas Básicos**

**Metadatos:**

{"id":"uuid","createdAt":"\<ISO\>","updatedAt":"\<ISO\>","version":1}

**Recurso genérico:**

{"id":"r1","name":"Recurso","status":"ACTIVE","tags":\["t1"\],"metadata":{}}

## **8\) CRUD (plantillas)**

* **Listado:** `GET /<recurso>?page=0&size=20&sort=name,asc&status=ACTIVE`

* **Por ID:** `GET /<recurso>/{id}`

* **Crear:** `POST /<recurso>` (+ `X-Idempotency-Key`)

{"name":"Nuevo","status":"ACTIVE"}

**201:**

{"id":"r3","name":"Nuevo","status":"ACTIVE","createdAt":"\<ISO\>"}

* **Actualizar:** `PUT /<recurso>/{id}` · **Parcial:** `PATCH /<recurso>/{id}`

* **Eliminar:** `DELETE /<recurso>/{id}` → `204`

## **9\) Acciones de Dominio**

* **Patrón:** `/<recurso>/{id}/<acción>` (POST/PUT)

* **Ej.:** `POST /orders/{id}/confirm`

{"id":"o-1","status":"CONFIRMED","effectiveAt":"\<ISO\>"}

## **10\) Operación y Seguridad**

* **Rate limit:** `429` \+ `X-RateLimit-*`

* **CORS:** orígenes permitidos; métodos `GET,POST,PUT,PATCH,DELETE,OPTIONS`

* **Deprecación:** headers `Deprecation: true`, `Sunset: <fecha>`, link de migración

## **11\) Códigos HTTP (mínimos)**

`200` OK · `201` Created · `204` No Content · `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found · `409` Conflict · `422` Unprocessable · `429` Too Many · `500` Internal · `503` Unavailable

### **Mini-ejemplos (copiar/pegar)**

**Listado**

GET https://api.\<dominio\>.com/api/v1/\<recurso\>?page=0\&size=20\&sort=name,asc\&search=foo

**Crear**

POST https://api.\<dominio\>.com/api/v1/\<recurso\>  
Headers: Authorization, Content-Type, X-Idempotency-Key  
Body: {"name":"Nuevo","status":"ACTIVE"}

**Error**

{"timestamp":"\<ISO\>","traceId":"\<uuid\>","status":404,"code":"NOT\_FOUND","message":"No existe"}

[image1]: <data:image/png;base64,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>