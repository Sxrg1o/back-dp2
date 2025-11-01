# Tests de QA para HU-C07

Este directorio contiene scripts de prueba automatizados para validar la Historia de Usuario HU-C07: "Añadir extras disponibles a mi selección".

## Contenido

- `test_hu_c07_api.sh` - Tests de endpoints de API
- `test_hu_c07_precios.py` - Tests de validación de cálculos de precios
- `README_QA.md` - Esta documentación

## Prerequisitos

### Para tests de API (Bash)
- `curl` instalado
- `python3` instalado (para formatear JSON)
- Acceso a internet (para probar contra backend remoto)

### Para tests de precios (Python)
- Python 3.8+
- Biblioteca `requests`:
  ```bash
  pip install requests
  ```

## Ejecución de Tests

### 1. Tests de API

Ejecuta todos los tests de endpoints:

```bash
cd tests/qa
chmod +x test_hu_c07_api.sh
./test_hu_c07_api.sh
```

**Con modo verbose** (muestra respuestas completas):
```bash
VERBOSE=true ./test_hu_c07_api.sh
```

**Contra backend local** (si tienes uno levantado):
```bash
API_URL=http://localhost:8000 ./test_hu_c07_api.sh
```

#### Qué valida este script:

- ✅ Health check del backend
- ✅ Endpoint de listado de productos (`/productos/cards`)
- ✅ Endpoint de categorías
- ✅ Endpoint de tipos de opciones
- ✅ Endpoint de producto-opciones
- ✅ Estructura de datos (campos requeridos)
- ✅ Endpoint de producto con opciones (`/productos/{id}/opciones`)

### 2. Tests de Validación de Precios

Ejecuta tests de cálculos de precios:

```bash
cd tests/qa
python3 test_hu_c07_precios.py
```

**Contra backend local**:
```bash
API_URL=http://localhost:8000 python3 test_hu_c07_precios.py
```

#### Qué valida este script:

- ✅ Cálculo básico: precio_base + opciones
- ✅ Multiplicación por cantidad
- ✅ Opciones sin costo adicional (S/0.00)
- ✅ Precisión de decimales (ej: S/3.50)
- ✅ Cálculo con productos reales de la API

## Ejemplos de Salida

### Test de API exitoso:
```
==========================================
  Test HU-C07: Opciones de Productos
==========================================

API Base URL: https://back-dp2.onrender.com

=== Tests de Endpoints ===

Test 1: Health check del backend... ✓ PASS (Status: 200)
Test 2: GET /productos/cards (listar productos)... ✓ PASS (Status: 200)
Test 3: GET /categorias (listar categorías)... ✓ PASS (Status: 200)
...

==========================================
  Resumen de Tests
==========================================
Total:  9
Pasados: 9
Fallidos: 0

✓ Todos los tests pasaron
```

### Test de Precios exitoso:
```
==================================================
  Tests de Validación de Precios HU-C07
==================================================

=== Test 1: Cálculo Básico de Precios ===

Precio base: S/35.00
Opciones seleccionadas:
  - Familiar (4 personas): +S/30.00
  - Ají extra picante: +S/2.00
Precio calculado: S/67.00
Precio esperado:  S/67.00
✓ PASS - Cálculo correcto

...

==================================================
  Resumen de Tests de Precios
==================================================
Total:   5
Pasados: 5
Fallidos: 0

✓ Todos los tests de precios pasaron
```

## Interpretación de Resultados

### Estados de Tests:

- **✓ PASS** (Verde) - Test pasó correctamente
- **✗ FAIL** (Rojo) - Test falló, requiere atención
- **⚠ SKIP** (Amarillo) - Test omitido por falta de datos

### Códigos de Salida:

- `0` - Todos los tests pasaron
- `1` - Al menos un test falló

## Casos de Uso

### Durante Desarrollo

Ejecuta los tests después de hacer cambios en el backend para asegurar que HU-C07 sigue funcionando:

```bash
# Tests rápidos de API
./test_hu_c07_api.sh

# Si pasaron, ejecutar validación de precios
python3 test_hu_c07_precios.py
```

### Antes de Deploy

Ejecuta contra el ambiente de staging:

```bash
API_URL=https://staging.tu-app.com ./test_hu_c07_api.sh
API_URL=https://staging.tu-app.com python3 test_hu_c07_precios.py
```

### Integración CI/CD

Puedes integrar estos scripts en tu pipeline:

```yaml
# .github/workflows/qa.yml
- name: Run QA Tests
  run: |
    cd tests/qa
    ./test_hu_c07_api.sh
    python3 test_hu_c07_precios.py
```

## Metodología de Testing

### Enfoque Híbrido (IA + Humano)

Estos scripts automatizan la parte técnica del testing:

**IA/Scripts automatizan:**
- ✅ Pruebas de endpoints de API
- ✅ Validación de estructura de datos
- ✅ Cálculos matemáticos de precios
- ✅ Tests de regresión

**QA Humano valida:**
- 👤 Experiencia de usuario (UX/UI)
- 👤 Flujos de navegación
- 👤 Validación visual
- 👤 Casos edge no previstos

### Cobertura de Testing

Para HU-C07, estos scripts cubren:

| Aspecto | Cobertura | Método |
|---------|-----------|--------|
| Endpoints de API | 100% | Script bash |
| Cálculos de precios | 100% | Script Python |
| Integración backend-frontend | Manual | QA Humano |
| Usabilidad de UI | Manual | QA Humano |

## Troubleshooting

### Error: "curl: command not found"
```bash
# macOS
brew install curl

# Ubuntu/Debian
sudo apt-get install curl
```

### Error: "requests module not found"
```bash
pip3 install requests
```

### Error: "Connection refused"
Verifica que el backend esté ejecutándose:
```bash
curl https://back-dp2.onrender.com/health
```

### Tests fallan contra localhost
Asegúrate de que el backend local esté levantado:
```bash
cd ../../
uvicorn src.main:app --reload --port 8000
```

## Mantenimiento

### Actualizar URL del Backend

Edita la variable `API_URL` en cada script o usa variables de entorno:

```bash
export API_URL=https://nuevo-backend.com
./test_hu_c07_api.sh
```

### Agregar Nuevos Tests

Para agregar nuevos tests de precios, edita `test_hu_c07_precios.py` y agrega una nueva función:

```python
def test_nuevo_caso(results: TestResult):
    """Test N: Descripción del nuevo test."""
    print("\n=== Test N: Nombre del Test ===\n")
    # Tu lógica de test aquí
    if condicion_exitosa:
        results.add_pass()
    else:
        results.add_fail()
```

Luego agrégala en `main()`:
```python
def main():
    # ... tests existentes
    test_nuevo_caso(results)
```

## Referencias

- Reporte QA completo: `REPORTE_QA_HU-C07_HU-C08.md`
- Casos de prueba: `CASOS_PRUEBA_QA.csv`
- Documentación API: https://back-dp2.onrender.com/docs

---

**Última actualización**: 2025-10-09
**Mantenido por**: Equipo QA
