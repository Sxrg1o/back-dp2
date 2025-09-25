# API de Gestión de Menú y Carta

Sistema completo de gestión de menú para restaurantes con arquitectura modular basada en agentes.

## 🏗️ Arquitectura

El sistema está organizado en módulos especializados (agentes):

- **Models**: DTOs y modelos de dominio
- **Data**: Catálogos y datos en memoria
- **Services**: Lógica de negocio
- **Main**: Endpoints y API REST

## 📋 Características

### Modelos de Dominio
- **Item**: Clase base abstracta para platos y bebidas
- **Plato**: Hereda de Item, incluye peso y tipo (ENTRADA, FONDO, POSTRE)
- **Bebida**: Hereda de Item, incluye litros y contenido alcohólico
- **Ingrediente**: Con información de alérgenos
- **GrupoPersonalizacion**: Para opciones adicionales
- **Opcion**: Opciones de personalización con precios

### Funcionalidades
- ✅ Gestión completa de menú
- ✅ Filtros por categoría, alérgenos, tipo
- ✅ Búsqueda por nombre
- ✅ Validación de disponibilidad
- ✅ Estadísticas del menú
- ✅ API REST completa con documentación

## 🚀 Instalación y Uso

### Opción 1: Setup automático (Recomendado)
```bash
# Ejecutar script de configuración automática
python setup.py
```

### Opción 2: Setup manual
#### 1. Crear entorno virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

#### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecución Local
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Verificar instalación
```bash
# Verificar que el servidor esté funcionando
curl http://127.0.0.1:8000/health
# o visitar en el navegador: http://127.0.0.1:8000/docs
```

### 5. Desactivar entorno virtual
```bash
deactivate
```

### Despliegue en Render
1. Sube el código a GitHub
2. En Render: New → Web Service
3. Runtime: Python
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 🐳 Dockerización

### Opción 1: Docker Compose (Recomendado)
```bash
# Desarrollo con hot reload
docker-compose up --build

# Producción
docker-compose -f docker-compose.prod.yml up --build -d
```

### Opción 2: Script de inicio
```bash
# Hacer ejecutable (Linux/Mac)
chmod +x scripts/docker-start.sh

# Desarrollo
./scripts/docker-start.sh dev

# Producción
./scripts/docker-start.sh prod

# Ver logs
./scripts/docker-start.sh logs

# Detener
./scripts/docker-start.sh stop

# Limpiar
./scripts/docker-start.sh clean
```

### Opción 3: Docker directo
```bash
# Construir imagen
docker build -t menu-api .

# Ejecutar contenedor
docker run -p 8000:8000 menu-api

# Ejecutar con hot reload (desarrollo)
docker run -p 8000:8000 -v $(pwd):/app menu-api uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### URLs de acceso
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📚 Endpoints Principales

### Items
- `GET /api/menu/items` - Todos los items
- `GET /api/menu/items/{id}` - Item específico
- `GET /api/menu/items/disponibles` - Solo disponibles
- `GET /api/menu/items/buscar?nombre=...` - Búsqueda

### Platos
- `GET /api/menu/platos` - Todos los platos
- `GET /api/menu/platos/entradas` - Entradas
- `GET /api/menu/platos/principales` - Platos principales
- `GET /api/menu/platos/postres` - Postres
- `GET /api/menu/platos/tipo/{tipo}` - Por tipo

### Bebidas
- `GET /api/menu/bebidas` - Todas las bebidas
- `GET /api/menu/bebidas/sin-alcohol` - Sin alcohol
- `GET /api/menu/bebidas/con-alcohol` - Con alcohol

### Ingredientes
- `GET /api/menu/ingredientes` - Todos los ingredientes
- `GET /api/menu/ingredientes/{id}` - Ingrediente específico
- `GET /api/menu/ingredientes/buscar?nombre=...` - Búsqueda

### Filtros
- `GET /api/menu/filtrar/categoria?categoria=...` - Por categoría
- `GET /api/menu/filtrar/alergenos?alergenos=...` - Con alérgenos
- `GET /api/menu/filtrar/sin-alergenos?alergenos=...` - Sin alérgenos

### Menú Completo
- `GET /api/menu/completo` - Menú organizado
- `GET /api/menu/estadisticas` - Estadísticas

### Acompañamientos
- `GET /api/menu/items/{id}/acompanamientos` - Acompañamientos de un item específico
- `GET /api/menu/acompanamientos` - Todos los acompañamientos disponibles

### Validación
- `GET /api/menu/validar-disponibilidad/{id}?cantidad=...` - Validar stock de un item
- `POST /api/menu/validar-disponibilidad-multiple` - Validar stock de múltiples items

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
python tests/run_tests.py

# Tests por módulo
python tests/run_tests.py --module menu
python tests/run_tests.py --module pedidos

# Con scripts del sistema
scripts\run-tests.bat          # Windows
./scripts/run-tests.sh         # Linux/Mac

# Con pytest
pytest tests/ -v
pytest tests/ --cov=app        # Con coverage
```

### Estructura de Tests
- **Menu y Carta**: 27 tests organizados por categorías
- **Gestión de Pedidos**: 13 tests con validaciones completas
- **Runner centralizado**: Ejecución modular y reportes detallados

Ver detalles en: [tests/README.md](tests/README.md)

## 🔍 Documentación

Una vez ejecutado, visita:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📊 Datos de Ejemplo

El sistema incluye datos de ejemplo:
- 5 platos (entradas, principales, postres)
- 3 bebidas (con y sin alcohol)
- 15 ingredientes con información de alérgenos
- Grupos de personalización para acompañamientos y salsas

## 🛠️ Extensión Futura

Para evolucionar a una arquitectura más compleja:
1. Añadir base de datos (SQLAlchemy + Alembic)
2. Separar servicios en microservicios
3. Implementar autenticación y autorización
4. Añadir sistema de órdenes completo
5. Integrar con sistemas de pago
