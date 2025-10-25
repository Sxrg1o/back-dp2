# Módulo: Categorías

[⬅ Volver al Índice](../../README.md)

## Descripción

Gestión completa de categorías de productos del menú. Permite crear, listar, consultar, actualizar y eliminar categorías, además de obtener categorías con sus productos asociados.

## Recurso Base

```
/api/v1/categorias
```

## Endpoints Disponibles

### Crear Categoría
- **[POST /categorias](endpoints/POST_categorias.md)** — Crea una nueva categoría en el sistema

### Listar Categorías
- **[GET /categorias](endpoints/GET_categorias.md)** — Obtiene una lista paginada de categorías

### Consultar Categoría Individual
- **[GET /categorias/{categoria_id}](endpoints/GET_categorias_categoria_id.md)** — Obtiene los detalles de una categoría específica

### Actualizar Categoría
- **[PUT /categorias/{categoria_id}](endpoints/PUT_categorias_categoria_id.md)** — Actualiza los datos de una categoría existente

### Eliminar Categoría
- **[DELETE /categorias/{categoria_id}](endpoints/DELETE_categorias_categoria_id.md)** — Elimina una categoría del sistema

### Listar Categorías con Productos (Cards)
- **[GET /categorias/productos/cards](endpoints/GET_categorias_productos_cards.md)** — Obtiene todas las categorías con sus productos en formato minimal (solo ID, nombre e imagen)

## Schema Principal

**CategoriaResponse:**
```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Entradas",
  "descripcion": "Aperitivos y platos de entrada",
  "imagen_path": "/static/categorias/entradas.jpg",
  "orden": 1,
  "activo": true,
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T05:16:30.123456Z"
}
```

## Reglas de Negocio

- ✅ El **nombre** de la categoría es **único** en el sistema
- ✅ El campo `orden` permite controlar la secuencia de visualización
- ✅ El campo `activo` permite ocultar/mostrar categorías sin eliminarlas
- ✅ Una categoría puede tener múltiples productos asociados
- ⚠️ Actualmente no requiere autenticación

## Casos de Uso Relacionados

**HU-C02:** Cliente nuevo — Ubicar rápidamente las secciones clave de consumo  
**HU-C05:** Cliente explorando — Explorar la oferta vigente por categorías  
**HU-A03:** Admin — Activar/ocultar y ordenar productos/categorías

## Errores Comunes

| HTTP | Code | Descripción |
|------|------|-------------|
| 400 | `VALIDATION_ERROR` | Datos de entrada inválidos |
| 404 | `NOT_FOUND` | Categoría no encontrada |
| 409 | `CONFLICT` | Categoría con nombre duplicado |
| 500 | `INTERNAL_ERROR` | Error interno del servidor |
