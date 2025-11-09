# DOCUMENTACIÓN COMPLETA - RESTAURANT BACKEND API

**Proyecto:** Back-DP2
**Framework:** FastAPI (Python 3.13+)
**Arquitectura:** Clean Architecture (Capas)
**ORM:** SQLAlchemy 2.0 (Async)
**Base de Datos:** MySQL / PostgreSQL
**Autenticación:** JWT (Access/Refresh Tokens)
**Versión:** 1.0.0
**Fecha:** Noviembre 2025

---

# TABLA DE CONTENIDOS

1. [Guía de Estándares de Codificación](#1-guía-de-estándares-de-codificación)
2. [Documento de Diseño Técnico (TDD)](#2-documento-de-diseño-técnico-tdd)
3. [Documentación de API REST](#3-documentación-de-api-rest)
4. [Modelos de Datos y Esquemas de BD](#4-modelos-de-datos-y-esquemas-de-bd)
5. [Anexos](#5-anexos)

---

# 1. GUÍA DE ESTÁNDARES DE CODIFICACIÓN

## 1.1 Convenciones de Nomenclatura

### 1.1.1 Variables

**Convención:** `snake_case` descriptivo

**Ejemplos del código:**
```python
# Variables locales (usuario_service.py:50-75)
usuario = await self.repository.get_by_email(login_data.email)
password_hash = security.get_password_hash(register_data.password)
token_data = {"sub": usuario.id, "email": usuario.email}
access_token = security.create_access_token(token_data)
refresh_token = security.create_refresh_token(token_data)
usuario_response = UsuarioResponse.model_validate(usuario)
existing_usuario = await self.repository.get_by_email(register_data.email)
created_usuario = await self.repository.create(usuario)
update_data = usuario_data.model_dump(exclude_none=True)
```

### 1.1.2 Funciones/Métodos

**Convención:** `snake_case` con verbos descriptivos

**Patrones de naming:**
- **CRUD:** `create`, `get_by_id`, `get_all`, `update`, `delete`
- **Business Logic:** `login`, `register`, `validate_product_data`
- **Privados:** `_generate_numero_pedido`, `_validate_price`

**Ejemplos del código:**
```python
# CRUD Operations (usuario_repository.py:31-117)
async def create(self, usuario: UsuarioModel) -> UsuarioModel
async def get_by_id(self, usuario_id: str) -> Optional[UsuarioModel]
async def get_by_email(self, email: str) -> Optional[UsuarioModel]
async def delete(self, usuario_id: str) -> bool
async def update(self, usuario_id: str, **kwargs) -> Optional[UsuarioModel]
async def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List, int]

# Business Logic (usuario_service.py:40-254)
async def login(self, login_data: LoginRequest) -> LoginResponse
async def register(self, register_data: RegisterRequest) -> RegisterResponse
async def refresh_token(self, refresh_data: RefreshTokenRequest) -> RefreshTokenResponse
async def get_usuario_by_id(self, usuario_id: str) -> UsuarioResponse
async def update_usuario(self, usuario_id: str, usuario_data: UsuarioUpdate) -> UsuarioResponse
async def delete_usuario(self, usuario_id: str) -> bool
```

### 1.1.3 Clases

**Convención:** `PascalCase` con sufijos descriptivos

**Sufijos por tipo:**
| Tipo | Sufijo | Ejemplo |
|------|--------|---------|
| Modelos | `Model` | `UsuarioModel`, `ProductoModel` |
| Repositorios | `Repository` | `UsuarioRepository`, `ProductoRepository` |
| Servicios | `Service` | `UsuarioService`, `PedidoService` |
| Schemas (DTOs) | `Create`/`Update`/`Response`/`Summary` | `UsuarioCreate`, `UsuarioResponse` |
| Excepciones | `Error` | `UsuarioNotFoundError`, `ValidationError` |
| Mixins | `Mixin` | `AuditMixin`, `SoftDeleteMixin` |

**Ejemplos del código:**
```python
# Models (usuario_model.py:15)
class UsuarioModel(BaseModel, AuditMixin):

# Repositories (usuario_repository.py:13)
class UsuarioRepository:

# Services (usuario_service.py:33)
class UsuarioService:

# Schemas (usuario_schema.py:10-68)
class UsuarioBase(BaseModel):
class UsuarioCreate(UsuarioBase):
class UsuarioUpdate(BaseModel):
class UsuarioResponse(UsuarioBase):
class UsuarioSummary(BaseModel):

# Exceptions (usuario_exceptions.py:7-70)
class UsuarioValidationError(ValidationError):
class UsuarioNotFoundError(NotFoundError):
class UsuarioConflictError(ConflictError):
class InvalidCredentialsError(UnauthorizedError):

# Mixins (audit_mixin.py:15)
class AuditMixin:
```

### 1.1.4 Archivos

**Convención:** `snake_case` con sufijos descriptivos

**Patrones:**
- Modelos: `*_model.py`
- Repositorios: `*_repository.py`
- Servicios: `*_service.py`
- Controladores: `*_controller.py`
- Schemas: `*_schema.py`
- Excepciones: `*_exceptions.py`
- Enums: `*_enums.py`
- Mixins: `*_mixin.py`
- Utils: `*_utils.py`
- Validators: `*_validators.py`

**Evidencia en el proyecto:**
```
src/models/auth/usuario_model.py
src/models/menu/producto_model.py
src/repositories/auth/usuario_repository.py
src/repositories/menu/producto_repository.py
src/business_logic/auth/usuario_service.py
src/business_logic/pedidos/pedido_service.py
src/api/controllers/auth_controller.py
src/api/controllers/producto_controller.py
src/api/schemas/usuario_schema.py
src/api/schemas/producto_schema.py
src/business_logic/exceptions/usuario_exceptions.py
src/core/enums/pedido_enums.py
src/models/mixins/audit_mixin.py
src/core/utils/text_utils.py
src/business_logic/validators/producto_validators.py
```

### 1.1.5 Constantes

**Convención:** `SCREAMING_SNAKE_CASE`

**Ejemplos del código:**
```python
# Transiciones de estado (pedido_service.py:56-63)
VALID_TRANSITIONS = {
    EstadoPedido.PENDIENTE: [EstadoPedido.CONFIRMADO, EstadoPedido.CANCELADO],
    EstadoPedido.CONFIRMADO: [EstadoPedido.EN_PREPARACION, EstadoPedido.CANCELADO],
    EstadoPedido.EN_PREPARACION: [EstadoPedido.LISTO, EstadoPedido.CANCELADO],
    EstadoPedido.LISTO: [EstadoPedido.ENTREGADO],
    EstadoPedido.ENTREGADO: [],
    EstadoPedido.CANCELADO: [],
}

# Instancias singleton (security.py:130, database.py:137)
security = SecurityConfig()
db = DatabaseManager()
```

---

## 1.2 Formato y Estilo

### 1.2.1 Indentación
- **Espacios:** 4 espacios (NO tabs)
- **Evidencia:** Todo el código del proyecto usa 4 espacios

### 1.2.2 Límites de línea
- **Máximo:** 120 caracteres por línea
- **Preferencia:** Dividir líneas largas en múltiples líneas

### 1.2.3 Uso de llaves y formato
**Patrón Python:** No aplica (Python usa indentación)

**Para diccionarios y listas:**
```python
# Formato correcto (usuario_service.py:60-65)
token_data = {
    "sub": usuario.id,
    "email": usuario.email,
    "rol": usuario.rol.nombre
}

# Listas multilinea
controllers = [
    ("src.api.controllers.auth_controller", "Autenticación"),
    ("src.api.controllers.rol_controller", "Roles"),
    ("src.api.controllers.producto_controller", "Productos"),
]
```

### 1.2.4 Espaciado

**Reglas:**
- Espacios alrededor de operadores: `a + b`, `x = 10`
- Sin espacios en parámetros por defecto: `def func(a=5)`
- Espacio después de comas: `[1, 2, 3]`, `func(a, b, c)`

**Ejemplos del código:**
```python
# Correcto (producto_service.py:50)
precio_total = precio_base + precio_opciones
cantidad_disponible = stock - pedidos_pendientes

# Asignaciones con tipo (usuario_model.py:20-25)
email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
password_hash: Mapped[Optional[str]] = mapped_column(String(255))
nombre: Mapped[Optional[str]] = mapped_column(String(255))
```

---

## 1.3 Principios y Patrones de Diseño

### 1.3.1 Principios SOLID

#### **S - Single Responsibility Principle ✅ CUMPLE**

**Evidencia:**
```python
# Controller (auth_controller.py:145-155) - Solo HTTP
@router.post("/login")
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_database_session),
) -> LoginResponse:
    usuario_service = UsuarioService(session)
    result = await usuario_service.login(login_data)
    await session.commit()
    return result

# Service (usuario_service.py:40-80) - Solo lógica de negocio
async def login(self, login_data: LoginRequest) -> LoginResponse:
    usuario = await self.repository.get_by_email(login_data.email)
    if not usuario:
        raise InvalidCredentialsError("Email o contraseña incorrectos")
    if not security.verify_password(login_data.password, usuario.password_hash):
        raise InvalidCredentialsError("Email o contraseña incorrectos")
    access_token = security.create_access_token(token_data)
    return LoginResponse(access_token=access_token, usuario=usuario_response)

# Repository (usuario_repository.py:68-82) - Solo acceso a datos
async def get_by_email(self, email: str) -> Optional[UsuarioModel]:
    query = (
        select(UsuarioModel)
        .where(UsuarioModel.email == email)
        .options(selectinload(UsuarioModel.rol))
    )
    result = await self.session.execute(query)
    return result.scalars().first()
```

#### **O - Open/Closed Principle ✅ CUMPLE**

**Evidencia - Jerarquía de excepciones extensible:**
```python
# Base (base_exceptions.py:4-40)
class BusinessError(Exception):
    pass

class ValidationError(BusinessError):
    pass

class NotFoundError(BusinessError):
    pass

# Extensión (usuario_exceptions.py:7-22)
class UsuarioValidationError(ValidationError):
    pass

class UsuarioNotFoundError(NotFoundError):
    pass
```

#### **L - Liskov Substitution Principle ✅ CUMPLE**

**Evidencia:**
```python
# Base Model (base_model.py:17-64)
class BaseModel(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(26), primary_key=True)

    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Derived Model (usuario_model.py:15, 50-57)
class UsuarioModel(BaseModel, AuditMixin):
    # Hereda to_dict() y puede usarse donde se espera BaseModel
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        return result
```

#### **I - Interface Segregation Principle ✅ CUMPLE**

**Evidencia - Schemas específicos por caso de uso:**
```python
# usuario_schema.py:10-68
class UsuarioBase(BaseModel):
    email: Optional[EmailStr]
    nombre: Optional[str]
    telefono: Optional[str]

class UsuarioCreate(UsuarioBase):
    password: str  # Solo para creación

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]  # Todos opcionales

class UsuarioResponse(UsuarioBase):
    id: str
    activo: bool
    fecha_creacion: datetime  # Solo para respuesta

class UsuarioSummary(BaseModel):
    id: str
    email: str
    nombre: str  # Solo campos esenciales para listas
```

#### **D - Dependency Inversion Principle ✅ CUMPLE**

**Evidencia:**
```python
# Service (usuario_service.py:41-51)
class UsuarioService:
    def __init__(self, session: AsyncSession):  # Depende de abstracción
        self.repository = UsuarioRepository(session)
        self.rol_repository = RolRepository(session)
        self.settings = get_settings()

# Controller (auth_controller.py:133-137)
@router.post("/login")
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_database_session),  # Inyección
) -> LoginResponse:
```

### 1.3.2 Patrones de Diseño Implementados

#### **1. Repository Pattern**

**Ubicación:** `src/repositories/`
**Total:** 32 repositorios

**Evidencia:**
```python
# usuario_repository.py:13-31
class UsuarioRepository:
    """Repositorio para gestionar operaciones CRUD del modelo de usuarios.

    Proporciona acceso a la capa de persistencia siguiendo el patrón Repository.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, usuario: UsuarioModel) -> UsuarioModel:
        self.session.add(usuario)
        await self.session.flush()
        await self.session.refresh(usuario)
        return usuario
```

#### **2. Singleton Pattern**

**Ubicación:** `src/core/database.py`, `src/core/config.py`, `src/core/security.py`

**Evidencia:**
```python
# database.py:18-45
class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

# config.py:135-147
_settings_instance: Optional[Settings] = None

def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
```

#### **3. Dependency Injection Pattern**

**Evidencia:**
```python
# database.py:141-163
async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.session() as session:
        yield session

# auth_controller.py:133-137
@router.post("/login")
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_database_session),
) -> LoginResponse:
```

#### **4. Factory Pattern**

**Evidencia:**
```python
# main.py:163-202
def register_routers(app: FastAPI) -> None:
    controllers = [
        ("src.api.controllers.auth_controller", "Autenticación"),
        ("src.api.controllers.rol_controller", "Roles"),
    ]

    for module_name, tag in controllers:
        module = importlib.import_module(module_name)
        router = getattr(module, "router", None)
        if router and isinstance(router, APIRouter):
            app.include_router(router, prefix=api_prefix)
```

#### **5. Service Layer Pattern**

**Ubicación:** `src/business_logic/`
**Total:** 25+ servicios

**Evidencia:**
```python
# usuario_service.py:33-52
class UsuarioService:
    """Servicio para la gestión de usuarios y autenticación.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con usuarios, incluyendo autenticación, registro, validaciones.
    """

    def __init__(self, session: AsyncSession):
        self.repository = UsuarioRepository(session)
        self.rol_repository = RolRepository(session)
        self.settings = get_settings()
```

#### **6. Mixin Pattern**

**Ubicación:** `src/models/mixins/`

**Evidencia:**
```python
# audit_mixin.py:1-47
@declarative_mixin
class AuditMixin:
    @declared_attr
    def fecha_creacion(cls) -> Mapped[datetime]:
        return mapped_column(TIMESTAMP, nullable=False, server_default=func.now())

    @declared_attr
    def fecha_modificacion(cls) -> Mapped[datetime]:
        return mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

# Uso (usuario_model.py:15)
class UsuarioModel(BaseModel, AuditMixin):
    __tablename__ = "usuarios"
```

#### **7. Strategy Pattern (Enums)**

**Evidencia:**
```python
# pedido_enums.py:1-27
class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

class TipoDivision(str, Enum):
    EQUITATIVA = "equitativa"
    POR_ITEMS = "por_items"
    MANUAL = "manual"
```

#### **8. Middleware Pattern**

**Evidencia:**
```python
# dependencies.py:12-142
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            if isinstance(e, BusinessError):
                return await self._handle_business_error(e, request)
            else:
                return await self._handle_unexpected_error(e, request)

# main.py:259
app.add_middleware(ErrorHandlerMiddleware)
```

#### **9. DTO Pattern (Data Transfer Objects)**

**Ubicación:** `src/api/schemas/`
**Total:** 50+ schemas

**Evidencia:**
```python
# usuario_schema.py:10-68
class UsuarioBase(BaseModel):
    email: Optional[EmailStr] = Field(default=None)
    nombre: Optional[str] = Field(default=None)

class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=6)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v
```

#### **10. Context Manager Pattern**

**Evidencia:**
```python
# database.py:118-139
@asynccontextmanager
async def session(self):
    session = self._session_factory()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

# main.py:110-160
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando Restaurant Backend API...")
    await create_tables()
    yield
    logger.info("Cerrando Restaurant Backend API...")
    await close_database()
```

---

## 1.4 Manejo de Errores y Excepciones

### 1.4.1 Jerarquía de Excepciones

```
Exception (Python built-in)
└── BusinessError (base_exceptions.py:4)
    ├── ValidationError (base_exceptions.py:18)
    ├── NotFoundError (base_exceptions.py:23)
    ├── ConflictError (base_exceptions.py:28)
    ├── UnauthorizedError (base_exceptions.py:33)
    ├── ForbiddenError (base_exceptions.py:38)
    └── ExternalServiceError (base_exceptions.py:43)
        └── (Excepciones específicas por dominio)
```

**Evidencia:**
```python
# base_exceptions.py:4-43
class BusinessError(Exception):
    def __init__(self, message: str, error_code: str | None = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ValidationError(BusinessError):
    pass

class NotFoundError(BusinessError):
    pass

class ConflictError(BusinessError):
    pass
```

### 1.4.2 Excepciones Específicas por Dominio

**Total:** 22 archivos de excepciones, 75+ excepciones personalizadas

**Ejemplos:**
```python
# usuario_exceptions.py:7-70
class UsuarioValidationError(ValidationError):
    def __init__(self, message: str, error_code: str = "USUARIO_VALIDATION_ERROR"):
        super().__init__(message, error_code)

class UsuarioNotFoundError(NotFoundError):
    def __init__(self, message: str = "Usuario no encontrado"):
        super().__init__(message, "USUARIO_NOT_FOUND")

class UsuarioConflictError(ConflictError):
    def __init__(self, message: str, error_code: str = "USUARIO_CONFLICT"):
        super().__init__(message, error_code)

class InvalidCredentialsError(UnauthorizedError):
    def __init__(self, message: str = "Credenciales inválidas"):
        super().__init__(message, "INVALID_CREDENTIALS")
```

### 1.4.3 Formato de Respuesta de Error en APIs

**Formato estándar:**
```json
{
  "error": {
    "type": "ValidationError",
    "message": "El email ya está registrado",
    "code": "EMAIL_EXISTS"
  },
  "path": "/api/v1/auth/register",
  "method": "POST"
}
```

**Evidencia - Middleware global:**
```python
# dependencies.py:36-91
async def _handle_business_error(self, error, request: Request) -> JSONResponse:
    status_code_map = {
        ValidationError: 400,
        NotFoundError: 404,
        ConflictError: 409,
        UnauthorizedError: 401,
        ForbiddenError: 403,
        BusinessError: 400,
    }

    status_code = status_code_map.get(type(error), 400)

    error_response = {
        "error": {
            "type": type(error).__name__,
            "message": error.message,
            "code": getattr(error, "error_code", None),
        },
        "path": str(request.url.path),
        "method": request.method,
    }

    return JSONResponse(status_code=status_code, content=error_response)
```

### 1.4.4 Uso en Servicios

**Evidencia:**
```python
# usuario_service.py:40-115
async def login(self, login_data: LoginRequest) -> LoginResponse:
    usuario = await self.repository.get_by_email(login_data.email)

    if not usuario:
        raise InvalidCredentialsError("Email o contraseña incorrectos")

    if not usuario.activo:
        raise InactiveUserError("El usuario está inactivo")

    if not security.verify_password(login_data.password, usuario.password_hash):
        raise InvalidCredentialsError("Email o contraseña incorrectos")

async def register(self, register_data: RegisterRequest) -> RegisterResponse:
    if not register_data.email:
        raise UsuarioValidationError("El email es requerido")

    existing_usuario = await self.repository.get_by_email(register_data.email)
    if existing_usuario:
        raise UsuarioConflictError(f"Ya existe un usuario con el email '{register_data.email}'")
```

---

## 1.5 Comentarios y Documentación en Código

### 1.5.1 Docstrings

**Formato:** Google Style / NumPy Style

**Para módulos:**
```python
# usuario_model.py:1-4
"""
Modelo de Usuario para autenticación y gestión de usuarios.

Define la estructura de la tabla usuarios en la base de datos.
"""
```

**Para clases:**
```python
# usuario_service.py:33-45
class UsuarioService:
    """Servicio para la gestión de usuarios y autenticación.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con usuarios, incluyendo autenticación, registro, validaciones y manejo de excepciones.

    Attributes
    ----------
    repository : UsuarioRepository
        Repositorio para acceso a datos de usuarios.
    rol_repository : RolRepository
        Repositorio para validar roles.
    """
```

**Para métodos:**
```python
# usuario_repository.py:68-82
async def get_by_email(self, email: str) -> Optional[UsuarioModel]:
    """
    Obtiene un usuario por su email.

    Parameters
    ----------
    email : str
        Email del usuario a buscar

    Returns
    -------
    Optional[UsuarioModel]
        El usuario si existe, None en caso contrario
    """
```

### 1.5.2 Comentarios inline

**Solo para lógica compleja:**
```python
# main.py:17-53
# ======================= SOLUCION AL ERROR DE MAPPER =======================
# Importar TODOS los modelos aqui para registrarlos en SQLAlchemy
# ANTES de que cualquier controlador sea importado.
# Esto resuelve el error: failed to locate a name DivisionCuentaModel

# Auth models
from src.models.auth.rol_model import RolModel  # noqa: F401
from src.models.auth.usuario_model import UsuarioModel  # noqa: F401

# Pedidos models - CRITICO: importar ANTES de pagos
from src.models.pedidos.pedido_model import PedidoModel  # noqa: F401

# Pagos models - DESPUES de pedidos (por la relacion bidireccional)
from src.models.pagos.division_cuenta_model import DivisionCuentaModel  # noqa: F401
# ===========================================================================
```

---

## 1.6 Pruebas (Testing)

### 1.6.1 Estándar de nomenclatura para archivos de prueba

**Formato:** `test_*.py`

**Estructura del proyecto:**
```
tests/
├── unit/
│   ├── models/
│   │   ├── test_usuario_model.py
│   │   ├── test_producto_model.py
│   ├── repositories/
│   │   ├── test_usuario_repository.py
│   ├── services/
│   │   ├── test_usuario_service.py
├── integration/
│   ├── test_auth_flow.py
│   ├── test_pedido_flow.py
```

### 1.6.2 Framework de Testing

**Framework:** pytest + pytest-asyncio

**Evidencia - requirements.txt:**
```
pytest==8.4.2
pytest-asyncio==1.2.0
pytest-cov==7.0.0
```

### 1.6.3 Cobertura de Código

**Configuración:** pytest-cov
**Nivel mínimo exigido:** No especificado en el código (recomendado: 80%)

**Comando de ejecución:**
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

---

# 2. DOCUMENTO DE DISEÑO TÉCNICO (TDD)

## 2.1 Arquitectura del Sistema

### 2.1.1 Tipo de Arquitectura

**Arquitectura:** Clean Architecture (Arquitectura en Capas)

**Evidencia:**
```
src/
├── api/                    # API Layer (Presentación)
│   ├── controllers/        # Endpoints REST
│   └── schemas/            # DTOs (Pydantic)
├── business_logic/         # Business Logic Layer
│   ├── auth/               # Servicios de autenticación
│   ├── menu/               # Servicios de menú
│   ├── pedidos/            # Servicios de pedidos
│   ├── exceptions/         # Excepciones de negocio
│   └── validators/         # Validadores
├── repositories/           # Data Access Layer
│   ├── auth/               # Repos de autenticación
│   ├── menu/               # Repos de menú
│   └── pedidos/            # Repos de pedidos
├── models/                 # Data Layer
│   ├── auth/               # Modelos de usuarios
│   ├── menu/               # Modelos de productos
│   ├── pedidos/            # Modelos de pedidos
│   └── mixins/             # Mixins reutilizables
└── core/                   # Core Layer (Infraestructura)
    ├── config.py           # Configuración
    ├── database.py         # Gestión de BD
    ├── security.py         # Autenticación JWT
    ├── dependencies.py     # Middlewares
    ├── enums/              # Enumeraciones
    └── utils/              # Utilidades
```

### 2.1.2 Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                         API LAYER                           │
│  (Controllers: FastAPI Routers, HTTP Request/Response)      │
├─────────────────────────────────────────────────────────────┤
│                   BUSINESS LOGIC LAYER                      │
│  (Services: Lógica de negocio, Validaciones, Reglas)       │
├─────────────────────────────────────────────────────────────┤
│                   DATA ACCESS LAYER                         │
│  (Repositories: Acceso a datos, Queries SQLAlchemy)         │
├─────────────────────────────────────────────────────────────┤
│                       DATA LAYER                            │
│  (Models: ORM SQLAlchemy, Estructura de BD)                 │
├─────────────────────────────────────────────────────────────┤
│                       CORE LAYER                            │
│  (Config, Database, Security, Logging, Utils)               │
└─────────────────────────────────────────────────────────────┘
                            ↓↑
                    ┌───────────────┐
                    │  MySQL/Postgres│
                    └───────────────┘
```

### 2.1.3 Componentes Principales

#### **1. API Layer (24 controladores)**

**Responsabilidad:** Exponer endpoints REST

**Tecnología:** FastAPI

**Controladores principales:**
- `auth_controller.py` - Autenticación (login, register, refresh)
- `producto_controller.py` - CRUD de productos
- `pedido_controller.py` - Gestión de pedidos
- `mesa_controller.py` - Gestión de mesas
- `sync_controller.py` - Sincronización con Domotica
- Y 19 controladores más...

#### **2. Business Logic Layer (25+ servicios)**

**Responsabilidad:** Implementar lógica de negocio

**Subdominios:**
- **Auth:** `UsuarioService`, `RolService`, `SesionService`
- **Menu:** `ProductoService`, `CategoriaService`, `AlergenoService`
- **Pedidos:** `PedidoService`, `PedidoProductoService`, `PedidoOpcionService`
- **Mesas:** `MesaService`, `LocalService`, `ZonaService`
- **Pagos:** `DivisionCuentaService`

#### **3. Data Access Layer (32 repositorios)**

**Responsabilidad:** Acceso y persistencia de datos

**Patrón:** Repository Pattern

**Repositorios principales:**
- `UsuarioRepository` - CRUD de usuarios
- `ProductoRepository` - CRUD de productos
- `PedidoRepository` - CRUD de pedidos
- `MesaRepository` - CRUD de mesas

#### **4. Data Layer (22 modelos)**

**Responsabilidad:** Definir estructura de BD

**ORM:** SQLAlchemy 2.0 (Async)

**Modelos principales:**
- `UsuarioModel` - Tabla usuarios
- `ProductoModel` - Tabla productos
- `PedidoModel` - Tabla pedidos
- `MesaModel` - Tabla mesas

#### **5. Core Layer (Infraestructura)**

**Componentes:**
- `config.py` - Configuración centralizada (Pydantic Settings)
- `database.py` - Gestión de conexiones (Singleton)
- `security.py` - Autenticación JWT, hashing
- `logging.py` - Logging estructurado
- `dependencies.py` - Middlewares FastAPI

---

## 2.2 Flujo de Datos

### 2.2.1 Flujo Completo de una Petición

```
1. HTTP Request
   ↓
2. CONTROLLER (API Layer)
   - Recibe petición HTTP
   - Valida datos con Pydantic Schema
   - Extrae dependencias (DB Session)
   ↓
3. SERVICE (Business Logic Layer)
   - Aplica reglas de negocio
   - Ejecuta validaciones
   - Coordina repositorios
   ↓
4. REPOSITORY (Data Access Layer)
   - Construye queries SQLAlchemy
   - Ejecuta operaciones en BD
   - Retorna Models
   ↓
5. MODEL (Data Layer)
   - Representa entidad de BD
   - ORM SQLAlchemy
   ↓
6. REPOSITORY
   - Retorna Model al Service
   ↓
7. SERVICE
   - Transforma Model a Schema
   - Aplica lógica adicional
   - Retorna Schema
   ↓
8. CONTROLLER
   - Serializa Schema a JSON
   - Retorna HTTP Response
```

### 2.2.2 Ejemplo Concreto: Login de Usuario

**1. Controller** (`auth_controller.py:145-166`):
```python
@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_database_session),
) -> LoginResponse:
    try:
        usuario_service = UsuarioService(session)
        result = await usuario_service.login(login_data)
        await session.commit()
        return result
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))
```

**2. Service** (`usuario_service.py:40-80`):
```python
async def login(self, login_data: LoginRequest) -> LoginResponse:
    usuario = await self.repository.get_by_email(login_data.email)

    if not usuario:
        raise InvalidCredentialsError("Email o contraseña incorrectos")

    if not security.verify_password(login_data.password, usuario.password_hash):
        raise InvalidCredentialsError("Email o contraseña incorrectos")

    access_token = security.create_access_token(token_data)
    refresh_token = security.create_refresh_token(token_data)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        usuario=usuario_response
    )
