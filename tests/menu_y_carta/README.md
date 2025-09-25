# Tests del Módulo Menu y Carta

Este directorio contiene los tests específicos para el módulo de **Menu y Carta** de la API.

## Estructura

```
tests/menu_y_carta/
├── __init__.py
├── test_menu_y_carta_all_endpoints.py  # Tests principales del módulo
├── run_tests.py                        # Script para ejecutar tests del módulo
└── README.md                           # Este archivo
```

## Cómo ejecutar los tests del módulo

### Opción 1: Script específico del módulo (Recomendado)
```bash
# Desde el directorio raíz del proyecto
python tests/menu_y_carta/run_tests.py
```

### Opción 2: Ejecutar directamente
```bash
# Desde el directorio raíz del proyecto
python tests/menu_y_carta/test_menu_y_carta_all_endpoints.py
```

### Opción 3: Con pytest
```bash
# Desde el directorio raíz del proyecto
pytest tests/menu_y_carta/ -v
```

## Tests incluidos (27 tests)

### Endpoints básicos
- ✅ Root endpoint (`/`)
- ✅ Health check (`/health`)

### Endpoints de Items
- ✅ Obtener todos los items (`/api/menu/items`)
- ✅ Obtener item por ID (`/api/menu/items/{id}`)
- ✅ Obtener items disponibles (`/api/menu/items/disponibles`)
- ✅ Buscar items por nombre (`/api/menu/items/buscar`)

### Endpoints de Platos
- ✅ Obtener todos los platos (`/api/menu/platos`)
- ✅ Obtener entradas (`/api/menu/platos/entradas`)
- ✅ Obtener platos principales (`/api/menu/platos/principales`)
- ✅ Obtener postres (`/api/menu/platos/postres`)
- ✅ Obtener platos por tipo (`/api/menu/platos/tipo/{tipo}`)

### Endpoints de Bebidas
- ✅ Obtener todas las bebidas (`/api/menu/bebidas`)
- ✅ Obtener bebidas sin alcohol (`/api/menu/bebidas/sin-alcohol`)
- ✅ Obtener bebidas con alcohol (`/api/menu/bebidas/con-alcohol`)

### Endpoints de Ingredientes
- ✅ Obtener todos los ingredientes (`/api/menu/ingredientes`)
- ✅ Obtener ingrediente por ID (`/api/menu/ingredientes/{id}`)
- ✅ Buscar ingredientes por nombre (`/api/menu/ingredientes/buscar`)

### Endpoints de Filtros
- ✅ Filtrar por categoría (`/api/menu/filtrar/categoria`)
- ✅ Filtrar por alérgenos (`/api/menu/filtrar/alergenos`)
- ✅ Filtrar sin alérgenos (`/api/menu/filtrar/sin-alergenos`)
- ✅ Obtener items por ingrediente (`/api/menu/items/ingrediente/{id}`)

### Endpoints de Menú Completo
- ✅ Obtener menú completo (`/api/menu/completo`)
- ✅ Obtener estadísticas (`/api/menu/estadisticas`)

### Endpoints de Acompañamientos
- ✅ Obtener acompañamientos de item (`/api/menu/items/{id}/acompanamientos`)
- ✅ Obtener todos los acompañamientos (`/api/menu/acompanamientos`)

### Endpoints de Validación
- ✅ Validar disponibilidad (`/api/menu/validar-disponibilidad/{id}`)
- ✅ Validar disponibilidad múltiple (`/api/menu/validar-disponibilidad-multiple`)

## Módulos relacionados

Este módulo de tests está asociado con:
- `app/models/menu_y_carta/` - Modelos del módulo
- `app/data/menu_data.py` - Datos del menú
- `app/services/menu_service.py` - Servicios del menú
- `app/main.py` - Endpoints de la API

## Notas específicas del módulo

- Los tests verifican la funcionalidad completa del sistema de menú y carta
- Incluye validación de platos, bebidas, ingredientes y personalizaciones
- Verifica filtros por alérgenos, categorías y disponibilidad
- Valida la integridad de los datos y respuestas JSON
- Maneja casos de error y validaciones de negocio

## Solución de problemas

### Error de importación
Si obtienes errores de importación, asegúrate de ejecutar desde el directorio raíz:
```bash
cd /ruta/al/proyecto
python tests/menu_y_carta/run_tests.py
```

### Dependencias faltantes
Asegúrate de tener el entorno virtual activado:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### API no disponible
Los tests usan `TestClient` que no requiere que la API esté ejecutándose, pero las importaciones deben funcionar correctamente.
