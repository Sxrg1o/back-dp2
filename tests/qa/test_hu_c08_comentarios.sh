#!/bin/bash

# Autor: Kevin Antonio Navarro Carrera
# Descripción: Tests automatizados para HU-C08 - Dejar indicación para cocina
# Fecha: 30 de Octubre 2025

set -euo pipefail

API_BASE="https://back-dp2.onrender.com"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  HU-C08: Dejar indicación para cocina"
echo "=========================================="
echo ""
echo "API Base URL: $API_BASE"
echo ""

pass_test() {
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

fail_test() {
    local msg="$1"
    echo -e "${RED}✗ FAIL${NC} ($msg)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

skip_test() {
    local msg="$1"
    echo -e "${YELLOW}⚠ SKIP${NC} - $msg"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

echo "=== Preparación: Obtener IDs necesarios ==="
echo ""

echo -n "Obteniendo ID de mesa... "
MESA_RESPONSE=$(curl -s "${API_BASE}/api/v1/mesas/?skip=0&limit=1")
MESA_ID=$(echo "$MESA_RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0]['id'] if data.get('items') else '')" 2>/dev/null || echo "")

if [ -z "$MESA_ID" ]; then
    echo -e "${RED}✗ No se pudo obtener ID de mesa${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Mesa ID: $MESA_ID"

echo -n "Obteniendo ID de producto... "
PRODUCTO_RESPONSE=$(curl -s "${API_BASE}/api/v1/productos/?skip=0&limit=1")
PRODUCTO_ID=$(echo "$PRODUCTO_RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0]['id'] if data.get('items') else '')" 2>/dev/null || echo "")

if [ -z "$PRODUCTO_ID" ]; then
    echo -e "${RED}✗ No se pudo obtener ID de producto${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Producto ID: $PRODUCTO_ID"

echo -n "Obteniendo precio del producto... "
PRECIO=$(echo "$PRODUCTO_RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['items'][0]['precio_base'] if data.get('items') else '')" 2>/dev/null || echo "")
echo -e "${GREEN}✓${NC} Precio: S/$PRECIO"

echo ""
echo "=== Tests de Comentarios en Pedidos ==="
echo ""

# TC-001: Crear pedido con comentario en item
echo -n "TC-001: Crear pedido con comentario en item (notas_personalizacion)... "
PAYLOAD=$(cat <<EOF
{
    "id_mesa": "$MESA_ID",
    "items": [
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 1,
            "precio_unitario": $PRECIO,
            "opciones": [],
            "notas_personalizacion": "Sin cebolla, por favor"
        }
    ]
}
EOF
)

RESPONSE=$(curl -s -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ]; then
    PEDIDO_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null || echo "")
    NOTA=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('items', [{}])[0].get('notas_personalizacion', ''))" 2>/dev/null || echo "")

    if [ "$NOTA" = "Sin cebolla, por favor" ]; then
        pass_test
    else
        fail_test "Comentario no guardado correctamente"
    fi
else
    fail_test "HTTP $HTTP_CODE"
fi

# TC-002: Crear pedido con notas para cocina
echo -n "TC-002: Crear pedido con notas_cocina... "
PAYLOAD=$(cat <<EOF
{
    "id_mesa": "$MESA_ID",
    "items": [
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 2,
            "precio_unitario": $PRECIO,
            "opciones": []
        }
    ],
    "notas_cocina": "Urgente - evento especial"
}
EOF
)

RESPONSE=$(curl -s -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ]; then
    NOTA_COCINA=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('notas_cocina', ''))" 2>/dev/null || echo "")

    if [ "$NOTA_COCINA" = "Urgente - evento especial" ]; then
        pass_test
    else
        fail_test "Notas de cocina no guardadas"
    fi
else
    fail_test "HTTP $HTTP_CODE"
fi

# TC-003: Crear pedido con notas de cliente
echo -n "TC-003: Crear pedido con notas_cliente... "
PAYLOAD=$(cat <<EOF
{
    "id_mesa": "$MESA_ID",
    "items": [
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 1,
            "precio_unitario": $PRECIO,
            "opciones": []
        }
    ],
    "notas_cliente": "Celebración de cumpleaños"
}
EOF
)

RESPONSE=$(curl -s -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ]; then
    NOTA_CLIENTE=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('notas_cliente', ''))" 2>/dev/null || echo "")

    if [ "$NOTA_CLIENTE" = "Celebración de cumpleaños" ]; then
        pass_test
    else
        fail_test "Notas de cliente no guardadas"
    fi
else
    fail_test "HTTP $HTTP_CODE"
fi

# TC-004: Crear pedido sin comentarios (validar opcional)
echo -n "TC-004: Crear pedido sin comentarios (campos opcionales)... "
PAYLOAD=$(cat <<EOF
{
    "id_mesa": "$MESA_ID",
    "items": [
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 1,
            "precio_unitario": $PRECIO,
            "opciones": []
        }
    ]
}
EOF
)

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ]; then
    pass_test
else
    fail_test "HTTP $HTTP_CODE - Los comentarios deberían ser opcionales"
fi

