# Script de pruebas para Caso de Uso 1: Crear pedido completo simple
# Autor: Kevin Antonio Navarro Carrera
# Equipo: QA/SEG
# Modulo: Pedidos - Backend
# Fecha: 2025-10-29
# Adaptado para Windows PowerShell

# Configuración
$API_URL = if ($env:API_URL) { $env:API_URL } else { "http://localhost:8000" }
$VERBOSE = if ($env:VERBOSE) { $env:VERBOSE } else { "false" }

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  CU-01: Crear Pedido Completo Simple" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Base URL: $API_URL"
Write-Host ""

# Contador de tests
$TOTAL_TESTS = 0
$PASSED_TESTS = 0
$FAILED_TESTS = 0

# Función para test
function Run-Test {
    param(
        [string]$TestName,
        [string]$ExpectedStatus,
        [string]$Url,
        [string]$Method = "GET",
        [string]$Body = $null
    )

    $script:TOTAL_TESTS++
    Write-Host -NoNewline "TC-$($script:TOTAL_TESTS): $TestName... "

    try {
        $headers = @{ "Content-Type" = "application/json" }

        if ($Method -eq "POST" -and $Body) {
            $response = Invoke-WebRequest -Uri $Url -Method POST -Headers $headers -Body $Body -UseBasicParsing -ErrorAction Stop
        } else {
            $response = Invoke-WebRequest -Uri $Url -Method GET -UseBasicParsing -ErrorAction Stop
        }

        $statusCode = $response.StatusCode.ToString()
        $responseBody = $response.Content

        if ($VERBOSE -eq "true") {
            Write-Host ""
            Write-Host "Response: $responseBody"
            Write-Host "Status: $statusCode"
        }

        if ($statusCode -eq $ExpectedStatus) {
            Write-Host "✓ PASS (Status: $statusCode)" -ForegroundColor Green
            $script:PASSED_TESTS++
            return $responseBody
        } else {
            Write-Host "✗ FAIL (Expected: $ExpectedStatus, Got: $statusCode)" -ForegroundColor Red
            $script:FAILED_TESTS++
            if ($VERBOSE -eq "true") {
                Write-Host "Response body: $responseBody"
            }
            return $null
        }
    } catch {
        $statusCode = if ($_.Exception.Response) { $_.Exception.Response.StatusCode.value__ } else { "Error" }
        Write-Host "✗ FAIL (Expected: $ExpectedStatus, Got: $statusCode)" -ForegroundColor Red
        $script:FAILED_TESTS++
        if ($VERBOSE -eq "true") {
            Write-Host "Error: $_"
        }
        return $null
    }
}

Write-Host "=== Preparación: Obtener IDs necesarios ===" -ForegroundColor Yellow
Write-Host ""

