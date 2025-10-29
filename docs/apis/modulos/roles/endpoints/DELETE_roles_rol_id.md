# Especificación (breve) — DELETE Roles por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/roles/{rol_id}`
- **HTTP Method:** `DELETE`
- **Autenticación:** (Ninguna)
- **Notas:** En **DELETE** no enviar body.

**URL patrón (componentes separadas):**

```
{HOST}{BASE_PATH}/roles/{rol_id}
```

## ENTRADA

> **Body:** *(no aplica en DELETE).*

### Path Params

**DICTIONARY**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `rol_id` | string | YES | ULID | Identificador único del rol a eliminar. |

### Headers

**DICTIONARY**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `accept` | string | YES | `application/json` | Tipo de respuesta. |

## SALIDA (204 No Content)

**Sin contenido en el cuerpo de la respuesta.**

La operación exitosa retorna **HTTP 204** sin body.

## ERRORES (4xx/5xx)

**Problem+JSON**

```json
{
  "type": "https://back-dp2.onrender.com/errors/NOT_FOUND",
  "title": "Recurso no encontrado",
  "status": 404,
  "detail": "No se encontró el rol con ID '01K7ZCT8PNJA2J8EB83NHA1MK4'",
  "instance": "/api/v1/roles/01K7ZCT8PNJA2J8EB83NHA1MK4"
}
```

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 404 | `NOT_FOUND` | Recurso no encontrado | ID inexistente. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas (listas para usar)

### **Producción**

**URL completa:** `https://back-dp2.onrender.com/api/v1/roles/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**

```bash
curl -X DELETE \
  "https://back-dp2.onrender.com/api/v1/roles/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "accept: application/json"
```

### **Local**

**URL completa:** `http://127.0.0.1:8000/api/v1/roles/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**

```bash
curl -X DELETE \
  "http://127.0.0.1:8000/api/v1/roles/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "accept: application/json"
```

## Variables y constantes (resumen)

**Constantes:**
- `BASE_PATH = /api/v1`
- `RECURSO = /roles`

**Variables:**
- `HOST` = `https://back-dp2.onrender.com` (prod) | `http://127.0.0.1:8000` (local)
- `rol_id` — ID del rol a eliminar
