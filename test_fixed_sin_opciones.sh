#!/bin/bash

# Script de pruebas para CU-02 ADAPTADO: Pedido sin opciones (BD no tiene opciones cargadas)
# Adaptado para Windows (usa 'py' en lugar de 'python3')

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
API_URL="${API_URL:-http://localhost:8000}"
VERBOSE="${VERBOSE:-false}"

echo "=========================================="
echo "  CU-02 ADAPTADO: Pedido sin opciones"
echo "  (BD no tiene opciones cargadas)"
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
    shift 2

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "TC-$TOTAL_TESTS: $test_name... " >&2

    response=$("$@")
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$VERBOSE" = "true" ]; then
        echo "" >&2
        echo "Response: $body" >&2
        echo "Status: $status_code" >&2
    fi

    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $status_code)" >&2
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo "$body"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $status_code)" >&2
        FAILED_TESTS=$((FAILED_TESTS + 1))
        if [ "$VERBOSE" = "true" ]; then
            echo "Response body: $body" >&2
        fi
        echo "$body"
        return 1
    fi
}

echo "=== Preparación: Obtener IDs necesarios ==="
echo ""

# Obtener ID de una mesa
echo -n "Obteniendo ID de mesa... "
MESA_RESPONSE=$(curl -s "$API_URL/api/v1/mesas?limit=1")
MESA_ID=$(echo "$MESA_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')" 2>/dev/null)

if [ -n "$MESA_ID" ]; then
    echo -e "${GREEN}✓${NC} Mesa ID: $MESA_ID"
else
    echo -e "${RED}✗ No se encontraron mesas${NC}"
    exit 1
fi

# Obtener un producto
echo -n "Obteniendo producto... "
PRODUCTO_RESPONSE=$(curl -s "$API_URL/api/v1/productos/cards?limit=1")
PRODUCTO_ID=$(echo "$PRODUCTO_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0]['id'] if data.get('items') else '')" 2>/dev/null)
PRODUCTO_PRECIO=$(echo "$PRODUCTO_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0]['precio_base'] if data.get('items') else 0)" 2>/dev/null)
PRODUCTO_NOMBRE=$(echo "$PRODUCTO_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0]['nombre'] if data.get('items') else '')" 2>/dev/null)

if [ -n "$PRODUCTO_ID" ]; then
    echo -e "${GREEN}✓${NC} Producto: $PRODUCTO_NOMBRE (ID: $PRODUCTO_ID, Precio: S/$PRODUCTO_PRECIO)"
else
    echo -e "${RED}✗ No se encontraron productos${NC}"
    exit 1
fi

echo ""
echo "=== Tests de Creación de Pedido (sin opciones) ==="
echo ""

# TC-001: Crear pedido con 1 item sin opciones
PAYLOAD=$(cat <<EOF
{
  "id_mesa": "$MESA_ID",
  "items": [
    {
      "id_producto": "$PRODUCTO_ID",
      "cantidad": 2,
      "precio_unitario": $PRODUCTO_PRECIO,
      "opciones": [],
      "notas_personalizacion": "Test sin opciones"
    }
  ],
  "notas_cliente": "Test pedido sin opciones",
  "notas_cocina": "Verificar cálculos"
}
EOF
)

PEDIDO_RESPONSE=$(run_test "Crear pedido sin opciones - array vacio" "201" \
    curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

PEDIDO_ID=$(echo "$PEDIDO_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)

echo ""

# TC-002: Validar que el item tiene precio_opciones = 0
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar precio_opciones es 0 (sin opciones)... "
ITEM_PRECIO_OPCIONES=$(echo "$PEDIDO_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0].get('precio_opciones', -1) if data.get('items') else -1)" 2>/dev/null)

if { [ "$ITEM_PRECIO_OPCIONES" = "0.0" ] || [ "$ITEM_PRECIO_OPCIONES" = "0" ] || [ "$ITEM_PRECIO_OPCIONES" = "0.00" ]; }; then
    echo -e "${GREEN}✓ PASS${NC} (Precio opciones: S/$ITEM_PRECIO_OPCIONES)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Esperado: 0, Obtenido: S/$ITEM_PRECIO_OPCIONES)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# TC-003: Validar que el item tiene array de opciones vacío
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar que item tiene opciones vacio... "
OPCIONES_COUNT=$(echo "$PEDIDO_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(len(data['items'][0].get('opciones', [])) if data.get('items') else -1)" 2>/dev/null)

if [ "$OPCIONES_COUNT" = "0" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Opciones: $OPCIONES_COUNT)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Esperado: 0, Obtenido: $OPCIONES_COUNT)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# TC-004: Validar cálculo de subtotal del item (cantidad * precio_unitario)
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar cálculo de subtotal del item... "
ITEM_SUBTOTAL=$(echo "$PEDIDO_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0].get('subtotal', -1) if data.get('items') else -1)" 2>/dev/null)
SUBTOTAL_ESPERADO=$(py -c "print(2 * $PRODUCTO_PRECIO)")

if [ "$ITEM_SUBTOTAL" = "$SUBTOTAL_ESPERADO" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Subtotal: S/$ITEM_SUBTOTAL = 2 × S/$PRODUCTO_PRECIO)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Esperado: S/$SUBTOTAL_ESPERADO, Obtenido: S/$ITEM_SUBTOTAL)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# TC-005: Validar que el subtotal del pedido coincide
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar subtotal del pedido... "
PEDIDO_SUBTOTAL=$(echo "$PEDIDO_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data.get('subtotal', -1))" 2>/dev/null)