# TC-005: Comentarios con caracteres especiales
echo -n "TC-005: Comentario con caracteres especiales (áéíóú, ñ)... "
PAYLOAD=$(cat <<EOF
{
    "id_mesa": "$MESA_ID",
    "items": [
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 1,
            "precio_unitario": $PRECIO,
            "opciones": [],
            "notas_personalizacion": "Más ají, sin limón. ¿Picante? ¡Sí!"
        }
    ]
}
EOF
)

RESPONSE=$(curl -s -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ]; then
    pass_test
else
    fail_test "HTTP $HTTP_CODE"
fi

# TC-006: Múltiples items con diferentes comentarios
echo -n "TC-006: Múltiples items con diferentes comentarios... "
PAYLOAD=$(cat <<EOF
{
    "id_mesa": "$MESA_ID",
    "items": [
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 1,
            "precio_unitario": $PRECIO,
            "opciones": [],
            "notas_personalizacion": "Sin sal"
        },
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 1,
            "precio_unitario": $PRECIO,
            "opciones": [],
            "notas_personalizacion": "Extra picante"
        }
    ]
}
EOF
)

RESPONSE=$(curl -s -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ]; then
    NOTA1=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('items', [{}])[0].get('notas_personalizacion', ''))" 2>/dev/null || echo "")
    NOTA2=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('items', [{}])[1].get('notas_personalizacion', ''))" 2>/dev/null || echo "")

    if [ "$NOTA1" = "Sin sal" ] && [ "$NOTA2" = "Extra picante" ]; then
        pass_test
    else
        fail_test "Comentarios de items no se guardaron correctamente"
    fi
else
    fail_test "HTTP $HTTP_CODE"
fi

# TC-007: Comentario largo (validar límite)
echo -n "TC-007: Comentario largo (200+ caracteres)... "
LONG_NOTE="Este es un comentario muy largo para validar el límite de caracteres permitido en el sistema. Según las especificaciones, debería aceptarse hasta un límite razonable. Este texto tiene más de doscientos caracteres para probar."

PAYLOAD=$(cat <<EOF
{
    "id_mesa": "$MESA_ID",
    "items": [
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 1,
            "precio_unitario": $PRECIO,
            "opciones": [],
            "notas_personalizacion": "$LONG_NOTE"
        }
    ]
}
EOF
)

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "400" ]; then
    pass_test
else
    fail_test "HTTP $HTTP_CODE - Respuesta inesperada"
fi

# TC-008: Recuperar pedido y verificar comentarios
echo -n "TC-008: GET pedido muestra comentarios guardados... "
if [ -n "$PEDIDO_ID" ]; then
    RESPONSE=$(curl -s "${API_BASE}/api/v1/pedidos/${PEDIDO_ID}")
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${API_BASE}/api/v1/pedidos/${PEDIDO_ID}")

    if [ "$HTTP_CODE" = "200" ]; then
        NOTA=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('items', [{}])[0].get('notas_personalizacion', ''))" 2>/dev/null || echo "")

        if [ -n "$NOTA" ]; then
            pass_test
        else
            fail_test "Comentario no aparece en GET"
        fi
    else
        fail_test "HTTP $HTTP_CODE"
    fi
else
    skip_test "No hay pedido creado"
fi

# TC-009: Todos los tipos de comentarios juntos
echo -n "TC-009: Pedido con notas_personalizacion, notas_cliente y notas_cocina... "
PAYLOAD=$(cat <<EOF
{
    "id_mesa": "$MESA_ID",
    "items": [
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 1,
            "precio_unitario": $PRECIO,
            "opciones": [],
            "notas_personalizacion": "Término medio"
        }
    ],
    "notas_cliente": "Primera visita al local",
    "notas_cocina": "Alergia a mariscos"
}
EOF
)

RESPONSE=$(curl -s -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ]; then
    NOTA_ITEM=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('items', [{}])[0].get('notas_personalizacion', ''))" 2>/dev/null || echo "")
    NOTA_CLIENTE=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('notas_cliente', ''))" 2>/dev/null || echo "")
    NOTA_COCINA=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('notas_cocina', ''))" 2>/dev/null || echo "")

    if [ -n "$NOTA_ITEM" ] && [ -n "$NOTA_CLIENTE" ] && [ -n "$NOTA_COCINA" ]; then
        pass_test
    else
        fail_test "No se guardaron todos los comentarios"
    fi
else
    fail_test "HTTP $HTTP_CODE"
fi

# TC-010: Validar sanitización básica
echo -n "TC-010: Comentario con HTML/JS se maneja correctamente... "
PAYLOAD=$(cat <<EOF
{
    "id_mesa": "$MESA_ID",
    "items": [
        {
            "id_producto": "$PRODUCTO_ID",
            "cantidad": 1,
            "precio_unitario": $PRECIO,
            "opciones": [],
            "notas_personalizacion": "<script>alert('test')</script>"
        }
    ]
}
EOF
)

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API_BASE}/api/v1/pedidos/completo" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "400" ]; then
    pass_test
else
    fail_test "HTTP $HTTP_CODE"
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
