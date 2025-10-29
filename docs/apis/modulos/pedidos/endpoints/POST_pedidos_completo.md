# POST /pedidos/completo

> **⭐ Crear un pedido completo con items en una sola transacción**

## META

- **Host Producción:** `https://back-dp2.onrender.com`
- **Host Local:** `http://127.0.0.1:8000`
- **Path:** `/api/v1/pedidos/completo`
- **Método:** `POST`
- **Autenticación:** No requerida
- **Content-Type:** `application/json`

## DESCRIPCIÓN

Crea un pedido completo con todos sus items en **una sola transacción atómica**. Si algún item falla la validación, se deshace toda la operación.

**Características:**
- ✅ Transacción atómica (todo o nada)
- ✅ Generación automática de `numero_pedido`
- ✅ Cálculo automático de totales
- ✅ Validación de mesa, productos y disponibilidad
- ✅ Validación de precios y opciones

## ENTRADA

### Headers

| Header | Valor | Requerido |
|--------|-------|-----------|
| `Content-Type` | `application/json` | ✅ |

### Body Schema

```json
{
  "id_mesa": "string (ULID)",
  "items": [
    {
      "id_producto": "string (ULID)",
      "cantidad": "integer (>= 1)",
      "precio_unitario": "number (> 0)",
      "precio_opciones": "number (>= 0)",
      "notas_personalizacion": "string | null"
    }
  ],
  "notas_cliente": "string | null",
  "notas_cocina": "string | null"
}
```

### Campos Requeridos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_mesa` | `string` | ID ULID de la mesa (debe existir) |
| `items` | `array` | Lista de items del pedido (mín. 1 item) |
| `items[].id_producto` | `string` | ID ULID del producto (debe existir y estar disponible) |
| `items[].cantidad` | `integer` | Cantidad del producto (≥ 1) |
| `items[].precio_unitario` | `number` | Precio base del producto (> 0) |

### Campos Opcionales

| Campo | Tipo | Descripción | Default |
|-------|------|-------------|---------|
| `items[].precio_opciones` | `number` | Suma de precios de opciones adicionales | `0.00` |
| `items[].notas_personalizacion` | `string` | Notas específicas del item | `null` |
| `notas_cliente` | `string` | Notas del cliente | `null` |
| `notas_cocina` | `string` | Notas para la cocina | `null` |

## SALIDA

### Success Response (201 Created)

```json
{
  "id": "01J9ABCDEFGHIJKLMNOPQRSTUV",
  "numero_pedido": "20251028-M001-001",
  "id_mesa": "01J9ABCDEFGHIJKLMNOPQRSTUV",
  "estado": "PENDIENTE",
  "total": 110.00,
  "subtotal": 100.00,
  "impuestos": 10.00,
  "descuento": 0.00,
  "notas_cliente": "Mesa para evento",
  "notas_cocina": "Urgente",
  "fecha_creacion": "2025-10-28T22:30:00Z",
  "fecha_modificacion": "2025-10-28T22:30:00Z",
  "fecha_estimada_entrega": null,
  "fecha_entrega_real": null,
  "items": [
    {
      "id": "01J9ABCDEFGHIJKLMNOPQRSTUV",
      "id_pedido": "01J9ABCDEFGHIJKLMNOPQRSTUV",
      "id_producto": "01J9ABCDEFGHIJKLMNOPQRSTUV",
      "cantidad": 2,
      "precio_unitario": 25.50,
      "precio_opciones": 3.00,
      "subtotal": 57.00,
      "notas_personalizacion": "Sin cebolla",
      "fecha_creacion": "2025-10-28T22:30:00Z",
      "fecha_modificacion": "2025-10-28T22:30:00Z"
    }
  ]
}
```

### Diccionario de Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | `string` | ID ULID del pedido generado |
| `numero_pedido` | `string` | Número único: `YYYYMMDD-M{mesa_num}-{seq}` |
| `estado` | `string` | Estado inicial: `"PENDIENTE"` |
| `total` | `number` | Total final (subtotal + impuestos - descuento) |
| `subtotal` | `number` | Suma de subtotales de todos los items |
| `items[]` | `array` | Lista de items creados con sus IDs generados |
| `items[].subtotal` | `number` | `cantidad * (precio_unitario + precio_opciones)` |

## ERRORES

### 400 Bad Request - Datos Inválidos

```json
{
  "type": "validation_error",
  "title": "Datos de entrada inválidos",
  "detail": "La mesa con ID '01J123...' no existe",
  "status": 400
}
```

**Casos comunes:**
- Mesa no existe
- Producto no existe
- Producto no disponible
- Cantidad inválida (< 1)
- Precio inválido (≤ 0)
- Lista de items vacía

### 409 Conflict - Conflicto de Integridad

```json
{
  "type": "conflict_error",
  "title": "Conflicto de integridad",
  "detail": "Ya existe un pedido activo para esta mesa",
  "status": 409
}
```

### 500 Internal Server Error

```json
{
  "type": "internal_error",
  "title": "Error interno del servidor",
  "detail": "Error interno del servidor: Database connection failed",
  "status": 500
}
```

## EJEMPLOS

### Ejemplo 1: Pedido Simple (1 item)

**Request:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/pedidos/completo" \
  -H "Content-Type: application/json" \
  -d '{
    "id_mesa": "01J9MESA123ABCDEFGHIJKLMN",
    "items": [
      {
        "id_producto": "01J9PROD123ABCDEFGHIJKLMN",
        "cantidad": 1,
        "precio_unitario": 25.50,
        "precio_opciones": 0.00,
        "notas_personalizacion": null
      }
    ],
    "notas_cliente": "Primera vez",
    "notas_cocina": null
  }'
