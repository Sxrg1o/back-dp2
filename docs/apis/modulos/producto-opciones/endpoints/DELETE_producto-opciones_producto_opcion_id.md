# Especificación (breve) — DELETE Producto Opción por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/producto-opciones/{producto_opcion_id}`
- **HTTP Method:** `DELETE`
- **Autenticación:** (Ninguna)

## ENTRADA

### Path Params

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `producto_opcion_id` | string | YES | ID de la opción a eliminar (ULID). |

## SALIDA (204 No Content)

**Sin contenido en el cuerpo de la respuesta.**

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/producto-opciones/01K7ZF34CDEF7O8PI17RLE5PQ8`

**cURL:**
```bash
curl -X DELETE "https://back-dp2.onrender.com/api/v1/producto-opciones/01K7ZF34CDEF7O8PI17RLE5PQ8" \
  -H "accept: application/json"
```
