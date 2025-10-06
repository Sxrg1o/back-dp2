# Restaurant Backend API

Sistema completo de gestión de restaurantes desarrollado con **Clean Architecture** usando FastAPI, SQLAlchemy y MySQL.

## Arquitectura

### Estructura del Proyecto

```
proyecto-rpa/
├── src/
│   ├── api/
│   │   ├── controllers/     # FastAPI routers (endpoints REST)
│   │   └── schemas/         # Pydantic models (DTOs)
│   ├── business_logic/      # Lógica de negocio
│   │   ├── auth/           # Servicios de autenticación
│   │   ├── menu/           # Servicios de menú
│   │   ├── exceptions/     # Excepciones personalizadas
│   │   └── validators/     # Validadores de negocio
│   ├── repositories/        # Acceso a datos (patrón Repository)
│   │   ├── auth/
│   │   └── menu/
│   ├── models/              # SQLAlchemy models (entidades BD)
│   │   ├── auth/
│   │   ├── menu/
│   │   ├── mesas/
│   │   ├── pedidos/
│   │   └── pagos/
│   ├── core/
│   │   ├── config.py        # Configuración centralizada
│   │   ├── database.py      # Gestión de BD
│   │   ├── dependencies.py  # Dependencias y middleware
│   │   ├── enums/          # Enumeraciones del sistema
│   │   └── utils/          # Utilidades compartidas
│   └── main.py              # Punto de entrada FastAPI
├── tests/
│   ├── unit/               # Tests unitarios
│   ├── integration/        # Tests de integración
│   └── e2e/                # Tests end-to-end
├── docker/
│   ├── docker-compose.yml  # Orquestación de servicios
│   ├── mysql/              # Configuración MySQL
│   └── nginx/              # Configuración Nginx
├── requirements.txt         # Dependencias Python
├── Dockerfile              # Imagen Docker
└── README.md
```

### Capas de la Arquitectura

#### API Layer (`src/api/`)
- **Controllers**: Endpoints REST que manejan HTTP requests/responses
- **Schemas**: DTOs (Data Transfer Objects) con validación Pydantic

#### Business Layer (`src/business_logic/`)
- Lógica de negocio pura
- Validaciones complejas
- Reglas de dominio
- Excepciones personalizadas

#### Data Layer (`src/repositories/` + `src/models/`)
- **Models**: Entidades de base de datos (SQLAlchemy)
- **Repositories**: Patrón Repository para acceso a datos

#### Core Layer (`src/core/`)
- Configuración global
- Gestión de base de datos
- Middleware y dependencias
- Utilidades compartidas

## Características

### Gestión de Carta Digital
- Categorías de productos organizadas
- Productos con precios y opciones personalizables
- Sistema de alérgenos con niveles de riesgo
- Búsqueda y filtros avanzados
- Productos destacados

### Sistema de Carrito
- Carrito temporal por sesión de mesa
- Personalización de opciones por producto
- Cálculo automático de precios
- Validación de disponibilidad

### Gestión de Pedidos
- Estados de pedido en tiempo real
- Sistema de prioridades
- Notas de personalización
- Trazabilidad completa

### Sistema de Pagos
- Múltiples métodos de pago (efectivo, tarjeta, Yape, Plin)
- División automática de cuenta
- Gestión de propinas
- Estados de transacción

### Gestión de Mesas
- Códigos QR únicos por mesa
- Sesiones de mesa para múltiples comensales
- Control de ocupación y estados

## Modelo de Datos

### Módulos Principales:

1. **Autenticación** (`auth`)
   - `rol` - Roles de usuario
   - `usuario` - Gestión de usuarios

2. **Menú** (`menu`)
   - `alergeno` - Catálogo de alérgenos
   - `categoria` - Categorías de productos
   - `producto` - Productos del menú
   - `producto_alergeno` - Relación productos-alérgenos
   - `tipo_opcion` - Tipos de opciones
   - `producto_opcion` - Opciones personalizables

3. **Mesas** (`mesas`)
   - `mesa` - Mesas del restaurante
   - `sesiones_mesa` - Sesiones de comensales

4. **Pedidos** (`pedidos`)
   - `pedido` - Pedidos de clientes
   - `pedido_producto` - Items dentro de cada pedido
   - `pedido_opcion` - Opciones seleccionadas por item

