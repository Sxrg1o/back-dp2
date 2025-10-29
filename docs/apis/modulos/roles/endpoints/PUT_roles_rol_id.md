# Especificación (breve) — PUT Roles por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/roles/{rol_id}`
- **HTTP Method:** `PUT`
- **Autenticación:** (Ninguna)
- **Notas:** Actualiza los datos de un rol existente.

**URL patrón (componentes separadas):**

```
{HOST}{BASE_PATH}/roles/{rol_id}
```

## ENTRADA

### Path Params

**DICTIONARY**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `rol_id` | string | YES | ULID | Identificador único del rol a actualizar. |

### Headers

**DICTIONARY**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `accept` | string | YES | `application/json` | Tipo de respuesta. |
| `Content-Type` | string | YES | `application/json` | Tipo de contenido del body. |

### BODY

```json
{
  "nombre": "SuperAdministrador"
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `nombre` | string | NO | 3-50 caracteres | Nuevo nombre del rol. Debe ser único si se proporciona. |

## SALIDA (200 OK — ejemplo)

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "SuperAdministrador",
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T07:22:15.789012Z"
}
```

**DICTIONARY (OUTPUT)**

| Field | Data Type | Format | Comment |
|-------|-----------|--------|---------|
| `id` | string | ULID | Identificador único del rol. |
| `nombre` | string | | Nombre actualizado del rol. |
| `created_at` | string | ISO 8601 | Fecha de creación (sin cambios). |
| `updated_at` | string | ISO 8601 | Fecha de última actualización (nueva). |

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
| 400 | `VALIDATION_ERROR` | Parámetros inválidos | Nombre demasiado corto/largo. |
| 404 | `NOT_FOUND` | Recurso no encontrado | ID inexistente. |
| 409 | `CONFLICT` | Conflicto de negocio | Ya existe otro rol con ese nombre. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas (listas para usar)

### **Producción**

**URL completa:** `https://back-dp2.onrender.com/api/v1/roles/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**

```bash
curl -X PUT \
  "https://back-dp2.onrender.com/api/v1/roles/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "SuperAdministrador"}'
```

### **Local**

**URL completa:** `http://127.0.0.1:8000/api/v1/roles/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**

```bash
curl -X PUT \
  "http://127.0.0.1:8000/api/v1/roles/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "SuperAdministrador"}'
```

## Variables y constantes (resumen)

**Constantes:**
- `BASE_PATH = /api/v1`
- `RECURSO = /roles`

**Variables:**
- `HOST` = `https://back-dp2.onrender.com` (prod) | `http://127.0.0.1:8000` (local)
- `rol_id` — ID del rol a actualizar
- `nombre` — Nuevo nombre del rol
