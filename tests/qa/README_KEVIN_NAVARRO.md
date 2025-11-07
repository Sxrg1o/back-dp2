# Tests de QA - Kevin Antonio Navarro Carrera

Este directorio contiene scripts de prueba automatizados para validar las Historias de Usuario asignadas a Kevin Navarro (Equipo QA/SEG).

## Contenido

### Scripts de Testing

- `test_hu_c07_api.sh` - Tests de endpoints de API (HU-C07: Añadir extras)
- `test_hu_c07_precios.py` - Tests de validación de cálculos de precios (HU-C07)
- `test_hu_c08_comentarios.sh` - Tests de comentarios en pedidos (HU-C08: Indicación para cocina)
- `test_common.sh` - Funciones compartidas (autenticación JWT, curl_auth)

### Documentación

- `README_KEVIN_NAVARRO.md` - Este archivo

### Historias de Usuario Asignadas

- **HU-C07**: Añadir extras disponibles a mi selección ✅ COMPLETADO
- **HU-C08**: Dejar indicación para cocina ✅ COMPLETADO
- **HU-C33**: Ver subtotal por grupo (División en frontend)
- **HU-C34**: Ver total a pagar consolidado (División en frontend)
- **HU-C35**: Cambiar de modalidad de pago (División en frontend)
- **HU-C36**: Ver lista de productos disponibles (División en frontend)

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

### 1B. Tests de HU-C08 (Comentarios en Pedidos)

Ejecuta tests de comentarios:

```bash
cd tests/qa
chmod +x test_hu_c08_comentarios.sh
QA_EMAIL="prueba1@example.com" QA_PASSWORD="pasiword" ./test_hu_c08_comentarios.sh
```

**Con modo verbose**:
```bash
QA_EMAIL="prueba1@example.com" QA_PASSWORD="pasiword" VERBOSE=true ./test_hu_c08_comentarios.sh
```

#### Qué valida este script:

- ✅ Autenticación JWT con credenciales QA
- ✅ Crear pedido con `notas_personalizacion` en items
- ✅ Crear pedido con `notas_cocina` a nivel de pedido
- ✅ Crear pedido con `notas_cliente` a nivel de pedido
- ✅ Validar campos opcionales (pedido sin comentarios)
- ✅ Caracteres especiales en comentarios (áéíóú, ñ, ¿¡)
- ✅ Múltiples items con diferentes comentarios
- ✅ Comentarios largos (200+ caracteres)
- ✅ Sanitización de HTML/JS en comentarios
- ✅ Persistencia de comentarios en GET pedido

**Resultados:** 9/10 tests PASS (90%)

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

## Issues de GitHub

### Backend (dp2-eder/back-dp2)

- **Issue #92**: Casos de Prueba - HU-C08: Dejar indicación para cocina
  - Estado: 9/10 tests PASS (90%)
  - Fecha: 06 de Noviembre 2025

### Frontend (dp2-eder/front-dp2)

- **Issue #31**: Casos de Prueba - HU-C08: Dejar indicación para cocina (Frontend)
  - Estado: 3/3 tests PASS (100%)
  - Fecha: 06 de Noviembre 2025

## Referencias

- Reporte QA completo: `REPORTE_QA_HU-C07_HU-C08.md`
- Casos de prueba: `CASOS_PRUEBA_QA.csv`
- Documentación API: https://back-dp2.onrender.com/docs
- Formato estándar QA: `/Users/kevinnavarro/Documents/Github/dp2/FORMATO ESTÁNDAR-EQUIPO QA.md`

---

**Última actualización**: 2025-11-06
**Mantenido por**: Kevin Antonio Navarro Carrera - Equipo QA/SEG
**Email**: kevin.navarro@example.com (si aplica)
