#!/usr/bin/env python3
"""
Script de validación de cálculos de precios para HU-C07
Autor: Equipo QA
Fecha: 2025-10-09

Este script valida que los cálculos de precios con opciones
se realicen correctamente según la lógica de negocio.
"""

import sys
import json
import requests
from decimal import Decimal
from typing import List, Dict, Any

# Configuración
API_URL = "https://back-dp2.onrender.com"

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


def get_producto_con_opciones(producto_id: str) -> Dict[str, Any]:
    """Obtiene un producto con todas sus opciones."""
    url = f"{API_URL}/api/v1/productos/{producto_id}/opciones"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error al obtener producto: {response.status_code}")

    return response.json()


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


def test_producto_real_api(results: TestResult):
    """Test 2: Validar cálculo con producto real de la API."""
    print("\n=== Test 2: Cálculo con Producto Real de API ===\n")

    try:
        # Obtener primer producto
        response = requests.get(f"{API_URL}/api/v1/productos/cards?limit=1")
        productos = response.json()

        if not productos.get('items'):
            print(f"{Colors.YELLOW}⚠ SKIP{Colors.NC} - No hay productos disponibles")
            return

        producto_id = productos['items'][0]['id']
        producto_data = get_producto_con_opciones(producto_id)

        print(f"Producto: {producto_data['nombre']}")
        print(f"Precio base: S/{producto_data['precio_base']}")

        if not producto_data.get('opciones'):
            print(f"{Colors.YELLOW}⚠ SKIP{Colors.NC} - Producto sin opciones")
            return

        print(f"Opciones disponibles: {len(producto_data['opciones'])}")

        # Seleccionar opciones que tienen precio adicional > 0
        opciones_con_precio = [
            op for op in producto_data['opciones']
            if Decimal(op['precio_adicional']) > 0
        ]

        if not opciones_con_precio:
            print(f"{Colors.YELLOW}⚠ SKIP{Colors.NC} - No hay opciones con precio adicional")
            return

        # Tomar primeras 3 opciones con precio
        opciones_seleccionadas = opciones_con_precio[:3]

        print(f"\nOpciones seleccionadas para prueba:")
        for op in opciones_seleccionadas:
            print(f"  - {op['nombre']}: +S/{op['precio_adicional']}")

        precio_calculado = calcular_precio_total(
            producto_data['precio_base'],
            opciones_seleccionadas
        )

        # Calcular manualmente para verificar
        precio_esperado = Decimal(producto_data['precio_base'])
        for op in opciones_seleccionadas:
            precio_esperado += Decimal(op['precio_adicional'])

        print(f"\nPrecio calculado por función: S/{precio_calculado}")
        print(f"Precio esperado (manual):     S/{precio_esperado}")

        if precio_calculado == precio_esperado:
            print(f"{Colors.GREEN}✓ PASS{Colors.NC} - Cálculo correcto con producto real")
            results.add_pass()
        else:
            print(f"{Colors.RED}✗ FAIL{Colors.NC} - Cálculo incorrecto")
            results.add_fail()

    except Exception as e:
        print(f"{Colors.RED}✗ ERROR{Colors.NC} - {str(e)}")
        results.add_fail()


def test_multiplicacion_cantidad(results: TestResult):
    """Test 3: Validar multiplicación por cantidad."""
    print("\n=== Test 3: Multiplicación por Cantidad ===\n")

    precio_base = Decimal("35.00")
    opciones = [
        {"nombre": "Familiar", "precio_adicional": "30.00"},
        {"nombre": "Ají picante", "precio_adicional": "2.00"},
    ]

    precio_unitario = calcular_precio_total(str(precio_base), opciones)
    cantidad = 2

    precio_total = precio_unitario * cantidad
    precio_esperado = Decimal("134.00")  # (35 + 30 + 2) * 2

    print(f"Precio unitario: S/{precio_unitario}")
    print(f"Cantidad: {cantidad}")
    print(f"Precio total calculado: S/{precio_total}")
    print(f"Precio esperado:        S/{precio_esperado}")

    if precio_total == precio_esperado:
        print(f"{Colors.GREEN}✓ PASS{Colors.NC} - Multiplicación correcta")
        results.add_pass()
    else:
        print(f"{Colors.RED}✗ FAIL{Colors.NC} - Multiplicación incorrecta")
        results.add_fail()


def test_opciones_sin_costo(results: TestResult):
    """Test 4: Validar opciones sin costo adicional."""
    print("\n=== Test 4: Opciones sin Costo Adicional ===\n")

    precio_base = Decimal("35.00")
    opciones = [
        {"nombre": "Personal", "precio_adicional": "0.00"},
        {"nombre": "Sin ají", "precio_adicional": "0.00"},
        {"nombre": "Ají normal", "precio_adicional": "0.00"},
    ]

    precio_calculado = calcular_precio_total(str(precio_base), opciones)
    precio_esperado = Decimal("35.00")  # Solo precio base

    print(f"Precio base: S/{precio_base}")
    print(f"Opciones seleccionadas (todas sin costo):")
    for op in opciones:
        print(f"  - {op['nombre']}: +S/{op['precio_adicional']}")
    print(f"Precio calculado: S/{precio_calculado}")
    print(f"Precio esperado:  S/{precio_esperado}")

    if precio_calculado == precio_esperado:
        print(f"{Colors.GREEN}✓ PASS{Colors.NC} - Opciones sin costo no afectan precio")
        results.add_pass()
    else:
        print(f"{Colors.RED}✗ FAIL{Colors.NC} - Cálculo incorrecto")
        results.add_fail()


def test_precision_decimales(results: TestResult):
    """Test 5: Validar precisión de decimales."""
    print("\n=== Test 5: Precisión de Decimales ===\n")

    precio_base = Decimal("28.00")
    opciones = [
        {"nombre": "Con yuca", "precio_adicional": "3.50"},
        {"nombre": "Cancha", "precio_adicional": "2.00"},
    ]

    precio_calculado = calcular_precio_total(str(precio_base), opciones)
    precio_esperado = Decimal("33.50")  # 28 + 3.50 + 2

    print(f"Precio base: S/{precio_base}")
    print(f"Opciones con decimales:")
    for op in opciones:
        print(f"  - {op['nombre']}: +S/{op['precio_adicional']}")
    print(f"Precio calculado: S/{precio_calculado}")
    print(f"Precio esperado:  S/{precio_esperado}")

    if precio_calculado == precio_esperado:
        print(f"{Colors.GREEN}✓ PASS{Colors.NC} - Precisión decimal correcta")
        results.add_pass()
    else:
        print(f"{Colors.RED}✗ FAIL{Colors.NC} - Error en precisión decimal")
        results.add_fail()


def main():
    """Ejecuta todos los tests de validación de precios."""
    print("="*50)
    print("  Tests de Validación de Precios HU-C07")
    print("="*50)
    print(f"API Base URL: {API_URL}")

    results = TestResult()

    # Ejecutar tests
    test_calculo_basico(results)
    test_multiplicacion_cantidad(results)
    test_opciones_sin_costo(results)
    test_precision_decimales(results)
    test_producto_real_api(results)

    # Mostrar resumen
    results.print_summary()

    return results.failed


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Tests interrumpidos por el usuario{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}✗ Error fatal: {str(e)}{Colors.NC}")
        sys.exit(1)
