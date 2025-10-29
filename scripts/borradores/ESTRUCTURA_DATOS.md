# Estructura de Datos - Sistema de Pedidos

Este documento describe la estructura de datos utilizada en el sistema de pedidos del restaurante.

## Diagrama de Relaciones

```
┌─────────────────┐
│     MESAS       │
│   (mesas)       │
├─────────────────┤
│ id (PK)         │
│ numero          │
│ capacidad       │
│ ubicacion       │
│ activo          │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────────────┐
│      PEDIDOS            │
│   (pedido)              │
├─────────────────────────┤
│ id (PK)                 │
│ id_mesa (FK) ────┐      │
│ numero_pedido    │      │
│ estado           │      │
│ subtotal         │      │
│ impuestos        │      │
│ descuentos       │      │
│ total            │      │
│ notas_cliente    │      │
│ notas_cocina     │      │
│ fecha_confirmado │      │
│ fecha_creacion   │      │
└────────┬─────────┘      │
         │                │
         │ 1:N            │
         │                │
         ▼                │
┌─────────────────────────┐
│  PEDIDO_PRODUCTO        │
│ (pedido_producto)       │
├─────────────────────────┤
│ id (PK)                 │
│ id_pedido (FK) ──┐      │
│ id_producto (FK)─┼──┐   │
│ cantidad         │  │   │
│ precio_unitario  │  │   │
│ precio_opciones  │  │   │
│ subtotal         │  │   │
│ notas_personali- │  │   │
│   zacion         │  │   │
└────────┬─────────┘  │   │
         │            │   │
         │ 1:N        │   │
         │            │   │
         ▼            │   │
┌─────────────────────────┐
│   PEDIDO_OPCION         │
│  (pedido_opcion)        │
├─────────────────────────┤
│ id (PK)                 │
│ id_pedido_producto (FK) │
│ id_producto_opcion (FK) │
│ precio_adicional        │
│ fecha_creacion          │
└─────────────────────────┘
         ▲
         │ N:1
         │
         └─────────────────┐
                           │
                    ┌──────┴──────────┐
                    │                 │
         ┌──────────┴──────────┐      │
         │                     │      │
         │ 1:N                 │      │
         │                     │      │
         ▼                     │      │
┌──────────────────────────┐  │      │
│     PRODUCTO            │  │      │
│    (producto)           │  │      │
├──────────────────────────┤  │      │
│ id (PK)                  │  │      │
│ nombre                   │  │      │
│ descripcion              │  │      │
│ precio                   │  │      │
│ activo                   │  │      │
└──────────────────────────┘  │      │
                              │      │
                              │      │
         ┌────────────────────┘      │
         │                           │
         │ 1:N                       │
         │                           │
         ▼                           │
┌──────────────────────────┐        │
│   PRODUCTO_OPCION        │        │
│  (producto_opcion)       │        │
├──────────────────────────┤        │
│ id (PK)                  │        │
│ id_producto (FK) ────────┼────────┤
│ id_tipo_opcion (FK) ─┐   │        │
│ nombre               │   │        │
│ descripcion          │   │        │
│ precio_adicional     │   │        │
│ activo               │   │        │
└──────────────────────┘   │        │
                           │        │
                           │        │
         ┌─────────────────┘        │
         │                          │
         │ 1:N                      │
         │                          │
         ▼                          │
┌──────────────────────────┐       │
│   TIPO_OPCION            │       │
│  (tipo_opcion)           │       │
├──────────────────────────┤       │
│ id (PK)                  │       │
│ codigo                   │       │
│ nombre                   │       │
│ descripcion              │       │
│ activo                   │       │
│ orden                    │       │
│ seleccion_minima         │       │
│ seleccion_maxima         │       │
└──────────────────────────┘       │
                                   │
                                   │
                    ┌──────────────┘
                    │
                    └─ N:1
```

## Descripción de Tablas

### 1. MESAS (mesas)

Representa las mesas del restaurante donde se sirven los pedidos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | ULID | Identificador único |
| numero | INT | Número de la mesa |
| capacidad | INT | Cantidad de personas que pueden sentarse |
| ubicacion | VARCHAR | Ubicación física de la mesa |
| activo | BOOLEAN | Indica si la mesa está disponible |
| fecha_creacion | TIMESTAMP | Fecha de creación |
| fecha_modificacion | TIMESTAMP | Fecha de última modificación |

### 2. PEDIDO (pedido)

