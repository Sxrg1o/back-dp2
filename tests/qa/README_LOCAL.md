# Guía de Ejecución de Tests QA en Ambiente Local

## 📋 Archivos Disponibles

### Tests CU-05 (Validaciones y Errores)

**3 versiones del mismo test:**

1. **`test_cu05_validaciones_errores.py`** ⭐ **RECOMENDADO**
   - Multiplataforma (Windows/Linux/Mac)
   - No requiere herramientas externas (solo Python + requests)
   - Mejor manejo de errores y salida formateada

2. **`test_cu05_validaciones_errores.bat`**
   - Nativo de Windows
   - Requiere `curl` instalado

3. **`test_cu05_validaciones_errores.sh`**
   - Original en Bash (Linux/Mac)
   - Requiere Git Bash o WSL en Windows

**Ver `GUIA_EJECUCION_TESTS_CU05.md` para detalles completos de cada versión.**

---

## Requisitos Previos

- **Python 3.9+** instalado
- **bash** (shell de Linux/Mac o WSL en Windows)
- **curl** instalado
- Estar en la rama correcta del proyecto

## Paso 1: Preparar el Entorno Virtual

```bash
# Navega a la carpeta del backend
cd back-dp2

# Crea el entorno virtual (si no existe)
python -m venv venv

# Actívalo
# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

## Paso 2: Instalar Dependencias

```bash
# Instala las dependencias del proyecto
pip install -r requirements.txt

# Para Windows, usa:
pip install -r requirements-windows.txt
```

## Paso 3: Iniciar el Servidor Local

En una terminal (con el entorno virtual activado):

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Verifica que el servidor esté corriendo visitando:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/openapi.json

## Paso 4: Ejecutar los Tests (en otra terminal)

En otra terminal, ejecuta:

```bash
# Asegúrate de estar en la raíz del proyecto
cd back-dp2

# Activa el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# OPCIÓN A: Usar Python (RECOMENDADO para Windows)
python tests/qa/test_cu05_validaciones_errores.py

# OPCIÓN B: Usar BAT (solo Windows, requiere curl)
tests\qa\test_cu05_validaciones_errores.bat

# OPCIÓN C: Usar Bash (Linux/Mac o Git Bash en Windows)
bash tests/qa/test_cu05_validaciones_errores.sh
```

### Opciones de Ejecución

#### Python (todas las plataformas):
```bash
# Puerto personalizado
python tests/qa/test_cu05_validaciones_errores.py --port 8001

# URL completa
python tests/qa/test_cu05_validaciones_errores.py --url http://localhost:8001

# Modo verbose
python tests/qa/test_cu05_validaciones_errores.py --verbose

# Ver ayuda
python tests/qa/test_cu05_validaciones_errores.py --help
```

#### BAT (Windows):
```cmd
# Puerto personalizado
set API_URL=http://localhost:8001
tests\qa\test_cu05_validaciones_errores.bat

# Modo verbose
set VERBOSE=true
tests\qa\test_cu05_validaciones_errores.bat
```

#### Bash (Linux/Mac/Git Bash):
```bash
# Puerto personalizado
API_URL=http://localhost:8001 bash tests/qa/test_cu05_validaciones_errores.sh

# Modo verbose
VERBOSE=true bash tests/qa/test_cu05_validaciones_errores.sh

# Combinar ambas opciones
API_URL=http://localhost:8001 VERBOSE=true bash tests/qa/test_cu05_validaciones_errores.sh
```

## Resultados Esperados

El script ejecutará **11 tests** y mostrará:

```
✓ TC-1: Mesa inexistente (esperado 400)
✓ TC-2: Mesa vacía (esperado 422)
✓ TC-3: Producto inexistente (esperado 400)
✓ TC-4: Cantidad = 0 (esperado 422)
✓ TC-5: Cantidad negativa (esperado 422)
✓ TC-6: Precio = 0 (esperado 422)
✓ TC-7: Precio negativo (esperado 422)
✓ TC-8: Items vacío (esperado 422)
✓ TC-9: GET pedido inexistente (esperado 404)
✓ TC-10: PATCH pedido inexistente (esperado 404)
✓ TC-11: DELETE pedido inexistente (esperado 404)

Resumen:
Total: 11 | Pasados: 11 | Fallidos: 0 | Éxito: 100%
```

## Solución de Problemas

### "API no disponible en http://localhost:8000"

**Causa:** El servidor no está corriendo o no está en ese puerto.

**Solución:**
```bash
# Asegúrate de que el servidor esté corriendo
python -m uvicorn src.main:app --reload

# Si usas otro puerto, especifícalo:
API_URL=http://localhost:8001 bash tests/qa/test_cu05_validaciones_errores.sh
```

### "No se encontró mesa/producto válido"

**Causa:** La base de datos está vacía.

**Solución:**
```bash
# Ejecuta el script de seed para cargar datos:
python scripts/seed_cevicheria_data.py

# O sincroniza datos:
python scripts/sincronizar_datos.py
```

### "Permission denied: tests/qa/test_cu05_validaciones_errores.sh"

**Causa:** El script no tiene permisos de ejecución.

**Solución:**
```bash
chmod +x tests/qa/test_cu05_validaciones_errores.sh
```

### Error con Python en el script

**Causa:** `python3` no está en el PATH.

**Solución:**
```bash
# Edita el script y cambia `python3 -c` a `python -c`
# O instala python3:
which python3  # Para verificar
```

## Mapeo de Códigos HTTP

| TC | Test | Código | Significado |
|----|----|--------|-------------|
| 1 | Mesa inexistente | 400 | Bad Request - Datos semánticamente inválidos |
| 2 | Mesa vacía | 422 | Unprocessable Entity - Validación de schema falla |
| 3 | Producto inexistente | 400 | Bad Request |
| 4 | Cantidad = 0 | 422 | Unprocessable Entity |
| 5 | Cantidad negativa | 422 | Unprocessable Entity |
| 6 | Precio = 0 | 422 | Unprocessable Entity |
| 7 | Precio negativo | 422 | Unprocessable Entity |
| 8 | Items vacío | 422 | Unprocessable Entity |
| 9 | GET pedido inexistente | 404 | Not Found |
| 10 | PATCH pedido inexistente | 404 | Not Found |
| 11 | DELETE pedido inexistente | 404 | Not Found |

## Notas Importantes

- Los tests se ejecutan contra la API en tiempo real
- Se requiere acceso a la base de datos para obtener mesas y productos válidos
- El entorno debe estar correctamente configurado en `.env`
- Los tests son idempotentes (puedes ejecutarlos múltiples veces)

## Contacto

**Tester Responsable:** Kevin Antonio Navarro Carrera  
**Fecha de Creación:** 2025-11-05  
**Última Actualización:** 2025-11-09
