# Especificación (breve) — GET Producto con Opciones

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/productos/{producto_id}/opciones`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}{BASE_PATH}/productos/{producto_id}/opciones`

## DESCRIPCIÓN

Obtiene los detalles completos de un producto con todas sus opciones **agrupadas por tipo de opción**.

**Incluye:**
- ✅ `descripcion` y `precio_base` del producto
- ✅ Opciones agrupadas en `tipos_opciones[]` por tipo
- ✅ Cada tipo incluye metadata (obligatorio, múltiple selección, orden)

## ENTRADA

### Path Params

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `producto_id` | string | YES | ULID | ID del producto. |

## SALIDA (200 OK)

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Ceviche Clásico",
  "descripcion": "Pescado fresco del día marinado en limón",
  "precio_base": "25.00",
  "tipos_opciones": [
    {
      "id_tipo_opcion": "01K7ZE23BCDE6N7OH06QKD4OP7",
      "nombre_tipo": "Nivel de picante",
      "obligatorio": true,
      "multiple_seleccion": false,
      "orden": 1,
      "opciones": [
        {
          "id": "01K7ZF34CDEF7O8PI17RLE5PQ8",
          "nombre": "Sin ají",
          "precio_adicional": "0.00"
        },
        {
          "id": "01K7ZF45DEFG8P9QJ28SMF6QR9",
          "nombre": "Ají suave",
          "precio_adicional": "0.00"
        },
        {
          "id": "01K7ZF56EFGH9Q0RK39TNG7RS0",
          "nombre": "Ají picante",
          "precio_adicional": "2.00"
        }
      ]
    },
    {
      "id_tipo_opcion": "01K7ZG67FGHI0R1SL40UOH8ST1",
      "nombre_tipo": "Acompañamientos",
      "obligatorio": false,
      "multiple_seleccion": true,
      "orden": 2,
      "opciones": [
        {
          "id": "01K7ZH78GHIJ1S2TM51VPI9TU2",
          "nombre": "Camote",
          "precio_adicional": "3.00"
        },
        {
          "id": "01K7ZH89HIJK2T3UN62WQJ0UV3",
          "nombre": "Choclo",
          "precio_adicional": "3.00"
        }
      ]
    }
  ]
}
```

**DICTIONARY (OUTPUT)**

| Field | Data Type | Format | Comment |
|-------|-----------|--------|---------|
| `id` | string | ULID | ID del producto. |
| `nombre` | string | | Nombre del producto. |
| `descripcion` | string | | Descripción del producto. |
| `precio_base` | string | decimal | Precio base sin extras. |
| `tipos_opciones` | array | | Lista de tipos de opciones agrupadas. |
| `tipos_opciones[].id_tipo_opcion` | string | ULID | ID del tipo de opción. |
| `tipos_opciones[].nombre_tipo` | string | | Nombre del tipo (ej: "Nivel de picante"). |
| `tipos_opciones[].obligatorio` | boolean | | Si el cliente debe seleccionar al menos una. |
| `tipos_opciones[].multiple_seleccion` | boolean | | Si puede seleccionar múltiples opciones. |
| `tipos_opciones[].orden` | integer | | Orden de visualización del tipo. |
| `tipos_opciones[].opciones` | array | | Lista de opciones dentro del tipo. |
| `tipos_opciones[].opciones[].id` | string | ULID | ID de la opción. |
| `tipos_opciones[].opciones[].nombre` | string | | Nombre de la opción (ej: "Ají suave"). |
| `tipos_opciones[].opciones[].precio_adicional` | string | decimal | Precio adicional de la opción. |

## ERRORES

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 404 | `NOT_FOUND` | Recurso no encontrado | Producto no existe. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/productos/01K7ZCT8PNJA2J8EB83NHA1MK4/opciones`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/productos/01K7ZCT8PNJA2J8EB83NHA1MK4/opciones" \
  -H "accept: application/json"
```

## Caso de Uso

**HU-C07:** Cliente que personaliza — Añadir extras disponibles a mi selección
