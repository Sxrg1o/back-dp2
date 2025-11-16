# Quick Start - Tests QA Locales

## ¿Qué es este directorio?

Este directorio contiene scripts de tests para validar la funcionalidad del caso de uso CU-05 (Validaciones y Errores) en la API de pedidos.

**Tests disponibles:**
- `test_cu05_validaciones_errores.sh` - Script de tests en bash
- `run_tests_local.py` - Ejecutor Python (recomendado)
- `run_tests_local.bat` - Ejecutor Windows

---

## Inicio Rápido

### Opción 1: Con Python (Recomendado)

```bash
# Terminal 1: Iniciar el servidor
cd back-dp2
source venv/bin/activate  # En Windows: venv\Scripts\activate
python -m uvicorn src.main:app --reload

# Terminal 2: Ejecutar tests
cd back-dp2
python tests/qa/run_tests_local.py
```

### Opción 2: Con Bash (Linux/Mac/WSL)

```bash
# Terminal 1: Iniciar el servidor
cd back-dp2
source venv/bin/activate
python -m uvicorn src.main:app --reload

# Terminal 2: Ejecutar tests
cd back-dp2
bash tests/qa/test_cu05_validaciones_errores.sh
```

### Opción 3: Con Batch (Windows)

```cmd
REM Terminal 1: Iniciar el servidor
cd back-dp2
venv\Scripts\activate
python -m uvicorn src.main:app --reload

REM Terminal 2: Ejecutar tests
cd tests\qa
run_tests_local.bat
```

---

## Opciones Avanzadas

### Con puerto personalizado

```bash
# Python
python tests/qa/run_tests_local.py --port 8001

# Bash
API_URL=http://localhost:8001 bash tests/qa/test_cu05_validaciones_errores.sh

# Batch
run_tests_local.bat 8001
```

### Modo verbose (ver respuestas completas)

```bash
# Python
python tests/qa/run_tests_local.py --verbose

# Bash
VERBOSE=true bash tests/qa/test_cu05_validaciones_errores.sh
```

---

## Resultados Esperados

**11 Tests** divididos en:

| Grupo | Tests | Código HTTP Esperado |
|-------|-------|---------------------|
| Validación de Mesa | 2 | 400, 422 |
| Validación de Producto | 1 | 400 |
| Validación de Cantidad | 2 | 422 |
| Validación de Precio | 2 | 422 |
| Items Vacíos | 1 | 422 |
| Pedido Inexistente | 3 | 404 |

**Ejemplo de salida:**
```
Total:  11
Pasados: 11
Fallidos: 0
Éxito: 100%

✓ Todos los tests pasaron
```

---

## Solución de Problemas

### "API no disponible"
→ Asegúrate de que el servidor está corriendo en Terminal 1

### "No se encontró mesa/producto válido"
→ Ejecuta: `python scripts/seed_cevicheria_data.py` antes de los tests

### "curl: command not found"
→ Instala curl o usa la opción Python

### "bash: command not found" (Windows)
→ Usa `run_tests_local.py` o `run_tests_local.bat`

---

## Documentación Completa

Ver `README_LOCAL.md` para instrucciones detalladas y solución de problemas.

---

## Contacto

**Tester:** Kevin Antonio Navarro Carrera  
**Última actualización:** 2025-11-09