```

**3. Repository** (`usuario_repository.py:68-82`):
```python
async def get_by_email(self, email: str) -> Optional[UsuarioModel]:
    query = (
        select(UsuarioModel)
        .where(UsuarioModel.email == email)
        .options(selectinload(UsuarioModel.rol))
    )
    result = await self.session.execute(query)
    return result.scalars().first()
```

**4. Model** (`usuario_model.py:15-52`):
```python
class UsuarioModel(BaseModel, AuditMixin):
    __tablename__ = "usuarios"

    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    id_rol: Mapped[str] = mapped_column(ForeignKey("roles.id"))

    rol: Mapped["RolModel"] = relationship("RolModel", lazy="selectin")
```

---

## 2.3 Integraciones

### 2.3.1 Servicios Externos Consumidos

#### **1. Sistema Domotica (Legacy)**

**Descripción:** Sistema de scraping de datos del sistema legacy

**Endpoint de integración:** `POST /api/v1/sync/platos`

**Evidencia:**
```python
# sync_controller.py:27-229
@router.post("/platos")
async def sincronizar_platos_domotica(
    productos_domotica: List[ProductoDomotica],
    session: AsyncSession = Depends(get_database_session),
):
    """
    Endpoint para recibir datos scraped del sistema Domotica.

    Sincroniza categorías y productos desde el sistema legacy.
    """
