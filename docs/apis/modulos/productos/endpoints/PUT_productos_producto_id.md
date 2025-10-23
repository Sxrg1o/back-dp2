# Especificación (breve) — PUT Producto por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/productos/{producto_id}`
- **HTTP Method:** `PUT`
- **Autenticación:** (Ninguna)

## ENTRADA

### Path Params

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `producto_id` | string | YES | ID del producto (ULID). |

### BODY

```json
{
  "nombre": "Ceviche Premium",
  "precio_base": "30.00",
  "disponible": false
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `nombre` | string | NO | Nuevo nombre (único). |
| `descripcion` | string | NO | Nueva descripción. |
| `precio_base` | string | NO | Nuevo precio. |
| `imagen_path` | string | NO | Nueva ruta de imagen. |
| `disponible` | boolean | NO | Nuevo estado disponibilidad. |
| `id_categoria` | string | NO | Nueva categoría. |

## SALIDA (200 OK)

```json
{
  "id": "01K7ZD12XYZW4M5NG95PJC3NO6",
  "nombre": "Ceviche Premium",
  "descripcion": "Pescado fresco del día marinado en limón",
  "precio_base": "30.00",
  "imagen_path": "/static/productos/ceviche-clasico.jpg",
  "disponible": false,
  "id_categoria": "01K7ZCT9QRST3K9FC94OIB2NL5",
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T07:22:15.789012Z"
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/productos/01K7ZD12XYZW4M5NG95PJC3NO6`

**cURL:**
```bash
curl -X PUT "https://back-dp2.onrender.com/api/v1/productos/01K7ZD12XYZW4M5NG95PJC3NO6" \
  -H "Content-Type: application/json" \
  -d '{"precio_base": "30.00", "disponible": false}'
```