Representa un pedido completo de un cliente.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | ULID | Identificador único |
| id_mesa | ULID (FK) | Referencia a la mesa |
| numero_pedido | VARCHAR | Número único del pedido (ej: 20250129-M1-001) |
| estado | ENUM | Estado del pedido (pendiente, confirmado, en_preparacion, listo, entregado, cancelado) |
| subtotal | DECIMAL(10,2) | Suma de todos los items sin impuestos |
| impuestos | DECIMAL(10,2) | Monto de impuestos (típicamente 18% IGV) |
| descuentos | DECIMAL(10,2) | Descuentos aplicados |
| total | DECIMAL(10,2) | Total final (subtotal + impuestos - descuentos) |
| notas_cliente | TEXT | Notas especiales del cliente |
| notas_cocina | TEXT | Instrucciones especiales para la cocina |
| fecha_confirmado | TIMESTAMP | Cuándo se confirmó el pedido |
| fecha_en_preparacion | TIMESTAMP | Cuándo comenzó la preparación |
| fecha_listo | TIMESTAMP | Cuándo estuvo listo |
| fecha_entregado | TIMESTAMP | Cuándo se entregó |
| fecha_cancelado | TIMESTAMP | Cuándo se canceló |
| fecha_creacion | TIMESTAMP | Fecha de creación |
| fecha_modificacion | TIMESTAMP | Fecha de última modificación |

### 3. PEDIDO_PRODUCTO (pedido_producto)

Representa un item/producto dentro de un pedido.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | ULID | Identificador único |
| id_pedido | ULID (FK) | Referencia al pedido |
| id_producto | ULID (FK) | Referencia al producto del menú |
| cantidad | INT | Cantidad de unidades (>= 1) |
| precio_unitario | DECIMAL(10,2) | Precio base del producto |
| precio_opciones | DECIMAL(10,2) | Suma de precios de opciones adicionales |
| subtotal | DECIMAL(10,2) | cantidad * (precio_unitario + precio_opciones) |
| notas_personalizacion | TEXT | Notas especiales para este item |
| fecha_creacion | TIMESTAMP | Fecha de creación |
| fecha_modificacion | TIMESTAMP | Fecha de última modificación |

### 4. PEDIDO_OPCION (pedido_opcion)

Representa una opción/personalización seleccionada para un item del pedido.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | ULID | Identificador único |
| id_pedido_producto | ULID (FK) | Referencia al item del pedido |
| id_producto_opcion | ULID (FK) | Referencia a la opción disponible |
| precio_adicional | DECIMAL(10,2) | Precio de la opción al momento del pedido |
| fecha_creacion | TIMESTAMP | Fecha de creación |
| creado_por | ULID | Usuario que creó el registro |
| modificado_por | ULID | Usuario que modificó el registro |

### 5. PRODUCTO (producto)

Representa un producto disponible en el menú.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | ULID | Identificador único |
| nombre | VARCHAR | Nombre del producto |
| descripcion | TEXT | Descripción detallada |
| precio | DECIMAL(10,2) | Precio base del producto |
| activo | BOOLEAN | Indica si está disponible |
| fecha_creacion | TIMESTAMP | Fecha de creación |
| fecha_modificacion | TIMESTAMP | Fecha de última modificación |

### 6. PRODUCTO_OPCION (producto_opcion)

Representa una opción disponible para un producto.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | ULID | Identificador único |
| id_producto | ULID (FK) | Referencia al producto |
| id_tipo_opcion | ULID (FK) | Referencia al tipo de opción |
| nombre | VARCHAR | Nombre de la opción (ej: "Nivel 3 de Ají") |
| descripcion | TEXT | Descripción de la opción |
| precio_adicional | DECIMAL(10,2) | Precio adicional por esta opción |
| activo | BOOLEAN | Indica si está disponible |
| fecha_creacion | TIMESTAMP | Fecha de creación |
| fecha_modificacion | TIMESTAMP | Fecha de última modificación |

### 7. TIPO_OPCION (tipo_opcion)

Representa un tipo/categoría de opciones.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | ULID | Identificador único |
| codigo | VARCHAR | Código interno (ej: "nivel_aji") |
| nombre | VARCHAR | Nombre del tipo (ej: "Nivel de Ají") |
| descripcion | TEXT | Descripción del tipo |
| activo | BOOLEAN | Indica si está activo |
| orden | INT | Orden de visualización |
| seleccion_minima | INT | Mínimo de opciones a seleccionar (0 = opcional) |
| seleccion_maxima | INT | Máximo de opciones (NULL = sin límite) |
| fecha_creacion | TIMESTAMP | Fecha de creación |
| fecha_modificacion | TIMESTAMP | Fecha de última modificación |

