# Especificación (breve) — DELETE Categoría por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/categorias/{categoria_id}`
- **HTTP Method:** `DELETE`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}{BASE_PATH}/categorias/{categoria_id}`

## ENTRADA

### Path Params

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `categoria_id` | string | YES | ULID | Identificador único de la categoría a eliminar. |

## SALIDA (204 No Content)

**Sin contenido en el cuerpo de la respuesta.**

## ERRORES

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 404 | `NOT_FOUND` | Recurso no encontrado | ID inexistente. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/categorias/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**
```bash
curl -X DELETE "https://back-dp2.onrender.com/api/v1/categorias/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "accept: application/json"
```
