# Especificación (breve) — POST Alérgenos

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/alergenos`
- **HTTP Method:** `POST`
- **Autenticación:** (Ninguna)

## ENTRADA

### BODY

```json
{
  "nombre": "Mariscos",
  "descripcion": "Productos del mar",
  "icono_path": "/static/alergenos/mariscos.svg"
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `nombre` | string | YES | Nombre del alérgeno (único). |
| `descripcion` | string | NO | Descripción del alérgeno. |
| `icono_path` | string | NO | Ruta del ícono. |

## SALIDA (201 Created)

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Mariscos",
  "descripcion": "Productos del mar",
  "icono_path": "/static/alergenos/mariscos.svg",
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T05:16:30.123456Z"
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/alergenos`

**cURL:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/alergenos" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Mariscos", "descripcion": "Productos del mar"}'
```