5. **Pagos** (`pagos`)
   - `division_cuenta` - División de cuentas
   - `division_cuenta_detalle` - Detalle de división
   - `pago` - Pagos realizados

## Stack Tecnológico

- **Backend**: Python 3.11+ con FastAPI
- **Base de datos**: MySQL 8.0+
- **ORM**: SQLAlchemy 2.0+ (async)
- **Validación**: Pydantic v2
- **Migraciones**: Alembic
- **Autenticación**: JWT (python-jose)
- **Cache**: Redis
- **Contenedores**: Docker & Docker Compose
- **Testing**: pytest + pytest-asyncio

## Instalación y Configuración

### Prerequisitos

- Python 3.11+
- Docker & Docker Compose
- Git

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd back-dp2
```

### 2. Configurar Variables de Entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 3. Ejecutar con Docker (Recomendado)

```bash
# Construir y ejecutar todos los servicios
docker-compose -f docker/docker-compose.yml up -d

# Ver logs
docker-compose -f docker/docker-compose.yml logs -f restaurant-api
```

### 4. Instalación Local (Desarrollo)

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
# Asegúrate de tener MySQL ejecutándose

# Ejecutar migraciones
alembic upgrade head

# Ejecutar aplicación
uvicorn src.main:app --reload
```

## Endpoints de la API

### Menu Management

```http
GET    /api/v1/productos/              # Listar productos con filtros
POST   /api/v1/productos/              # Crear producto
GET    /api/v1/productos/{id}          # Obtener producto específico
PUT    /api/v1/productos/{id}          # Actualizar producto
DELETE /api/v1/productos/{id}          # Eliminar producto

GET    /api/v1/productos/featured      # Productos destacados
GET    /api/v1/productos/category/{id} # Productos por categoría
POST   /api/v1/productos/calculate-price # Calcular precio con opciones

GET    /api/v1/categorias/             # Listar categorías
POST   /api/v1/categorias/             # Crear categoría

GET    /api/v1/alergenos/              # Listar alérgenos
POST   /api/v1/alergenos/              # Crear alérgeno
```

### Order Management

```http
GET    /api/v1/pedidos/               # Listar pedidos
POST   /api/v1/pedidos/               # Crear pedido
GET    /api/v1/pedidos/{id}           # Obtener pedido específico
PUT    /api/v1/pedidos/{id}/estado    # Cambiar estado de pedido

POST   /api/v1/carrito/add-item       # Agregar item al carrito
GET    /api/v1/carrito/{session_id}   # Obtener carrito por sesión
```

### Payment Management

```http
POST   /api/v1/pagos/                 # Procesar pago
GET    /api/v1/pagos/pedido/{id}      # Pagos por pedido
POST   /api/v1/pagos/division         # Dividir cuenta
```

### Table Management

```http
GET    /api/v1/mesas/                 # Listar mesas
POST   /api/v1/mesas/{id}/session     # Crear sesión de mesa
GET    /api/v1/mesas/{id}/qr          # Generar QR de mesa
```

## Documentación de la API

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=src

# Tests específicos
pytest tests/unit/business_logic/
pytest tests/integration/
```

## Despliegue

### Variables de Entorno de Producción

```env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=mysql+aiomysql://user:pass@host:3306/db
SECRET_KEY=your-super-secret-production-key
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

### Docker Production

```bash
# Construir imagen
docker build -t restaurant-backend .

# Ejecutar contenedor
docker run -d \
  --name restaurant-api \
  -p 8000:8000 \
  --env-file .env.production \
  restaurant-backend
```

## Monitoreo y Logs

- **Health Check**: `GET /health`
- **Logs estructurados**: JSON format en producción
- **Métricas**: Integración con Sentry (configurado)

## Seguridad

- Autenticación JWT
- Validación de entrada con Pydantic
- Manejo seguro de errores
- Rate limiting (configurable)
- CORS configurado
- Sanitización de datos

## Contribuir

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas:

- Email: desarrollo@restaurante.com
- Issues: GitHub Issues

---

**Desarrollado usando Clean Architecture y las mejores prácticas de desarrollo**
