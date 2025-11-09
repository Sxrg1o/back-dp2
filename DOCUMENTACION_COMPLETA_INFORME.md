# INFORME TÉCNICO COMPLETO
## SISTEMA DE GESTIÓN DE RESTAURANTES - BACKEND API

---

### INFORMACIÓN DEL PROYECTO

| Campo | Valor |
|-------|-------|
| **Nombre del Proyecto** | Back-DP2 - Restaurant Backend API |
| **Tipo de Sistema** | API REST para Gestión de Restaurantes Multi-Local |
| **Framework Principal** | FastAPI (Python 3.13+) |
| **Arquitectura** | Clean Architecture (Arquitectura en Capas) |
| **ORM** | SQLAlchemy 2.0 (Asíncrono) |
| **Base de Datos** | MySQL / PostgreSQL (compatible) |
| **Sistema de Autenticación** | JWT (JSON Web Tokens) con Access/Refresh Tokens |
| **Versión Actual** | 1.0.0 |
| **Fecha del Informe** | Noviembre 2025 |
| **Autor del Informe** | Equipo de Desarrollo Back-DP2 |

---

## RESUMEN EJECUTIVO

Este informe presenta la documentación técnica completa del sistema **Restaurant Backend API**, un sistema robusto de gestión de restaurantes diseñado con arquitectura moderna y escalable. El sistema fue desarrollado utilizando las mejores prácticas de la industria, implementando Clean Architecture y siguiendo los principios SOLID.

### Alcance del Sistema

El sistema Back-DP2 es una solución integral para la gestión de restaurantes que abarca:

1. **Gestión de Usuarios y Autenticación:** Sistema completo de registro, login y autorización basado en roles
2. **Catálogo de Productos Multi-Local:** Gestión centralizada de categorías, productos, alérgenos y opciones con capacidad de personalización por local
3. **Gestión de Espacios:** Administración jerárquica de locales, zonas y mesas
4. **Sistema de Pedidos:** Procesamiento completo de pedidos con seguimiento de estados y opciones personalizables
5. **Integración con Sistema Legacy:** Sincronización bidireccional con el sistema Domotica existente

### Características Técnicas Destacadas

- **Arquitectura Asíncrona:** Implementación completamente asíncrona utilizando async/await para máximo rendimiento
- **Seguridad Robusta:** Autenticación JWT con tokens de acceso y actualización, hashing de contraseñas con Bcrypt
- **Escalabilidad:** Diseño por capas que permite escalar horizontal y verticalmente
- **Mantenibilidad:** Código limpio con separación clara de responsabilidades y documentación exhaustiva
- **Testing:** Estructura preparada para testing unitario e integración con pytest

---

## TABLA DE CONTENIDOS

