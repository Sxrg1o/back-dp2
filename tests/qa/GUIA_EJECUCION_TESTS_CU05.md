# Guía de Ejecución de Tests CU-05 en Windows

## 📋 Archivos Disponibles

Se han creado **3 versiones** del mismo test de validaciones:

1. **`test_cu05_validaciones_errores.sh`** - Original (Bash/Linux) ❌ No funciona en Windows
2. **`test_cu05_validaciones_errores.bat`** - Nativo Windows ✅ Requiere curl
3. **`test_cu05_validaciones_errores.py`** - Python ✅ **RECOMENDADO** (multiplataforma)

---

## 🚀 Opción 1: Ejecutar con Python (RECOMENDADO)

### Ventajas
- ✅ No requiere herramientas externas
- ✅ Multiplataforma (Windows/Linux/Mac)
- ✅ Más robusto y con mejor manejo de errores
- ✅ Colores en la terminal
- ✅ Fácil de mantener

### Requisitos
```bash
pip install requests
```

### Uso Básico
```bash
# 1. Inicia el servidor en una terminal
cd back-dp2
venv\Scripts\activate
python -m uvicorn src.main:app --reload

# 2. En otra terminal, ejecuta los tests
cd back-dp2
venv\Scripts\activate
python tests/qa/test_cu05_validaciones_errores.py
```

### Opciones Avanzadas
```bash
# Especificar puerto diferente
python tests/qa/test_cu05_validaciones_errores.py --port 8001

# Especificar URL completa
python tests/qa/test_cu05_validaciones_errores.py --url http://localhost:8001

# Modo verbose (muestra respuestas completas)
python tests/qa/test_cu05_validaciones_errores.py --verbose

# Sin colores
python tests/qa/test_cu05_validaciones_errores.py --no-color

# Ayuda
python tests/qa/test_cu05_validaciones_errores.py --help
```

---

## 🚀 Opción 2: Ejecutar con BAT (Windows)

### Ventajas
- ✅ Nativo de Windows
- ✅ No requiere Python adicional

### Desventajas
- ❌ Requiere `curl` instalado
- ❌ Solo funciona en Windows

### Requisitos
- **curl** debe estar instalado (viene con Windows 10+)

### Verificar curl
```cmd
curl --version
```

Si no está instalado, instala [Git for Windows](https://git-scm.com/download/win) que incluye curl.

### Uso Básico
```cmd
# 1. Inicia el servidor en una terminal
cd back-dp2
venv\Scripts\activate
python -m uvicorn src.main:app --reload

# 2. En otra terminal, ejecuta los tests
cd back-dp2
tests\qa\test_cu05_validaciones_errores.bat
```

### Opciones Avanzadas
```cmd
# Especificar URL diferente
set API_URL=http://localhost:8001
tests\qa\test_cu05_validaciones_errores.bat

# Modo verbose
set VERBOSE=true
tests\qa\test_cu05_validaciones_errores.bat
```

---

## 📊 Ejemplo de Salida

```
==========================================
  CU-05: Validaciones y Errores
==========================================

Configuración
API Base URL: http://localhost:8000
Ambiente: Local

Verificando API en http://localhost:8000... ✓ OK

Commit: a3f2d1c
Rama: main
Fecha: 2025-11-10 15:30:45

=== Tests de Validación de Mesa ===

TC-01: Mesa inexistente debe retornar 400... ✓ PASS (Status: 400)
TC-02: Mesa vacía debe retornar 422... ✓ PASS (Status: 422)

=== Tests de Validación de Productos ===

Obteniendo mesa para tests... ✓ OK (01JMESA123...)
TC-03: Producto inexistente debe retornar 400... ✓ PASS (Status: 400)

[... más tests ...]

==========================================
  Resumen de Tests
==========================================
Total:  11
Pasados: 11
Fallidos: 0
Éxito: 100%

✓ Todos los tests pasaron
```

---

## 🔧 Solución de Problemas

### Error: API no disponible

**Causa:** El servidor no está corriendo.

**Solución:**
```bash
cd back-dp2
venv\Scripts\activate
python -m uvicorn src.main:app --reload
```

### Error: `curl` no encontrado (solo BAT)

**Causa:** curl no está en el PATH.

**Solución:**
- Instala [Git for Windows](https://git-scm.com/download/win)
- O usa la versión de Python en su lugar

### Error: `requests` no encontrado (solo Python)

**Causa:** Librería requests no instalada.

**Solución:**
```bash
pip install requests
```

### Error: Puerto ocupado

**Causa:** Ya hay un servidor corriendo en ese puerto.

**Solución:**
```bash
# Usa un puerto diferente
python -m uvicorn src.main:app --reload --port 8001

# Luego ejecuta tests con ese puerto
python tests/qa/test_cu05_validaciones_errores.py --port 8001
```

---

## 📝 Casos de Prueba Incluidos

Los 3 archivos ejecutan los mismos 11 tests:

### Tests de Validación de Mesa (2)
- TC-01: Mesa inexistente → 400
- TC-02: Mesa vacía → 422

### Tests de Validación de Productos (1)
- TC-03: Producto inexistente → 400

### Tests de Validación de Cantidad (2)
- TC-04: Cantidad = 0 → 422
- TC-05: Cantidad negativa → 422

### Tests de Validación de Precio (2)
- TC-06: Precio = 0 → 422
- TC-07: Precio negativo → 422

### Tests de Validación de Items (1)
- TC-08: Items vacío → 422

### Tests de Validación de Pedido Inexistente (3)
- TC-09: GET pedido inexistente → 404
- TC-10: PATCH pedido inexistente → 404
- TC-11: DELETE pedido inexistente → 404

---

## 🎯 Recomendación Final

**Usa la versión de Python** (`test_cu05_validaciones_errores.py`):
- Es la más robusta y mantenible
- Funciona en cualquier plataforma
- Mejor manejo de errores
- Más opciones de configuración

```bash
python tests/qa/test_cu05_validaciones_errores.py --verbose
```
