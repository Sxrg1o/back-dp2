# 🧪 Scripts de Prueba para el Microservicio de Menú

Este directorio contiene una suite completa de scripts para probar y diagnosticar el microservicio de menú.

## 📋 Scripts Disponibles

### 1. 🚀 **run_all_tests.py** - Ejecutor Maestro
**Propósito**: Ejecuta todos los scripts de prueba en secuencia.

```bash
python run_all_tests.py
```

**Características**:
- ✅ Ejecuta todos los tests automáticamente
- 📊 Genera reporte consolidado
- ⏱️ Controla tiempos de ejecución
- 🔧 Proporciona recomendaciones

---

### 2. 🔍 **test_all_endpoints.py** - Prueba Completa
**Propósito**: Prueba exhaustiva de todos los endpoints GET.

```bash
python test_all_endpoints.py
python test_all_endpoints.py http://localhost:8002  # URL personalizada
```

**Características**:
- 🎯 Prueba 25+ endpoints diferentes
- ⚡ Mide rendimiento y tiempos de respuesta
- 📊 Genera reporte detallado en JSON
- 🔍 Diagnostica problemas específicos
- 📈 Estadísticas de rendimiento

**Endpoints probados**:
- Health checks (`/health`, `/`, `/info`)
- Documentación (`/docs`, `/redoc`)
- Ingredientes (CRUD + filtros + búsquedas)
- Ítems (CRUD + filtros + búsquedas)
- Relaciones (ítems con ingredientes)
- Administrativos (`/seed-data`)

---

### 3. ⚡ **quick_test.py** - Prueba Rápida
**Propósito**: Verificación rápida de endpoints principales.

```bash
python quick_test.py
```

**Características**:
- 🚀 Ejecución rápida (< 30 segundos)
- 🎯 Enfocado en endpoints críticos
- 📊 Resumen conciso
- 💡 Ideal para verificación rápida

**Endpoints probados**:
- Health check
- Listar ingredientes e ítems
- Ítems con ingredientes
- Filtros básicos

---

### 4. 🔧 **test_service_connectivity.py** - Diagnóstico de Conectividad
**Propósito**: Verifica la conectividad y estado del servicio.

```bash
python test_service_connectivity.py
python test_service_connectivity.py http://localhost:8002
```

**Características**:
- 🔌 Prueba conectividad básica
- 📋 Obtiene información del servicio
- 🗄️ Verifica acceso a base de datos
- ⚡ Mide rendimiento
- 🔍 Diagnóstico automático

---

### 5. 🗄️ **diagnose_db.py** - Diagnóstico de Base de Datos
**Propósito**: Verifica la integridad y contenido de la base de datos.

```bash
python diagnose_db.py
```

**Características**:
- 📁 Verifica existencia del archivo
- 🏗️ Valida estructura de tablas
- 📊 Cuenta registros por tabla
- 🔍 Analiza relaciones de datos
- 💡 Sugiere soluciones

---

### 6. 🥬 **test_items_with_ingredientes.py** - Prueba Específica
**Propósito**: Prueba específica del endpoint de ítems con ingredientes.

```bash
python test_items_with_ingredientes.py
```

**Características**:
- 🍽️ Prueba el nuevo endpoint optimizado
- 📊 Muestra datos detallados
- ⚡ Prueba de rendimiento
- 📈 Estadísticas de uso

---

## 🚀 Guía de Uso

### Para Desarrollo Diario
```bash
# Verificación rápida
python quick_test.py

# Si hay problemas, diagnóstico completo
python diagnose_db.py
python test_service_connectivity.py
```

### Para Testing Completo
```bash
# Ejecutar todas las pruebas
python run_all_tests.py

# O pruebas individuales
python test_all_endpoints.py
```

### Para Diagnóstico de Problemas
```bash
# 1. Verificar base de datos
python diagnose_db.py

# 2. Verificar conectividad
python test_service_connectivity.py

# 3. Prueba completa
python test_all_endpoints.py
```

---

## 📊 Interpretación de Resultados

### ✅ **Éxito Total**
- Todos los endpoints responden correctamente
- Base de datos accesible y con datos
- Tiempos de respuesta aceptables (< 1s)

### ⚠️ **Problemas Menores**
- Algunos endpoints fallan
- Base de datos accesible pero con problemas
- Tiempos de respuesta altos

### ❌ **Problemas Graves**
- Servicio no responde
- Base de datos inaccesible
- Múltiples endpoints fallan

---

## 🔧 Solución de Problemas

### Problema: "No se puede conectar al servicio"
**Soluciones**:
1. Verificar que el microservicio esté ejecutándose:
   ```bash
   python main.py
   ```
2. Verificar que el puerto 8002 esté disponible
3. Comprobar firewall/antivirus

### Problema: "Base de datos vacía"
**Soluciones**:
1. Cargar datos de prueba:
   ```bash
   python create_peru_data_simple.py
   ```
2. O usar el endpoint:
   ```bash
   curl -X POST http://localhost:8002/seed-data
   ```

### Problema: "Endpoints lentos"
**Soluciones**:
1. Verificar recursos del sistema
2. Optimizar consultas de base de datos
3. Implementar cache

### Problema: "Errores 500"
**Soluciones**:
1. Revisar logs del microservicio
2. Verificar configuración de base de datos
3. Comprobar dependencias

---

## 📈 Métricas de Rendimiento

### Tiempos Esperados
- **Health check**: < 100ms
- **Listar ingredientes**: < 200ms
- **Listar ítems**: < 300ms
- **Ítems con ingredientes**: < 500ms

### Indicadores de Problemas
- **> 1 segundo**: Lento, revisar optimizaciones
- **> 5 segundos**: Muy lento, problema de rendimiento
- **Timeout**: Servicio no responde

---

## 🛠️ Personalización

### Cambiar URL del Servicio
```python
# En cualquier script
tester = MenuServiceTester("http://mi-servidor:8002")
```

### Agregar Nuevos Endpoints
```python
# En test_all_endpoints.py
self.test_endpoint("GET", "/mi-nuevo-endpoint", "Mi nuevo endpoint")
```

### Modificar Timeouts
```python
# En test_service_connectivity.py
tester = ServiceConnectivityTester()
tester.timeout = 30  # 30 segundos
```

---

## 📚 Archivos de Reporte

Los scripts generan archivos de reporte:
- `test_report_YYYYMMDD_HHMMSS.json`: Reporte detallado
- Logs en consola con emojis para fácil lectura

---

## 🎯 Mejores Prácticas

1. **Ejecutar quick_test.py** antes de commits
2. **Usar run_all_tests.py** antes de releases
3. **Diagnosticar con diagnose_db.py** cuando hay problemas
4. **Monitorear rendimiento** regularmente
5. **Mantener datos de prueba** actualizados

---

**¡Happy Testing! 🧪✨**
