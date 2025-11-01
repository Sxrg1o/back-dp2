# Test script for Windows PowerShell
# CU-01: Crear Pedido Completo Simple

$API_URL = "http://localhost:8000"

Write-Host "=========================================="
Write-Host "  CU-01: Crear Pedido Completo Simple"
Write-Host "=========================================="
Write-Host ""
Write-Host "API Base URL: $API_URL"
Write-Host ""

$TOTAL_TESTS = 0
$PASSED_TESTS = 0
$FAILED_TESTS = 0

Write-Host "=== Preparacion: Obtener IDs necesarios ==="
Write-Host ""

# Obtener ID de una mesa
Write-Host -NoNewline "Obteniendo ID de mesa... "
try {
    $mesaResponse = Invoke-RestMethod -Uri "$API_URL/api/v1/mesas?limit=1" -Method GET
    $MESA_ID = $mesaResponse.items[0].id

    if ($MESA_ID) {
        Write-Host "[OK] Mesa ID: $MESA_ID" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] No se encontraron mesas" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[ERROR] $_" -ForegroundColor Red
    exit 1
}

# Obtener ID de un producto
Write-Host -NoNewline "Obteniendo ID de producto... "
try {
    $productoResponse = Invoke-RestMethod -Uri "$API_URL/api/v1/productos/cards?limit=1" -Method GET
    $PRODUCTO_ID = $productoResponse.items[0].id
    $PRODUCTO_PRECIO = $productoResponse.items[0].precio_base
    $PRODUCTO_NOMBRE = $productoResponse.items[0].nombre

    if ($PRODUCTO_ID) {
        Write-Host "[OK] Producto: $PRODUCTO_NOMBRE (ID: $PRODUCTO_ID, Precio: S/$PRODUCTO_PRECIO)" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] No se encontraron productos" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[ERROR] $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Tests de Creacion de Pedido Simple ==="
Write-Host ""

# TC-001: Crear pedido simple
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$TOTAL_TESTS : Crear pedido simple con 1 item sin opciones... "

$payload = @{
    id_mesa = $MESA_ID
    items = @(
        @{
            id_producto = $PRODUCTO_ID
            cantidad = 1
            precio_unitario = $PRODUCTO_PRECIO
            opciones = @()
            notas_personalizacion = $null
        }
    )
    notas_cliente = "Test pedido simple"
    notas_cocina = $null
} | ConvertTo-Json -Depth 10

try {
    $pedidoResponse = Invoke-RestMethod -Uri "$API_URL/api/v1/pedidos/completo" -Method POST -Body $payload -ContentType "application/json"
    Write-Host "[PASS] Status: 201" -ForegroundColor Green
    $PASSED_TESTS++
    $PEDIDO_ID = $pedidoResponse.id
    $NUMERO_PEDIDO = $pedidoResponse.numero_pedido
} catch {
    Write-Host "[FAIL] Error: $_" -ForegroundColor Red
    $FAILED_TESTS++
    $PEDIDO_ID = $null
}

Write-Host ""

# TC-002: Validar ID generado
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$TOTAL_TESTS : Validar que pedido tiene ID generado (ULID)... "
if ($PEDIDO_ID -and $PEDIDO_ID.Length -eq 26) {
    Write-Host "[PASS] ID: $PEDIDO_ID" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "[FAIL] ID invalido o vacio" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-003: Validar numero_pedido
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$TOTAL_TESTS : Validar que pedido tiene numero_pedido generado... "
if ($NUMERO_PEDIDO) {
    Write-Host "[PASS] Numero: $NUMERO_PEDIDO" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "[FAIL] Numero de pedido vacio" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-004: Validar estado inicial
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$TOTAL_TESTS : Validar que estado inicial es pendiente... "
$ESTADO = $pedidoResponse.estado
if ($ESTADO -eq "pendiente") {
    Write-Host "[PASS] Estado: $ESTADO" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "[FAIL] Estado esperado: pendiente, obtenido: $ESTADO" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-005: Validar subtotal
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$TOTAL_TESTS : Validar calculo correcto de subtotal... "
$SUBTOTAL = $pedidoResponse.subtotal
if ($SUBTOTAL -eq $PRODUCTO_PRECIO) {
    Write-Host "[PASS] Subtotal: S/$SUBTOTAL" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "[FAIL] Esperado: S/$PRODUCTO_PRECIO, Obtenido: S/$SUBTOTAL" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-006: Validar total
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$TOTAL_TESTS : Validar que total = subtotal... "
$TOTAL = $pedidoResponse.total
if ($TOTAL -eq $SUBTOTAL) {
    Write-Host "[PASS] Total: S/$TOTAL" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "[FAIL] Total: S/$TOTAL != Subtotal: S/$SUBTOTAL" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-007: Validar items
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$TOTAL_TESTS : Validar que pedido contiene items... "
$ITEMS_COUNT = $pedidoResponse.items.Count
if ($ITEMS_COUNT -eq 1) {
    Write-Host "[PASS] Items: $ITEMS_COUNT" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "[FAIL] Esperado: 1 item, Obtenido: $ITEMS_COUNT" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-008: Validar estructura del item
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$TOTAL_TESTS : Validar estructura completa del item... "
$ITEM_ID = $pedidoResponse.items[0].id
$ITEM_CANTIDAD = $pedidoResponse.items[0].cantidad
$ITEM_PRECIO_OPCIONES = [decimal]$pedidoResponse.items[0].precio_opciones

if ($ITEM_ID -and $ITEM_CANTIDAD -eq 1 -and $ITEM_PRECIO_OPCIONES -eq 0) {
    Write-Host "[PASS] ID: OK, Cantidad: $ITEM_CANTIDAD, Precio opciones: S/$ITEM_PRECIO_OPCIONES" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "[FAIL] Estructura incompleta o incorrecta (ID: $ITEM_ID, Cant: $ITEM_CANTIDAD, PrecioOpc: $ITEM_PRECIO_OPCIONES)" -ForegroundColor Red
    $FAILED_TESTS++
}

Write-Host ""
Write-Host "=== Tests de Consulta del Pedido Creado ==="
Write-Host ""

if ($PEDIDO_ID) {
    # TC-009: Obtener pedido por ID
    $TOTAL_TESTS++
    Write-Host -NoNewline "TC-$TOTAL_TESTS : Obtener pedido basico por ID (GET /pedidos/{id})... "
    try {
        $getPedido = Invoke-RestMethod -Uri "$API_URL/api/v1/pedidos/$PEDIDO_ID" -Method GET
        if ($getPedido.id -eq $PEDIDO_ID) {
            Write-Host "[PASS] Status: 200, ID correcto" -ForegroundColor Green
            $PASSED_TESTS++
        } else {
            Write-Host "[FAIL] ID no coincide" -ForegroundColor Red
            $FAILED_TESTS++
        }
    } catch {
        Write-Host "[FAIL] Error: $_" -ForegroundColor Red
        $FAILED_TESTS++
    }

    # TC-010: Obtener pedido por numero
    if ($NUMERO_PEDIDO) {
        $TOTAL_TESTS++
        Write-Host -NoNewline "TC-$TOTAL_TESTS : Obtener pedido basico por numero (GET /pedidos/numero/{numero})... "
        try {
            $getPedidoNum = Invoke-RestMethod -Uri "$API_URL/api/v1/pedidos/numero/$NUMERO_PEDIDO" -Method GET
            if ($getPedidoNum.numero_pedido -eq $NUMERO_PEDIDO) {
                Write-Host "[PASS] Status: 200, Numero correcto" -ForegroundColor Green
                $PASSED_TESTS++
            } else {
                Write-Host "[FAIL] Numero no coincide" -ForegroundColor Red
                $FAILED_TESTS++
            }
        } catch {
            Write-Host "[FAIL] Error: $_" -ForegroundColor Red
            $FAILED_TESTS++
        }
    }
} else {
    Write-Host "[SKIP] No se pudo crear pedido, tests de consulta omitidos" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================="
Write-Host "  Resumen de Tests"
Write-Host "=========================================="
Write-Host "Total:    $TOTAL_TESTS"
Write-Host "Pasados:  $PASSED_TESTS" -ForegroundColor Green
Write-Host "Fallidos: $FAILED_TESTS" -ForegroundColor Red
Write-Host ""

if ($FAILED_TESTS -eq 0) {
    Write-Host "[SUCCESS] Todos los tests pasaron" -ForegroundColor Green
    exit 0
} else {
    Write-Host "[FAILED] Algunos tests fallaron" -ForegroundColor Red
    exit 1
}
