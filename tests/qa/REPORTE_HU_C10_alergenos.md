# Casos de Prueba - HU-C10: Ver Alérgenos de Productos

## Información General

- **Historia de Usuario**: HU-C10
- **Descripción**: Cliente con restricciones alimentarias puede ver alérgenos de productos para evitar riesgos de salud
- **Fecha de Ejecución**: 14 de Noviembre 2025
- **Tester**: Kevin Antonio Navarro Carrera
- **Metodología**: Automatizada (Bash + curl)
- **Ambiente**: Backend producción (https://back-dp2.onrender.com)

---

## Test Cases Ejecutados

### TC-001: Obtener lista de alérgenos del sistema
- **Objetivo**: Validar que el endpoint retorna el catálogo completo de alérgenos disponibles
- **Método**: Script bash automatizado
- **Pasos**:
  1. Ejecutar GET /api/v1/alergenos
  2. Validar respuesta HTTP 200
  3. Verificar estructura de respuesta con campo items
- **Resultado Esperado**: Lista de alérgenos con estructura correcta
- **Resultado Obtenido**: Catálogo con 8 alérgenos disponibles
- **Status**: pass

### TC-002: Validar existencia de alérgenos en catálogo
- **Objetivo**: Confirmar que el sistema tiene alérgenos catalogados
- **Método**: Script bash automatizado
- **Pasos**:
  1. Parsear respuesta del endpoint anterior
  2. Contar elementos en array items
  3. Validar que count > 0
- **Resultado Esperado**: Al menos 1 alérgeno en el catálogo
- **Resultado Obtenido**: 8 alérgenos catalogados
- **Status**: pass

### TC-003: Obtener productos con alérgenos
- **Objetivo**: Validar endpoint que retorna productos que tienen alérgenos asignados
- **Método**: Script bash automatizado
- **Pasos**:
  1. Ejecutar GET /api/v1/productos/con-alergenos
  2. Validar respuesta HTTP 200
  3. Verificar estructura con productos y sus alérgenos
- **Resultado Esperado**: Lista de productos con información de alérgenos
- **Resultado Obtenido**: 100 productos retornados correctamente
- **Status**: pass

### TC-004: Validar estructura de productos con alérgenos
- **Objetivo**: Confirmar que la estructura de respuesta es correcta
- **Método**: Script bash automatizado
- **Pasos**:
  1. Parsear respuesta JSON
  2. Validar campo items existe
  3. Contar elementos
- **Resultado Esperado**: Estructura válida con array items
- **Resultado Obtenido**: 100 productos con estructura correcta
- **Status**: pass

### TC-005: Obtener alérgenos de producto específico
- **Objetivo**: Validar que se pueden consultar alérgenos de un producto individual
- **Método**: Script bash automatizado
- **Pasos**:
  1. Seleccionar producto de la lista de productos con alérgenos
  2. Ejecutar GET /api/v1/productos/{id}/alergenos
  3. Validar HTTP 200
- **Resultado Esperado**: Lista de alérgenos del producto
- **Resultado Obtenido**: Producto "Leche de Tigre" retorna sus alérgenos correctamente
- **Status**: pass

### TC-006: Validar estructura de alérgenos del producto
- **Objetivo**: Confirmar que la información de alérgenos es completa y válida
- **Método**: Script bash automatizado
- **Pasos**:
  1. Parsear respuesta de alérgenos del producto
  2. Validar estructura del array
  3. Contar alérgenos presentes
- **Resultado Esperado**: Array válido con información de alérgenos
- **Resultado Obtenido**: Producto tiene 2 alérgenos correctamente estructurados
- **Status**: pass

### TC-007: Validar límite de alérgenos por producto
- **Objetivo**: Verificar que productos no exceden el límite de 10 alérgenos
- **Método**: Script bash automatizado
- **Pasos**:
  1. Obtener cantidad de alérgenos del producto
  2. Validar que count <= 10
- **Resultado Esperado**: Producto tiene máximo 10 alérgenos
- **Resultado Obtenido**: Producto tiene 2 de 10 alérgenos máximo
- **Status**: pass

---

## Resultados

### Resumen Ejecutivo
Total:     7 tests
Pasados:   7 (100%)
Fallidos:  0 (0%)
Bloqueados: 0

### Captura de Pantalla

![Ejecución del script](https://raw.githubusercontent.com/dp2-eder/back-dp2/qa/tests/qa/screenshots/ss_test_hu_c10_alergenos.png)

Ejecución del script mostrando los 7 tests pasados exitosamente

---

## Script de Pruebas

**Ubicación:** `tests/qa/test_hu_c10_alergenos.sh`

**Ejecución:**
```bash
cd tests/qa
./test_hu_c10_alergenos.sh
```

---

## Endpoints Probados

```
GET    /api/v1/alergenos                        # Catálogo de alérgenos
GET    /api/v1/productos/con-alergenos          # Productos con alérgenos
GET    /api/v1/productos/{id}/alergenos         # Alérgenos de producto específico
```

---

## Análisis de Fallos

No se identificaron fallos en la funcionalidad de visualización de alérgenos. Todos los tests pasaron correctamente.

### Observaciones

Durante las pruebas se identificaron dos issues relacionados con gestión de alérgenos (fuera del alcance de HU-C10):

**Issue #120 - Endpoint de asignación no disponible:**
- El endpoint POST /productos-alergenos retorna 404
- Esto es parte de gestión de alérgenos, no de visualización
- Reportado como bug separado

**Issue #121 - Validación de límite faltante:**
- No existe validación del límite de 10 alérgenos en el backend
- TC-007 pasa porque ningún producto tiene más de 10, pero la validación no está implementada
- Reportado como bug separado

Ambos issues están fuera del alcance de HU-C10 (visualización) y corresponden a HU-A04 (gestión).

---

## Issues Relacionados

- Issue #120 - Endpoint POST /productos-alergenos retorna 404
- Issue #121 - Sistema permite asignar más de 10 alérgenos por producto
- HU-C10 - Historia de Usuario base

---

## Estado Final

Aprobado - Todos los tests de visualización pasaron correctamente.

Los endpoints de consulta de alérgenos funcionan como se espera. Los issues identificados corresponden a funcionalidad de gestión (fuera del alcance de esta historia).

---

Tester: Kevin Antonio Navarro Carrera
Equipo: QA/SEG
Fecha: 14 de Noviembre 2025
