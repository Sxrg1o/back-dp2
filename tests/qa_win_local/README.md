# Tests de QA para Windows (Local)

Esta carpeta cont## Estructura de archivos

### Archivos de configuración y utilidades
- `README.md` - Documentación completa
- `INICIO_RAPIDO.bat` - Guía rápida de inicio
- `verificar_entorno.bat` - Verifica que todo esté listo
- `run_all_tests.bat` - Ejecuta todos los tests automáticamente
- `test_common.bat` - Funciones comunes (autenticación, curl con token)

### Tests de Casos de Uso (CU)
- `test_cu01_crear_pedido_simple.bat` - Crear pedido simple
- `test_cu02_crear_pedido_con_opciones.bat` - Crear pedido con opciones
- `test_cu03_listar_pedidos.bat` - Listar pedidos
- `test_cu04_cambiar_estado_pedido.bat` - Cambiar estado de pedido
- `test_cu05_validaciones_errores.bat` - Validaciones y errores
- `test_cu06_crear_sesion.bat` - Crear sesión de mesa
- `test_cu07_listar_sesiones.bat` - Listar sesiones
- `test_cu08_actualizar_cerrar_sesion.bat` - Actualizar/cerrar sesión

### Tests de Historias de Usuario (HU)
- `test_hu_c02.py` - Pantalla inicial (Python)
- `test_hu_c07_api.bat` - API de opciones de productos
- `test_hu_c07_precios.py` - Validación de cálculo de precios (Python)
- `test_hu_c08_comentarios.bat` - Comentarios en pedidoses adaptadas de los tests de QA para ejecutarse en Windows usando archivos `.bat` y apuntando al servidor local.

## Diferencias con los tests originales

- **Formato**: Scripts `.bat` en lugar de `.sh` (compatibles con cmd de Windows)
- **URL**: Apunta a `http://localhost:8000` en lugar de `https://back-dp2.onrender.com`
- **Herramientas**: Usa `curl` para Windows y Python para parsear JSON

## Prerequisitos

1. **Python 3.8+** instalado y en el PATH del sistema
2. **curl para Windows**:
   - Viene incluido en Windows 10/11 (1803+)
   - O descarga desde: https://curl.se/windows/
3. **Servidor backend corriendo localmente**:
   ```cmd
   cd e:\PROYECTOS\DP2\V8\back-dp2
   venv\Scripts\activate
   python src\main.py
   ```
   El servidor debería estar corriendo en `http://localhost:8000`

## Configuración

### Variables de entorno (opcional)

Puedes configurar estas variables antes de ejecutar los tests:

```cmd
set API_URL=http://localhost:8000
set QA_EMAIL=test@test.com
set QA_PASSWORD=test123
set VERBOSE=true
```

## Ejecución de Tests

### Ejecutar un test individual

```cmd
cd tests\qa_win_local
test_cu01_crear_pedido_simple.bat
```

### Ejecutar todos los tests

```cmd
cd tests\qa_win_local
run_all_tests.bat
```

## Estructura de archivos

- `test_common.bat` - Funciones comunes (autenticación, curl con token)
- `test_cu01_crear_pedido_simple.bat` - Test de creación de pedido simple
- `test_cu02_crear_pedido_con_opciones.bat` - Test de creación de pedido con opciones
- `test_cu03_listar_pedidos.bat` - Test de listar pedidos
- `test_cu04_cambiar_estado_pedido.bat` - Test de cambio de estado
- `test_cu05_validaciones_errores.bat` - Test de validaciones y errores
- `test_cu06_crear_sesion.bat` - Test de crear sesión de mesa
- `test_cu07_listar_sesiones.bat` - Test de listar sesiones
- `test_cu08_actualizar_cerrar_sesion.bat` - Test de actualizar/cerrar sesión
- `run_all_tests.bat` - Script para ejecutar todos los tests

## Interpretación de resultados

- `✓ PASS` - Test pasó correctamente (verde)
- `✗ FAIL` - Test falló (rojo)
- Al final se muestra un resumen con total de tests, pasados y fallados

## Troubleshooting

### "curl no se reconoce como comando"
- Verifica que curl esté instalado: `curl --version`
- Si no está, descárgalo o usa Git Bash

### "python no se reconoce como comando"
- Verifica la instalación: `python --version`
- Asegúrate de que Python esté en el PATH del sistema

### "Connection refused" o errores de conexión
- Verifica que el servidor backend esté corriendo en `http://localhost:8000`
- Inicia el servidor con: `python src\main.py`

### Tests fallan con error 401 (Unauthorized)
- Verifica que el usuario de prueba exista en la base de datos
- Revisa las credenciales en las variables de entorno o en el script

## Notas

- Los tests crean datos de prueba en la base de datos local
- Algunos tests pueden fallar si no hay datos semilla (productos, mesas, etc.)
- Ejecuta los scripts de seed si es necesario: `python scripts\seed_cevicheria_data.py`