```

**Datos sincronizados:**
- Categorías de productos
- Productos con precios
- Mesas y zonas
- Imágenes

#### **2. Base de Datos MySQL/PostgreSQL**

**Tipo:** Relacional

**ORM:** SQLAlchemy 2.0 (Async)

**Driver:** aiomysql / asyncpg

**Evidencia - requirements.txt:**
```
aiomysql==0.2.0
SQLAlchemy==2.0.43
```

**Configuración:**
```python
# config.py:60-65
database_url: str = Field(
    default="mysql+aiomysql://user:password@localhost:3306/restaurant_db",
    validation_alias="DATABASE_URL"
)
```

---

## 2.4 Seguridad

### 2.4.1 Autenticación

**Mecanismo:** JWT (JSON Web Tokens)

**Tipos de tokens:**
1. **Access Token:** Expiración corta (30 minutos por defecto)
2. **Refresh Token:** Expiración larga (7 días por defecto)

**Evidencia:**
```python
# config.py:75-81
secret_key: str = Field(validation_alias="SECRET_KEY")
algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")
access_token_expire_minutes: int = Field(
    default=30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
)
refresh_token_expire_days: int = Field(
    default=7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS"
)
```

**Implementación:**
```python
# security.py:56-95
def create_access_token(self, data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=self.settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode,
        self.settings.secret_key,
        algorithm=self.settings.algorithm
    )
    return encoded_jwt