# Obtener ID de una mesa
Write-Host -NoNewline "Obteniendo ID de mesa... "
try {
    $mesaResponse = Invoke-RestMethod -Uri "$API_URL/api/v1/mesas?limit=1" -Method GET -UseBasicParsing
    $MESA_ID = $mesaResponse.items[0].id

    if ($MESA_ID) {
        Write-Host "✓ Mesa ID: $MESA_ID" -ForegroundColor Green
    } else {
        Write-Host "✗ No se encontraron mesas" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Error al obtener mesas: $_" -ForegroundColor Red
    exit 1
}

# Obtener ID de un producto
Write-Host -NoNewline "Obteniendo ID de producto... "
try {
    $productoResponse = Invoke-RestMethod -Uri "$API_URL/api/v1/productos/cards?limit=1" -Method GET -UseBasicParsing
    $PRODUCTO_ID = $productoResponse.items[0].id
    $PRODUCTO_PRECIO = $productoResponse.items[0].precio_base
    $PRODUCTO_NOMBRE = $productoResponse.items[0].nombre

    if ($PRODUCTO_ID) {
        Write-Host "✓ Producto: $PRODUCTO_NOMBRE (ID: $PRODUCTO_ID, Precio: S/$PRODUCTO_PRECIO)" -ForegroundColor Green
    } else {
        Write-Host "✗ No se encontraron productos" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Error al obtener productos: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Tests de Creación de Pedido Simple ===" -ForegroundColor Yellow
Write-Host ""

# TC-001: Crear pedido simple con 1 item sin opciones
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

$testName = 'Crear pedido simple con 1 item sin opciones'
$pedidoResponseJson = Run-Test -TestName $testName -ExpectedStatus "201" -Url "$API_URL/api/v1/pedidos/completo" -Method "POST" -Body $payload

if ($pedidoResponseJson) {
    $pedidoResponse = $pedidoResponseJson | ConvertFrom-Json
    $PEDIDO_ID = $pedidoResponse.id
} else {
    $PEDIDO_ID = $null
}

Write-Host ""

# TC-002: Validar que el pedido tiene ID generado
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$($TOTAL_TESTS): Validar que pedido tiene ID generado (ULID)... "
if ($PEDIDO_ID -and $PEDIDO_ID.Length -eq 26) {
    Write-Host "✓ PASS (ID: $PEDIDO_ID)" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "✗ FAIL (ID inválido o vacío)" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-003: Validar que el pedido tiene numero_pedido generado
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$($TOTAL_TESTS): Validar que pedido tiene numero_pedido generado... "
$NUMERO_PEDIDO = $pedidoResponse.numero_pedido
if ($NUMERO_PEDIDO) {
    Write-Host "✓ PASS (Número: $NUMERO_PEDIDO)" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "✗ FAIL (Número de pedido vacío)" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-004: Validar estado inicial es pendiente
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$($TOTAL_TESTS): Validar que estado inicial es pendiente... "
$ESTADO = $pedidoResponse.estado
if ($ESTADO -eq "pendiente") {
    Write-Host "✓ PASS (Estado: $ESTADO)" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "✗ FAIL (Estado esperado: pendiente, obtenido: $ESTADO)" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-005: Validar cálculo de subtotal
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$($TOTAL_TESTS): Validar cálculo correcto de subtotal... "
$SUBTOTAL = $pedidoResponse.subtotal
if ($SUBTOTAL -eq $PRODUCTO_PRECIO) {
    Write-Host "✓ PASS (Subtotal: S/$SUBTOTAL)" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "✗ FAIL (Esperado: S/$PRODUCTO_PRECIO, Obtenido: S/$SUBTOTAL)" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-006: Validar que total = subtotal
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$($TOTAL_TESTS): Validar que total = subtotal... "
$TOTAL = $pedidoResponse.total
if ($TOTAL -eq $SUBTOTAL) {
    Write-Host "✓ PASS (Total: S/$TOTAL)" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "✗ FAIL (Total: S/$TOTAL != Subtotal: S/$SUBTOTAL)" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-007: Validar que el pedido tiene items
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$($TOTAL_TESTS): Validar que pedido contiene items... "
$ITEMS_COUNT = $pedidoResponse.items.Count
if ($ITEMS_COUNT -eq 1) {
    Write-Host "✓ PASS (Items: $ITEMS_COUNT)" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "✗ FAIL (Esperado: 1 item, Obtenido: $ITEMS_COUNT)" -ForegroundColor Red
    $FAILED_TESTS++
}

# TC-008: Validar estructura del item
$TOTAL_TESTS++
Write-Host -NoNewline "TC-$($TOTAL_TESTS): Validar estructura completa del item... "
$ITEM_ID = $pedidoResponse.items[0].id
$ITEM_CANTIDAD = $pedidoResponse.items[0].cantidad
$ITEM_PRECIO_OPCIONES = $pedidoResponse.items[0].precio_opciones

if ($ITEM_ID -and $ITEM_CANTIDAD -eq 1 -and $ITEM_PRECIO_OPCIONES -eq 0.0) {
    Write-Host "✓ PASS (ID: OK, Cantidad: $ITEM_CANTIDAD, Precio opciones: S/$ITEM_PRECIO_OPCIONES)" -ForegroundColor Green
    $PASSED_TESTS++
} else {
    Write-Host "✗ FAIL (Estructura incompleta o incorrecta)" -ForegroundColor Red
    $FAILED_TESTS++
}

Write-Host ""
Write-Host "=== Tests de Consulta del Pedido Creado ===" -ForegroundColor Yellow
Write-Host ""

if ($PEDIDO_ID) {
    # TC-009: Obtener pedido por ID
    Run-Test -TestName "Obtener pedido por ID (GET /pedidos/{id})" -ExpectedStatus "200" -Url "$API_URL/api/v1/pedidos/$PEDIDO_ID" | Out-Null

    # TC-010: Obtener pedido por número
    if ($NUMERO_PEDIDO) {
        Run-Test -TestName "Obtener pedido por número (GET /pedidos/numero/{numero})" -ExpectedStatus "200" -Url "$API_URL/api/v1/pedidos/numero/$NUMERO_PEDIDO" | Out-Null
    }
} else {
    Write-Host "⚠ SKIP - No se pudo crear pedido, tests de consulta omitidos" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Resumen de Tests" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Total:  $TOTAL_TESTS"
Write-Host "Pasados: $PASSED_TESTS" -ForegroundColor Green
Write-Host "Fallidos: $FAILED_TESTS" -ForegroundColor Red
Write-Host ""

if ($FAILED_TESTS -eq 0) {
    Write-Host "✓ Todos los tests pasaron" -ForegroundColor Green
    exit 0
} else {
    Write-Host "✗ Algunos tests fallaron" -ForegroundColor Red
    exit 1
}
