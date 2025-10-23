# Especificación (breve) — GET Productos (Cards)

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/productos/cards`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}{BASE_PATH}/productos/cards?skip={skip}&limit={limit}`

## DESCRIPCIÓN

Lista **TODOS** los productos en formato **card** con información completa de categoría. Incluye:
- **Producto:** ID, nombre, imagen, precio
- **Categoría:** ID, nombre, imagen

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
      "id": "01K7ZD12XYZW4M5NG95PJC3NO6",
      "nombre": "Ceviche Clásico",
      "imagen_path": "/static/productos/ceviche-clasico.jpg",
      "precio_base": "25.00",
      "categoria": {
        "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
        "nombre": "Ceviches",
        "imagen_path": "/static/categorias/ceviches.jpg"
      }
    }
  ],
  "skip": 0,
  "limit": 100,
  "total": 274
}
```

**DICTIONARY (OUTPUT)**

| Field | Data Type | Format | Comment |
|-------|-----------|--------|---------|
| `items[].id` | string | ULID | ID del producto. |
| `items[].nombre` | string | | Nombre del producto. |
| `items[].imagen_path` | string | | Ruta de la imagen. |
| `items[].precio_base` | string | decimal | Precio base del producto. |
| `items[].categoria` | object | | Información de la categoría. |
| `items[].categoria.id` | string | ULID | ID de la categoría. |
| `items[].categoria.nombre` | string | | Nombre de la categoría. |
| `items[].categoria.imagen_path` | string | | Ruta de la imagen de categoría. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/productos/cards?skip=0&limit=100`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/productos/cards?skip=0&limit=100" \
  -H "accept: application/json"
```
