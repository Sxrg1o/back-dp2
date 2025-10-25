# Catálogo de APIs — Restaurant Backend

> **Documentación oficial de los endpoints del backend del sistema de restaurante**

## 📋 OpenAPI Specification

**OpenAPI 3.1:** [`/openapi.json`](https://back-dp2.onrender.com/openapi.json) (generado automáticamente por FastAPI)

## 📚 Módulos

### Gestión de Recursos

- **[Roles](modulos/roles/README.md)** — Gestión de roles de usuario
- **[Categorías](modulos/categorias/README.md)** — Gestión de categorías de productos
- **[Alérgenos](modulos/alergenos/README.md)** — Gestión de alérgenos
- **[Productos](modulos/productos/README.md)** — Gestión de productos del menú
- **[Tipos de Opciones](modulos/tipos-opciones/README.md)** — Gestión de tipos de opciones para productos
- **[Producto Opciones](modulos/producto-opciones/README.md)** — Gestión de opciones específicas de productos

### Operaciones Especiales

- **[Sincronización](modulos/sync/README.md)** — Endpoints de sincronización con sistema externo (Domótica)
- **[Default](modulos/default/README.md)** — Endpoints raíz y health check

## ⚙️ Información Meta

- **[Overview](meta/overview.md)** — Arquitectura general del sistema
- **[Hosts](meta/hosts.md)** — Configuración de hosts por ambiente
- **[Autenticación](meta/auth.md)** — Esquemas de autenticación
- **[Convenciones](meta/conventions.md)** — Convenciones de API (fechas, paginación, errores)

## 🎯 Guía Rápida

### Base Path

Todos los endpoints (excepto `/` y `/health`) usan el prefijo:

```
/api/v1
```

### Hosts por Ambiente

- **Producción:** `https://back-dp2.onrender.com`
- **Local:** `http://127.0.0.1:8000`

### Ejemplo de URL Completa

```
{HOST}/api/v1/{recurso}
```

**Ejemplo:** `https://back-dp2.onrender.com/api/v1/productos?skip=0&limit=20`

## 📖 Formato de Documentación

Cada endpoint está documentado con:

- ✅ **META** — Información del endpoint (host, path, método, autenticación)
- ✅ **ENTRADA** — Query params, path params, headers, body
- ✅ **SALIDA** — Respuesta exitosa con ejemplos y diccionarios
- ✅ **ERRORES** — Códigos de error con Problem+JSON
- ✅ **URLs** — URLs completas y comandos cURL para Producción y Local

## 🚀 Navegación Rápida

| Módulo | Recurso Base | Descripción |
|--------|--------------|-------------|
| Roles | `/roles` | CRUD de roles del sistema |
| Categorías | `/categorias` | CRUD de categorías + vista con productos |
| Alérgenos | `/alergenos` | CRUD de alérgenos |
| Productos | `/productos` | CRUD de productos + vistas especiales (cards, opciones) |
| Tipos Opciones | `/tipos-opciones` | CRUD de tipos de opciones |
| Producto Opciones | `/producto-opciones` | CRUD de opciones de productos |
| Sincronización | `/sync` | Sincronización con Domótica (platos, mesas, enrich) |
| Default | `/` | Root y health check |
