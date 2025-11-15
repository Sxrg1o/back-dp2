# Casos de Prueba - HU-C11: Confirmar Envío de Pedido

## Información General

- **Historia de Usuario**: HU-C11
- **Descripción**: Cliente listo para enviar puede confirmar el envío de su pedido para que el negocio lo reciba sin errores
- **Fecha de Ejecución**: 14 de Noviembre 2025
- **Tester**: Kevin Antonio Navarro Carrera
- **Metodología**: Automatizada (Bash + curl)
- **Ambiente**: Backend producción (https://back-dp2.onrender.com)

---

## Test Cases Ejecutados

### TC-001: Crear pedido completo
- **Objetivo**: Validar que se puede crear un pedido con todos los datos necesarios
- **Método**: Script bash automatizado
- **Pasos**:
  1. Obtener sesión activa de mesa
  2. Ejecutar POST /api/v1/pedidos/completo con productos
  3. Validar respuesta HTTP 201
  4. Verificar que retorna ID de pedido
- **Resultado Esperado**: Pedido creado con status 201
- **Resultado Obtenido**: Pedido creado correctamente
- **Status**: pass

### TC-002: Validar cálculo automático de total
- **Objetivo**: Confirmar que el backend calcula el total del pedido correctamente
- **Método**: Script bash automatizado
- **Pasos**:
  1. Extraer campo total de la respuesta del pedido
  2. Validar que total es mayor a 0
  3. Verificar formato de moneda correcto
- **Resultado Esperado**: Total calculado automáticamente
- **Resultado Obtenido**: Total: S/20.00 (correcto según productos)
- **Status**: pass

### TC-003: Validar datos obligatorios del pedido
- **Objetivo**: Verificar que el pedido tiene todos los campos requeridos
- **Método**: Script bash automatizado
- **Pasos**:
  1. Validar presencia de campo id
  2. Validar campo numero_pedido con formato correcto
  3. Validar campo estado (debe ser "pendiente")
- **Resultado Esperado**: Todos los campos obligatorios presentes
- **Resultado Obtenido**: ID: OK, Número: 20251115-M1-004, Estado: pendiente
- **Status**: pass

### TC-004: Enviar pedido a cocina
- **Objetivo**: Validar que se puede confirmar el envío del pedido
- **Método**: Script bash automatizado
- **Pasos**:
  1. Tomar ID del pedido creado
  2. Ejecutar POST /api/v1/pedidos/enviar con el ID
  3. Validar respuesta HTTP 201
- **Resultado Esperado**: Pedido enviado exitosamente
- **Resultado Obtenido**: Pedido confirmado con status 201
- **Status**: pass

### TC-005: Obtener pedido confirmado
- **Objetivo**: Verificar que el pedido se puede consultar después de enviarlo
- **Método**: Script bash automatizado
- **Pasos**:
  1. Ejecutar GET /api/v1/pedidos/{id}
  2. Validar respuesta HTTP 200
  3. Verificar que retorna datos del pedido
- **Resultado Esperado**: Pedido retornado correctamente
- **Resultado Obtenido**: Pedido consultado exitosamente
- **Status**: pass

### TC-006: Validar estado del pedido confirmado
- **Objetivo**: Confirmar que el pedido mantiene el estado correcto después del envío
- **Método**: Script bash automatizado
- **Pasos**:
  1. Extraer campo estado de la respuesta
  2. Validar que estado es "pendiente" (esperando preparación)
- **Resultado Esperado**: Estado del pedido es "pendiente"
- **Resultado Obtenido**: Estado confirmado como "pendiente"
- **Status**: pass

---

## Resultados

### Resumen Ejecutivo
Total:     6 tests
Pasados:   6 (100%)
Fallidos:  0 (0%)
Bloqueados: 0

### Captura de Pantalla

![Ejecución del script](https://raw.githubusercontent.com/dp2-eder/back-dp2/qa/tests/qa/screenshots/ss_test_hu_c11_confirmar_pedido.png)

Ejecución del script mostrando los 6 tests pasados exitosamente

---

## Script de Pruebas

**Ubicación:** `tests/qa/test_hu_c11_confirmar_pedido.sh`

**Ejecución:**
```bash
cd tests/qa
./test_hu_c11_confirmar_pedido.sh
```

---

## Endpoints Probados

```
POST   /api/v1/pedidos/completo    # Crear pedido con todos los datos
POST   /api/v1/pedidos/enviar      # Confirmar envío del pedido
GET    /api/v1/pedidos/{id}        # Consultar estado del pedido
```

---

## Análisis de Fallos

No se identificaron fallos en la funcionalidad de confirmación de pedidos. Todos los tests pasaron correctamente.

### Observaciones

El flujo completo de creación y confirmación de pedido funciona correctamente:
- Creación de pedido con cálculo automático de total
- Validación de datos obligatorios
- Confirmación de envío
- Consulta posterior del pedido

---

## Issues Relacionados

- HU-C11 - Historia de Usuario base

---

## Estado Final

Aprobado - Todos los tests de confirmación de pedido pasaron correctamente.

El flujo de confirmación de pedido funciona como se espera. El backend calcula correctamente el total y mantiene los estados apropiados durante el proceso.

---

Tester: Kevin Antonio Navarro Carrera
Equipo: QA/SEG
Fecha: 14 de Noviembre 2025
