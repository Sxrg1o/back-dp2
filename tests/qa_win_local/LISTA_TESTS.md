# Lista de Tests QA para Windows Local

## Total: 13 archivos de test

### Tests de Casos de Uso (8 tests .bat)
1. ✅ `test_cu01_crear_pedido_simple.bat` - Crear pedido completo simple
2. ✅ `test_cu02_crear_pedido_con_opciones.bat` - Crear pedido con opciones
3. ✅ `test_cu03_listar_pedidos.bat` - Listar pedidos con paginación
4. ✅ `test_cu04_cambiar_estado_pedido.bat` - Cambiar estados de pedido
5. ✅ `test_cu05_validaciones_errores.bat` - Validaciones y manejo de errores
6. ✅ `test_cu06_crear_sesion.bat` - Crear sesión de mesa
7. ✅ `test_cu07_listar_sesiones.bat` - Listar sesiones con filtros
8. ✅ `test_cu08_actualizar_cerrar_sesion.bat` - Actualizar y cerrar sesión

### Tests de Historias de Usuario (5 tests)
9. ✅ `test_hu_c02.py` - Pantalla inicial (Python)
10. ✅ `test_hu_c07_api.bat` - API de opciones de productos
11. ✅ `test_hu_c07_precios.py` - Validación de cálculo de precios (Python)
12. ✅ `test_hu_c08_comentarios.bat` - Comentarios en pedidos

### Archivos de utilidad (5 archivos)
- `test_common.bat` - Funciones comunes
- `run_all_tests.bat` - Ejecuta todos los tests
- `verificar_entorno.bat` - Verifica prerequisitos
- `INICIO_RAPIDO.bat` - Guía rápida
- `README.md` - Documentación completa

## Cobertura de Tests

### Módulo Pedidos
- ✅ Crear pedido simple
- ✅ Crear pedido con opciones
- ✅ Listar pedidos
- ✅ Cambiar estado de pedido
- ✅ Validaciones y errores
- ✅ Comentarios en pedidos

### Módulo Sesiones
- ✅ Crear sesión de mesa
- ✅ Listar sesiones
- ✅ Actualizar sesión
- ✅ Cerrar sesión
- ✅ Filtros por estado y mesa

### Módulo Productos
- ✅ Listar productos
- ✅ Opciones de productos
- ✅ Cálculo de precios con opciones
- ✅ Validación de estructura de datos

### Módulo Categorías
- ✅ Listar categorías
- ✅ Filtrar productos por categoría

## Comparación con tests originales

| Test Original (Bash) | Test Windows (Bat) | Estado |
|---------------------|-------------------|---------|
| test_cu01_crear_pedido_simple.sh | test_cu01_crear_pedido_simple.bat | ✅ |
| test_cu02_crear_pedido_con_opciones.sh | test_cu02_crear_pedido_con_opciones.bat | ✅ |
| test_cu03_listar_pedidos.sh | test_cu03_listar_pedidos.bat | ✅ |
| test_cu04_cambiar_estado_pedido.sh | test_cu04_cambiar_estado_pedido.bat | ✅ |
| test_cu05_validaciones_errores.sh | test_cu05_validaciones_errores.bat | ✅ |
| test_cu06_crear_sesion.sh | test_cu06_crear_sesion.bat | ✅ |
| test_cu07_listar_sesiones.sh | test_cu07_listar_sesiones.bat | ✅ |
| test_cu08_actualizar_cerrar_sesion.sh | test_cu08_actualizar_cerrar_sesion.bat | ✅ |
| test_hu_c02.py | test_hu_c02.py | ✅ |
| test_hu_c07_api.sh | test_hu_c07_api.bat | ✅ |
| test_hu_c07_precios.py | test_hu_c07_precios.py | ✅ |
| test_hu_c08_comentarios.sh | test_hu_c08_comentarios.bat | ✅ |
| test_common.sh | test_common.bat | ✅ |

**Total: 13/13 tests convertidos (100%)**

## Diferencias principales

### URL del servidor
- **Original**: `https://back-dp2.onrender.com` (servidor remoto)
- **Windows Local**: `http://localhost:8000` (servidor local)

### Formato de scripts
- **Original**: Scripts Bash (.sh) - requiere Linux/Git Bash
- **Windows Local**: Scripts Batch (.bat) - nativos de Windows cmd

### Herramientas
- **Ambos usan**: 
  - `curl` para peticiones HTTP
  - `python` para parsear JSON
  - Contadores de tests pasados/fallados
  - Colores en output (limitados en cmd)

## Cómo ejecutar

### Opción 1: Ejecutar todos los tests
```cmd
cd tests\qa_win_local
run_all_tests.bat
```

### Opción 2: Ejecutar un test específico
```cmd
cd tests\qa_win_local
test_cu01_crear_pedido_simple.bat
```

### Opción 3: Tests de Python
```cmd
cd tests\qa_win_local
python test_hu_c02.py
python test_hu_c07_precios.py
```

## Prerequisitos

1. **Python 3.8+** instalado
2. **curl** (incluido en Windows 10+)
3. **Servidor backend** corriendo en `http://localhost:8000`
4. **Datos de prueba** (usuario test@test.com, mesas, productos)

## Verificar entorno antes de ejecutar

```cmd
cd tests\qa_win_local
verificar_entorno.bat
```

Este script verificará:
- ✓ Python instalado
- ✓ curl instalado
- ✓ Servidor backend activo
- ✓ Credenciales de prueba funcionando
- ✓ Datos de prueba disponibles
