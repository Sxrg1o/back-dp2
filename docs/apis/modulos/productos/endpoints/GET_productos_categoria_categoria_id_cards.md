# Especificación (breve) — GET Productos por Categoría (Cards)

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/productos/categoria/{categoria_id}/cards`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}{BASE_PATH}/productos/categoria/{categoria_id}/cards?skip={skip}&limit={limit}`

## DESCRIPCIÓN

Lista productos **filtrados por categoría** en formato **card** con información completa de categoría.

## ENTRADA

### Path Params

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `categoria_id` | string | YES | ULID | ID de la categoría para filtrar. |

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
  "total": 12
}
```

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/productos/categoria/01K7ZCT8PNJA2J8EB83NHA1MK4/cards?skip=0&limit=100`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/productos/categoria/01K7ZCT8PNJA2J8EB83NHA1MK4/cards?skip=0&limit=100" \
  -H "accept: application/json"
```