def create_refresh_token(self, data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=self.settings.refresh_token_expire_days
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        self.settings.secret_key,
        algorithm=self.settings.algorithm,
    )
    return encoded_jwt
```

### 2.4.2 Hashing de Contraseñas

**Algoritmo:** Bcrypt

**Evidencia:**
```python
# security.py:13-37
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityConfig:
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
```

### 2.4.3 CORS (Cross-Origin Resource Sharing)

**Configuración:**
```python
# main.py:248-255
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# config.py:83-93
allowed_origins: List[str] = Field(
    default=["http://localhost:3000", "http://localhost:8080"],
    validation_alias="ALLOWED_ORIGINS"
)
allowed_methods: List[str] = Field(
    default=["GET", "POST", "PUT", "DELETE", "PATCH"],
    validation_alias="ALLOWED_METHODS"
)
allowed_headers: List[str] = Field(
    default=["*"],
    validation_alias="ALLOWED_HEADERS"
)
```

---

# 3. DOCUMENTACIÓN DE API REST

## 3.1 Información General

- **Framework:** FastAPI 0.118.0
- **Prefijo Global:** `/api/v1`
- **Base URL (Dev):** `http://localhost:8000`
- **Base URL (Prod):** Configurable via `HOST` y `PORT`
- **Documentación Interactiva:**
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`

**Evidencia:**
```python
# main.py:237-246
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)
```

---

## 3.2 Autenticación

### 3.2.1 Obtener Access Token

**Endpoint:** `POST /api/v1/auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "status": 200,
  "code": "SUCCESS",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "id": "01JCABCDEFGHIJKLMNOPQRSTUV",
    "email": "user@example.com",
    "nombre": "Juan Pérez",
    "telefono": "987654321",
    "id_rol": "01JCDEFGHIJKLMNOPQRSTUVWXY",
    "activo": true,
    "ultimo_acceso": "2025-11-05T10:30:00",
    "fecha_creacion": "2025-01-01T00:00:00",
    "fecha_modificacion": "2025-11-05T10:30:00"
  }
}
```

**Errores:**
- `401 Unauthorized` - Credenciales inválidas o usuario inactivo
- `500 Internal Server Error` - Error del servidor

**Evidencia:** `auth_controller.py:145-211`

### 3.2.2 Renovar Access Token

**Endpoint:** `POST /api/v1/auth/refresh`

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "status": 200,
  "code": "SUCCESS",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores:**
- `401 Unauthorized` - Refresh token inválido o expirado

**Evidencia:** `auth_controller.py:284-345`

### 3.2.3 Usar el Token

**Header requerido para endpoints protegidos:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 3.3 Endpoints Principales

### 3.3.1 Autenticación y Usuarios

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/auth/login` | Iniciar sesión | auth_controller.py:145 |
| POST | `/api/v1/auth/register` | Registrar nuevo usuario | auth_controller.py:214 |
| POST | `/api/v1/auth/refresh` | Renovar access token | auth_controller.py:284 |
| GET | `/api/v1/auth/me` | Obtener usuario actual | auth_controller.py:348 |

