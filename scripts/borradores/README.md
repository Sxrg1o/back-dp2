# Scripts de Prueba - Borradores

Esta carpeta contiene scripts de prueba y borradores para validar diferentes flujos del sistema de pedidos.

## Scripts Disponibles

### 1. `test_pedidos_flow.py`

Script completo que prueba el flujo de pedidos de principio a fin.

#### ¿Qué hace?

Este script simula el proceso completo de un pedido en el restaurante:

1. **Selecciona una mesa** - Obtiene una mesa existente o crea una nueva
2. **Crea un nuevo pedido** - Genera un pedido con número único
3. **Obtiene productos disponibles** - Consulta los productos del menú
4. **Obtiene opciones disponibles** - Consulta los tipos de opciones y sus valores
5. **Agrega productos al pedido** - Inserta items de productos en el pedido
6. **Selecciona opciones** - Asocia opciones a cada producto
7. **Calcula totales** - Actualiza subtotales, impuestos y total
8. **Confirma el pedido** - Cambia el estado del pedido a "confirmado"

#### Estructura del Flujo

```
Mesa
  ↓
Pedido (estado: PENDIENTE)
  ↓
Productos del Pedido
  ├─ Producto 1
  │  ├─ Opción 1 (precio adicional)
  │  └─ Opción 2 (precio adicional)
  └─ Producto 2
     ├─ Opción 1 (precio adicional)
     └─ Opción 2 (precio adicional)
  ↓
Actualizar Totales
  ├─ Subtotal = suma de todos los items
  ├─ Impuestos = subtotal * 18%
  ├─ Descuentos = 0
  └─ Total = subtotal + impuestos - descuentos
  ↓
Confirmar Pedido (estado: CONFIRMADO)
```

#### Cómo Ejecutar

```bash
# Desde la raíz del proyecto
python -m scripts.borradores.test_pedidos_flow
```

#### Requisitos

- Base de datos configurada (SQLite o MySQL según `DATABASE_URL`)
- Datos de prueba precargados (mesas, productos, opciones)
- Variables de entorno configuradas en `.env`

#### Salida Esperada

El script mostrará:

```
================================================================================
🍽️  FLUJO COMPLETO DE PEDIDOS - PRUEBA
================================================================================

📍 PASO 1: Seleccionando una mesa...
   ✓ Mesa seleccionada: 1 (ID: ...)

📋 PASO 2: Creando un nuevo pedido...
   ✓ Pedido creado: 20250129-M1-001 (ID: ...)
   - Estado: pendiente
   - Total inicial: S/. 0.00

... (más detalles del proceso)

📊 PASO 8: Obteniendo detalles finales del pedido...

================================================================================
📋 RESUMEN FINAL DEL PEDIDO
================================================================================
Número de pedido: 20250129-M1-001
Mesa: 1
Estado: confirmado
Subtotal: S/. 150.00
Impuestos: S/. 27.00
Descuentos: S/. 0.00
Total: S/. 177.00
...
================================================================================

✅ ¡Flujo de pedidos completado exitosamente!
```

## Modelos Utilizados

El script interactúa con los siguientes modelos:

- **MesaModel** - Representa las mesas del restaurante
- **PedidoModel** - Representa un pedido completo
- **PedidoProductoModel** - Items/productos dentro de un pedido
- **PedidoOpcionModel** - Opciones seleccionadas para cada producto
- **ProductoModel** - Productos del menú
- **ProductoOpcionModel** - Opciones disponibles para productos
- **TipoOpcionModel** - Tipos/categorías de opciones

## Tablas de Base de Datos

El script utiliza las siguientes tablas:

- `mesas` - Mesas del restaurante
- `pedido` - Pedidos
- `pedido_producto` - Items de pedidos
- `pedido_opcion` - Opciones de items
- `producto` - Productos del menú
- `producto_opcion` - Opciones de productos
- `tipo_opcion` - Tipos de opciones

## Notas Importantes

1. **Datos de Prueba**: Asegúrate de que haya datos precargados en la base de datos (mesas, productos, opciones)
2. **Transacciones**: El script usa transacciones de SQLAlchemy para garantizar consistencia
3. **IDs ULID**: Los IDs se generan automáticamente usando ULID
4. **Cálculos**: Los totales se calculan automáticamente basados en los precios de productos y opciones
5. **Estados**: El pedido comienza en estado PENDIENTE y termina en CONFIRMADO

## Troubleshooting

### Error: "No hay productos disponibles"
- Asegúrate de ejecutar primero `python -m scripts.seed_cevicheria_data`

### Error: "No se puede conectar a la base de datos"
- Verifica que `DATABASE_URL` esté configurada en `.env`
- Verifica que la base de datos esté disponible

### Error: "Foreign key constraint failed"
- Asegúrate de que las mesas, productos y opciones existan en la base de datos

## Extensiones Futuras

Puedes extender este script para:

- Probar diferentes combinaciones de opciones
- Simular múltiples pedidos simultáneamente
- Probar cambios de estado del pedido
- Validar cálculos de totales con descuentos
- Probar cancelación de pedidos
- Simular pedidos con múltiples productos