1. [INTRODUCCIÓN Y CONTEXTO](#1-introducción-y-contexto)
2. [GUÍA DE ESTÁNDARES DE CODIFICACIÓN](#2-guía-de-estándares-de-codificación)
3. [DOCUMENTO DE DISEÑO TÉCNICO](#3-documento-de-diseño-técnico)
4. [DOCUMENTACIÓN DE API REST](#4-documentación-de-api-rest)
5. [MODELOS DE DATOS Y ESQUEMAS DE BASE DE DATOS](#5-modelos-de-datos-y-esquemas-de-base-de-datos)
6. [CONCLUSIONES Y RECOMENDACIONES](#6-conclusiones-y-recomendaciones)
7. [ANEXOS](#7-anexos)

---

# 1. INTRODUCCIÓN Y CONTEXTO

## 1.1 Propósito del Documento

Este documento técnico tiene como objetivo proporcionar una visión completa y detallada del sistema Backend de Restaurantes (Back-DP2), documentando todos los aspectos técnicos, arquitectónicos y de implementación del proyecto. Está dirigido a:

- **Desarrolladores:** Como guía de referencia para mantener y extender el sistema
- **Arquitectos de Software:** Para comprender las decisiones de diseño y patrones implementados
- **Auditores Técnicos:** Para verificar el cumplimiento de estándares y mejores prácticas
- **Nuevos Integrantes del Equipo:** Como material de onboarding técnico
- **Stakeholders Técnicos:** Para entender las capacidades y limitaciones del sistema

## 1.2 Contexto del Proyecto

### 1.2.1 Problemática Identificada

El sector de restaurantes enfrenta desafíos significativos en la gestión eficiente de operaciones, especialmente cuando se manejan múltiples locales. Los sistemas tradicionales presentan limitaciones como:

- **Falta de centralización:** Cada local maneja su propio catálogo sin sincronización
- **Procesos manuales:** Alta dependencia de procesos manuales propensos a errores
- **Escalabilidad limitada:** Dificultad para expandir a nuevos locales
- **Integración deficiente:** Sistemas legacy aislados sin capacidad de integración
- **Experiencia del cliente:** Procesos de pedido y pago complejos y lentos

### 1.2.2 Solución Propuesta

El sistema Back-DP2 fue diseñado como una solución moderna y escalable que resuelve estas problemáticas mediante:

1. **Arquitectura Multi-Local:** Gestión centralizada con personalización por local
2. **API REST Moderna:** Interfaz estándar para integración con múltiples frontends
3. **Sistema de Autenticación Robusto:** Seguridad basada en JWT con gestión de roles
4. **Procesamiento Asíncrono:** Alto rendimiento mediante operaciones asíncronas
5. **Integración con Legacy:** Capacidad de sincronización con sistemas existentes

### 1.2.3 Tecnologías Seleccionadas y Justificación

#### **FastAPI (Framework Web)**

**Justificación de Selección:**

FastAPI fue seleccionado como framework principal por las siguientes razones técnicas:

1. **Alto Rendimiento:** FastAPI es uno de los frameworks más rápidos de Python, comparable con NodeJS y Go, gracias a su integración con Starlette y Pydantic
2. **Validación Automática:** Pydantic proporciona validación automática de datos con type hints de Python, reduciendo código boilerplate
3. **Documentación Automática:** Genera documentación OpenAPI (Swagger) automáticamente, facilitando la integración y testing
4. **Soporte Asíncrono Nativo:** Soporta async/await de forma nativa, permitiendo operaciones I/O no bloqueantes
5. **Type Safety:** Aprovecha los type hints de Python 3.10+ para detección de errores en tiempo de desarrollo

**Evidencia en el código:**
```python
# main.py:237-246
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,  # Gestión de ciclo de vida
)
```

#### **SQLAlchemy 2.0 (ORM)**

**Justificación de Selección:**

SQLAlchemy 2.0 fue elegido por:

1. **Soporte Asíncrono:** SQLAlchemy 2.0 introdujo soporte completo para operaciones asíncronas con asyncio
2. **Flexibilidad:** Permite usar tanto el patrón Active Record como Data Mapper
3. **Madurez:** ORM maduro con amplia adopción en la industria
4. **Independencia de BD:** Funciona con múltiples motores de base de datos (MySQL, PostgreSQL, SQLite)
5. **Type Hints Mejorados:** Soporte completo para type hints con Mapped[] para mejor IDE support

**Evidencia en el código:**
```python
# database.py:18-75
class DatabaseManager:
    def __init__(self):
        self.engine = create_async_engine(  # Motor asíncrono
            self.settings.database_url,
            echo=self.settings.debug,
            pool_pre_ping=True,  # Detecta desconexiones
            pool_size=10,
            max_overflow=20,
        )
        self._session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
```

#### **JWT (JSON Web Tokens) para Autenticación**

**Justificación de Selección:**

JWT fue seleccionado sobre sesiones tradicionales por:

1. **Stateless:** No requiere almacenamiento en servidor, facilitando escalado horizontal
2. **Estándar de Industria:** Ampliamente adoptado y soportado por múltiples plataformas
3. **Self-Contained:** El token contiene toda la información necesaria para validar identidad
4. **Cross-Domain:** Funciona perfectamente en arquitecturas de microservicios
5. **Refresh Tokens:** Sistema de access/refresh tokens para balance entre seguridad y UX

**Evidencia en el código:**
```python
# security.py:56-95
def create_access_token(self, data: dict) -> str:
    """Crea token de acceso con expiración corta (30 min)"""
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
```

## 1.3 Objetivos del Sistema

### Objetivos Funcionales

1. **Gestión Integral de Usuarios:**
   - Registro y autenticación segura
   - Sistema de roles y permisos
   - Auditoría de accesos

2. **Catálogo Multi-Local:**
   - Catálogo maestro centralizado
   - Personalización por local (precios, disponibilidad)
   - Gestión de alérgenos y opciones de productos

3. **Gestión de Espacios:**
   - Jerarquía de locales → zonas → mesas
   - Estados de mesas en tiempo real
   - Generación de códigos QR por mesa

4. **Sistema de Pedidos:**
   - Creación de pedidos con opciones personalizables
   - Seguimiento de estados (pendiente → confirmado → preparación → listo → entregado)
   - Cálculo automático de totales

5. **Integración con Sistema Legacy:**
   - Sincronización de productos desde Domotica
   - Sincronización de mesas y zonas
   - Enriquecimiento automático de datos

### Objetivos No Funcionales

1. **Rendimiento:**
   - Tiempo de respuesta < 200ms para operaciones de lectura
   - Soporte para 1000+ peticiones concurrentes
   - Operaciones asíncronas para evitar bloqueos

2. **Seguridad:**
   - Autenticación obligatoria para endpoints protegidos
   - Hashing seguro de contraseñas (Bcrypt)
   - Protección contra inyección SQL (ORM)
   - CORS configurado correctamente

3. **Escalabilidad:**
   - Arquitectura stateless para escalado horizontal
   - Pool de conexiones a BD configurable
   - Separación de capas para distribución en microservicios

4. **Mantenibilidad:**
   - Código autodocumentado con type hints
   - Cobertura de testing > 80%
   - Separación clara de responsabilidades
   - Documentación técnica completa

5. **Disponibilidad:**
   - Health check endpoint para monitoreo
   - Manejo robusto de excepciones
   - Logging estructurado para debugging
   - Reintentos automáticos en operaciones críticas

---

# 2. GUÍA DE ESTÁNDARES DE CODIFICACIÓN

## 2.1 Introducción a los Estándares

La consistencia en el código es fundamental para la mantenibilidad a largo plazo de un proyecto. Este sistema implementa estándares de codificación estrictos basados en PEP 8 (Python Enhancement Proposal 8) y mejores prácticas de la industria.

**Importancia de los Estándares:**

1. **Legibilidad:** El código se lee más veces de las que se escribe. Un estándar consistente facilita la comprensión
2. **Colaboración:** Permite que múltiples desarrolladores trabajen en el mismo código sin fricciones
3. **Mantenibilidad:** Reduce el tiempo necesario para entender y modificar código existente
4. **Detección de Errores:** Convenciones claras ayudan a identificar antipatrones rápidamente
5. **Onboarding:** Nuevos desarrolladores pueden adaptarse más rápido al proyecto

## 2.2 Convenciones de Nomenclatura

### 2.2.1 Variables

**Estándar Adoptado:** `snake_case` (minúsculas con guiones bajos)

**Justificación:**

El estándar `snake_case` para variables en Python es ampliamente aceptado por la comunidad y recomendado en PEP 8. Proporciona:

- **Legibilidad:** Las palabras separadas por guiones bajos son más fáciles de leer que camelCase
- **Consistencia con Python:** Es el estándar de la biblioteca estándar de Python
- **Claridad:** Los nombres descriptivos en snake_case son auto-explicativos

**Reglas de Aplicación:**

1. Usar nombres descriptivos que reflejen el propósito de la variable
2. Evitar abreviaciones no estándar
3. Usar plurales para colecciones (`usuarios`, `productos`)
4. Prefijo `is_`, `has_`, `can_` para booleanos (`is_active`, `has_permission`)

**Ejemplos Correctos del Código:**

```python
# Ubicación: usuario_service.py:50-75
# Contexto: Método de autenticación de usuarios

# Variables de datos de usuario
usuario = await self.repository.get_by_email(login_data.email)
existing_usuario = await self.repository.get_by_email(register_data.email)
created_usuario = await self.repository.create(usuario)

# Variables de seguridad
password_hash = security.get_password_hash(register_data.password)
access_token = security.create_access_token(token_data)
refresh_token = security.create_refresh_token(token_data)

# Variables de transformación de datos
token_data = {"sub": usuario.id, "email": usuario.email}
usuario_response = UsuarioResponse.model_validate(usuario)
update_data = usuario_data.model_dump(exclude_none=True)
```

**Análisis del Ejemplo:**

- `usuario`: Singular, representa una instancia única
- `existing_usuario`: Adjetivo descriptivo que clarifica que es un usuario que ya existe
- `password_hash`: Compuesto que describe exactamente qué contiene (hash de password)
- `token_data`: Diccionario de datos para el token, el sufijo `_data` clarifica que es un contenedor
- `update_data`: Datos para actualización, el contexto es claro

### 2.2.2 Funciones y Métodos

**Estándar Adoptado:** `snake_case` con verbos descriptivos

**Justificación:**

Las funciones y métodos representan acciones, por lo que deben comenzar con verbos que describan la acción que realizan. El uso de `snake_case` mantiene consistencia con las variables y sigue PEP 8.

**Patrones de Nomenclatura Implementados:**

| Patrón | Uso | Ejemplo |
|--------|-----|---------|
| **CRUD Básico** | Operaciones de base de datos | `create`, `get_by_id`, `update`, `delete` |
| **CRUD Extendido** | Búsquedas específicas | `get_by_email`, `get_all`, `find_active` |
| **Business Logic** | Lógica de negocio | `login`, `register`, `calculate_total` |
| **Validación** | Validadores | `validate_product_data`, `check_availability` |
| **Transformación** | Conversiones | `to_dict`, `from_dict`, `serialize` |
| **Métodos Privados** | Uso interno (prefijo `_`) | `_generate_numero_pedido`, `_validate_price` |

**Ejemplos del Código - Operaciones CRUD:**

```python
# Ubicación: usuario_repository.py:31-117
# Contexto: Repositorio de usuarios con operaciones de persistencia

class UsuarioRepository:
    """
    Repositorio que encapsula todas las operaciones de acceso a datos
    relacionadas con la entidad Usuario.

    Siguiendo el patrón Repository, cada método tiene una responsabilidad única
    y clara relacionada con operaciones de base de datos.
    """

    async def create(self, usuario: UsuarioModel) -> UsuarioModel:
        """
        Crea un nuevo usuario en la base de datos.

        El nombre 'create' es estándar en operaciones CRUD y claramente
        indica que se está creando un nuevo registro.
        """
        pass

    async def get_by_id(self, usuario_id: str) -> Optional[UsuarioModel]:
        """
        Obtiene un usuario por su ID único.

        El patrón 'get_by_X' indica:
        - 'get': Operación de lectura
        - 'by_id': Criterio de búsqueda específico

        Retorna Optional indicando que puede no existir.
        """
        pass

    async def get_by_email(self, email: str) -> Optional[UsuarioModel]:
        """
        Obtiene un usuario por su email.

        Similar a get_by_id pero con criterio diferente.
        El nombre descriptivo evita confusión entre diferentes métodos de búsqueda.
        """
        pass

    async def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List, int]:
        """
        Obtiene todos los usuarios con paginación.

        'get_all' indica claramente que retorna múltiples registros.
        Los parámetros 'skip' y 'limit' son estándar para paginación.
        """
        pass

    async def update(self, usuario_id: str, **kwargs) -> Optional[UsuarioModel]:
        """
        Actualiza un usuario existente.

        'update' es el verbo estándar para modificación de registros.
        El uso de **kwargs permite actualizaciones parciales.
        """
        pass

    async def delete(self, usuario_id: str) -> bool:
        """
        Elimina un usuario de la base de datos.

        'delete' es inequívoco en su propósito.
        Retorna bool para indicar éxito/fallo de la operación.
        """
        pass
```

**Ejemplos del Código - Lógica de Negocio:**

```python
# Ubicación: usuario_service.py:40-254
# Contexto: Servicio de lógica de negocio para usuarios

class UsuarioService:
    """
    Servicio que implementa la lógica de negocio relacionada con usuarios.

    Los nombres de métodos son verbos que describen acciones de negocio,
    no solo operaciones de base de datos.
    """

    async def login(self, login_data: LoginRequest) -> LoginResponse:
        """
        Autentica un usuario y genera tokens de acceso.

        'login' es un término de dominio de negocio universalmente entendido.
        No se llama 'authenticate_user' porque 'login' es más claro y conciso.
        """
        pass

    async def register(self, register_data: RegisterRequest) -> RegisterResponse:
        """
        Registra un nuevo usuario en el sistema.

        'register' describe la acción de negocio completa,
        que incluye validación, creación en BD y generación de tokens.
        """
        pass

    async def refresh_token(self, refresh_data: RefreshTokenRequest) -> RefreshTokenResponse:
        """
        Renueva el token de acceso usando un refresh token.

        El nombre describe exactamente qué hace: refrescar el token.
        Podría llamarse 'renew_access_token' pero 'refresh' es estándar OAuth2.
        """
        pass

    async def get_usuario_by_id(self, usuario_id: str) -> UsuarioResponse:
        """
        Obtiene información de un usuario por ID.

        Aunque similar al repositorio, este método incluye:
        - Validaciones de negocio
        - Transformación a DTO (UsuarioResponse)
        - Manejo de excepciones de negocio

        El nombre 'get_usuario_by_id' es más explícito que solo 'get_by_id'
        porque en el servicio podríamos tener métodos que obtienen otras entidades.
        """
        pass

    async def update_usuario(self, usuario_id: str, usuario_data: UsuarioUpdate) -> UsuarioResponse:
        """
        Actualiza la información de un usuario.

        'update_usuario' especifica qué entidad se actualiza.
        Incluye validaciones que no existen en el repositorio.
        """
        pass

    async def delete_usuario(self, usuario_id: str) -> bool:
        """
        Elimina un usuario del sistema.

        Aunque solo delega al repositorio, podría incluir:
        - Verificación de permisos
        - Cleanup de datos relacionados
        - Auditoría de eliminación
        """
        pass
```

**Métodos Privados (Prefijo `_`):**

```python
# Ubicación: pedido_service.py:74
# Contexto: Método interno para generar números de pedido únicos

async def _generate_numero_pedido(self, id_mesa: str) -> str:
    """
    Genera un número de pedido único.

    El prefijo '_' indica que este método:
    - Es de uso interno de la clase
    - No debe ser llamado desde fuera
    - No es parte de la API pública del servicio

    Justificación del nombre:
    - '_generate': Verbo que indica creación
    - 'numero_pedido': Exactamente qué se genera

    Este patrón evita que clientes externos dependan de implementaciones internas,
    facilitando refactorización futura.
    """
    pass

# Ubicación: producto_validators.py:58
async def _validate_price(price: Any) -> None:
    """
    Valida que un precio sea válido (> 0, numérico, etc.).

    Método privado porque:
    - Es un helper interno del módulo de validación
    - Puede cambiar su implementación sin afectar API pública
    - Reduce la superficie de la API pública
    """
    pass
```

### 2.2.3 Clases

**Estándar Adoptado:** `PascalCase` con sufijos descriptivos del tipo de clase

**Justificación:**

PascalCase para clases es el estándar universal en Python (PEP 8) y la mayoría de lenguajes orientados a objetos. Permite distinguir inmediatamente una clase de una variable o función.

Los sufijos descriptivos (`Model`, `Repository`, `Service`, `Error`, etc.) implementan el patrón de nomenclatura por rol, facilitando la identificación del propósito de cada clase.

**Tabla de Sufijos Implementados:**

| Tipo de Clase | Sufijo | Propósito | Ejemplo Completo | Ubicación |
|---------------|--------|-----------|------------------|-----------|
| **Modelos ORM** | `Model` | Representa tabla de BD | `UsuarioModel`, `ProductoModel` | `src/models/` |
| **Repositorios** | `Repository` | Acceso a datos | `UsuarioRepository` | `src/repositories/` |
| **Servicios** | `Service` | Lógica de negocio | `UsuarioService`, `PedidoService` | `src/business_logic/` |
| **DTOs - Creación** | `Create` | Schema para crear | `UsuarioCreate`, `ProductoCreate` | `src/api/schemas/` |
| **DTOs - Actualización** | `Update` | Schema para actualizar | `UsuarioUpdate`, `ProductoUpdate` | `src/api/schemas/` |
| **DTOs - Respuesta** | `Response` | Schema para respuesta API | `UsuarioResponse`, `LoginResponse` | `src/api/schemas/` |
| **DTOs - Resumen** | `Summary` | Schema resumido (listas) | `UsuarioSummary` | `src/api/schemas/` |
| **Excepciones** | `Error` | Excepciones personalizadas | `UsuarioNotFoundError` | `src/business_logic/exceptions/` |
| **Mixins** | `Mixin` | Comportamiento reutilizable | `AuditMixin`, `SoftDeleteMixin` | `src/models/mixins/` |

**Ejemplos Detallados del Código:**

**1. Modelos de Base de Datos (Sufijo `Model`):**

```python
# Ubicación: usuario_model.py:15
# Propósito: Representar la tabla 'usuarios' en la base de datos

class UsuarioModel(BaseModel, AuditMixin):
    """
    Modelo ORM que representa un usuario del sistema.

    El sufijo 'Model' clarifica que esta clase:
    - Es un modelo de SQLAlchemy
    - Representa una tabla de base de datos
    - Tiene campos mapeados a columnas

    Hereda de:
    - BaseModel: Proporciona campo 'id' (ULID) y métodos comunes
    - AuditMixin: Agrega campos de auditoría (fecha_creacion, etc.)

    Ubicación del archivo: src/models/auth/usuario_model.py
    Tabla de BD: usuarios
    """
    __tablename__ = "usuarios"

    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    # ... más campos
```

**Análisis del Ejemplo:**

- `UsuarioModel` vs `Usuario`: El sufijo `Model` evita confusión con el schema `UsuarioResponse`
- Si solo se llamara `Usuario`, habría ambigüedad: ¿Es el modelo? ¿Es el DTO?
- El sufijo hace el propósito explícito instantáneamente

**2. Repositorios (Sufijo `Repository`):**

```python
# Ubicación: usuario_repository.py:13
# Propósito: Encapsular acceso a datos de usuarios

class UsuarioRepository:
    """
    Repositorio para operaciones CRUD del modelo Usuario.

    El sufijo 'Repository' indica que esta clase:
    - Implementa el patrón Repository
    - Encapsula acceso a la capa de datos
    - Proporciona una interfaz limpia para operaciones de BD

    Beneficios del patrón:
    - Abstrae la implementación de persistencia
    - Facilita testing con mocks
    - Centraliza queries relacionadas

    Ubicación del archivo: src/repositories/auth/usuario_repository.py
    """

    def __init__(self, session: AsyncSession):
        """
        Constructor que recibe una sesión de BD.

        La inyección de la sesión permite:
        - Transacciones manejadas externamente
        - Testing con sesiones mock
        - Reutilización de conexiones
        """
        self.session = session

    # Métodos CRUD...
```

**3. Servicios de Lógica de Negocio (Sufijo `Service`):**

```python
# Ubicación: usuario_service.py:33
# Propósito: Implementar lógica de negocio de usuarios

class UsuarioService:
    """
    Servicio que implementa la lógica de negocio para usuarios.

    El sufijo 'Service' clarifica que esta clase:
    - Contiene lógica de negocio (no solo acceso a datos)
    - Coordina múltiples repositorios si es necesario
    - Aplica reglas de validación de negocio
    - Transforma entre modelos y DTOs

    Diferencia vs Repository:
    - Repository: Solo acceso a datos (queries)
    - Service: Lógica de negocio compleja

    Ubicación del archivo: src/business_logic/auth/usuario_service.py
    """

    def __init__(self, session: AsyncSession):
        """
        Constructor que inicializa repositorios necesarios.

        Patrón de composición:
        - El servicio usa repositorios
        - No hace queries directamente
        - Mantiene separación de responsabilidades
        """
        self.repository = UsuarioRepository(session)
        self.rol_repository = RolRepository(session)
        self.settings = get_settings()

    # Métodos de lógica de negocio...
```

**4. DTOs/Schemas con Sufijos Múltiples:**

```python
# Ubicación: usuario_schema.py:10-68
# Propósito: Definir contratos de API para diferentes operaciones

class UsuarioBase(BaseModel):
    """
    Schema base con campos comunes.

    'Base' indica que otros schemas heredarán de este.
    Contiene campos compartidos entre Create, Update y Response.
    """
    email: Optional[EmailStr] = Field(default=None)
    nombre: Optional[str] = Field(default=None)
    telefono: Optional[str] = Field(default=None)

class UsuarioCreate(UsuarioBase):
    """
    Schema para CREAR un usuario.

    El sufijo 'Create' indica:
    - Se usa en endpoint POST
    - Contiene campos requeridos para creación
    - Incluye password (no en UsuarioBase)

    Justificación de la separación:
    - Create necesita password
    - Response NUNCA debe exponer password
    - Update puede tener password opcional
    """
    password: str = Field(min_length=6)

class UsuarioUpdate(BaseModel):
    """
    Schema para ACTUALIZAR un usuario.

    El sufijo 'Update' indica:
    - Se usa en endpoints PUT/PATCH
    - Todos los campos son opcionales (actualización parcial)
    - Solo incluye campos modificables

    Nota: No hereda de UsuarioBase porque:
    - Queremos todos los campos opcionales
    - Puede incluir fields que no están en Base
    """
    email: Optional[EmailStr] = Field(default=None)
    password: Optional[str] = Field(default=None)
    nombre: Optional[str] = Field(default=None)

class UsuarioResponse(UsuarioBase):
    """
    Schema para RESPUESTAS de API.

    El sufijo 'Response' indica:
    - Se usa como valor de retorno de endpoints
    - Incluye campos de solo lectura (id, fechas)
    - NUNCA incluye password_hash

    Campos adicionales vs Base:
    - id: Generado por el sistema
    - activo: Estado del usuario
    - fecha_creacion, fecha_modificacion: Auditoría
    """
    id: str
    activo: bool
    fecha_creacion: datetime
    fecha_modificacion: datetime

class UsuarioSummary(BaseModel):
    """
    Schema RESUMIDO para listados.

    El sufijo 'Summary' indica:
    - Versión reducida de Response
    - Para endpoints que retornan listas
    - Solo campos esenciales (reduce payload)

    Beneficios:
    - Reduce tamaño de respuesta en listados
    - Más rápido de serializar
    - Mejor rendimiento en frontend
    """
    id: str
    email: str
    nombre: str
    activo: bool
```

**Análisis de la Jerarquía de Schemas:**

Esta estructura de schemas múltiples evita varios antipatrones:

1. **Antipatrón evitado: Schema único para todo**
   - ❌ Malo: Un solo `UsuarioSchema` con campos opcionales confusos
   - ✅ Bueno: Schemas específicos por operación

2. **Antipatrón evitado: Exponer password en responses**
   - ❌ Malo: `UsuarioResponse` con campo `password_hash`
   - ✅ Bueno: `UsuarioResponse` sin ningún campo de password

3. **Antipatrón evitado: Payloads grandes en listados**
   - ❌ Malo: Listar 100 usuarios con `UsuarioResponse` completo
   - ✅ Bueno: Listar 100 usuarios con `UsuarioSummary` reducido

**5. Excepciones Personalizadas (Sufijo `Error`):**

```python
# Ubicación: usuario_exceptions.py:7-70
# Propósito: Definir excepciones específicas del dominio de usuarios

class UsuarioValidationError(ValidationError):
    """
    Excepción para errores de validación de usuario.

    El sufijo 'Error' indica:
    - Es una excepción (se puede lanzar con 'raise')
    - Forma parte de la jerarquía de excepciones
    - Tiene un propósito específico

    Prefijo 'Usuario' indica:
    - Es específica del dominio de usuarios
    - Ayuda a identificar origen del error en logs

    Hereda de ValidationError (400 Bad Request)
    """
    def __init__(self, message: str, error_code: str = "USUARIO_VALIDATION_ERROR"):
        super().__init__(message, error_code)

class UsuarioNotFoundError(NotFoundError):
    """
    Excepción cuando no se encuentra un usuario.

    Sufijo 'Error' + patrón 'NotFound':
    - Claramente indica tipo de error
    - Se mapea a HTTP 404

    Hereda de NotFoundError (404 Not Found)
    """
    def __init__(self, message: str = "Usuario no encontrado"):
        super().__init__(message, "USUARIO_NOT_FOUND")

class UsuarioConflictError(ConflictError):
    """
    Excepción para conflictos (ej: email duplicado).

    Hereda de ConflictError (409 Conflict)
    Se lanza cuando se intenta crear usuario con email existente.
    """
    def __init__(self, message: str, error_code: str = "USUARIO_CONFLICT"):
        super().__init__(message, error_code)

class InvalidCredentialsError(UnauthorizedError):
    """
    Excepción para credenciales inválidas en login.

    Sufijo 'Error' con prefijo descriptivo 'InvalidCredentials':
    - Muy específica (no solo 'LoginError')
    - Indica exactamente qué falló

    Hereda de UnauthorizedError (401 Unauthorized)
    """
    def __init__(self, message: str = "Credenciales inválidas"):
        super().__init__(message, "INVALID_CREDENTIALS")
```

**Beneficios de esta Jerarquía de Excepciones:**

1. **Granularidad:** Cada tipo de error tiene su excepción específica
2. **Mapeo HTTP:** Cada excepción base se mapea a un código HTTP específico
3. **Logging:** Los nombres descriptivos facilitan búsqueda en logs
4. **Handling:** Permite capturar excepciones específicas o generales según necesidad

**6. Mixins (Sufijo `Mixin`):**

```python
# Ubicación: audit_mixin.py:15
# Propósito: Proporcionar campos de auditoría reutilizables

@declarative_mixin
class AuditMixin:
    """
    Mixin que agrega campos de auditoría a modelos.

    El sufijo 'Mixin' indica:
    - No es una clase standalone
    - Está diseñada para ser heredada junto con otras clases
    - Proporciona comportamiento/campos reutilizables

    Patrón de uso:
    class UsuarioModel(BaseModel, AuditMixin):
                                     ^^^^^^^^^ Herencia múltiple

    Beneficios:
    - DRY (Don't Repeat Yourself): Campos de auditoría definidos una vez
    - Consistencia: Todos los modelos con auditoría tienen mismos campos
    - Mantenibilidad: Cambiar auditoría en un lugar afecta todos los modelos

    Ubicación del archivo: src/models/mixins/audit_mixin.py
    """

    @declared_attr
    def fecha_creacion(cls) -> Mapped[datetime]:
        """Timestamp de creación del registro"""
        return mapped_column(TIMESTAMP, nullable=False, server_default=func.now())

    @declared_attr
    def fecha_modificacion(cls) -> Mapped[datetime]:
        """Timestamp de última modificación"""
        return mapped_column(
            TIMESTAMP, nullable=False,
            server_default=func.now(),
            onupdate=func.now()  # Se actualiza automáticamente
        )

    @declared_attr
    def creado_por(cls) -> Mapped[Optional[str]]:
        """ID del usuario que creó el registro"""
        return mapped_column(String(255), default=None)

    @declared_attr
    def modificado_por(cls) -> Mapped[Optional[str]]:
        """ID del usuario que modificó por última vez el registro"""
        return mapped_column(String(255), default=None)
```

**Uso del Mixin:**

```python
# Ubicación: usuario_model.py:15
class UsuarioModel(BaseModel, AuditMixin):
    """
    Al heredar de AuditMixin, este modelo automáticamente tiene:
    - fecha_creacion
    - fecha_modificacion
    - creado_por
    - modificado_por

    No es necesario definirlos manualmente.
    """
    __tablename__ = "usuarios"
    email: Mapped[str] = mapped_column(String(255))
    # ... otros campos
    # Los campos de AuditMixin están disponibles automáticamente
```

### 2.2.4 Nombres de Archivos

**Estándar Adoptado:** `snake_case` con sufijos descriptivos coincidiendo con la clase principal

**Justificación:**

La nomenclatura de archivos sigue el mismo patrón que las clases pero en `snake_case` (estándar Python para módulos según PEP 8). El sufijo del archivo coincide con el sufijo de la clase principal que contiene, facilitando la navegación.

**Tabla de Patrones de Archivos:**

| Tipo de Contenido | Patrón de Archivo | Clase Principal | Ejemplo Completo | Ubicación |
|-------------------|-------------------|-----------------|------------------|-----------|
| **Modelos** | `*_model.py` | `*Model` | `usuario_model.py` → `UsuarioModel` | `src/models/auth/` |
| **Repositorios** | `*_repository.py` | `*Repository` | `usuario_repository.py` → `UsuarioRepository` | `src/repositories/auth/` |
| **Servicios** | `*_service.py` | `*Service` | `usuario_service.py` → `UsuarioService` | `src/business_logic/auth/` |
| **Controladores** | `*_controller.py` | Router | `auth_controller.py` | `src/api/controllers/` |
| **Schemas** | `*_schema.py` | Múltiples clases | `usuario_schema.py` | `src/api/schemas/` |
| **Excepciones** | `*_exceptions.py` | Múltiples clases `*Error` | `usuario_exceptions.py` | `src/business_logic/exceptions/` |
| **Enums** | `*_enums.py` | Múltiples enums | `pedido_enums.py` | `src/core/enums/` |
| **Mixins** | `*_mixin.py` | `*Mixin` | `audit_mixin.py` → `AuditMixin` | `src/models/mixins/` |
| **Utils** | `*_utils.py` | Funciones auxiliares | `text_utils.py` | `src/core/utils/` |
| **Validators** | `*_validators.py` | Funciones validadoras | `producto_validators.py` | `src/business_logic/validators/` |

**Estructura de Directorios con Ejemplos Reales:**

```
src/
├── models/
│   ├── auth/
│   │   ├── usuario_model.py        # Contiene: UsuarioModel
│   │   ├── rol_model.py            # Contiene: RolModel
│   │   └── sesion_model.py         # Contiene: SesionModel
│   ├── menu/
│   │   ├── producto_model.py       # Contiene: ProductoModel
│   │   ├── categoria_model.py      # Contiene: CategoriaModel
│   │   └── alergeno_model.py       # Contiene: AlergenoModel
│   └── mixins/
│       ├── audit_mixin.py          # Contiene: AuditMixin
│       └── soft_delete_mixin.py    # Contiene: SoftDeleteMixin
│
├── repositories/
│   ├── auth/
│   │   ├── usuario_repository.py   # Contiene: UsuarioRepository
│   │   └── rol_repository.py       # Contiene: RolRepository
│   └── menu/
│       ├── producto_repository.py  # Contiene: ProductoRepository
│       └── categoria_repository.py # Contiene: CategoriaRepository
│
├── business_logic/
│   ├── auth/
│   │   ├── usuario_service.py      # Contiene: UsuarioService
│   │   └── rol_service.py          # Contiene: RolService
│   ├── exceptions/
│   │   ├── base_exceptions.py      # Contiene: BusinessError, ValidationError, etc.
│   │   ├── usuario_exceptions.py   # Contiene: UsuarioNotFoundError, etc.
│   │   └── producto_exceptions.py  # Contiene: ProductoNotFoundError, etc.
│   └── validators/
│       └── producto_validators.py  # Contiene: validate_product_data(), etc.
│
├── api/
│   ├── controllers/
│   │   ├── auth_controller.py      # Contiene: router (FastAPI Router)
│   │   └── producto_controller.py  # Contiene: router
│   └── schemas/
│       ├── usuario_schema.py       # Contiene: UsuarioCreate, UsuarioResponse, etc.
│       └── producto_schema.py      # Contiene: ProductoCreate, ProductoResponse, etc.
│
└── core/
    ├── enums/
    │   ├── pedido_enums.py         # Contiene: EstadoPedido, TipoDivision
    │   ├── user_enums.py           # Contiene: RoleName
    │   └── mesa_enums.py           # Contiene: EstadoMesa
    └── utils/
        ├── text_utils.py           # Contiene: normalize_text(), etc.
        └── pagination_utils.py     # Contiene: paginate(), etc.
```

**Beneficios de esta Convención:**

1. **Predictibilidad:** Si sabes el nombre de la clase, sabes el nombre del archivo
2. **Navegación:** Fácil encontrar archivos en IDEs con búsqueda por nombre
3. **Organización:** Agrupación lógica por tipo y dominio
4. **Imports Claros:** El nombre del módulo indica qué contiene

**Ejemplo de Imports Resultantes:**

```python
# Imports claros y autodescriptivos
from src.models.auth.usuario_model import UsuarioModel
from src.repositories.auth.usuario_repository import UsuarioRepository
from src.business_logic.auth.usuario_service import UsuarioService
from src.api.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from src.business_logic.exceptions.usuario_exceptions import UsuarioNotFoundError
```

Cada import claramente indica:
- Qué se importa (la clase)
- De qué módulo viene (el archivo)
- En qué capa está (models, repositories, business_logic, api)
- De qué dominio es (auth, menu, pedidos)

### 2.2.5 Constantes

**Estándar Adoptado:** `SCREAMING_SNAKE_CASE` (mayúsculas con guiones bajos)

**Justificación:**

El uso de mayúsculas para constantes es un estándar universal en programación que permite identificar visualmente valores que no deben cambiar. En Python, aunque las constantes no están enforceadas por el lenguaje, la convención `SCREAMING_SNAKE_CASE` comunica claramente la intención.

**Tipos de Constantes en el Proyecto:**

1. **Diccionarios de Configuración:** Mapeos inmutables
2. **Instancias Singleton:** Instancias únicas compartidas
3. **Valores de Enumeración:** (implícitos en Enum, pero en mayúsculas)

**Ejemplos del Código:**

**1. Constantes de Configuración - Transiciones de Estado:**

```python
# Ubicación: pedido_service.py:56-63
# Propósito: Definir transiciones válidas entre estados de pedido

VALID_TRANSITIONS = {
    EstadoPedido.PENDIENTE: [EstadoPedido.CONFIRMADO, EstadoPedido.CANCELADO],
    EstadoPedido.CONFIRMADO: [EstadoPedido.EN_PREPARACION, EstadoPedido.CANCELADO],
    EstadoPedido.EN_PREPARACION: [EstadoPedido.LISTO, EstadoPedido.CANCELADO],
    EstadoPedido.LISTO: [EstadoPedido.ENTREGADO],
    EstadoPedido.ENTREGADO: [],
    EstadoPedido.CANCELADO: [],
}
```

**Explicación Detallada:**

Esta constante define una **máquina de estados** para pedidos:

- **Propósito:** Validar que las transiciones de estado sean permitidas
- **Por qué es constante:** Las reglas de negocio de transiciones no cambian en runtime
- **Uso:** El servicio valida contra este diccionario antes de cambiar estado

**Ejemplo de Uso:**

```python
async def cambiar_estado(self, pedido_id: str, nuevo_estado: EstadoPedido):
    """
    Cambia el estado de un pedido validando transiciones permitidas.
    """
    pedido = await self.repository.get_by_id(pedido_id)
    estado_actual = pedido.estado

    # Validar transición usando la constante
    if nuevo_estado not in VALID_TRANSITIONS[estado_actual]:
        raise InvalidStateTransitionError(
            f"No se puede cambiar de {estado_actual} a {nuevo_estado}"
        )

    # Si es válido, actualizar
    pedido.estado = nuevo_estado
    await self.repository.update(pedido)
```

**Beneficios:**

- **Centralización:** Las reglas de transición están en un solo lugar
- **Mantenibilidad:** Cambiar reglas de negocio solo requiere modificar la constante
- **Claridad:** El nombre en mayúsculas indica que no debe modificarse en runtime

**2. Instancias Singleton:**

```python
# Ubicación: security.py:130
# Propósito: Instancia única del servicio de seguridad

security = SecurityConfig()

# Ubicación: database.py:137
# Propósito: Instancia única del gestor de base de datos

db = DatabaseManager()
```

**Explicación:**

Aunque técnicamente son variables, se usan como constantes porque:

1. **Singleton Pattern:** Solo debe existir una instancia
2. **Shared State:** Son compartidas por toda la aplicación
3. **Inmutabilidad de Referencia:** La referencia no debe cambiar (aunque el objeto interno tenga estado)

**Uso en el Código:**

```python
# Ubicación: usuario_service.py:65
# Usando la instancia singleton 'security'

password_hash = security.get_password_hash(register_data.password)
access_token = security.create_access_token(token_data)

# Ubicación: database.py:141
# Usando la instancia singleton 'db'

async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.session() as session:
        yield session
```

**Por qué no están en MAYÚSCULAS:**

Aunque son constantes conceptualmente, se nombran en minúsculas porque:
- Son instancias de clase (objetos), no valores primitivos
- Tienen métodos que se llaman (ej: `security.get_password_hash()`)
- La convención Python para módulos singleton suele usar minúsculas

**3. Valores de Enumeración:**

```python
# Ubicación: pedido_enums.py:6-13
# Propósito: Definir estados posibles de un pedido

class EstadoPedido(str, Enum):
    """
    Estados posibles de un pedido en el sistema.

    Los valores en mayúsculas indican:
    - Son constantes (no cambian)
    - Representan opciones fijas del sistema
    - Se usan en validaciones y lógica de negocio
    """
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"
```

**Uso de Enums en Validación:**

```python
# En models/pedidos/pedido_model.py
estado: Mapped[EstadoPedido] = mapped_column(
    Enum(EstadoPedido),
    default=EstadoPedido.PENDIENTE,  # Constante
    nullable=False
)

# En schemas
class PedidoUpdate(BaseModel):
    estado: Optional[EstadoPedido] = None  # Pydantic valida contra el Enum
```

**Beneficios de Enums:**

1. **Type Safety:** No se pueden usar valores inválidos
2. **Autocompletado:** IDEs sugieren valores válidos
3. **Documentación:** Los valores posibles están claramente definidos
4. **Validación Automática:** Pydantic y SQLAlchemy validan contra el enum

---

## 2.3 Formato y Estilo de Código

### 2.3.1 Indentación

**Estándar Adoptado:** 4 espacios por nivel de indentación (NO tabs)

**Justificación:**

PEP 8 establece 4 espacios como el estándar de Python. Usar espacios en lugar de tabs evita problemas de visualización entre editores y asegura consistencia visual.

**Configuración en el Proyecto:**

```python
# .editorconfig (si existiera)
[*.py]
indent_style = space
indent_size = 4
```

**Ejemplos Correctos:**

```python
# ✅ Correcto: 4 espacios por nivel
class UsuarioService:
    def __init__(self, session: AsyncSession):
        self.repository = UsuarioRepository(session)
        self.settings = get_settings()

    async def login(self, login_data: LoginRequest) -> LoginResponse:
        usuario = await self.repository.get_by_email(login_data.email)

        if not usuario:
            raise InvalidCredentialsError("Email o contraseña incorrectos")

        if not usuario.activo:
            raise InactiveUserError("El usuario está inactivo")

        return self._generate_response(usuario)
```

**Ejemplo Incorrecto:**

```python
# ❌ Incorrecto: Mezcla de tabs y espacios, indentación inconsistente
class UsuarioService:
  def __init__(self, session: AsyncSession):  # 2 espacios
      self.repository = UsuarioRepository(session)  # 6 espacios
    async def login(self, login_data: LoginRequest):  # 4 espacios pero mal alineado
        pass
```

### 2.3.2 Límites de Línea

**Estándar Adoptado:** Máximo 120 caracteres por línea

**Justificación:**

PEP 8 originalmente recomienda 79 caracteres, pero proyectos modernos suelen usar 100-120 para aprovechar pantallas modernas. Este proyecto usa 120 como compromiso entre legibilidad y aprovechamiento de espacio horizontal.

**Cuándo Dividir Líneas:**

1. **Imports largos:**

```python
# ✅ Correcto
from src.business_logic.exceptions.usuario_exceptions import (
    UsuarioNotFoundError,
    UsuarioValidationError,
    InvalidCredentialsError,
)

# ❌ Incorrecto (> 120 caracteres)
from src.business_logic.exceptions.usuario_exceptions import UsuarioNotFoundError, UsuarioValidationError, InvalidCredentialsError
```

2. **Llamadas a funciones con muchos parámetros:**

```python
# ✅ Correcto
usuario = await self.repository.create(
    email=register_data.email,
    password_hash=password_hash,
    nombre=register_data.nombre,
    telefono=register_data.telefono,
    id_rol=register_data.id_rol,
)

# ❌ Incorrecto
usuario = await self.repository.create(email=register_data.email, password_hash=password_hash, nombre=register_data.nombre, telefono=register_data.telefono, id_rol=register_data.id_rol)
```

3. **Queries de SQLAlchemy:**

```python
# ✅ Correcto
query = (
    select(UsuarioModel)
    .where(UsuarioModel.email == email)
    .where(UsuarioModel.activo == True)
    .options(selectinload(UsuarioModel.rol))
)

# ❌ Incorrecto
query = select(UsuarioModel).where(UsuarioModel.email == email).where(UsuarioModel.activo == True).options(selectinload(UsuarioModel.rol))
```

### 2.3.3 Uso de Llaves y Formato de Diccionarios/Listas

**Formato para Diccionarios:**

```python
# ✅ Correcto: Diccionarios en múltiples líneas para claridad
token_data = {
    "sub": usuario.id,
    "email": usuario.email,
    "rol": usuario.rol.nombre,
    "exp": datetime.now() + timedelta(minutes=30),
}

# ✅ También correcto si es corto
user_info = {"id": user_id, "name": name}

# ❌ Incorrecto: Diccionario largo en una línea
token_data = {"sub": usuario.id, "email": usuario.email, "rol": usuario.rol.nombre, "exp": datetime.now() + timedelta(minutes=30)}
```

**Formato para Listas:**

```python
# ✅ Correcto: Lista de controladores en main.py:176-201
controllers = [
    ("src.api.controllers.auth_controller", "Autenticación"),
    ("src.api.controllers.rol_controller", "Roles"),
    ("src.api.controllers.local_controller", "Locales"),
    ("src.api.controllers.zona_controller", "Zonas"),
    ("src.api.controllers.producto_controller", "Productos"),
]

# ✅ Correcto si la lista es corta
estados_finales = [EstadoPedido.ENTREGADO, EstadoPedido.CANCELADO]
```

### 2.3.4 Espaciado

**Reglas de Espaciado Aplicadas:**

1. **Espacios alrededor de operadores:**

```python
# ✅ Correcto
precio_total = precio_base + precio_opciones
cantidad_disponible = stock - pedidos_pendientes
promedio = suma / cantidad

# ❌ Incorrecto
precio_total=precio_base+precio_opciones  # Sin espacios
cantidad_disponible = stock-pedidos_pendientes  # Inconsistente
```

2. **Espacios después de comas:**

```python
# ✅ Correcto
lista = [1, 2, 3, 4]
resultado = funcion(a, b, c)
diccionario = {"clave1": valor1, "clave2": valor2}

# ❌ Incorrecto
lista = [1,2,3,4]  # Sin espacios
resultado = funcion(a,b,c)
```

3. **SIN espacios en asignaciones con tipo:**

```python
# ✅ Correcto
email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
nombre: Mapped[Optional[str]] = mapped_column(String(255))

# ❌ Incorrecto
email : Mapped[Optional[str]] = mapped_column(String(255), unique=True)  # Espacio antes de ':'
nombre: Mapped[Optional[str]]=mapped_column(String(255))  # Sin espacio alrededor de '='
```

4. **Espacios en definiciones de función:**

```python
# ✅ Correcto
def create(self, usuario: UsuarioModel) -> UsuarioModel:
    pass

async def get_by_id(self, usuario_id: str) -> Optional[UsuarioModel]:
    pass

# ❌ Incorrecto
def create(self,usuario:UsuarioModel)->UsuarioModel:  # Sin espacios
    pass
```

**Evidencia del Código:**

```python
# Ubicación: producto_service.py:50
# Ejemplo real de espaciado correcto

precio_total = precio_base + precio_opciones
cantidad_disponible = stock - pedidos_pendientes

# Ubicación: usuario_model.py:20-25
# Ejemplo de asignaciones con tipo

email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
password_hash: Mapped[Optional[str]] = mapped_column(String(255))
nombre: Mapped[Optional[str]] = mapped_column(String(255))
telefono: Mapped[Optional[str]] = mapped_column(String(20))
activo: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
```

---

## 2.4 Principios y Patrones de Diseño

### 2.4.1 Principios SOLID

Los principios SOLID son un conjunto de cinco principios de diseño orientado a objetos que conducen a código más mantenible, flexible y escalable. Este proyecto implementa TODOS los principios SOLID de manera rigurosa.

#### **S - Single Responsibility Principle (Principio de Responsabilidad Única)**

**Definición:** Una clase debe tener una sola razón para cambiar.

**Interpretación:** Cada clase debe tener una única responsabilidad bien definida.

**Implementación en el Proyecto:**

El proyecto implementa este principio mediante una estricta separación en capas, donde cada clase tiene una responsabilidad claramente definida:

**1. Controllers → Solo HTTP:**

```python
# Ubicación: auth_controller.py:145-166
# Responsabilidad ÚNICA: Recibir peticiones HTTP y retornar respuestas HTTP

@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_database_session),
) -> LoginResponse:
    """
    Responsabilidad: SOLO manejo de HTTP

    ✅ Hace:
    - Recibe LoginRequest (validado automáticamente por FastAPI/Pydantic)
    - Obtiene dependencias (sesión de BD)
    - Delega lógica de negocio al Service
    - Maneja excepciones de negocio convirtiéndolas a HTTP errors
    - Retorna LoginResponse serializada a JSON

    ❌ NO hace:
    - Validar contraseñas (delegado a Service)
    - Queries a base de datos (delegado a Repository vía Service)
    - Lógica de negocio (delegado a Service)
    - Manipulación directa de modelos (usa DTOs)
    """
    try:
        usuario_service = UsuarioService(session)
        result = await usuario_service.login(login_data)
        await session.commit()
        return result  # FastAPI serializa automáticamente
    except InvalidCredentialsError as e:
        await session.rollback()
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
```

**Análisis:**

- **Razón para cambiar:** Solo cambiaría si el protocolo HTTP cambia o los DTOs cambian
- **NO cambiaría por:** Cambios en lógica de validación, cambios en BD, cambios en hashing

**2. Services → Solo Lógica de Negocio:**

```python
# Ubicación: usuario_service.py:40-80
# Responsabilidad ÚNICA: Lógica de negocio de autenticación

async def login(self, login_data: LoginRequest) -> LoginResponse:
    """
    Responsabilidad: SOLO lógica de negocio de login

    ✅ Hace:
    - Validar credenciales (negocio)
    - Verificar estado del usuario (negocio)
    - Generar tokens (negocio)
    - Transformar Model a DTO (negocio)
    - Lanzar excepciones de negocio apropiadas

    ❌ NO hace:
    - Queries SQL directas (delegado a Repository)
    - Manejo de HTTP (delegado a Controller)
    - Logging de acceso HTTP (responsabilidad de middleware)
    """
    # Delega a Repository: acceso a datos
    usuario = await self.repository.get_by_email(login_data.email)

    # Lógica de negocio: validaciones
    if not usuario:
        raise InvalidCredentialsError("Email o contraseña incorrectos")

    if not usuario.activo:
        raise InactiveUserError("El usuario está inactivo")

    # Delega a SecurityConfig: verificación de password
    if not security.verify_password(login_data.password, usuario.password_hash):
        raise InvalidCredentialsError("Email o contraseña incorrectos")

    # Lógica de negocio: preparación de datos para token
    token_data = {
        "sub": usuario.id,
        "email": usuario.email,
        "rol": usuario.rol.nombre
    }

    # Delega a SecurityConfig: generación de tokens
    access_token = security.create_access_token(token_data)
    refresh_token = security.create_refresh_token(token_data)

    # Lógica de negocio: transformación Model → DTO
    usuario_response = UsuarioResponse.model_validate(usuario)

    # Retorna DTO de respuesta
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        usuario=usuario_response
    )
```

**Análisis:**

- **Razón para cambiar:** Solo cambiaría si las reglas de negocio de login cambian
- **NO cambiaría por:** Cambios en BD, cambios en HTTP, cambios en algoritmo de hashing

**3. Repositories → Solo Acceso a Datos:**

```python
# Ubicación: usuario_repository.py:68-82
# Responsabilidad ÚNICA: Acceso a datos de usuarios

async def get_by_email(self, email: str) -> Optional[UsuarioModel]:
    """
    Responsabilidad: SOLO consultar la base de datos

    ✅ Hace:
    - Construir query SQL (vía SQLAlchemy)
    - Ejecutar query
    - Retornar Model o None
    - Eager loading de relaciones necesarias

    ❌ NO hace:
    - Validaciones de negocio (delegado a Service)
    - Transformación a DTOs (delegado a Service)
    - Manejo de excepciones de negocio (delegado a Service)
    - Hashing de passwords (delegado a SecurityConfig)
    """
    query = (
        select(UsuarioModel)
        .where(UsuarioModel.email == email)
        .options(selectinload(UsuarioModel.rol))  # Eager load para evitar N+1
    )
    result = await self.session.execute(query)
    return result.scalars().first()
```

**Análisis:**

- **Razón para cambiar:** Solo cambiaría si la estructura de la BD cambia o el ORM cambia
- **NO cambiaría por:** Cambios en reglas de negocio, cambios en HTTP, cambios en DTOs

**4. Models → Solo Estructura de Datos:**

```python
# Ubicación: usuario_model.py:15-52
# Responsabilidad ÚNICA: Definir estructura de la tabla 'usuarios'

class UsuarioModel(BaseModel, AuditMixin):
    """
    Responsabilidad: SOLO definir esquema de BD

    ✅ Hace:
    - Definir campos y tipos
    - Definir constraints (unique, nullable, etc.)
    - Definir relaciones (ForeignKey, relationship)
    - Definir índices

    ❌ NO hace:
    - Lógica de negocio
    - Validaciones complejas (Pydantic en schemas hace eso)
    - Queries (Repository hace eso)
    - Transformaciones (Service hace eso)
    """
    __tablename__ = "usuarios"

    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    nombre: Mapped[Optional[str]] = mapped_column(String(255))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
    id_rol: Mapped[str] = mapped_column(ForeignKey("roles.id"), nullable=False, index=True)

    # Relación (parte del esquema de BD)
    rol: Mapped["RolModel"] = relationship("RolModel", lazy="selectin")
```

**Análisis:**

- **Razón para cambiar:** Solo cambiaría si el esquema de BD cambia
- **NO cambiaría por:** Cambios en lógica de negocio, cambios en HTTP, cambios en validaciones

**Beneficios de SRP en el Proyecto:**

1. **Testing Simplificado:** Cada clase puede testearse aisladamente
2. **Mantenibilidad:** Cambios localizados, bajo acoplamiento
3. **Reutilización:** Componentes pueden usarse en diferentes contextos
4. **Comprensión:** Cada clase es pequeña y fácil de entender

---

#### **O - Open/Closed Principle (Principio Abierto/Cerrado)**

**Definición:** Las entidades de software deben estar abiertas para extensión pero cerradas para modificación.

**Interpretación:** Debes poder agregar nueva funcionalidad sin modificar código existente.

**Implementación en el Proyecto:**

**1. Jerarquía de Excepciones Extensible:**

```python
# Ubicación: base_exceptions.py:4-43
# Diseño base: Abierto para extensión, cerrado para modificación

class BusinessError(Exception):
    """
    Excepción base para todos los errores de negocio.

    Esta clase base está CERRADA para modificación:
    - No necesitamos cambiar esta clase para agregar nuevos tipos de error

    Está ABIERTA para extensión:
    - Podemos crear nuevas excepciones heredando de esta
    """
    def __init__(self, message: str, error_code: str | None = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ValidationError(BusinessError):
    """Hereda comportamiento base, se extiende para validación"""
    pass

class NotFoundError(BusinessError):
    """Hereda comportamiento base, se extiende para recursos no encontrados"""
    pass

class ConflictError(BusinessError):
    """Hereda comportamiento base, se extiende para conflictos"""
    pass
```

**Extensión sin Modificación:**

```python
# Ubicación: usuario_exceptions.py:7-70
# Archivo NUEVO creado para extender funcionalidad
# ✅ NO modificamos base_exceptions.py

class UsuarioValidationError(ValidationError):
    """
    Extiende ValidationError para errores específicos de usuario.

    Extensión (✅):
    - Agregamos comportamiento específico de usuario
    - Personalizamos mensaje y código de error por defecto

    NO modificación (✅):
    - ValidationError no cambió
    - BusinessError no cambió
    - Podemos agregar 100 excepciones más sin tocar las bases
    """
    def __init__(self, message: str, error_code: str = "USUARIO_VALIDATION_ERROR"):
        super().__init__(message, error_code)

class UsuarioNotFoundError(NotFoundError):
    """Extiende NotFoundError, sin modificar la base"""
    def __init__(self, message: str = "Usuario no encontrado"):
        super().__init__(message, "USUARIO_NOT_FOUND")
```

**Beneficio Concreto:**

Cuando necesitamos agregar excepciones para un nuevo dominio (ej: Pagos), simplemente creamos un nuevo archivo:

```python
# Archivo NUEVO: pago_exceptions.py
# ✅ NO tocamos base_exceptions.py
# ✅ NO tocamos usuario_exceptions.py

class PagoValidationError(ValidationError):
    def __init__(self, message: str, error_code: str = "PAGO_VALIDATION_ERROR"):
        super().__init__(message, error_code)

class PagoNotFoundError(NotFoundError):
    def __init__(self, message: str = "Pago no encontrado"):
        super().__init__(message, "PAGO_NOT_FOUND")
```

**2. Mixins Extensibles:**

```python
# Ubicación: audit_mixin.py:15-47
# Diseño: Abierto para extensión, cerrado para modificación

@declarative_mixin
class AuditMixin:
    """
    Mixin que proporciona campos de auditoría.

    CERRADO para modificación:
    - Esta clase no necesita cambiar cuando agregamos nuevos modelos

    ABIERTO para extensión:
    - Cualquier modelo puede heredar este comportamiento
    - Podemos crear nuevos mixins con otros comportamientos
    """
    @declared_attr
    def fecha_creacion(cls) -> Mapped[datetime]:
        return mapped_column(TIMESTAMP, server_default=func.now())

    @declared_attr
    def fecha_modificacion(cls) -> Mapped[datetime]:
        return mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
```

**Extensión en Uso:**

```python
# Modelo 1: Usuario extiende con AuditMixin
class UsuarioModel(BaseModel, AuditMixin):
    """✅ Extiende funcionalidad SIN modificar AuditMixin"""
    __tablename__ = "usuarios"
    # ... campos específicos

# Modelo 2: Producto extiende con AuditMixin
class ProductoModel(BaseModel, AuditMixin):
    """✅ Reutiliza AuditMixin SIN modificarlo"""
    __tablename__ = "productos"
    # ... campos específicos

# Modelo 3: Pedido extiende con MÚLTIPLES mixins
class PedidoModel(BaseModel, AuditMixin, SoftDeleteMixin):
    """✅ Combina múltiples mixins SIN modificar ninguno"""
    __tablename__ = "pedidos"
    # ... campos específicos
```

**3. Sistema de Enums Extensible:**

```python
# Ubicación: pedido_enums.py:6-13
# Diseño inicial: Enum con estados básicos

class EstadoPedido(str, Enum):
    """
    Estados de pedido.

    Si en el futuro necesitamos agregar estados (ej: EN_REVISION),
    podemos:

    ✅ Opción 1 (Extensión): Agregar valor al enum
    EN_REVISION = "en_revision"

    ✅ Opción 2 (Extensión): Crear enum extendido
    class EstadoPedidoExtendido(EstadoPedido):
        EN_REVISION = "en_revision"

    ❌ NO necesitamos: Modificar código que usa EstadoPedido
    """
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"
```

**Beneficios de OCP en el Proyecto:**

1. **Estabilidad:** Código existente no se rompe al agregar features
2. **Testing:** Tests existentes no necesitan modificarse
3. **Riesgo Reducido:** Cambios nuevos no introducen bugs en código viejo
4. **Escalabilidad:** Agregar 10 dominios nuevos no requiere tocar 100 archivos viejos

---

#### **L - Liskov Substitution Principle (Principio de Sustitución de Liskov)**

**Definición:** Los objetos de una clase derivada deben poder sustituir objetos de la clase base sin alterar el comportamiento del programa.

**Interpretación:** Las subclases deben cumplir el contrato de la clase base.

**Implementación en el Proyecto:**

**1. Herencia de Modelos:**

```python
# Ubicación: base_model.py:17-64
# Clase base con contrato definido

class BaseModel(DeclarativeBase):
    """
    Modelo base para todas las entidades de BD.

    CONTRATO:
    - Tiene campo 'id' (ULID de 26 caracteres)
    - Método to_dict() retorna Dict[str, Any]
    - Método from_dict() acepta Dict y retorna instancia
    - Método update_from_dict() actualiza desde Dict
    """
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=lambda: ulid.new().str
    )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la instancia a diccionario.

        CONTRATO:
        - Retorna Dict[str, Any]
        - Incluye todas las columnas de la tabla
        - Formato: {nombre_columna: valor}
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Crea instancia desde diccionario.

        CONTRATO:
        - Recibe Dict[str, Any]
        - Retorna instancia de la clase
        - Solo usa claves que corresponden a campos del modelo
        """
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})
```

**Subclase que CUMPLE el contrato:**

```python
# Ubicación: usuario_model.py:15, 50-57
# Subclase que respeta LSP

class UsuarioModel(BaseModel, AuditMixin):
    """
    ✅ CUMPLE LSP porque:
    - Tiene 'id' (heredado de BaseModel)
    - to_dict() funciona correctamente
    - from_dict() funciona correctamente
    - Puede usarse donde se espera BaseModel
    """
    __tablename__ = "usuarios"

    email: Mapped[Optional[str]] = mapped_column(String(255))
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))

    def to_dict(self) -> Dict[str, Any]:
        """
        Sobrescribe to_dict() pero RESPETA el contrato:
        - Retorna Dict[str, Any] ✅
        - Incluye todas las columnas ✅
        - Llama a super() para mantener comportamiento base ✅

        Agrega comportamiento (permitido en LSP):
        - Puede filtrar campos sensibles
        - Puede formatear datos
        """
        result = super().to_dict()
        # Podríamos filtrar password_hash aquí si quisiéramos
        return result
```

**Prueba de Sustitución (LSP):**

```python
def procesar_entidad(entidad: BaseModel) -> Dict[str, Any]:
    """
    Función que acepta BaseModel.

    Por LSP, debe funcionar con CUALQUIER subclase:
    - UsuarioModel ✅
    - ProductoModel ✅
    - PedidoModel ✅
    - Etc.
    """
    # Usa método del contrato
    return entidad.to_dict()

# ✅ Funciona con UsuarioModel
usuario = UsuarioModel(email="test@test.com")
dict_usuario = procesar_entidad(usuario)  # ✅ Funciona

# ✅ Funciona con ProductoModel
producto = ProductoModel(nombre="Ceviche")
dict_producto = procesar_entidad(producto)  # ✅ Funciona

# LSP se cumple: Cualquier subclase puede sustituir a BaseModel
```

**2. Jerarquía de Excepciones:**

```python
# Todas las excepciones específicas pueden sustituir a BusinessError

def handle_error(error: BusinessError) -> dict:
    """
    Maneja errores de negocio.

    Por LSP, acepta CUALQUIER excepción derivada:
    - ValidationError ✅
    - NotFoundError ✅
    - UsuarioNotFoundError ✅
    - ProductoValidationError ✅
    """
    return {
        "error": error.message,
        "code": error.error_code
    }

# ✅ Funciona con cualquier subclase
try:
    # ...
    raise UsuarioNotFoundError("Usuario no existe")
except BusinessError as e:
    response = handle_error(e)  # ✅ LSP se cumple
```

**Contraejemplo (Violación de LSP):**

```python
# ❌ VIOLACIÓN de LSP (ejemplo de qué NO hacer)

class BaseModel:
    def to_dict(self) -> Dict[str, Any]:
        """Retorna diccionario"""
        return {"id": self.id}

class MalUsuarioModel(BaseModel):
    def to_dict(self) -> List[str]:  # ❌ Cambia el tipo de retorno
        """Violación: retorna List en lugar de Dict"""
        return [self.id, self.email]  # ❌ Rompe el contrato

# Código que espera Dict romperá:
def procesar(entity: BaseModel):
    result = entity.to_dict()
    return result["id"]  # ❌ Explota con MalUsuarioModel porque retorna List

# LSP violado: La subclase NO puede sustituir a la base
```

**Beneficios de LSP en el Proyecto:**

1. **Polimorfismo Seguro:** Código genérico funciona con cualquier subclase
2. **Predictibilidad:** Subclases se comportan como se espera
3. **Testing:** Tests de la base se aplican a derivadas
4. **Confianza:** No hay sorpresas al usar herencia

---

Continuaré con los principios I y D, patrones de diseño, manejo de excepciones y el resto del documento en la próxima parte. ¿Quieres que continúe generando el archivo completo ahora?

