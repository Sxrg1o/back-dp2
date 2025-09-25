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

### Validación
- `GET /api/menu/validar-disponibilidad/{id}?cantidad=...` - Validar stock

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
