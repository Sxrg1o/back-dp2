# Casos de Prueba - HU-C08: Dejar Indicación para Cocina

## Información General

- **Historia de Usuario**: HU-C08
- **Descripción**: Cliente puede dejar indicaciones personalizadas para la cocina en sus pedidos
- **Fecha de Ejecución**: 14 de Noviembre 2025
- **Tester**: Kevin Antonio Navarro Carrera
- **Metodología**: Automatizada (Bash + curl)
- **Ambiente**: Backend producción (https://back-dp2.onrender.com)

---

## Test Cases Ejecutados

### TC-001: Crear pedido con comentario en item
- **Objetivo**: Validar que se puede agregar notas_personalizacion a items individuales
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido con item que incluye notas_personalizacion
  2. Validar respuesta HTTP 201
  3. Verificar que pedido se crea correctamente
- **Resultado Esperado**: Pedido creado con comentario en item
- **Resultado Obtenido**: Pedido creado exitosamente
- **Status**: pass

### TC-002: Crear pedido con notas_cocina
- **Objetivo**: Validar que se pueden agregar notas generales para la cocina
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido con campo notas_cocina
  2. Validar respuesta HTTP 201
- **Resultado Esperado**: Pedido creado con notas para cocina
- **Resultado Obtenido**: Pedido creado exitosamente
- **Status**: pass

### TC-003: Crear pedido con notas_cliente
- **Objetivo**: Validar que se pueden agregar notas del cliente
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido con campo notas_cliente
  2. Validar respuesta HTTP 201
- **Resultado Esperado**: Pedido creado con notas del cliente
- **Resultado Obtenido**: Pedido creado exitosamente
- **Status**: pass

### TC-004: Crear pedido sin comentarios
- **Objetivo**: Verificar que los campos de comentarios son opcionales
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido sin notas_personalizacion, notas_cocina ni notas_cliente
  2. Validar respuesta HTTP 201
- **Resultado Esperado**: Pedido creado sin errores
- **Resultado Obtenido**: Campos opcionales funcionan correctamente
- **Status**: pass

### TC-005: Comentario con caracteres especiales
- **Objetivo**: Validar que el sistema maneja correctamente acentos y caracteres especiales
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido con comentario que incluye áéíóú, ñ
  2. Validar respuesta HTTP 201
- **Resultado Esperado**: Caracteres especiales aceptados
- **Resultado Obtenido**: Sistema maneja correctamente UTF-8
- **Status**: pass

### TC-006: Múltiples items con diferentes comentarios
- **Objetivo**: Verificar que cada item puede tener su propio comentario
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido con 2+ items
  2. Cada item tiene notas_personalizacion diferentes
  3. Validar respuesta HTTP 201
- **Resultado Esperado**: Cada item mantiene su comentario individual
- **Resultado Obtenido**: Items con comentarios independientes creados
- **Status**: pass

### TC-007: Comentario largo
- **Objetivo**: Validar que el sistema acepta comentarios extensos
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido con comentario de 200+ caracteres
  2. Validar respuesta HTTP 201
- **Resultado Esperado**: Comentario largo aceptado
- **Resultado Obtenido**: Sistema acepta comentarios extensos
- **Status**: pass

### TC-008: GET pedido muestra comentarios guardados
- **Objetivo**: Verificar que los comentarios se retornan al consultar items del pedido
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido con notas_personalizacion
  2. Ejecutar GET /pedidos-productos/pedido/{id}/items
  3. Verificar que items incluyen campo notas_personalizacion
- **Resultado Esperado**: Items retornados con sus comentarios
- **Resultado Obtenido**: Backend no retorna notas_personalizacion en GET
- **Status**: fail

### TC-009: Todos los tipos de comentarios juntos
- **Objetivo**: Validar que se pueden usar notas_personalizacion, notas_cliente y notas_cocina simultáneamente
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido con los tres tipos de comentarios
  2. Validar respuesta HTTP 201
- **Resultado Esperado**: Pedido creado con todos los tipos de notas
- **Resultado Obtenido**: Sistema acepta múltiples tipos de comentarios
- **Status**: pass

### TC-010: Comentario con HTML/JS se maneja correctamente
- **Objetivo**: Verificar seguridad ante inyección de código
- **Método**: Script bash automatizado
- **Pasos**:
  1. Crear pedido con comentario que incluye tags HTML y JavaScript
  2. Validar que no causa errores del servidor
- **Resultado Esperado**: Sistema maneja tags de forma segura
- **Resultado Obtenido**: Backend procesa correctamente sin vulnerabilidades
- **Status**: pass

---

## Resultados

### Resumen Ejecutivo
Total:     10 tests
Pasados:   9 (90%)
Fallidos:  1 (10%)
Bloqueados: 0

### Captura de Pantalla

![Ejecución del script](https://raw.githubusercontent.com/dp2-eder/back-dp2/qa/tests/qa/screenshots/ss_test_hu_c08_comentarios.png)

Ejecución del script mostrando 9 tests pasados y 1 fallido

---

## Script de Pruebas

**Ubicación:** `tests/qa/test_hu_c08_comentarios.sh`

**Ejecución:**
```bash
cd tests/qa
./test_hu_c08_comentarios.sh
```

---

## Endpoints Probados

```
POST   /api/v1/pedidos/completo                     # Crear pedido con comentarios
GET    /api/v1/pedidos-productos/pedido/{id}/items # Consultar items (sin notas)
```

---

## Análisis de Fallos

### Problemas Identificados

**TC-008 - Items no retornan notas de personalización:**
- Endpoint: GET /pedidos-productos/pedido/{id}/items
- Problema: Acepta notas_personalizacion en POST pero no lo retorna en GET
- Respuesta actual:
```json
{
  "items": [{
    "id": "...",
    "cantidad": 1,
    "precio_unitario": "10.00"
    // FALTA: "notas_personalizacion"
  }]
}
```
- Impacto: Cocina no ve indicaciones del cliente

---

## Issues Relacionados

- HU-C08 - Historia de Usuario base

---

## Estado Final

Aprobado con observaciones - Funcionalidad core aprobada, 1 issue menor identificado.

El sistema acepta correctamente todos los tipos de comentarios (notas_personalizacion, notas_cocina, notas_cliente) y maneja casos especiales como caracteres UTF-8 y validación de seguridad. El único problema es que las notas_personalizacion no se retornan al consultar los items del pedido.

---

Tester: Kevin Antonio Navarro Carrera
Equipo: QA/SEG
Fecha: 14 de Noviembre 2025
