# Módulo: Alérgenos

[⬅ Volver al Índice](../../README.md)

## Descripción

Gestión de alérgenos del sistema. Permite crear, listar, consultar, actualizar y eliminar alérgenos que pueden ser asociados a productos.

## Recurso Base

```
/api/v1/alergenos
```

## Endpoints Disponibles

- **[POST /alergenos](endpoints/POST_alergenos.md)** — Crea un nuevo alérgeno
- **[GET /alergenos](endpoints/GET_alergenos.md)** — Lista todos los alérgenos (paginado)
- **[GET /alergenos/{alergeno_id}](endpoints/GET_alergenos_alergeno_id.md)** — Obtiene un alérgeno por ID
- **[PUT /alergenos/{alergeno_id}](endpoints/PUT_alergenos_alergeno_id.md)** — Actualiza un alérgeno
- **[DELETE /alergenos/{alergeno_id}](endpoints/DELETE_alergenos_alergeno_id.md)** — Elimina un alérgeno

## Schema Principal

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

## Reglas de Negocio

- ✅ El **nombre** del alérgeno es **único** en el sistema
- ✅ Un producto puede tener hasta **10 alérgenos** asociados
- ✅ Catálogo de alérgenos centralizado y reutilizable

## Caso de Uso

**HU-C10:** Cliente con restricciones alimentarias — Ver alérgenos del producto elegido  
**HU-A04:** Admin — Gestionar alérgenos por producto

## Errores Comunes

| HTTP | Code | Descripción |
|------|------|-------------|
| 400 | `VALIDATION_ERROR` | Datos de entrada inválidos |
| 404 | `NOT_FOUND` | Alérgeno no encontrado |
| 409 | `CONFLICT` | Alérgeno con nombre duplicado |
| 500 | `INTERNAL_ERROR` | Error interno del servidor |
