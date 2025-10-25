# Especificación (breve) — POST Sync Mesas

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/sync/mesas`
- **HTTP Method:** `POST`
- **Autenticación:** (Ninguna)
- **Notas:** Endpoint **interno** para sincronización con Domótica

**URL patrón:** `{HOST}/api/v1/sync/mesas`

## DESCRIPCIÓN

Recibe datos de mesas extraídos mediante scraping del sistema **Domótica**.

**⚠️ Actualmente solo confirma la recepción de los datos sin procesamiento adicional (funcionalidad futura).**

## ENTRADA

### BODY

```json
[
  {
    "numero": "M01",
    "capacidad": 4,
    "estado": "disponible"
  },
  {
    "numero": "M02",
    "capacidad": 6,
    "estado": "ocupada"
  }
]
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `[].numero` | string | YES | Número/código de la mesa. |
| `[].capacidad` | integer | YES | Capacidad de la mesa. |
| `[].estado` | string | YES | Estado actual de la mesa. |

## SALIDA (200 OK)

```json
{
  "status": "success",
  "message": "Datos de mesas recibidos correctamente",
  "mesas_recibidas": 2,
  "mesas": [
    {
      "numero": "M01",
      "capacidad": 4,
      "estado": "disponible"
    },
    {
      "numero": "M02",
      "capacidad": 6,
      "estado": "ocupada"
    }
  ]
}
```

## ERRORES

| HTTP | Code | Comment |
|------|------|---------|
| 400 | `VALIDATION_ERROR` | Payload malformado. |
| 500 | `INTERNAL_ERROR` | Error durante sincronización. |

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/sync/mesas`

**cURL:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/sync/mesas" \
  -H "Content-Type: application/json" \
  -d '[{"numero": "M01", "capacidad": 4, "estado": "disponible"}]'
```

## Notas

- ⚠️ Actualmente solo registra la recepción (no procesa)
- ✅ Funcionalidad completa será implementada en el futuro
