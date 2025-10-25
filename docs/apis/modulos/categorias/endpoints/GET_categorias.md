# Especificación (breve) — GET Categorías

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/categorias`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)
- **Notas:** En **GET** no enviar body.

**URL patrón:** `{HOST}{BASE_PATH}{RECURSO}?skip={skip}&limit={limit}`

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
      "nombre": "Entradas",
      "descripcion": "Aperitivos y platos de entrada",
      "imagen_path": "/static/categorias/entradas.jpg",
      "orden": 1,
      "activo": true,
      "created_at": "2024-10-23T05:16:30.123456Z",
      "updated_at": "2024-10-23T05:16:30.123456Z"
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
| `items` | array | | Lista de categorías. |
| `skip` | integer | | Offset aplicado. |
| `limit` | integer | | Tamaño de página. |
| `total` | integer | | Total de registros. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/categorias?skip=0&limit=100`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/categorias?skip=0&limit=100" \
  -H "accept: application/json"
```
