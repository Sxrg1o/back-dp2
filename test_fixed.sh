#!/bin/bash

# Script de pruebas para Caso de Uso 3: Listar pedidos
# Autor: Kevin Antonio Navarro Carrera
# Equipo: QA/SEG
# Modulo: Pedidos - Backend
# Fecha: 2025-10-29
# Adaptado para Windows (usa 'py' en lugar de 'python3')

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# IMPORTANTE: Mantener URL de producción para pruebas del QA
API_URL="${API_URL:-https://back-dp2.onrender.com}"
VERBOSE="${VERBOSE:-false}"

echo "=========================================="
echo "  CU-03: Listar Pedidos"
echo "=========================================="
echo ""
echo "API Base URL: $API_URL"
echo ""

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Función para test
# CORRECCION: Logs a stderr, JSON a stdout
run_test() {
    local test_name="$1"
    local expected_status="$2"
    shift 2

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "TC-$TOTAL_TESTS: $test_name... " >&2

    response=$("$@")
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $status_code)" >&2
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo "$body"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $status_code)" >&2
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo "$body"
        return 1
    fi
}

echo "=== Tests de Listado de Pedidos ==="
echo ""

# TC-001: Listar pedidos sin filtros
PEDIDOS_RESPONSE=$(run_test "Listar pedidos - GET /pedidos" "200" \
    curl -s -w "\n%{http_code}" "$API_URL/api/v1/pedidos")

echo ""

# TC-002: Validar estructura de respuesta paginada
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar estructura de respuesta paginada... "
# CORRECCION: python3 -> py
HAS_ITEMS=$(echo "$PEDIDOS_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print('items' in data)" 2>/dev/null)
HAS_TOTAL=$(echo "$PEDIDOS_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print('total' in data)" 2>/dev/null)

if [ "$HAS_ITEMS" = "True" ] && [ "$HAS_TOTAL" = "True" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Campos: items, total presentes)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Estructura incorrecta - HAS_ITEMS: $HAS_ITEMS, HAS_TOTAL: $HAS_TOTAL)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# TC-003: Listar pedidos con paginación (skip y limit)
run_test "Listar pedidos con paginación - skip=0 limit=5" "200" \
    curl -s -w "\n%{http_code}" "$API_URL/api/v1/pedidos?skip=0&limit=5" > /dev/null

echo ""

# TC-004: Validar que limit funciona correctamente
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar que limit=5 retorna máximo 5 items... "
PEDIDOS_LIMIT=$(curl -s "$API_URL/api/v1/pedidos?skip=0&limit=5")
# CORRECCION: python3 -> py
ITEMS_COUNT=$(echo "$PEDIDOS_LIMIT" | py -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('items', [])))" 2>/dev/null)

if [ "$ITEMS_COUNT" -le 5 ]; then
    echo -e "${GREEN}✓ PASS${NC} (Items retornados: $ITEMS_COUNT <= 5)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Items retornados: $ITEMS_COUNT > 5)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

echo ""
echo "=== Tests de Filtros de Pedidos ==="
echo ""

# TC-005: Filtrar pedidos por estado PENDIENTE
# NOTA: El endpoint podría usar 'pendiente' (minúsculas) en lugar de 'PENDIENTE'
FILTRO_PENDIENTE_RESPONSE=$(run_test "Filtrar por estado pendiente" "200" \
    curl -s -w "\n%{http_code}" "$API_URL/api/v1/pedidos?estado=pendiente")

echo ""

# TC-006: Validar que filtro por estado funciona
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar que filtro estado=pendiente retorna solo pendientes... "
# CORRECCION: python3 -> py
ESTADOS=$(echo "$FILTRO_PENDIENTE_RESPONSE" | py -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('items', [])
estados = [item.get('estado', '') for item in items]
todos_pendientes = all(estado == 'pendiente' for estado in estados) if estados else True
print(todos_pendientes)
" 2>/dev/null)

if [ "$ESTADOS" = "True" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Todos los pedidos tienen estado=pendiente)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Hay pedidos con estado diferente a pendiente)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# TC-007: Filtrar pedidos por estado CONFIRMADO
run_test "Filtrar por estado confirmado" "200" \
    curl -s -w "\n%{http_code}" "$API_URL/api/v1/pedidos?estado=confirmado" > /dev/null

