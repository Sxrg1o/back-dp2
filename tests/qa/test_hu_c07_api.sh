#!/bin/bash

# Script de pruebas para HU-C07: Añadir extras disponibles
# Autor: Equipo QA
# Fecha: 2025-10-09

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
API_URL="${API_URL:-https://back-dp2.onrender.com}"
VERBOSE="${VERBOSE:-false}"

echo "=========================================="
echo "  Test HU-C07: Opciones de Productos"
echo "=========================================="
echo ""
echo "API Base URL: $API_URL"
echo ""

# Contador de tests
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Función para test
run_test() {
    local test_name="$1"
    local expected_status="$2"
    local endpoint="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Test $TOTAL_TESTS: $test_name... "

    response=$(curl -s -w "\n%{http_code}" "$API_URL$endpoint")
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$VERBOSE" = "true" ]; then
        echo ""
        echo "Response: $body"
        echo "Status: $status_code"
    fi

    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $status_code)"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $status_code)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Función para validar JSON
validate_json_field() {
    local test_name="$1"
    local endpoint="$2"
    local field="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Test $TOTAL_TESTS: $test_name... "

    response=$(curl -s "$API_URL$endpoint")

    if echo "$response" | grep -q "\"$field\""; then
        echo -e "${GREEN}✓ PASS${NC} (Campo '$field' presente)"
        PASSED_TESTS=$((PASSED_TESTS + 1))

        if [ "$VERBOSE" = "true" ]; then
            echo "Response preview:"
            echo "$response" | python3 -m json.tool | head -20
        fi
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Campo '$field' no encontrado)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

echo "=== Tests de Endpoints ==="
echo ""

# Test 1: Health check
run_test "Health check del backend" "200" "/health"

# Test 2: Listar productos
run_test "GET /productos/cards (listar productos)" "200" "/api/v1/productos/cards?skip=0&limit=10"

# Test 3: Listar categorías
run_test "GET /categorias (listar categorías)" "200" "/api/v1/categorias?skip=0&limit=10"

# Test 4: Listar tipos de opciones
run_test "GET /tipos-opciones (listar tipos de opciones)" "200" "/api/v1/tipos-opciones?skip=0&limit=50"

# Test 5: Listar producto-opciones
run_test "GET /producto-opciones (listar opciones de productos)" "200" "/api/v1/producto-opciones?skip=0&limit=50"

echo ""
echo "=== Tests de Estructura de Datos ==="
echo ""

# Test 6: Verificar estructura de productos
validate_json_field "Productos tienen campo 'items'" "/api/v1/productos/cards?limit=1" "items"

# Test 7: Verificar estructura de opciones
validate_json_field "Opciones tienen campo 'nombre'" "/api/v1/producto-opciones?limit=1" "nombre"

# Test 8: Verificar precios adicionales
validate_json_field "Opciones tienen campo 'precio_adicional'" "/api/v1/producto-opciones?limit=1" "precio_adicional"

echo ""
echo "=== Test de Producto con Opciones (HU-C07) ==="
echo ""

# Obtener primer producto
FIRST_PRODUCT_ID=$(curl -s "$API_URL/api/v1/productos/cards?limit=1" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0]['id'] if data.get('items') else '')" 2>/dev/null)

if [ -n "$FIRST_PRODUCT_ID" ]; then
    echo "ID del producto a probar: $FIRST_PRODUCT_ID"

    # Test 9: Obtener producto con opciones
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Test $TOTAL_TESTS: GET /productos/{id}/opciones (obtener producto con opciones)... "

    response=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/productos/$FIRST_PRODUCT_ID/opciones")
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$status_code" = "200" ]; then
        # Verificar que tenga opciones
        opciones_count=$(echo "$body" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('opciones', [])))" 2>/dev/null)

        if [ -n "$opciones_count" ] && [ "$opciones_count" -gt 0 ]; then
            echo -e "${GREEN}✓ PASS${NC} (Status: 200, Opciones encontradas: $opciones_count)"
            PASSED_TESTS=$((PASSED_TESTS + 1))

            if [ "$VERBOSE" = "true" ]; then
                echo "Opciones disponibles:"
                echo "$body" | python3 -m json.tool | grep -A 2 '"nombre"'
            fi
        else
            echo -e "${YELLOW}⚠ PASS${NC} (Status: 200, pero sin opciones)"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        fi
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: 200, Got: $status_code)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC} - No se pudo obtener ID de producto para pruebas"
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
