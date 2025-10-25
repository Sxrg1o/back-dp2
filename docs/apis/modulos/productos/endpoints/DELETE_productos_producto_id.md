# Especificación (breve) — DELETE Producto por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/productos/{producto_id}`
- **HTTP Method:** `DELETE`
- **Autenticación:** (Ninguna)

## ENTRADA

### Path Params

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `producto_id` | string | YES | ID del producto a eliminar (ULID). |

## SALIDA (204 No Content)

**Sin contenido en el cuerpo de la respuesta.**

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/productos/01K7ZD12XYZW4M5NG95PJC3NO6`

**cURL:**
```bash
curl -X DELETE "https://back-dp2.onrender.com/api/v1/productos/01K7ZD12XYZW4M5NG95PJC3NO6" \
  -H "accept: application/json"
```