# TC-008: Filtrar pedidos por estado EN_PREPARACION
# NOTA: Podría ser 'en_preparacion' (minúsculas con guión bajo)
run_test "Filtrar por estado en_preparacion" "200" \
    curl -s -w "\n%{http_code}" "$API_URL/api/v1/pedidos?estado=en_preparacion" > /dev/null

echo ""

# TC-009: Obtener ID de mesa para filtro
echo -n "Obteniendo ID de mesa para filtro... "
# CORRECCION: python3 -> py
MESA_ID=$(curl -s "$API_URL/api/v1/mesas?limit=1" | py -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')" 2>/dev/null)

if [ -n "$MESA_ID" ]; then
    echo -e "${GREEN}✓${NC} Mesa ID: $MESA_ID"

    # TC-010: Filtrar pedidos por mesa
    FILTRO_MESA_RESPONSE=$(run_test "Filtrar por ID de mesa" "200" \
        curl -s -w "\n%{http_code}" "$API_URL/api/v1/pedidos?id_mesa=$MESA_ID")

    echo ""

    # TC-011: Validar que filtro por mesa funciona
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "TC-$TOTAL_TESTS: Validar que filtro id_mesa retorna solo pedidos de esa mesa... "
    # CORRECCION: python3 -> py
    MESAS_MATCH=$(echo "$FILTRO_MESA_RESPONSE" | py -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('items', [])
mesa_ids = [item.get('id_mesa', '') for item in items]
todos_misma_mesa = all(mid == '$MESA_ID' for mid in mesa_ids) if mesa_ids else True
print(todos_misma_mesa)
" 2>/dev/null)

    if [ "$MESAS_MATCH" = "True" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Todos los pedidos son de la mesa $MESA_ID)"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAIL${NC} (Hay pedidos de otras mesas)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC} - No hay mesas disponibles"
    TOTAL_TESTS=$((TOTAL_TESTS + 2))  # Contar tests omitidos
fi

echo ""
echo "=== Tests de Validación de Datos ==="
echo ""

# TC-012: Validar campos requeridos en items del listado
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar campos requeridos en pedidos... "
FIRST_PEDIDO=$(curl -s "$API_URL/api/v1/pedidos?limit=1")
# CORRECCION: python3 -> py
HAS_ID=$(echo "$FIRST_PEDIDO" | py -c "import sys, json; data = json.load(sys.stdin); print('id' in data['items'][0] if data.get('items') else False)" 2>/dev/null)
HAS_NUMERO=$(echo "$FIRST_PEDIDO" | py -c "import sys, json; data = json.load(sys.stdin); print('numero_pedido' in data['items'][0] if data.get('items') else False)" 2>/dev/null)
HAS_ESTADO=$(echo "$FIRST_PEDIDO" | py -c "import sys, json; data = json.load(sys.stdin); print('estado' in data['items'][0] if data.get('items') else False)" 2>/dev/null)
HAS_TOTAL=$(echo "$FIRST_PEDIDO" | py -c "import sys, json; data = json.load(sys.stdin); print('total' in data['items'][0] if data.get('items') else False)" 2>/dev/null)

if [ "$HAS_ID" = "True" ] && [ "$HAS_NUMERO" = "True" ] && [ "$HAS_ESTADO" = "True" ] && [ "$HAS_TOTAL" = "True" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Campos: id, numero_pedido, estado, total)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Faltan campos requeridos - ID:$HAS_ID NUM:$HAS_NUMERO EST:$HAS_ESTADO TOT:$HAS_TOTAL)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

echo ""
echo "=========================================="
echo "  Resumen de Tests"
echo "=========================================="
echo "Total:  $TOTAL_TESTS"
echo -e "Pasados: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Fallidos: ${RED}$FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ Todos los tests pasaron${NC}"
    exit 0
else
    echo -e "${RED}✗ Algunos tests fallaron${NC}"
    exit 1
fi
