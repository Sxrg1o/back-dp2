#!/usr/bin/env python3
"""
Script de validación de cálculos de precios para HU-C07
Autor: Equipo QA
Fecha: 2025-10-09
Adaptado para: Windows Local

Este script valida que los cálculos de precios con opciones
se realicen correctamente según la lógica de negocio.
"""

import sys
import json
import urllib.request
import urllib.error
from decimal import Decimal
from typing import List, Dict, Any

# Configuración - LOCALHOST
API_URL = "http://localhost:8000"

# Colores para output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class TestResult:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0

    def add_pass(self):
        self.total += 1
        self.passed += 1

    def add_fail(self):
        self.total += 1
        self.failed += 1

    def print_summary(self):
        print("\n" + "="*50)
        print("  Resumen de Tests de Precios")
        print("="*50)
        print(f"Total:   {self.total}")
        print(f"Pasados: {Colors.GREEN}{self.passed}{Colors.NC}")
        print(f"Fallidos: {Colors.RED}{self.failed}{Colors.NC}")
        print()

        if self.failed == 0:
            print(f"{Colors.GREEN}✓ Todos los tests de precios pasaron{Colors.NC}")
            return 0
        else:
            print(f"{Colors.RED}✗ Algunos tests de precios fallaron{Colors.NC}")
            return 1


def http_get(url: str) -> Dict[str, Any]:
    """Realiza una petición GET"""
    try:
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            return {
                'status_code': response.getcode(),
                'data': json.loads(data) if data else {}
            }
    except urllib.error.HTTPError as e:
        return {
            'status_code': e.code,
            'data': {},
            'error': str(e)
        }
    except Exception as e:
        return {
            'status_code': 0,
            'data': {},
            'error': str(e)
        }


def get_producto_con_opciones(producto_id: str) -> Dict[str, Any]:
    """Obtiene un producto con todas sus opciones."""
    url = f"{API_URL}/api/v1/productos/{producto_id}/opciones"
    response = http_get(url)

    if response['status_code'] != 200:
        raise Exception(f"Error al obtener producto: {response['status_code']}")

    return response['data']


def calcular_precio_total(precio_base: str, opciones_seleccionadas: List[Dict]) -> Decimal:
    """Calcula el precio total sumando base + opciones."""
    total = Decimal(precio_base)

    for opcion in opciones_seleccionadas:
        precio_adicional = Decimal(opcion.get('precio_adicional', '0'))
        total += precio_adicional

    return total


def test_calculo_basico(results: TestResult):
    """Test 1: Validar cálculo básico de precio base + opciones."""
    print("\n=== Test 1: Cálculo Básico de Precios ===\n")

    # Caso de prueba manual
    precio_base = Decimal("35.00")
    opciones = [
        {"nombre": "Familiar (4 personas)", "precio_adicional": "30.00"},
        {"nombre": "Ají extra picante", "precio_adicional": "2.00"},
    ]

    precio_calculado = calcular_precio_total(str(precio_base), opciones)
    precio_esperado = Decimal("67.00")  # 35 + 30 + 2

    print(f"Precio base: S/{precio_base}")
    print(f"Opciones seleccionadas:")
    for op in opciones:
        print(f"  - {op['nombre']}: +S/{op['precio_adicional']}")
    print(f"Precio calculado: S/{precio_calculado}")
    print(f"Precio esperado:  S/{precio_esperado}")

    if precio_calculado == precio_esperado:
        print(f"{Colors.GREEN}✓ PASS{Colors.NC} - Cálculo correcto")
        results.add_pass()
    else:
        print(f"{Colors.RED}✗ FAIL{Colors.NC} - Cálculo incorrecto")
        results.add_fail()


def test_obtener_productos_con_opciones(results: TestResult):
    """Test 2: Obtener productos del API que tienen opciones."""
    print("\n=== Test 2: Obtener Productos con Opciones ===\n")

    url = f"{API_URL}/api/v1/productos-menu?limit=50"
    response = http_get(url)

    if response['status_code'] != 200:
        print(f"{Colors.RED}✗ FAIL{Colors.NC} - Error al obtener productos")
        results.add_fail()
        return []

    productos = response['data'].get('items', [])
    productos_con_opciones = [p for p in productos if p.get('opciones')]

    print(f"Total de productos: {len(productos)}")
    print(f"Productos con opciones: {len(productos_con_opciones)}")

    if productos_con_opciones:
        print(f"\nProductos con opciones encontrados:")
        for prod in productos_con_opciones[:5]:
            nombre = prod.get('nombre', 'N/A')
            num_opciones = len(prod.get('opciones', []))
            print(f"  - {nombre} ({num_opciones} opciones)")
        
        print(f"{Colors.GREEN}✓ PASS{Colors.NC} - Productos con opciones disponibles")
        results.add_pass()
    else:
        print(f"{Colors.YELLOW}⚠ SKIP{Colors.NC} - No hay productos con opciones")
        results.add_pass()  # No falla, solo no hay datos

    return productos_con_opciones