### 3.3.2 Roles

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/roles` | Crear rol | rol_controller.py:25 |
| GET | `/api/v1/roles/{rol_id}` | Obtener rol por ID | rol_controller.py:62 |
| GET | `/api/v1/roles` | Listar roles (paginado) | rol_controller.py:99 |
| PUT | `/api/v1/roles/{rol_id}` | Actualizar rol | rol_controller.py:141 |
| DELETE | `/api/v1/roles/{rol_id}` | Eliminar rol | rol_controller.py:184 |

### 3.3.3 Locales

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/locales` | Crear local | local_controller.py:25 |
| GET | `/api/v1/locales/{local_id}` | Obtener local por ID | local_controller.py:62 |
| GET | `/api/v1/locales/codigo/{codigo}` | Obtener local por código | local_controller.py:99 |
| GET | `/api/v1/locales` | Listar locales | local_controller.py:136 |
| PUT | `/api/v1/locales/{local_id}` | Actualizar local | local_controller.py:178 |
| DELETE | `/api/v1/locales/{local_id}` | Eliminar local | local_controller.py:221 |

### 3.3.4 Zonas

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/zonas` | Crear zona | zona_controller.py:25 |
| GET | `/api/v1/zonas/{zona_id}` | Obtener zona por ID | zona_controller.py:65 |
| GET | `/api/v1/zonas/local/{local_id}` | Listar zonas por local | zona_controller.py:102 |
| GET | `/api/v1/zonas/nivel/{nivel}` | Listar zonas por nivel | zona_controller.py:146 |
| GET | `/api/v1/zonas` | Listar todas las zonas | zona_controller.py:190 |
| PUT | `/api/v1/zonas/{zona_id}` | Actualizar zona | zona_controller.py:232 |
| DELETE | `/api/v1/zonas/{zona_id}` | Eliminar zona | zona_controller.py:278 |

### 3.3.5 Mesas

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/mesas` | Crear mesa | mesa_controller.py:96 |
| POST | `/api/v1/mesas/batch` | Crear múltiples mesas | mesa_controller.py:23 |
| DELETE | `/api/v1/mesas/batch` | Eliminar múltiples mesas | mesa_controller.py:48 |
| GET | `/api/v1/mesas/{mesa_id}` | Obtener mesa por ID (detalle) | mesa_controller.py:133 |
| GET | `/api/v1/mesas` | Listar mesas | mesa_controller.py:170 |
| GET | `/api/v1/mesas/{mesa_id}/local` | Obtener local de una mesa | mesa_controller.py:290 |
| GET | `/api/v1/mesas/qr/urls` | Listar URLs de QR | mesa_controller.py:332 |
| PUT | `/api/v1/mesas/{mesa_id}` | Actualizar mesa | mesa_controller.py:212 |
| DELETE | `/api/v1/mesas/{mesa_id}` | Eliminar mesa | mesa_controller.py:255 |

### 3.3.6 Categorías

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/categorias` | Crear categoría | categoria_controller.py:26 |
| GET | `/api/v1/categorias` | Listar categorías (filtros multi-local) | categoria_controller.py:63 |
| GET | `/api/v1/categorias/{categoria_id}` | Obtener categoría por ID | categoria_controller.py:119 |
| PUT | `/api/v1/categorias/{categoria_id}` | Actualizar categoría | categoria_controller.py:156 |
| DELETE | `/api/v1/categorias/{categoria_id}` | Eliminar categoría | categoria_controller.py:199 |

### 3.3.7 Productos

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/productos` | Crear producto | producto_controller.py:29 |
| GET | `/api/v1/productos` | Listar productos (filtros multi-local) | producto_controller.py:310 |
| GET | `/api/v1/productos/cards` | Listar productos (formato card) | producto_controller.py:108 |
| GET | `/api/v1/productos/categoria/{cat_id}/cards` | Productos por categoría (cards) | producto_controller.py:154 |
| GET | `/api/v1/productos/{producto_id}` | Obtener producto por ID | producto_controller.py:202 |
| GET | `/api/v1/productos/{producto_id}/opciones` | Producto con opciones agrupadas | producto_controller.py:239 |
| GET | `/api/v1/productos/{producto_id}/alergenos` | Alérgenos de un producto | producto_controller.py:276 |
| GET | `/api/v1/productos/con-alergenos` | Productos con alérgenos | producto_controller.py:65 |
| PUT | `/api/v1/productos/{producto_id}` | Actualizar producto | producto_controller.py:366 |
| DELETE | `/api/v1/productos/{producto_id}` | Eliminar producto | producto_controller.py:409 |

### 3.3.8 Pedidos

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/pedidos` | Crear pedido | pedido_controller.py:32 |
| POST | `/api/v1/pedidos/completo` | Crear pedido completo con items | pedido_controller.py:72 |
| GET | `/api/v1/pedidos/{pedido_id}` | Obtener pedido por ID | pedido_controller.py:136 |
| GET | `/api/v1/pedidos/numero/{numero}` | Obtener pedido por número | pedido_controller.py:173 |
| GET | `/api/v1/pedidos` | Listar pedidos (filtros) | pedido_controller.py:210 |
| GET | `/api/v1/pedidos/detallado` | Listar pedidos detallados | pedido_controller.py:260 |
| PUT | `/api/v1/pedidos/{pedido_id}` | Actualizar pedido | pedido_controller.py:315 |
| PATCH | `/api/v1/pedidos/{pedido_id}/estado` | Cambiar estado de pedido | pedido_controller.py:358 |
| DELETE | `/api/v1/pedidos/{pedido_id}` | Eliminar pedido | pedido_controller.py:401 |

### 3.3.9 Sincronización (Integración Domotica)

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/sync/platos` | Sincronizar platos desde Domotica | sync_controller.py:27 |
| POST | `/api/v1/sync/mesas` | Sincronizar mesas desde Domotica | sync_controller.py:232 |
| POST | `/api/v1/sync/enrich` | Enriquecer datos existentes | sync_controller.py:392 |

### 3.3.10 Catálogo Multi-Local

#### Locales - Categorías

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/locales/{id_local}/categorias` | Crear relación local-categoría | locales_categorias_controller.py:32 |
| GET | `/api/v1/locales/{id_local}/categorias` | Listar categorías del local | locales_categorias_controller.py:84 |
| POST | `/api/v1/locales/{id_local}/categorias/activar` | Activar categoría | locales_categorias_controller.py:249 |
| POST | `/api/v1/locales/{id_local}/categorias/desactivar` | Desactivar categoría | locales_categorias_controller.py:291 |
| POST | `/api/v1/locales/{id_local}/categorias/activar-lote` | Activar múltiples categorías | locales_categorias_controller.py:331 |

#### Locales - Productos

| Método | Endpoint | Descripción | Archivo |
|--------|----------|-------------|---------|
| POST | `/api/v1/locales/{id_local}/productos` | Crear relación con overrides | locales_productos_controller.py:31 |
| GET | `/api/v1/locales/{id_local}/productos` | Listar productos del local | locales_productos_controller.py:83 |
| POST | `/api/v1/locales/{id_local}/productos/activar` | Activar producto con overrides | locales_productos_controller.py:248 |
| POST | `/api/v1/locales/{id_local}/productos/desactivar` | Desactivar producto | locales_productos_controller.py:290 |
| PATCH | `/api/v1/locales/{id_local}/productos/overrides` | Actualizar overrides | locales_productos_controller.py:330 |
| POST | `/api/v1/locales/{id_local}/productos/activar-lote` | Activar múltiples productos | locales_productos_controller.py:370 |

---

## 3.4 Schemas (DTOs) de Request/Response

### 3.4.1 Autenticación

**LoginRequest:**
```python
{
  "email": "EmailStr (requerido)",
  "password": "str (requerido, min 1)"
}
```

**LoginResponse:**
```python
{
  "status": "int (200)",
  "code": "str (SUCCESS)",
  "access_token": "str",
  "refresh_token": "str",
  "token_type": "str (bearer)",
  "usuario": "UsuarioResponse"
}
```

**RegisterRequest:**
```python
{
  "email": "EmailStr (requerido, max 255)",
  "password": "str (requerido, min 6, max 100)",
  "nombre": "str (opcional, max 255)",
  "telefono": "str (opcional, max 20)",
  "id_rol": "str (requerido)"
}
```

**Evidencia:** `usuario_schema.py:10-120`

### 3.4.2 Productos

**ProductoCreate:**
```python
{
  "nombre": "str (requerido, max 255)",
  "descripcion": "str (opcional)",
  "precio_base": "float (requerido, >= 0)",
  "id_categoria": "str (requerido)",
  "imagen_path": "str (opcional)",
  "disponible": "bool (default: true)",
  "destacado": "bool (default: false)"
}
```

**ProductoResponse:**
```python
{
  "id": "str",
  "nombre": "str",
  "descripcion": "str",
  "precio_base": "float",
  "id_categoria": "str",
  "imagen_path": "str",
  "disponible": "bool",
  "destacado": "bool",
  "fecha_creacion": "datetime",
  "fecha_modificacion": "datetime"
}
```

**Evidencia:** `producto_schema.py:10-150`

### 3.4.3 Pedidos

**PedidoCompletoCreate:**
```python
{
  "id_mesa": "str (requerido)",
  "items": [
    {
      "id_producto": "str (requerido)",
      "cantidad": "int (requerido, >= 1)",
      "precio_unitario": "float (requerido, > 0)",
      "precio_opciones": "float (default: 0.00)",
      "notas_personalizacion": "str (opcional)"
    }
  ],
  "notas_cliente": "str (opcional)",
  "notas_cocina": "str (opcional)"
}
```

**PedidoResponse:**
```python
{
  "id": "str",
  "numero_pedido": "str",
  "id_mesa": "str",
  "id_usuario": "str",
  "estado": "EstadoPedido",
  "subtotal": "float",
  "impuestos": "float",
  "descuentos": "float",
  "total": "float",
  "notas_cliente": "str",
  "notas_cocina": "str",
  "fecha_confirmado": "datetime",
  "fecha_en_preparacion": "datetime",
  "fecha_listo": "datetime",
  "fecha_entregado": "datetime",
  "fecha_cancelado": "datetime"
}
```

**Evidencia:** `pedido_schema.py:10-200`

---

## 3.5 Códigos de Estado HTTP

### 3.5.1 Respuestas Exitosas

| Código | Significado | Uso |
|--------|-------------|-----|
| 200 OK | Operación exitosa | GET, PUT, PATCH |
| 201 Created | Recurso creado | POST |
| 204 No Content | Eliminación exitosa | DELETE |

### 3.5.2 Errores del Cliente

| Código | Significado | Uso |
|--------|-------------|-----|
| 400 Bad Request | Datos inválidos o validación fallida | ValidationError |
| 401 Unauthorized | No autenticado o token inválido | UnauthorizedError |
| 403 Forbidden | Sin permisos | ForbiddenError |
| 404 Not Found | Recurso no encontrado | NotFoundError |
| 409 Conflict | Conflicto de integridad (duplicados) | ConflictError |

### 3.5.3 Errores del Servidor

| Código | Significado | Uso |
|--------|-------------|-----|
| 500 Internal Server Error | Error inesperado del servidor | Exception genérica |

**Evidencia:**
```python
# dependencies.py:36-91
async def _handle_business_error(self, error, request: Request) -> JSONResponse:
    status_code_map = {
        ValidationError: 400,
        NotFoundError: 404,
        ConflictError: 409,
        UnauthorizedError: 401,
        ForbiddenError: 403,
        BusinessError: 400,
    }
