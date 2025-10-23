# Módulo: Default (Root & Health)

[⬅ Volver al Índice](../../README.md)

## Descripción

Endpoints raíz del sistema. Proporcionan información básica sobre el API y permiten verificar el estado de salud del servicio.

## Endpoints Disponibles

- **[GET /](endpoints/GET_root.md)** — Endpoint raíz del API
- **[GET /health](endpoints/GET_health.md)** — Health check del sistema

## Características

### GET /
- Proporciona información básica sobre el API
- Devuelve la versión, ambiente y enlaces a documentación
- **No requiere** el prefijo `/api/v1`

### GET /health
- Verifica el estado de salud del sistema
- Útil para monitoreo y balanceadores de carga
- **No requiere** el prefijo `/api/v1`

## Respuestas de Éxito

### GET / (200 OK)
```json
{
  "message": "Restaurant Backend API",
  "version": "1.0.0",
  "environment": "production",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

### GET /health (200 OK)
```json
{
  "status": "healthy",
  "service": "restaurant-backend",
  "version": "1.0.0",
  "environment": "production"
}
```

## URLs Completas

**Producción:**
- Root: `https://back-dp2.onrender.com/`
- Health: `https://back-dp2.onrender.com/health`

**Local:**
- Root: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/health`

## Notas Técnicas

- ⚠️ Estos endpoints **NO** usan el prefijo `/api/v1`
- ✅ Ambos endpoints son **públicos** y **no requieren autenticación**
- ✅ El health check siempre retorna **200 OK** si el servicio está activo
