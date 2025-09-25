# 🚀 Guía de Despliegue en Render

Esta guía te ayudará a desplegar tu API de Gestión de Restaurante en Render de forma fácil y rápida.

## 📋 Prerrequisitos

1. **Cuenta en Render**: [render.com](https://render.com)
2. **Código en GitHub**: Tu proyecto debe estar en un repositorio de GitHub
3. **Git configurado**: Para hacer push de cambios

## 🔧 Preparación del Proyecto

### 1. Archivos de Configuración Creados

Ya se han creado los siguientes archivos necesarios:

- ✅ `render.yaml` - Configuración de servicios
- ✅ `Procfile` - Comando de inicio
- ✅ `runtime.txt` - Versión de Python
- ✅ `requirements.txt` - Dependencias actualizadas

### 2. Verificar Estructura del Proyecto

```
back-dp2/
├── app/
│   ├── main.py              # ✅ Punto de entrada
│   ├── models/              # ✅ Modelos de datos
│   ├── services/            # ✅ Lógica de negocio
│   └── data/                # ✅ Datos estáticos
├── tests/                   # ✅ Tests organizados
├── requirements.txt         # ✅ Dependencias
├── render.yaml             # ✅ Configuración Render
├── Procfile                # ✅ Comando de inicio
├── runtime.txt             # ✅ Versión Python
└── README.md               # ✅ Documentación
```

## 🚀 Pasos para Desplegar

### Paso 1: Subir Código a GitHub

```bash
# 1. Inicializar repositorio (si no existe)
git init

# 2. Agregar archivos
git add .

# 3. Hacer commit
git commit -m "Preparar proyecto para despliegue en Render"

# 4. Conectar con GitHub (reemplaza con tu URL)
git remote add origin https://github.com/tu-usuario/back-dp2.git

# 5. Subir código
git push -u origin main
```

### Paso 2: Crear Servicio en Render

1. **Ir a Render**: [dashboard.render.com](https://dashboard.render.com)

2. **Crear Nuevo Servicio**:
   - Click en "New +"
   - Seleccionar "Web Service"

3. **Conectar Repositorio**:
   - Seleccionar tu repositorio de GitHub
   - Branch: `main`

4. **Configurar Servicio**:
   ```
   Name: menu-api-restaurante
   Environment: Python 3
   Region: Oregon (US West)
   Branch: main
   Root Directory: (dejar vacío)
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Variables de Entorno** (opcional):
   ```
   PYTHONPATH = /opt/render/project/src
   PYTHONUNBUFFERED = 1
   ```

6. **Configurar Health Check**:
   - Health Check Path: `/health`

### Paso 3: Desplegar

1. **Click en "Create Web Service"**
2. **Esperar el Build**: Render construirá tu aplicación
3. **Verificar Logs**: Revisar que no hay errores
4. **Probar la API**: Usar la URL proporcionada

## 🔍 Verificación del Despliegue

### URLs de Prueba

Una vez desplegado, prueba estas URLs:

```bash
# Health Check
GET https://tu-app.onrender.com/health

# Documentación API
GET https://tu-app.onrender.com/docs

# Menú completo
GET https://tu-app.onrender.com/api/menu/completo

# Items disponibles
GET https://tu-app.onrender.com/api/menu/items/disponibles

# Estadísticas
GET https://tu-app.onrender.com/api/menu/estadisticas
```

### Comandos de Prueba

```bash
# Probar con curl
curl https://tu-app.onrender.com/health

# Probar con PowerShell (Windows)
Invoke-RestMethod -Uri "https://tu-app.onrender.com/health"

# Probar con Python
import requests
response = requests.get("https://tu-app.onrender.com/health")
print(response.json())
```

## ⚙️ Configuración Avanzada

### 1. Dominio Personalizado

Si tienes un dominio propio:

1. En Render Dashboard → Tu Servicio → Settings
2. Custom Domains → Add Custom Domain
3. Seguir las instrucciones de DNS

### 2. Variables de Entorno

Para configuraciones específicas:

```bash
# En Render Dashboard → Environment
PYTHONPATH=/opt/render/project/src
PYTHONUNBUFFERED=1
DEBUG=False
LOG_LEVEL=INFO
```

### 3. Auto-Deploy

Para despliegues automáticos:

1. Settings → Auto-Deploy
2. Activar "Auto-Deploy"
3. Seleccionar branch (main)

## 🐛 Solución de Problemas

### Error: "Module not found"

**Problema**: No encuentra módulos de la app
**Solución**: Verificar que `PYTHONPATH` esté configurado

### Error: "Port binding"

**Problema**: No puede usar el puerto
**Solución**: Usar `$PORT` en el comando de inicio

### Error: "Build failed"

**Problema**: Fallo en la instalación de dependencias
**Solución**: 
1. Verificar `requirements.txt`
2. Revisar logs de build
3. Probar localmente primero

### Error: "Health check failed"

**Problema**: El health check no responde
**Solución**: 
1. Verificar que `/health` endpoint existe
2. Revisar logs de la aplicación
3. Probar endpoint manualmente

## 📊 Monitoreo

### Logs en Tiempo Real

1. Render Dashboard → Tu Servicio → Logs
2. Ver logs en tiempo real
3. Filtrar por nivel de log

### Métricas

1. Render Dashboard → Tu Servicio → Metrics
2. Ver CPU, memoria, requests
3. Configurar alertas si es necesario

## 🔄 Actualizaciones

### Desplegar Cambios

```bash
# 1. Hacer cambios en tu código
# 2. Commit y push
git add .
git commit -m "Nueva funcionalidad"
git push origin main

# 3. Render detectará cambios automáticamente
# 4. Esperar nuevo despliegue
```

### Rollback

Si algo sale mal:

1. Render Dashboard → Tu Servicio → Deploys
2. Seleccionar versión anterior
3. Click en "Rollback"

## 💰 Costos

### Plan Gratuito

- ✅ 750 horas/mes gratis
- ✅ Sleep después de 15 min de inactividad
- ✅ 512 MB RAM
- ✅ 0.1 CPU

### Plan Pago

- 💰 $7/mes por servicio
- ✅ Siempre activo
- ✅ 512 MB RAM
- ✅ 0.1 CPU
- ✅ Dominio personalizado

## 🎯 Próximos Pasos

1. **Configurar CI/CD**: GitHub Actions para tests automáticos
2. **Base de Datos**: Agregar PostgreSQL para persistencia
3. **Monitoreo**: Configurar alertas y métricas
4. **Backup**: Configurar respaldos automáticos
5. **SSL**: Configurar HTTPS (automático en Render)

## 📞 Soporte

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **GitHub Issues**: Para problemas del código

---

**¡Tu API estará disponible en: `https://tu-app.onrender.com`** 🎉