if [ "$PEDIDO_SUBTOTAL" = "$SUBTOTAL_ESPERADO" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Subtotal pedido: S/$PEDIDO_SUBTOTAL)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Esperado: S/$SUBTOTAL_ESPERADO, Obtenido: S/$PEDIDO_SUBTOTAL)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# TC-006: Validar notas de personalización
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar notas de personalización del item... "
NOTAS_PERSONALIZACION=$(echo "$PEDIDO_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0].get('notas_personalizacion', '') if data.get('items') else '')" 2>/dev/null)

if [ "$NOTAS_PERSONALIZACION" = "Test sin opciones" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Notas correctas)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Notas incorrectas: '$NOTAS_PERSONALIZACION')"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

echo ""
echo "=== Test de Pedido con Múltiples Items ==="
echo ""

# TC-007: Crear pedido con múltiples items (sin opciones)
PAYLOAD_MULTI=$(cat <<EOF
{
  "id_mesa": "$MESA_ID",
  "items": [
    {
      "id_producto": "$PRODUCTO_ID",
      "cantidad": 1,
      "precio_unitario": $PRODUCTO_PRECIO,
      "opciones": [],
      "notas_personalizacion": "Item 1"
    },
    {
      "id_producto": "$PRODUCTO_ID",
      "cantidad": 2,
      "precio_unitario": $PRODUCTO_PRECIO,
      "opciones": [],
      "notas_personalizacion": "Item 2"
    }
  ],
  "notas_cliente": "Test múltiples items",
  "notas_cocina": null
}
EOF
)

PEDIDO_MULTI_RESPONSE=$(run_test "Crear pedido con 2 items sin opciones" "201" \
    curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD_MULTI")

echo ""

# TC-008: Validar que el pedido tiene 2 items
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar que pedido tiene 2 items... "
ITEMS_COUNT=$(echo "$PEDIDO_MULTI_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('items', [])))" 2>/dev/null)

if [ "$ITEMS_COUNT" = "2" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Items: $ITEMS_COUNT)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Esperado: 2, Obtenido: $ITEMS_COUNT)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# TC-009: Validar subtotal total (1*precio + 2*precio = 3*precio)
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "TC-$TOTAL_TESTS: Validar subtotal total de múltiples items... "
SUBTOTAL_MULTI=$(echo "$PEDIDO_MULTI_RESPONSE" | py -c "import sys, json; data = json.load(sys.stdin); print(data.get('subtotal', -1))" 2>/dev/null)
SUBTOTAL_MULTI_ESPERADO=$(py -c "print(3 * $PRODUCTO_PRECIO)")

if [ "$SUBTOTAL_MULTI" = "$SUBTOTAL_MULTI_ESPERADO" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Subtotal: S/$SUBTOTAL_MULTI = 3 × S/$PRODUCTO_PRECIO)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (Esperado: S/$SUBTOTAL_MULTI_ESPERADO, Obtenido: S/$SUBTOTAL_MULTI)"
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
    echo ""
    echo -e "${YELLOW}NOTA: Test adaptado para BD sin opciones cargadas${NC}"
    echo -e "${YELLOW}Para probar con opciones reales, primero carga datos de opciones en la BD${NC}"
    exit 0
else
    echo -e "${RED}✗ Algunos tests fallaron${NC}"
    exit 1
fi