## Flujo de Datos - Ejemplo Completo

### Escenario: Cliente ordena Ceviche con opciones

```
1. MESA SELECCIONADA
   Mesa #3 (capacidad: 4 personas)

2. PEDIDO CREADO
   Pedido: 20250129-M3-001
   Estado: PENDIENTE
   Total: S/. 0.00

3. PRODUCTO AGREGADO
   - Ceviche de Pescado (S/. 45.00)
   - Cantidad: 1
   - Subtotal item: S/. 45.00

4. OPCIONES SELECCIONADAS
   - Nivel de Ají: 3 (+ S/. 2.00)
   - Acompañamiento: Camote frito (+ S/. 3.00)
   - Subtotal item actualizado: S/. 50.00

5. TOTALES CALCULADOS
   - Subtotal: S/. 50.00
   - Impuestos (18%): S/. 9.00
   - Descuentos: S/. 0.00
   - Total: S/. 59.00

6. PEDIDO CONFIRMADO
   Estado: CONFIRMADO
   Fecha confirmado: 2025-01-29 14:30:00
```

## Cálculos Importantes

### Subtotal de un Item
```
subtotal_item = cantidad × (precio_unitario + precio_opciones)
```

### Subtotal del Pedido
```
subtotal_pedido = Σ(subtotal_item para cada item)
```

### Impuestos
```
impuestos = subtotal_pedido × 0.18  (18% IGV)
```

### Total del Pedido
```
total_pedido = subtotal_pedido + impuestos - descuentos
```

## Estados del Pedido

```
PENDIENTE
    ↓
CONFIRMADO
    ↓
EN_PREPARACION
    ↓
LISTO
    ↓
ENTREGADO

O en cualquier momento:
    ↓
CANCELADO
```

## Restricciones y Validaciones

### Tabla PEDIDO_PRODUCTO
- `cantidad >= 1` (mínimo 1 unidad)
- `precio_unitario > 0` (debe ser positivo)
- `precio_opciones >= 0` (no negativo)
- `subtotal >= 0` (no negativo)

### Tabla PEDIDO
- `subtotal >= 0` (no negativo)
- `total >= 0` (no negativo)

### Tabla TIPO_OPCION
- `seleccion_minima >= 0`
- `seleccion_maxima >= seleccion_minima` (si no es NULL)

## Índices Principales

Para optimizar consultas frecuentes:

```sql
-- Búsqueda rápida de pedidos por mesa
CREATE INDEX idx_pedido_id_mesa ON pedido(id_mesa);

-- Búsqueda rápida de items de un pedido
CREATE INDEX idx_pedido_producto_id_pedido ON pedido_producto(id_pedido);

-- Búsqueda rápida de opciones de un item
CREATE INDEX idx_pedido_opcion_id_pedido_producto ON pedido_opcion(id_pedido_producto);

-- Búsqueda rápida de opciones de un producto
CREATE INDEX idx_producto_opcion_id_producto ON producto_opcion(id_producto);

-- Búsqueda por número de pedido
CREATE INDEX idx_pedido_numero_pedido ON pedido(numero_pedido);
```

## Cascadas de Eliminación

- Si se elimina un **PEDIDO**, se eliminan automáticamente todos sus **PEDIDO_PRODUCTO**
- Si se elimina un **PEDIDO_PRODUCTO**, se eliminan automáticamente todas sus **PEDIDO_OPCION**
- Si se elimina un **PRODUCTO_OPCION**, se restringe la eliminación si hay **PEDIDO_OPCION** asociadas

## Consideraciones de Diseño

1. **Precios Congelados**: Los precios en `PEDIDO_PRODUCTO` y `PEDIDO_OPCION` son copias del precio al momento del pedido, no referencias dinámicas.

2. **Auditoría**: Todos los cambios se registran con `fecha_creacion` y `fecha_modificacion`.

3. **Timestamps de Estado**: Se registra cuándo ocurrió cada cambio de estado importante.

4. **Notas**: Se permiten notas tanto del cliente como para la cocina.

5. **Flexibilidad**: El sistema permite múltiples opciones por item y múltiples items por pedido.
