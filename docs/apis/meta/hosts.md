# Hosts por Ambiente

[⬅ Volver al Índice](../README.md)

## Configuración de Hosts

El API está disponible en diferentes ambientes con las siguientes URLs base:

### **Producción**
```
https://back-dp2.onrender.com
```
- **Descripción:** Ambiente de producción en Render
- **Base Path:** `/api/v1`
- **URL Completa:** `https://back-dp2.onrender.com/api/v1`

### **Local**
```
http://127.0.0.1:8000
```
- **Descripción:** Ambiente local de desarrollo
- **Base Path:** `/api/v1`
- **URL Completa:** `http://127.0.0.1:8000/api/v1`

## Uso en Aplicaciones

### Variables de Entorno

Se recomienda configurar el host como variable de entorno:

```bash
# Producción
export API_HOST=https://back-dp2.onrender.com

# Local
export API_HOST=http://127.0.0.1:8000
```

### Construcción de URLs

Todas las URLs siguen el patrón:

```
{HOST}{BASE_PATH}{RECURSO}[?query_params]
```

**Ejemplo:**
```bash
# Producción
https://back-dp2.onrender.com/api/v1/productos?skip=0&limit=20

# Local
http://127.0.0.1:8000/api/v1/productos?skip=0&limit=20
```

## Endpoints Especiales

Los siguientes endpoints **NO** incluyen `/api/v1`:

- **`GET /`** — Root endpoint
- **`GET /health`** — Health check
- **`GET /openapi.json`** — OpenAPI specification
- **`GET /docs`** — Swagger UI
- **`GET /redoc`** — ReDoc UI

**Ejemplo:**
```bash
https://back-dp2.onrender.com/health
http://127.0.0.1:8000/docs
```
