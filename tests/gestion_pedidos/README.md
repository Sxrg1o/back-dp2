# Tests del Módulo Gestión de Pedidos

Este directorio contiene los tests específicos para el módulo de **Gestión de Pedidos** de la API.

## Estructura

```
tests/gestion_pedidos/
├── __init__.py
├── test_pedidos_endpoints.py  # Tests principales del módulo
├── run_tests.py              # Script para ejecutar tests del módulo
└── README.md                 # Este archivo
```

## Cómo ejecutar los tests del módulo

### Opción 1: Script específico del módulo (Recomendado)
```bash
# Desde el directorio raíz del proyecto
python tests/gestion_pedidos/run_tests.py
```

### Opción 2: Ejecutar directamente
```bash
# Desde el directorio raíz del proyecto
python tests/gestion_pedidos/test_pedidos_endpoints.py
```

### Opción 3: Con pytest
```bash
# Desde el directorio raíz del proyecto
pytest tests/gestion_pedidos/ -v
```

## Tests incluidos (13 tests)

### Gestión de Órdenes
- ✅ Crear nueva orden (`POST /api/pedidos/ordenes`)
- ✅ Obtener todas las órdenes (`GET /api/pedidos/ordenes`)
- ✅ Obtener orden por ID (`GET /api/pedidos/ordenes/{id}`)
- ✅ Agregar item a orden (`POST /api/pedidos/ordenes/{id}/items`)
- ✅ Cambiar estado de orden (`PUT /api/pedidos/ordenes/{id}/estado`)
- ✅ Validar disponibilidad de orden (`GET /api/pedidos/ordenes/{id}/validar-disponibilidad`)

### Gestión de Meseros
- ✅ Obtener todos los meseros (`GET /api/pedidos/meseros`)
- ✅ Crear mesero (`POST /api/pedidos/meseros`)
- ✅ Obtener mesero por ID (`GET /api/pedidos/meseros/{id}`)

### Gestión de Mesas
- ✅ Obtener todas las mesas (`GET /api/pedidos/mesas`)
- ✅ Obtener mesas disponibles (`GET /api/pedidos/mesas/disponibles`)
- ✅ Crear grupo de mesa (`POST /api/pedidos/mesas`)
- ✅ Obtener mesa por ID (`GET /api/pedidos/mesas/{id}`)

### Estadísticas y Reportes
- ✅ Obtener estadísticas de pedidos (`GET /api/pedidos/estadisticas`)
- ✅ Obtener resumen de órdenes (`GET /api/pedidos/resumen`)

## Módulos relacionados

Este módulo de tests está asociado con:
- `app/models/gestion_pedidos/` - Modelos del módulo
- `app/services/pedidos_service.py` - Servicios de pedidos
- `app/main.py` - Endpoints de la API
- `app/models/menu_y_carta/` - Dependencia del catálogo de menú

## Notas específicas del módulo

- Los tests verifican la funcionalidad completa del sistema de gestión de pedidos
- Incluye validación de órdenes, items, meseros y mesas
- Verifica transiciones de estado de órdenes
- Valida disponibilidad de items del menú
- Maneja casos de error y validaciones de negocio
- **Nota**: Cliente y Cuenta están en otros módulos (estancia_cliente y division_de_cuenta)

## Estados de Órdenes

El módulo maneja los siguientes estados de órdenes:
- `EN_COLA` - Orden en cola de espera
- `EN_PREPARACION` - Orden siendo preparada
- `LISTO_PARA_SALIR` - Orden lista para entregar
- `DESPACHADO` - Orden entregada
- `CANCELADO` - Orden cancelada

## Tipos de Mesas

El módulo soporta diferentes tipos de mesas:
- `INDIVIDUAL` - Mesa para una persona
- `PAREJA` - Mesa para dos personas
- `FAMILIAR` - Mesa para familias
- `GRUPO` - Mesa para grupos grandes
- `VIP` - Mesa VIP
- `TERRAZA` - Mesa en terraza

## Solución de problemas

### Error de importación
Si obtienes errores de importación, asegúrate de ejecutar desde el directorio raíz:
```bash
cd /ruta/al/proyecto
python tests/gestion_pedidos/run_tests.py
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

## Integración con otros módulos

Este módulo está diseñado para integrarse con:
- **Menu y Carta**: Para obtener items del menú
- **Estancia Cliente** (futuro): Para gestión de clientes
- **División de Cuenta** (futuro): Para división de cuentas
