# Especificación (breve) — PUT Producto Opción por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/producto-opciones/{producto_opcion_id}`
- **HTTP Method:** `PUT`
- **Autenticación:** (Ninguna)

## ENTRADA

### Path Params

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `producto_opcion_id` | string | YES | ID de la opción (ULID). |

### BODY

```json
{
  "precio_adicional": "2.00",
  "disponible": false
}
```

## SALIDA (200 OK)

```json
{
  "id": "01K7ZF34CDEF7O8PI17RLE5PQ8",
  "nombre": "Ají suave",
  "precio_adicional": "2.00",
  "disponible": false,
  "id_producto": "01K7ZD12XYZW4M5NG95PJC3NO6",
  "id_tipo_opcion": "01K7ZE23BCDE6N7OH06QKD4OP7",
  "orden": 1,
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T07:22:15.789012Z"
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/producto-opciones/01K7ZF34CDEF7O8PI17RLE5PQ8`

**cURL:**
```bash
curl -X PUT "https://back-dp2.onrender.com/api/v1/producto-opciones/01K7ZF34CDEF7O8PI17RLE5PQ8" \
  -H "Content-Type: application/json" \
  -d '{"precio_adicional": "2.00"}'
```
