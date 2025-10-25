# Especificación (breve) — POST Tipos de Opciones

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/tipos-opciones`
- **HTTP Method:** `POST`
- **Autenticación:** (Ninguna)

## ENTRADA

### BODY

```json
{
  "nombre": "Nivel de picante",
  "descripcion": "Selecciona el nivel de ají",
  "obligatorio": true,
  "multiple_seleccion": false,
  "orden": 1
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `nombre` | string | YES | Nombre del tipo (único). |
| `descripcion` | string | NO | Descripción del tipo. |
| `obligatorio` | boolean | NO | Si es obligatorio seleccionar (default: false). |
| `multiple_seleccion` | boolean | NO | Si permite múltiples opciones (default: false). |
| `orden` | integer | NO | Orden de visualización (default: 0). |

## SALIDA (201 Created)

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Nivel de picante",
  "descripcion": "Selecciona el nivel de ají",
  "obligatorio": true,
  "multiple_seleccion": false,
  "orden": 1,
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T05:16:30.123456Z"
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/tipos-opciones`

**cURL:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/tipos-opciones" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Nivel de picante", "obligatorio": true}'
```
