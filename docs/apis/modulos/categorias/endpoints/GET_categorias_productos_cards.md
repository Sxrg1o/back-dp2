# Especificación (breve) — GET Categorías con Productos (Cards)

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/categorias/productos/cards`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)
- **Notas:** **⚠️ Este endpoint debe ir ANTES de `/{categoria_id}` en la ruta para evitar conflictos.**

**URL patrón:** `{HOST}{BASE_PATH}/categorias/productos/cards?skip={skip}&limit={limit}`

## DESCRIPCIÓN

Obtiene todas las categorías con sus productos asociados en **formato minimal**. Solo incluye:
- **Categorías:** ID, nombre, imagen
- **Productos:** ID, nombre, imagen

**Caso de uso:** HU-C05 — Cliente explorando la carta por categorías.

## ENTRADA

### Query Params

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `skip` | integer | NO | >=0 | Offset (default `0`). |
| `limit` | integer | NO | 1..500 | Tamaño de página (default `100`). |

## SALIDA (200 OK)

```json
{
  "items": [
    {
      "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
      "nombre": "Ceviches",
      "imagen_path": "/static/categorias/ceviches.jpg",
      "productos": [
        {
          "id": "01K7ZD12XYZW4M5NG95PJC3NO6",
          "nombre": "Ceviche Clásico",
          "imagen_path": "/static/productos/ceviche-clasico.jpg"
        },
        {
          "id": "01K7ZD23ABCD5N6OH06QKD4OP7",
          "nombre": "Ceviche Mixto",
          "imagen_path": "/static/productos/ceviche-mixto.jpg"
        }
      ]
    },
    {
      "id": "01K7ZCT9QRST3K9FC94OIB2NL5",
      "nombre": "Tiraditos",
      "imagen_path": "/static/categorias/tiraditos.jpg",
      "productos": [
        {
          "id": "01K7ZD34EFGH6O7PI17RLE5PQ8",
          "nombre": "Tiradito de Pescado",
          "imagen_path": "/static/productos/tiradito-pescado.jpg"
        }
      ]
    }
  ],
  "skip": 0,
  "limit": 100,
  "total": 8
}
```

**DICTIONARY (OUTPUT)**

| Field | Data Type | Format | Comment |
|-------|-----------|--------|---------|
| `items` | array | | Lista de categorías con productos. |
| `items[].id` | string | ULID | ID de la categoría. |
| `items[].nombre` | string | | Nombre de la categoría. |
| `items[].imagen_path` | string | | Ruta de la imagen de la categoría. |
| `items[].productos` | array | | Lista de productos de la categoría. |
| `items[].productos[].id` | string | ULID | ID del producto. |
| `items[].productos[].nombre` | string | | Nombre del producto. |
| `items[].productos[].imagen_path` | string | | Ruta de la imagen del producto. |
| `skip` | integer | | Offset aplicado. |
| `limit` | integer | | Tamaño de página. |
| `total` | integer | | Total de categorías. |

## ERRORES

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 400 | `VALIDATION_ERROR` | Parámetros inválidos | `skip`/`limit` fuera de rango. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/categorias/productos/cards?skip=0&limit=100`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/categorias/productos/cards?skip=0&limit=100" \
  -H "accept: application/json"
```

## Notas Técnicas

- ⚠️ Este endpoint **NO incluye** precio, descripción ni otros campos de productos
- ✅ Solo retorna información mínima para visualización tipo "card"
- ✅ Útil para pantallas de navegación rápida del menú
