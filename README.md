# 🍽️ Restaurant Backend API

Sistema completo de gestión de restaurantes desarrollado con **Arquitectura en Capas (Layered Architecture)** usando FastAPI, SQLAlchemy y MySQL.

## 🏗️ Arquitectura

### Estructura en Capas

```
📁 app/
├── 🎨 presentation/     # Capa de Presentación
│   ├── api/            # Endpoints REST
│   ├── schemas/        # DTOs/Modelos Pydantic
│   ├── middleware/     # Middlewares
│   └── dependencies/   # Dependencias FastAPI
├── 🧠 business/        # Capa de Negocio
│   ├── services/       # Servicios de dominio
│   ├── validators/     # Validadores
│   ├── rules/          # Reglas de negocio
│   └── exceptions/     # Excepciones de dominio
├── 💾 data/            # Capa de Datos
│   ├── models/         # Modelos SQLAlchemy
│   ├── repositories/   # Repositorios
│   ├── database/       # Configuración BD
│   └── migrations/     # Migraciones Alembic
├── 🔄 shared/          # Capa Compartida
│   ├── entities/       # Entidades de dominio
│   ├── enums/          # Enumeraciones
│   ├── utils/          # Utilidades
│   └── constants/      # Constantes
└── ⚙️ config/          # Configuración
    └── settings/       # Configuración por entorno
```

## 🚀 Características

### 🍽️ Gestión de Carta Digital
- ✅ Categorías de productos organizadas
- ✅ Productos con precios y opciones personalizables
- ✅ Sistema de alérgenos con niveles de riesgo
- ✅ Búsqueda y filtros avanzados
- ✅ Productos destacados

### 🛒 Sistema de Carrito
- ✅ Carrito temporal por sesión de mesa
- ✅ Personalización de opciones por producto
- ✅ Cálculo automático de precios
- ✅ Validación de disponibilidad

### 🍴 Gestión de Pedidos
- ✅ Estados de pedido en tiempo real
- ✅ Sistema de prioridades
- ✅ Notas de personalización
- ✅ Trazabilidad completa

### 💳 Sistema de Pagos
- ✅ Múltiples métodos de pago (efectivo, tarjeta, Yape, Plin)
- ✅ División automática de cuenta
- ✅ Gestión de propinas
- ✅ Estados de transacción

### 🏪 Gestión de Mesas
- ✅ Códigos QR únicos por mesa
- ✅ Sesiones de mesa para múltiples comensales
- ✅ Control de ocupación y estados

## 📊 Modelo de Datos

### 20 Tablas Principales:

1. **rol** - Roles de usuario
2. **usuario** - Gestión de usuarios
3. **alergeno** - Catálogo de alérgenos
4. **categoria** - Categorías de productos
5. **producto** - Productos del menú
6. **producto_alergeno** - Relación productos-alérgenos
7. **tipo_opcion** - Tipos de opciones (nivel ají, acompañamiento, etc.)
8. **producto_opcion** - Opciones personalizables por producto
9. **mesa** - Mesas del restaurante
10. **sesiones_mesa** - Sesiones de comensales por mesa
11. **pedido** - Pedidos de clientes
12. **pedido_producto** - Items dentro de cada pedido
13. **pedido_opcion** - Opciones seleccionadas por item
14. **division_cuenta** - División de cuentas
15. **division_cuenta_detalle** - Detalle de división por persona
16. **pago** - Pagos realizados

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.11+ con FastAPI
- **Base de datos**: MySQL 8.0+
- **ORM**: SQLAlchemy 2.0+ (async)
- **Validación**: Pydantic v2
- **Migraciones**: Alembic
- **Autenticación**: JWT (python-jose)
- **Cache**: Redis
- **Contenedores**: Docker & Docker Compose
- **Testing**: pytest + pytest-asyncio

## 📦 Instalación y Configuración

### Prerequisitos

- Python 3.11+
- Docker & Docker Compose
- Git

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd restaurant-backend
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
pip install -r requirements/development.txt

# Configurar base de datos
# Asegúrate de tener MySQL ejecutándose

# Ejecutar migraciones
alembic upgrade head

# Ejecutar aplicación
uvicorn main:app --reload
```

## 🌐 Endpoints de la API

### 📋 Menu Management

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

### 🍴 Order Management

```http
GET    /api/v1/pedidos/               # Listar pedidos
POST   /api/v1/pedidos/               # Crear pedido
GET    /api/v1/pedidos/{id}           # Obtener pedido específico
PUT    /api/v1/pedidos/{id}/estado    # Cambiar estado de pedido

POST   /api/v1/carrito/add-item       # Agregar item al carrito
GET    /api/v1/carrito/{session_id}   # Obtener carrito por sesión
```

### 💳 Payment Management

```http
POST   /api/v1/pagos/                 # Procesar pago
GET    /api/v1/pagos/pedido/{id}      # Pagos por pedido
POST   /api/v1/pagos/division         # Dividir cuenta
```

### 🏪 Table Management

```http
GET    /api/v1/mesas/                 # Listar mesas
POST   /api/v1/mesas/{id}/session     # Crear sesión de mesa
GET    /api/v1/mesas/{id}/qr          # Generar QR de mesa
```

## 📚 Documentación de la API

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/unit/business/
pytest tests/integration/
```

## 🚀 Despliegue

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

## 📊 Monitoreo y Logs

- **Health Check**: `GET /health`
- **Logs estructurados**: JSON format en producción
- **Métricas**: Integración con Sentry (configurado)

## 🔒 Seguridad

- ✅ Autenticación JWT
- ✅ Validación de entrada con Pydantic
- ✅ Manejo seguro de errores
- ✅ Rate limiting (configurable)
- ✅ CORS configurado
- ✅ Sanitización de datos

## 🤝 Contribuir

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico o preguntas:

- 📧 Email: desarrollo@restaurante.com
- 📝 Issues: GitHub Issues
- 📖 Wiki: GitHub Wiki

---

**Desarrollado con ❤️ usando Arquitectura en Capas y las mejores prácticas de desarrollo**