```

---

## 3.6 Paginación

**Parámetros Query estándar:**
- `skip`: Offset de registros (default: 0)
- `limit`: Cantidad máxima de registros (default: 100, max: 500)

**Formato de respuesta paginada:**
```json
{
  "items": [...],
  "total": 250
}
```

**Ejemplo:**
```
GET /api/v1/productos?skip=0&limit=20
```

**Evidencia:** `pagination_utils.py` y todos los endpoints GET de listado

---

## 3.7 Filtros Multi-Local

**Parámetros de filtro:**
- `id_mesa`: Filtra por el local de la mesa (resuelve local automáticamente)
- `id_local`: Filtra directamente por local

**Endpoints con soporte:**
- `GET /api/v1/categorias`
- `GET /api/v1/productos`
- `GET /api/v1/tipos-opciones`
- `GET /api/v1/producto-opciones`

**Overrides aplicados:**
- **Productos:** precio, nombre, descripción, disponibilidad
- **Opciones:** precio_adicional

**Ejemplo:**
```
GET /api/v1/productos?id_mesa=01JCABCD...
```

**Evidencia:** `producto_controller.py:310-363`, `categoria_controller.py:63-116`

---

# 4. MODELOS DE DATOS Y ESQUEMAS DE BD

## 4.1 Configuración de Base de Datos

### 4.1.1 ORM Utilizado

**ORM:** SQLAlchemy 2.0 (Async)

**Características:**
- Motor asíncrono: `create_async_engine`
- Sesiones asíncronas: `AsyncSession`
- Base declarativa: `DeclarativeBase`
- IDs tipo ULID (26 caracteres, ordenados cronológicamente)

**Evidencia:**
```python
# database.py:18-75
class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None

    def __init__(self):
        self.settings = get_settings()
        self.engine = create_async_engine(
            self.settings.database_url,
            echo=self.settings.debug,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
        self._session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
```

### 4.1.2 Drivers de Base de Datos

**MySQL:**
```
aiomysql==0.2.0
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/restaurant_db
```

**PostgreSQL:**
```
asyncpg (alternativa)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/restaurant_db
```

**SQLite (Desarrollo):**
```
aiosqlite==0.21.0
DATABASE_URL=sqlite+aiosqlite:///./restaurant.db
```

---

## 4.2 Modelo Base

### 4.2.1 BaseModel

**Ubicación:** `models/base_model.py:17-64`

**Campos:**
```python
class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=lambda: ulid.new().str
    )
```

**Métodos:**
- `to_dict()`: Convierte modelo a diccionario
- `from_dict(data)`: Crea instancia desde diccionario
- `update_from_dict(data)`: Actualiza instancia desde diccionario

---

## 4.3 Mixins

### 4.3.1 AuditMixin

**Ubicación:** `models/mixins/audit_mixin.py:15-47`

**Campos proporcionados:**
```python
@declarative_mixin
class AuditMixin:
    fecha_creacion: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    fecha_modificacion: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    creado_por: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    modificado_por: Mapped[Optional[str]] = mapped_column(String(255), default=None)
```

**Uso:**
```python
class UsuarioModel(BaseModel, AuditMixin):
    # Hereda fecha_creacion, fecha_modificacion, creado_por, modificado_por
```

### 4.3.2 SoftDeleteMixin

**Ubicación:** `models/mixins/soft_delete_mixin.py:12-31`

**Campos proporcionados:**
```python
@declarative_mixin
class SoftDeleteMixin:
    deleted_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
```

**Nota:** Actualmente NO está siendo usado en ningún modelo del proyecto.

---

## 4.4 Modelos Principales

### 4.4.1 Módulo AUTH (Autenticación)

#### **RolModel**

**Tabla:** `roles`
**Archivo:** `models/auth/rol_model.py:15-45`

**Campos:**
| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| id | String(26) | PK | ULID |
| nombre | String(50) | NOT NULL, UNIQUE | Nombre del rol |
| descripcion | String(255) | NULLABLE | Descripción |
| activo | Boolean | NOT NULL, default=True | Estado |
| fecha_creacion | TIMESTAMP | NOT NULL, auto | Auditoría |
| fecha_modificacion | TIMESTAMP | NOT NULL, auto | Auditoría |
| creado_por | String(255) | NULLABLE | Auditoría |
| modificado_por | String(255) | NULLABLE | Auditoría |

**Código:**
```python
class RolModel(BaseModel, AuditMixin):
    __tablename__ = "roles"

    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
```

---

#### **UsuarioModel**

**Tabla:** `usuarios`
**Archivo:** `models/auth/usuario_model.py:15-65`

**Campos:**
| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| id | String(26) | PK | ULID |
| email | String(255) | NULLABLE, UNIQUE, INDEXED | Email único |
| password_hash | String(255) | NULLABLE | Hash Bcrypt |
| nombre | String(255) | NULLABLE | Nombre completo |
| telefono | String(20) | NULLABLE | Teléfono |
| activo | Boolean | NULLABLE, default=True, INDEXED | Estado |
| id_rol | String(36) | FK→roles.id, NOT NULL, INDEXED | Rol |
| ultimo_acceso | TIMESTAMP | NULLABLE | Último acceso |
| fecha_creacion | TIMESTAMP | NOT NULL, auto | Auditoría |
| fecha_modificacion | TIMESTAMP | NOT NULL, auto | Auditoría |

**Índices:**
- `idx_email` en email
- `idx_rol` en id_rol
- `idx_activo` en activo

**Relaciones:**
- `rol`: ManyToOne → RolModel (lazy="selectin", ondelete="RESTRICT")

**Código:**
```python
class UsuarioModel(BaseModel, AuditMixin):
    __tablename__ = "usuarios"

    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
    id_rol: Mapped[str] = mapped_column(ForeignKey("roles.id"), nullable=False, index=True)
    ultimo_acceso: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)

    # Relaciones
    rol: Mapped["RolModel"] = relationship("RolModel", lazy="selectin")
