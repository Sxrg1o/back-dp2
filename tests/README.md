# Tests de la API - Sistema de Gestión de Restaurante

Este directorio contiene los tests organizados por módulos para verificar el funcionamiento de todos los endpoints de la API.

## Estructura Modular

```
tests/
├── __init__.py
├── requirements-test.txt  # Dependencias para tests
├── README.md             # Este archivo
├── menu_y_carta/         # Tests del módulo Menu y Carta
│   ├── __init__.py
│   ├── test_menu_y_carta_all_endpoints.py
│   ├── run_tests.py
│   └── README.md
└── gestion_pedidos/      # Tests del módulo Gestión de Pedidos
    ├── __init__.py
    ├── test_pedidos_endpoints.py
    ├── run_tests.py
    └── README.md
```

## Cómo ejecutar los tests

### Por módulo (Recomendado)
```bash
# Tests del módulo Menu y Carta
python tests/menu_y_carta/run_tests.py

# Tests del módulo Gestión de Pedidos
python tests/gestion_pedidos/run_tests.py

# O ejecutar directamente
python tests/menu_y_carta/test_menu_y_carta_all_endpoints.py
python tests/gestion_pedidos/test_pedidos_endpoints.py
```

### Con pytest
```bash
# Todos los tests
pytest tests/ -v

# Solo tests del módulo Menu y Carta
pytest tests/menu_y_carta/ -v

# Solo tests del módulo Gestión de Pedidos
pytest tests/gestion_pedidos/ -v
```

## Módulos de Tests

### 🍽️ Menu y Carta (27 tests)
Tests completos para el módulo de gestión de menú y carta:
- Endpoints básicos (root, health)
- Gestión de items, platos y bebidas
- Filtros y búsquedas
- Validaciones de disponibilidad
- Acompañamientos y personalizaciones

Ver detalles en: [tests/menu_y_carta/README.md](menu_y_carta/README.md)

### 🍽️ Gestión de Pedidos (13 tests)
Tests completos para el módulo de gestión de pedidos:
- Gestión de órdenes y estados
- Gestión de meseros y mesas
- Validación de disponibilidad
- Estadísticas y reportes
- Integración con catálogo de menú

Ver detalles en: [tests/gestion_pedidos/README.md](gestion_pedidos/README.md)

### 📊 Reportes y Analytics (Próximamente)
Tests para el módulo de reportes (cuando se implemente)

## Dependencias

Los tests requieren las siguientes dependencias adicionales:
- `pytest` - Framework de testing
- `httpx` - Cliente HTTP para tests
- `requests` - Cliente HTTP alternativo

## Notas

- Los tests usan `TestClient` de FastAPI para simular requests HTTP
- Todos los tests verifican códigos de estado HTTP y estructura de respuestas
- Los tests incluyen validaciones tanto para casos exitosos como de error
- El script `run_tests.py` instala automáticamente las dependencias necesarias

## Solución de problemas

### Error de importación
Si obtienes errores de importación, asegúrate de ejecutar los tests desde el directorio raíz del proyecto:
```bash
cd /ruta/al/proyecto
python tests/run_tests.py
```

### Dependencias faltantes
Si faltan dependencias, instálalas manualmente:
```bash
pip install -r tests/requirements-test.txt
```

### API no disponible
Asegúrate de que la API esté funcionando antes de ejecutar los tests. Los tests usan `TestClient` que no requiere que la API esté ejecutándose, pero las importaciones deben funcionar correctamente.
