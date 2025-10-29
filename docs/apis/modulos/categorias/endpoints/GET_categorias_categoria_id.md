# Especificación (breve) — GET Categoría por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/categorias/{categoria_id}`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}{BASE_PATH}/categorias/{categoria_id}`

## ENTRADA

### Path Params

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `categoria_id` | string | YES | ULID | Identificador único de la categoría. |

## SALIDA (200 OK)

```json
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
```

## ERRORES

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 404 | `NOT_FOUND` | Recurso no encontrado | ID inexistente. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/categorias/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/categorias/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "accept: application/json"
```