```

---

### 4.4.2 Módulo MENU (Catálogo)

#### **CategoriaModel**

**Tabla:** `categorias`
**Archivo:** `models/menu/categoria_model.py:15-50`

**Campos:**
| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| id | String(26) | PK | ULID |
| nombre | String(100) | NOT NULL, UNIQUE, INDEXED | Nombre |
| descripcion | Text | NULLABLE | Descripción |
| imagen_path | String(255) | NULLABLE | Ruta imagen |
| activo | Boolean | NOT NULL, default=True, INDEXED | Estado |
| fecha_creacion | TIMESTAMP | NOT NULL, auto | Auditoría |
| fecha_modificacion | TIMESTAMP | NOT NULL, auto | Auditoría |

**Relaciones:**
- `productos`: OneToMany → ProductoModel (cascade="all, delete-orphan")

**Código:**
```python
class CategoriaModel(BaseModel, AuditMixin):
    __tablename__ = "categorias"

    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    imagen_path: Mapped[Optional[str]] = mapped_column(String(255))
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    # Relaciones
    productos: Mapped[List["ProductoModel"]] = relationship(
        "ProductoModel",
        back_populates="categoria",
        cascade="all, delete-orphan"
    )
```

---

#### **ProductoModel**

**Tabla:** `productos`
**Archivo:** `models/menu/producto_model.py:20-75`

**Campos:**
| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| id | String(26) | PK | ULID |
| id_categoria | String(26) | FK→categorias.id, NOT NULL, INDEXED | Categoría |
| nombre | String(255) | NOT NULL, INDEXED | Nombre |
| descripcion | Text | NULLABLE | Descripción |
| precio_base | DECIMAL(10,2) | NOT NULL, INDEXED | Precio |
| imagen_path | String(255) | NULLABLE | Ruta imagen |
| imagen_alt_text | String(255) | NULLABLE | Texto alt |
| disponible | Boolean | NOT NULL, default=True, INDEXED | Disponibilidad |
| destacado | Boolean | NOT NULL, default=False, INDEXED | Destacado |
| fecha_creacion | TIMESTAMP | NOT NULL, auto | Auditoría |
| fecha_modificacion | TIMESTAMP | NOT NULL, auto | Auditoría |

**Índices:**
- `idx_busqueda` FULLTEXT en (nombre, descripcion) - MySQL

**Relaciones:**
- `categoria`: ManyToOne → CategoriaModel (lazy="selectin", ondelete="RESTRICT")
- `opciones`: OneToMany → ProductoOpcionModel (cascade="all, delete-orphan")

**Código:**
```python
class ProductoModel(BaseModel, AuditMixin):
    __tablename__ = "productos"

    id_categoria: Mapped[str] = mapped_column(
        ForeignKey("categorias.id"), nullable=False, index=True
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    precio_base: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, index=True)
    imagen_path: Mapped[Optional[str]] = mapped_column(String(255))
    disponible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    destacado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    # Relaciones
    categoria: Mapped["CategoriaModel"] = relationship("CategoriaModel", lazy="selectin")
    opciones: Mapped[List["ProductoOpcionModel"]] = relationship(
        "ProductoOpcionModel",
        back_populates="producto",
        cascade="all, delete-orphan"
    )
