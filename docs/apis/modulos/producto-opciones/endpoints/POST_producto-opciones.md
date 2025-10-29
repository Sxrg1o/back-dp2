# Especificación (breve) — POST Producto Opciones

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/producto-opciones`
- **HTTP Method:** `POST`
- **Autenticación:** (Ninguna)

## ENTRADA

### BODY

```json
{
  "nombre": "Ají suave",
  "precio_adicional": "0.00",
  "disponible": true,
  "id_producto": "01K7ZD12XYZW4M5NG95PJC3NO6",
  "id_tipo_opcion": "01K7ZE23BCDE6N7OH06QKD4OP7",
  "orden": 1
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `nombre` | string | YES | Nombre de la opción. |
| `precio_adicional` | string | NO | Precio adicional (default: "0.00"). |
| `disponible` | boolean | NO | Si está disponible (default: true). |
| `id_producto` | string | YES | ID del producto (ULID). |
| `id_tipo_opcion` | string | YES | ID del tipo de opción (ULID). |
| `orden` | integer | NO | Orden de visualización (default: 0). |

## SALIDA (201 Created)

```json
{
  "id": "01K7ZF34CDEF7O8PI17RLE5PQ8",
  "nombre": "Ají suave",
  "precio_adicional": "0.00",
  "disponible": true,
  "id_producto": "01K7ZD12XYZW4M5NG95PJC3NO6",
  "id_tipo_opcion": "01K7ZE23BCDE6N7OH06QKD4OP7",
  "orden": 1,
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T05:16:30.123456Z"
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/producto-opciones`

**cURL:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/producto-opciones" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Ají suave", "id_producto": "01K7ZD12XYZW4M5NG95PJC3NO6", "id_tipo_opcion": "01K7ZE23BCDE6N7OH06QKD4OP7"}'
```
