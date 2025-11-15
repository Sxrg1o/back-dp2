# Casos de Prueba - HU-C09: Revisar Orden Antes de Confirmar

## Información General

- **Historia de Usuario**: HU-C09
- **Descripción**: Cliente puede revisar su orden antes de confirmar para verificar cantidades, precios y total
- **Fecha de Ejecución**: 14 de Noviembre 2025
- **Tester**: Kevin Antonio Navarro Carrera
- **Metodología**: Automatizada (Bash + curl)
- **Ambiente**: Backend producción (https://back-dp2.onrender.com)

---

## Test Cases Ejecutados

### TC-001: Obtener detalle de pedido
- **Objetivo**: Validar que se puede consultar el detalle completo de un pedido
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear un pedido de prueba con productos
  2. Ejecutar GET /api/v1/pedidos/{id}
  3. Validar respuesta HTTP 200
- **Resultado Esperado**: Pedido retornado con todos sus datos
- **Resultado Obtenido**: Pedido consultado exitosamente
- **Status**: pass

### TC-002: Validar que muestra cantidades de items
- **Objetivo**: Verificar que el endpoint retorna los items del pedido con sus cantidades
- **Método**: Script bash automatizado
- **Pasos**:
  1. Parsear respuesta del endpoint
  2. Buscar campo items o productos
  3. Validar que contiene array con items
- **Resultado Esperado**: Campo items presente con productos del pedido
- **Resultado Obtenido**: No hay items en la respuesta del endpoint principal
- **Status**: fail

### TC-003: Validar que muestra subtotal
- **Objetivo**: Confirmar que el pedido incluye el subtotal calculado
- **Método**: Script bash automatizado
- **Pasos**:
  1. Extraer campo subtotal de la respuesta
  2. Validar que es un número válido mayor a 0
- **Resultado Esperado**: Subtotal presente y calculado
- **Resultado Obtenido**: Subtotal: S/110.00
- **Status**: pass

### TC-004: Validar que muestra total
- **Objetivo**: Verificar que el pedido incluye el total calculado
- **Método**: Script bash automatizado
- **Pasos**:
  1. Extraer campo total de la respuesta
  2. Validar que es un número válido mayor a 0
- **Resultado Esperado**: Total presente y calculado
- **Resultado Obtenido**: Total: S/110.00
- **Status**: pass

### TC-005: Validar cálculo correcto del total
- **Objetivo**: Confirmar que el total coincide con la suma de items
- **Método**: Script bash automatizado
- **Pasos**:
  1. Comparar total con subtotal
  2. Validar que son valores consistentes
- **Resultado Esperado**: Total calculado correctamente
- **Resultado Obtenido**: Total: S/110.00 coincide con subtotal
- **Status**: pass

### TC-006: Listar items del pedido
- **Objetivo**: Validar endpoint específico para obtener items de un pedido
- **Método**: Script bash automatizado
- **Pasos**:
  1. Ejecutar GET /api/v1/pedidos-productos/pedido/{id}/items
  2. Validar respuesta HTTP 200
  3. Verificar que retorna array de items
- **Resultado Esperado**: Lista de items del pedido
- **Resultado Obtenido**: Items retornados correctamente
- **Status**: pass

### TC-007: Validar datos de items
- **Objetivo**: Verificar que cada item incluye cantidad y precio
- **Método**: Script bash automatizado
- **Pasos**:
  1. Parsear items retornados
  2. Validar presencia de campo cantidad
  3. Validar presencia de campo precio
- **Resultado Esperado**: Items con cantidad y precio
- **Resultado Obtenido**: Items incluyen cantidad y precio correctamente
- **Status**: pass

---

## Resultados

### Resumen Ejecutivo
Total:     7 tests
Pasados:   6 (85.7%)
Fallidos:  1 (14.3%)
Bloqueados: 0

### Captura de Pantalla

![Ejecución del script](https://raw.githubusercontent.com/dp2-eder/back-dp2/qa/tests/qa/screenshots/ss_test_hu_c09_revisar_orden.png)

Ejecución del script mostrando 6 tests pasados y 1 fallido

---

## Script de Pruebas

**Ubicación:** `tests/qa/test_hu_c09_revisar_orden.sh`

**Ejecución:**
```bash
cd tests/qa
./test_hu_c09_revisar_orden.sh
```

---

## Endpoints Probados

```
GET    /api/v1/pedidos/{id}                           # Detalle del pedido
GET    /api/v1/pedidos-productos/pedido/{id}/items   # Items del pedido
```

---

## Análisis de Fallos

### Problemas Identificados

**TC-002 - GET pedido no incluye items:**
- Endpoint: GET /pedidos/{id}
- Problema: No retorna array items, requiere segunda llamada a /pedidos-productos/pedido/{id}/items
- Impacto: Duplica latencia de red, complica frontend
- El endpoint retorna subtotal y total correctamente, pero falta información de los productos individuales

---

## Issues Relacionados

- HU-C09 - Historia de Usuario base

---

## Estado Final

Aprobado con observaciones - Funcionalidad core aprobada, 1 issue menor identificado.

La funcionalidad de revisión de orden funciona correctamente. Los totales se calculan bien y existe un endpoint para obtener los items. La observación es sobre la estructura de la respuesta del endpoint principal que podría incluir los items para reducir llamadas al API.

---

Tester: Kevin Antonio Navarro Carrera
Equipo: QA/SEG
Fecha: 14 de Noviembre 2025