```

---

### 4.4.3 Módulo MESAS (Locales, Zonas, Mesas)

#### **LocalModel**

**Tabla:** `locales`
**Archivo:** `models/mesas/local_model.py:23-80`

**Campos:**
| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| id | String(26) | PK | ULID |
| codigo | String(20) | NOT NULL, UNIQUE | Código único |
| nombre | String(100) | NOT NULL | Nombre |
| direccion | String(255) | NOT NULL | Dirección |
| distrito | String(100) | NULLABLE | Distrito |
| ciudad | String(100) | NULLABLE | Ciudad |
| telefono | String(20) | NULLABLE | Teléfono |
| email | String(100) | NULLABLE | Email |
| tipo_local | Enum(TipoLocal) | NOT NULL | CENTRAL/SUCURSAL |
| capacidad_total | Integer | NULLABLE | Capacidad |
| activo | Boolean | NOT NULL, default=True | Estado |
| fecha_apertura | Date | NULLABLE | Fecha apertura |

**Índices:**
- `idx_local_activo` en activo
- `idx_local_tipo` en tipo_local
- `idx_local_codigo` en codigo

**Relaciones:**
- `zonas`: OneToMany → ZonaModel (cascade="all, delete-orphan")
- `sesiones`: OneToMany → SesionModel (cascade="all, delete-orphan")

**Código:**
```python
class LocalModel(BaseModel, AuditMixin):
    __tablename__ = "locales"

    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo_local: Mapped[TipoLocal] = mapped_column(Enum(TipoLocal), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    # Relaciones
    zonas: Mapped[List["ZonaModel"]] = relationship(
        "ZonaModel",
        back_populates="local",
        cascade="all, delete-orphan"
    )
```

---

#### **MesaModel**

**Tabla:** `mesas`
**Archivo:** `models/mesas/mesa_model.py:18-65`

**Campos:**
| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| id | String(26) | PK | ULID |
| numero | String(50) | NOT NULL, UNIQUE | Número mesa |
| capacidad | Integer | NULLABLE | Capacidad |
| id_zona | String(36) | FK→zonas.id, NULLABLE, INDEXED | Zona |
| nota | String(255) | NULLABLE | Notas |
| activo | Boolean | NOT NULL, default=True | Estado |
| estado | Enum(EstadoMesa) | NOT NULL, default=DISPONIBLE | Estado mesa |

**Relaciones:**
- `zona`: ManyToOne → ZonaModel (lazy="selectin", ondelete="SET NULL")

**Enums:**
```python
class EstadoMesa(str, Enum):
    LIBRE = "libre"
    DISPONIBLE = "disponible"
    OCUPADA = "ocupada"
    RESERVADA = "reservada"
    MANTENIMIENTO = "mantenimiento"
    FUERA_SERVICIO = "fuera_servicio"
```

**Código:**
```python
class MesaModel(BaseModel, AuditMixin):
    __tablename__ = "mesas"

    numero: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    capacidad: Mapped[Optional[int]] = mapped_column(Integer)
    id_zona: Mapped[Optional[str]] = mapped_column(
        ForeignKey("zonas.id"), nullable=True, index=True
    )
    estado: Mapped[EstadoMesa] = mapped_column(
        Enum(EstadoMesa), default=EstadoMesa.DISPONIBLE, nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relaciones
    zona: Mapped[Optional["ZonaModel"]] = relationship(
        "ZonaModel", lazy="selectin"
    )
```

---

### 4.4.4 Módulo PEDIDOS

#### **PedidoModel**

**Tabla:** `pedidos`
**Archivo:** `models/pedidos/pedido_model.py:22-95`

**Campos:**
| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| id | String(26) | PK | ULID |
| id_mesa | String(36) | FK→mesas.id, NOT NULL | Mesa |
| id_usuario | String(36) | FK→usuarios.id, NOT NULL | Usuario |
| numero_pedido | String(50) | NOT NULL, UNIQUE, INDEXED | Número único |
| estado | Enum(EstadoPedido) | NOT NULL, default=PENDIENTE | Estado |
| subtotal | Numeric(10,2) | NOT NULL, default=0.00 | Subtotal |
| impuestos | Numeric(10,2) | NULLABLE, default=0.00 | Impuestos |
| descuentos | Numeric(10,2) | NULLABLE, default=0.00 | Descuentos |
| total | Numeric(10,2) | NOT NULL, default=0.00 | Total |
| notas_cliente | Text | NULLABLE | Notas cliente |
| notas_cocina | Text | NULLABLE | Notas cocina |
| fecha_confirmado | TIMESTAMP | NULLABLE | Timestamp confirmado |
| fecha_en_preparacion | TIMESTAMP | NULLABLE | Timestamp preparación |
| fecha_listo | TIMESTAMP | NULLABLE | Timestamp listo |
| fecha_entregado | TIMESTAMP | NULLABLE | Timestamp entregado |
| fecha_cancelado | TIMESTAMP | NULLABLE | Timestamp cancelado |

**Constraints:**
- CheckConstraint: `subtotal >= 0`
- CheckConstraint: `total >= 0`

**Relaciones:**
- `pedidos_productos`: OneToMany → PedidoProductoModel (cascade="all, delete-orphan")
- `divisiones_cuenta`: OneToMany → DivisionCuentaModel (cascade="all, delete-orphan")

**Enums:**
```python
class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"
```

**Código:**
```python
class PedidoModel(BaseModel, AuditMixin):
    __tablename__ = "pedidos"

    id_mesa: Mapped[str] = mapped_column(ForeignKey("mesas.id"), nullable=False)
    id_usuario: Mapped[str] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    numero_pedido: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    estado: Mapped[EstadoPedido] = mapped_column(
        Enum(EstadoPedido), default=EstadoPedido.PENDIENTE, nullable=False
    )
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)

    # Relaciones
    pedidos_productos: Mapped[List["PedidoProductoModel"]] = relationship(
        "PedidoProductoModel",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )
```

---

## 4.5 Diagrama ER Simplificado

```
┌─────────────┐
│   Roles     │
└──────┬──────┘
       │ 1
       │
       │ N
┌──────▼──────┐        ┌──────────────┐
│  Usuarios   │───────>│   Sesiones   │
└──────┬──────┘        └──────────────┘
       │
       │
       │
┌──────▼──────┐        ┌──────────────┐
│   Pedidos   │───────>│   Mesas      │
└──────┬──────┘        └──────┬───────┘
       │                      │
       │                      │
       │ 1                    │ N
       │                      │
       │ N              ┌─────▼─────┐
       │                │   Zonas   │
┌──────▼───────────┐    └─────┬─────┘
│PedidosProductos  │          │
└──────┬───────────┘          │ N
       │                      │
       │ N              ┌─────▼─────┐
       │                │  Locales  │
┌──────▼───────┐        └───────────┘
│  Productos   │
└──────┬───────┘
       │
       │ N
       │
┌──────▼───────┐
│ Categorías   │
└──────────────┘
```

---

## 4.6 Resumen Estadístico

- **Total de modelos:** 22
- **Total de tablas:** 22
- **Total de enums:** 13
- **Modelos con AuditMixin:** 19
- **Modelos con SoftDeleteMixin:** 0 (mixin existe pero no se usa)
- **Tablas de relación M:N:** 5 (locales_categorias, locales_productos, etc.)
- **Foreign Keys totales:** ~35
- **Índices definidos:** ~45

---

# 5. ANEXOS

## 5.1 Stack Tecnológico Completo

**Backend Framework:**
- FastAPI 0.118.0

**ORM:**
- SQLAlchemy 2.0.43 (Async)

**Base de Datos:**
- MySQL (aiomysql 0.2.0)
- PostgreSQL (alternativa con asyncpg)
- SQLite (desarrollo con aiosqlite 0.21.0)

**Autenticación:**
- python-jose 3.5.0 (JWT)
- passlib 1.7.4 + bcrypt 4.2.1 (hashing)

**Validación:**
- Pydantic 2.11.10
- Pydantic Settings 2.11.0
- email-validator 2.3.0

**Testing:**
- pytest 8.4.2
- pytest-asyncio 1.2.0
- pytest-cov 7.0.0

**Logging:**
- structlog 25.4.0

**Servidor:**
- Uvicorn 0.37.0

**Utilidades:**
- python-ulid 2.7.0 (IDs únicos)
- Faker 37.11.0 (datos de prueba)

---

## 5.2 Variables de Entorno

**Archivo:** `.env.example`

```bash
# Application
APP_NAME=Restaurant Backend API
APP_VERSION=1.0.0
APP_DESCRIPTION=Sistema de gestión de restaurantes con arquitectura en capas
DEBUG=true
ENVIRONMENT=development

# Database Auto-Creation
INIT_DB=true

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=mysql+aiomysql://restaurant_user:restaurant_password@localhost:3306/restaurant_db
DATABASE_TEST_URL=mysql+aiomysql://restaurant_user:restaurant_password@localhost:3306/restaurant_test_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE", "PATCH"]
ALLOWED_HEADERS=["*"]

# File uploads
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads
ALLOWED_EXTENSIONS=["jpg", "jpeg", "png", "gif", "webp"]

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

---

## 5.3 Comandos Útiles

### 5.3.1 Desarrollo

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# O usando el script main.py directamente
python src/main.py
```

### 5.3.2 Testing

```bash
# Ejecutar todos los tests
python -m pytest tests/ --tb=no -q

# Ejecutar con cobertura
python -m pytest tests/ --cov=src --cov-report=html

# Ejecutar tests específicos
python -m pytest tests/unit/models/test_usuario_model.py
```

### 5.3.3 Base de Datos

```bash
# Crear tablas (si INIT_DB=false)
# Se crean automáticamente al iniciar la app si INIT_DB=true

# Ver estructura de BD
mysql -u restaurant_user -p restaurant_db
SHOW TABLES;
DESCRIBE usuarios;
```

---

## 5.4 Estructura de Directorios Completa

```
back-dp2/
├── src/
│   ├── __init__.py
│   ├── main.py                          # Punto de entrada
│   ├── api/
│   │   ├── __init__.py
│   │   ├── controllers/                 # 24 controladores
│   │   │   ├── auth_controller.py
│   │   │   ├── producto_controller.py
│   │   │   ├── pedido_controller.py
│   │   │   └── ...
│   │   └── schemas/                     # 25 schemas
│   │       ├── usuario_schema.py
│   │       ├── producto_schema.py
│   │       └── ...
│   ├── business_logic/
│   │   ├── __init__.py
│   │   ├── auth/                        # Servicios auth
│   │   │   ├── usuario_service.py
│   │   │   ├── rol_service.py
│   │   │   └── sesion_service.py
│   │   ├── menu/                        # Servicios menu
│   │   │   ├── producto_service.py
│   │   │   ├── categoria_service.py
│   │   │   └── alergeno_service.py
│   │   ├── pedidos/                     # Servicios pedidos
│   │   │   ├── pedido_service.py
│   │   │   ├── pedido_producto_service.py
│   │   │   └── pedido_opcion_service.py
│   │   ├── mesas/                       # Servicios mesas
│   │   │   ├── mesa_service.py
│   │   │   ├── local_service.py
│   │   │   └── zona_service.py
│   │   ├── pagos/                       # Servicios pagos
│   │   ├── exceptions/                  # 22 archivos excepciones
│   │   │   ├── base_exceptions.py
│   │   │   ├── usuario_exceptions.py
│   │   │   ├── producto_exceptions.py
│   │   │   └── ...
│   │   └── validators/                  # Validadores
│   │       └── producto_validators.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── auth/                        # Repos auth
│   │   │   ├── usuario_repository.py
│   │   │   ├── rol_repository.py
│   │   │   └── sesion_repository.py
│   │   ├── menu/                        # Repos menu
│   │   │   ├── producto_repository.py
│   │   │   ├── categoria_repository.py
│   │   │   └── alergeno_repository.py
│   │   ├── pedidos/                     # Repos pedidos
│   │   ├── mesas/                       # Repos mesas
│   │   └── pagos/                       # Repos pagos
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py                # Modelo base
│   │   ├── mixins/                      # Mixins
│   │   │   ├── audit_mixin.py
│   │   │   └── soft_delete_mixin.py
│   │   ├── auth/                        # Modelos auth
│   │   │   ├── usuario_model.py
│   │   │   ├── rol_model.py
│   │   │   └── sesion_model.py
│   │   ├── menu/                        # Modelos menu
│   │   │   ├── producto_model.py
│   │   │   ├── categoria_model.py
│   │   │   └── alergeno_model.py
│   │   ├── pedidos/                     # Modelos pedidos
│   │   │   ├── pedido_model.py
│   │   │   ├── pedido_producto_model.py
│   │   │   └── pedido_opcion_model.py
│   │   ├── mesas/                       # Modelos mesas
│   │   │   ├── mesa_model.py
│   │   │   ├── local_model.py
│   │   │   └── zona_model.py
│   │   └── pagos/                       # Modelos pagos
│   │       ├── division_cuenta_model.py
│   │       └── division_cuenta_detalle_model.py
│   └── core/
│       ├── __init__.py
│       ├── config.py                    # Configuración
│       ├── database.py                  # Gestión BD
│       ├── security.py                  # Autenticación JWT
│       ├── dependencies.py              # Middlewares
│       ├── logging.py                   # Logging
│       ├── enums/                       # Enumeraciones
│       │   ├── pedido_enums.py
│       │   ├── user_enums.py
│       │   ├── mesa_enums.py
│       │   ├── pago_enums.py
│       │   ├── local_enums.py
│       │   ├── sesion_enums.py
│       │   └── alergeno_enums.py
│       └── utils/                       # Utilidades
│           ├── pagination_utils.py
│           └── text_utils.py
├── tests/
│   ├── unit/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── services/
│   └── integration/
├── scripts/
│   ├── seed_cevicheria_data.py          # Script de seed
│   └── enrich_data.py                   # Enriquecimiento datos
├── .env                                  # Variables de entorno
├── .env.example                          # Ejemplo de .env
├── requirements.txt                      # Dependencias
├── requirements-windows.txt              # Dependencias Windows
├── pytest.ini                            # Configuración pytest
├── README.md                             # Documentación básica
└── DOCUMENTACION_COMPLETA.md            # Este documento
```

---

## 5.5 Contacto y Soporte

**Documentación Interactiva:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Health Check:**
- `GET http://localhost:8000/health`

**Repositorio:**
- (Agregar URL del repositorio Git)

---

**Fin de la Documentación Completa**

**Última Actualización:** Noviembre 2025
**Versión del Documento:** 1.0.0