```

**Response (201):**
```json
{
  "id": "01J9PEDI123ABCDEFGHIJKLMN",
  "numero_pedido": "20251028-M003-001",
  "id_mesa": "01J9MESA123ABCDEFGHIJKLMN",
  "estado": "PENDIENTE",
  "total": 25.50,
  "subtotal": 25.50,
  "impuestos": 0.00,
  "descuento": 0.00,
  "notas_cliente": "Primera vez",
  "notas_cocina": null,
  "fecha_creacion": "2025-10-28T22:35:15Z",
  "fecha_modificacion": "2025-10-28T22:35:15Z",
  "items": [
    {
      "id": "01J9ITEM123ABCDEFGHIJKLMN",
      "id_pedido": "01J9PEDI123ABCDEFGHIJKLMN",
      "id_producto": "01J9PROD123ABCDEFGHIJKLMN",
      "cantidad": 1,
      "precio_unitario": 25.50,
      "precio_opciones": 0.00,
      "subtotal": 25.50,
      "notas_personalizacion": null,
      "fecha_creacion": "2025-10-28T22:35:15Z",
      "fecha_modificacion": "2025-10-28T22:35:15Z"
    }
  ]
}
```

### Ejemplo 2: Pedido Complejo (3 items con opciones)

**Request:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/pedidos/completo" \
  -H "Content-Type: application/json" \
  -d '{
    "id_mesa": "01J9MESA456ABCDEFGHIJKLMN",
    "items": [
      {
        "id_producto": "01J9CEVI123ABCDEFGHIJKLMN",
        "cantidad": 2,
        "precio_unitario": 30.00,
        "precio_opciones": 4.00,
        "notas_personalizacion": "Sin cebolla, ají picante, con choclo"
      },
      {
        "id_producto": "01J9ARRO456ABCDEFGHIJKLMN",
        "cantidad": 1,
        "precio_unitario": 22.00,
        "precio_opciones": 15.00,
        "notas_personalizacion": "Para 2 personas"
      },
      {
        "id_producto": "01J9BEBI789ABCDEFGHIJKLMN",
        "cantidad": 3,
        "precio_unitario": 5.00,
        "precio_opciones": 1.50,
        "notas_personalizacion": "Heladas"
      }
    ],
    "notas_cliente": "Celebración cumpleaños",
    "notas_cocina": "Servir todo junto por favor"
  }'
```

**Response (201):**
```json
{
  "id": "01J9PEDI456ABCDEFGHIJKLMN",
  "numero_pedido": "20251028-M005-002",
  "id_mesa": "01J9MESA456ABCDEFGHIJKLMN",
  "estado": "PENDIENTE",
  "total": 124.50,
  "subtotal": 124.50,
  "impuestos": 0.00,
  "descuento": 0.00,
  "notas_cliente": "Celebración cumpleaños",
  "notas_cocina": "Servir todo junto por favor",
  "fecha_creacion": "2025-10-28T22:40:22Z",
  "fecha_modificacion": "2025-10-28T22:40:22Z",
  "items": [
    {
      "id": "01J9ITEM456ABCDEFGHIJKLMN",
      "cantidad": 2,
      "precio_unitario": 30.00,
      "precio_opciones": 4.00,
      "subtotal": 68.00,
      "notas_personalizacion": "Sin cebolla, ají picante, con choclo"
    },
    {
      "id": "01J9ITEM789ABCDEFGHIJKLMN",
      "cantidad": 1,
      "precio_unitario": 22.00,
      "precio_opciones": 15.00,
      "subtotal": 37.00,
      "notas_personalizacion": "Para 2 personas"
    },
    {
      "id": "01J9ITEMABC DEFGHIJKLMN",
      "cantidad": 3,
      "precio_unitario": 5.00,
      "precio_opciones": 1.50,
      "subtotal": 19.50,
      "notas_personalizacion": "Heladas"
    }
  ]
}
```

### Ejemplo 3: Error - Mesa No Existe

**Request:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/pedidos/completo" \
  -H "Content-Type: application/json" \
  -d '{
    "id_mesa": "01J9INEXISTENTE123456789",
    "items": [
      {
        "id_producto": "01J9PROD123ABCDEFGHIJKLMN",
        "cantidad": 1,
        "precio_unitario": 25.50
      }
    ]
  }'
```

**Response (400):**
```json
{
  "type": "validation_error",
  "title": "Datos de entrada inválidos",
  "detail": "No se encontró la mesa con ID 01J9INEXISTENTE123456789",
  "status": 400
}
```

## CÁLCULOS AUTOMÁTICOS

### Subtotal por Item
```
subtotal_item = cantidad * (precio_unitario + precio_opciones)
```

### Total del Pedido
```
subtotal_pedido = suma(subtotal_item para cada item)
total_pedido = subtotal_pedido + impuestos - descuento
```

### Número de Pedido
```
formato: YYYYMMDD-M{mesa_numero}-{secuencia}
ejemplo: 20251028-M003-001
```

## URLs COMPLETAS

### Producción
```
POST https://back-dp2.onrender.com/api/v1/pedidos/completo
```

### Local
```
POST http://127.0.0.1:8000/api/v1/pedidos/completo
```

## NOTAS TÉCNICAS

- ⚠️ **Transacción Atómica:** Si cualquier item falla, se revierte todo el pedido
- 🔄 **Generación Automática:** El `numero_pedido` se genera automáticamente
- 📊 **Cálculos:** Todos los subtotales y totales se calculan automáticamente
- ✅ **Validaciones:** Se valida existencia de mesa, productos y disponibilidad
- 🏷️ **Estados:** El pedido siempre se crea en estado `PENDIENTE`
