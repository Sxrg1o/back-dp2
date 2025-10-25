# 🌱 Endpoint de Enriquecimiento de Datos

## 📋 Descripción

El endpoint `/api/v1/sync/enrich` permite enriquecer los datos existentes en la base de datos con información complementaria después de sincronizar los productos desde Domotica.

---

## 🎯 ¿Cuándo usar este endpoint?

**Ejecutar DESPUÉS de:**
1. ✅ Sincronizar productos con `POST /api/v1/sync/platos`
2. ✅ Verificar que los productos se crearon correctamente

**NO ejecutar ANTES de** tener productos en la base de datos.

---

## 🚀 Uso

### Request

```http
POST /api/v1/sync/enrich
Content-Type: application/json
```

**No requiere body** - El endpoint procesa automáticamente todos los productos existentes.

### Response Exitoso (200 OK)

```json
{
  "status": "success",
  "message": "Enriquecimiento completado exitosamente",
  "data": {
    "productos_procesados": 274,
    "alergenos_creados": 8,
    "alergenos_totales": 8,
    "tipos_opciones_creados": 4,
    "tipos_opciones_totales": 4
  }
}
```

### Response de Error (500 Internal Server Error)

```json
{
  "detail": "Error durante el enriquecimiento: [mensaje de error]"
}
```

---

## 🔧 ¿Qué hace el endpoint?

### 1. **Crea Alérgenos** (8 alérgenos comunes)
- 🥜 Maní
- 🦞 Mariscos
- 🐟 Pescado
- 🥛 Lácteos
- 🌾 Gluten
- 🥚 Huevos
- 🌰 Frutos Secos
- 🌶️ Ají

### 2. **Crea Tipos de Opciones** (4 tipos)
- 🌶️ Nivel de Ají (mínimo: 1, máximo: 1)
- 🍚 Acompañamiento (mínimo: 0, máximo: 3)
- 🥤 Bebida (mínimo: 0, máximo: 2)
- ➕ Extras (mínimo: 0, máximo: 5)

### 3. **Asocia Alérgenos a Productos**
Usando reglas inteligentes basadas en nombres:
- Productos con "CEVICHE" → Mariscos, Pescado, Ají
- Productos con "ARROZ CON MARISCOS" → Mariscos, Ají
- Productos con "CAUSA" → Huevos (presente), Mariscos (posible)
- Etc.

### 4. **Crea Opciones de Productos**
Para cada producto según su categoría:
- **Nivel de Ají**: Sin ají, Leve, Medio, Picante, Extra picante
- **Acompañamientos**: Arroz blanco, Yuca frita, Camote frito, Choclo
- **Bebidas**: Chicha morada, Inca Kola, Agua, Limonada
- **Extras**: Porción extra de limón, Ají extra, Cancha, Salsa criolla

### 5. **Crea Roles de Usuario** (si no existen)
- 👤 Cliente (usuario común)
- 👨‍🍳 Chef (cocina)
- 🎯 Mozo (atención)
- 👑 Admin (administrador)

### 6. **Actualiza Imágenes**
Asigna URLs de imágenes desde el seed data:
- 25 productos con imágenes de Google Drive
- 23 categorías con imágenes

---

## 📊 Ejemplo de Flujo Completo

```bash
# 1. Sincronizar productos desde Domotica (scraper)
curl -X POST http://localhost:8000/api/v1/sync/platos \
  -H "Content-Type: application/json" \
  -d @productos_domotica.json

# Respuesta: 274 productos sincronizados

# 2. Enriquecer datos
curl -X POST http://localhost:8000/api/v1/sync/enrich

# Respuesta:
# {
#   "status": "success",
#   "message": "Enriquecimiento completado exitosamente",
#   "data": {
#     "productos_procesados": 274,
#     "alergenos_creados": 8,
#     "tipos_opciones_creados": 4
#   }
# }

# 3. Verificar productos con opciones
curl http://localhost:8000/api/v1/productos/{producto_id}/opciones
```

---

## ⚠️ Consideraciones Importantes

### ✅ Es Seguro Re-ejecutar
- El endpoint verifica si los alérgenos/opciones ya existen antes de crearlos
- No duplica datos
- Puedes ejecutarlo múltiples veces sin problemas

### 🔄 Idempotente
- Primera ejecución: Crea todo
- Segunda ejecución: Solo actualiza si hay cambios
- Tercera ejecución: No hace nada si todo está actualizado

### ⏱️ Tiempo de Ejecución
- ~5-10 segundos para 274 productos
- Depende de la cantidad de productos en la BD

### 📝 Logs
El endpoint genera logs detallados:
```
🌱 Iniciando enriquecimiento de datos...
📊 Estado inicial: 274 productos, 0 alérgenos, 0 tipos de opciones
✅ Enriquecimiento completado: 8 alérgenos nuevos, 4 tipos nuevos
```

---

## 🐛 Troubleshooting

### Error: "No se encontraron productos"
**Solución**: Ejecutar primero `POST /api/v1/sync/platos`

### Error: "Error durante el enriquecimiento: [...]"
**Solución**: 
1. Verificar logs del servidor
2. Asegurarse de que la BD tiene productos
3. Verificar que el script `scripts/enrich_existing_data.py` existe

### Enriquecimiento muy lento
**Solución**: 
- Normal para >500 productos
- Considerar ejecutar el script directamente: `python -m scripts.enrich_existing_data`

---

## 🔗 Endpoints Relacionados

- `POST /api/v1/sync/platos` - Sincronizar productos desde Domotica
- `GET /api/v1/productos` - Listar productos
- `GET /api/v1/productos/{id}/opciones` - Ver producto con opciones
- `GET /api/v1/alergenos` - Listar alérgenos

---

## 📚 Referencias

- Script original: `scripts/enrich_existing_data.py`
- Controlador: `src/api/controllers/sync_controller.py`
- Documentación de testing: `docs/testing.md`
