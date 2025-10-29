# Especificación (breve) — DELETE Tipo de Opción por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/tipos-opciones/{tipo_opcion_id}`
- **HTTP Method:** `DELETE`
- **Autenticación:** (Ninguna)

## ENTRADA

### Path Params

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `tipo_opcion_id` | string | YES | ID del tipo de opción a eliminar (ULID). |

## SALIDA (204 No Content)

**Sin contenido en el cuerpo de la respuesta.**

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/tipos-opciones/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**
```bash
curl -X DELETE "https://back-dp2.onrender.com/api/v1/tipos-opciones/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "accept: application/json"
```