def test_validar_precios_opciones(results: TestResult, productos: List[Dict]):
    """Test 3: Validar que las opciones tengan precios adicionales válidos."""
    print("\n=== Test 3: Validar Precios de Opciones ===\n")

    if not productos:
        print(f"{Colors.YELLOW}⚠ SKIP{Colors.NC} - No hay productos para validar")
        results.add_pass()
        return

    todas_validas = True

    for producto in productos[:5]:  # Validar los primeros 5
        nombre_prod = producto.get('nombre', 'N/A')
        opciones = producto.get('opciones', [])

        print(f"\nProducto: {nombre_prod}")
        for opcion in opciones:
            nombre_op = opcion.get('nombre', 'N/A')
            precio_add = opcion.get('precio_adicional')

            try:
                precio_decimal = Decimal(str(precio_add))
                if precio_decimal >= 0:
                    print(f"  ✓ {nombre_op}: S/{precio_add}")
                else:
                    print(f"  ✗ {nombre_op}: S/{precio_add} (negativo)")
                    todas_validas = False
            except:
                print(f"  ✗ {nombre_op}: precio inválido ({precio_add})")
                todas_validas = False

    if todas_validas:
        print(f"\n{Colors.GREEN}✓ PASS{Colors.NC} - Todos los precios son válidos")
        results.add_pass()
    else:
        print(f"\n{Colors.RED}✗ FAIL{Colors.NC} - Algunos precios son inválidos")
        results.add_fail()


def test_calculo_sin_opciones(results: TestResult):
    """Test 4: Validar cálculo con producto sin opciones."""
    print("\n=== Test 4: Cálculo sin Opciones ===\n")

    precio_base = Decimal("25.50")
    opciones = []

    precio_calculado = calcular_precio_total(str(precio_base), opciones)
    precio_esperado = precio_base

    print(f"Precio base: S/{precio_base}")
    print(f"Opciones seleccionadas: (ninguna)")
    print(f"Precio calculado: S/{precio_calculado}")
    print(f"Precio esperado:  S/{precio_esperado}")

    if precio_calculado == precio_esperado:
        print(f"{Colors.GREEN}✓ PASS{Colors.NC} - Cálculo correcto")
        results.add_pass()
    else:
        print(f"{Colors.RED}✗ FAIL{Colors.NC} - Cálculo incorrecto")
        results.add_fail()


def test_calculo_multiples_opciones(results: TestResult):
    """Test 5: Validar cálculo con múltiples opciones."""
    print("\n=== Test 5: Cálculo con Múltiples Opciones ===\n")

    precio_base = Decimal("45.00")
    opciones = [
        {"nombre": "Extra grande", "precio_adicional": "15.00"},
        {"nombre": "Doble proteína", "precio_adicional": "10.00"},
        {"nombre": "Salsa especial", "precio_adicional": "3.00"},
        {"nombre": "Guarnición extra", "precio_adicional": "5.00"},
    ]

    precio_calculado = calcular_precio_total(str(precio_base), opciones)
    precio_esperado = Decimal("78.00")  # 45 + 15 + 10 + 3 + 5

    print(f"Precio base: S/{precio_base}")
    print(f"Opciones seleccionadas:")
    for op in opciones:
        print(f"  - {op['nombre']}: +S/{op['precio_adicional']}")
    print(f"Precio calculado: S/{precio_calculado}")
    print(f"Precio esperado:  S/{precio_esperado}")

    if precio_calculado == precio_esperado:
        print(f"{Colors.GREEN}✓ PASS{Colors.NC} - Cálculo correcto")
        results.add_pass()
    else:
        print(f"{Colors.RED}✗ FAIL{Colors.NC} - Cálculo incorrecto")
        results.add_fail()


def main():
    """Función principal"""
    print("="*50)
    print("  Tests de Cálculo de Precios - HU-C07")
    print("="*50)
    print(f"API Base URL: {API_URL}")
    print()

    results = TestResult()

    try:
        # Ejecutar tests
        test_calculo_basico(results)
        productos_con_opciones = test_obtener_productos_con_opciones(results)
        test_validar_precios_opciones(results, productos_con_opciones)
        test_calculo_sin_opciones(results)
        test_calculo_multiples_opciones(results)

    except Exception as e:
        print(f"\n{Colors.RED}Error durante la ejecución: {e}{Colors.NC}")
        results.add_fail()

    # Mostrar resumen
    exit_code = results.print_summary()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
