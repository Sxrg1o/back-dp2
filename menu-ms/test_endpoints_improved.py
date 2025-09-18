#!/usr/bin/env python3
"""
Script mejorado para probar endpoints con diagnósticos específicos.
Incluye análisis detallado de problemas conocidos y soluciones.
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys

class ImprovedMenuServiceTester:
    """Tester mejorado con diagnósticos específicos."""
    
    def __init__(self, base_url: str = "http://localhost:8002"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = {
            "working": [],
            "failing": [],
            "known_issues": [],
            "total_tests": 0,
            "start_time": datetime.now()
        }
        
        # Problemas conocidos y sus soluciones
        self.known_issues = {
            "ingredient_routes": {
                "description": "Rutas específicas de ingredientes fallan (422)",
                "affected_endpoints": ["/ingredientes/verduras", "/ingredientes/carnes", "/ingredientes/frutas", "/ingredientes/low-stock"],
                "cause": "FastAPI interpreta rutas específicas como parámetros de ruta genérica",
                "solution": "Reordenar rutas: específicas antes que genéricas",
                "status": "fixed_in_code"
            },
            "pydantic_validation": {
                "description": "Validación Pydantic falla en endpoints de ítems (500)",
                "affected_endpoints": ["/items/", "/items/filter/price", "/items/filter/etiqueta/SIN_GLUTEN"],
                "cause": "Campo 'tipo' faltante en entidades de dominio para DTOs",
                "solution": "Agregar campo 'tipo' dinámico en método to_domain()",
                "status": "fixed_in_code"
            },
            "duplicate_data": {
                "description": "Error de datos duplicados en seed-data (500)",
                "affected_endpoints": ["/seed-data"],
                "cause": "Constraint de unicidad falla al insertar datos existentes",
                "solution": "Manejar graciosamente datos duplicados",
                "status": "fixed_in_code"
            }
        }
    
    def test_endpoint_with_diagnosis(self, method: str, endpoint: str, description: str, 
                                   expected_status: int = 200, params: Dict = None) -> Dict[str, Any]:
        """Prueba un endpoint con diagnóstico específico."""
        url = f"{self.base_url}{endpoint}"
        self.results["total_tests"] += 1
        
        print(f"\n🔍 Probando: {description}")
        print(f"   📍 {method} {endpoint}")
        
        # Verificar si es un problema conocido
        known_issue = self.check_known_issue(endpoint)
        if known_issue:
            print(f"   ⚠️ Problema conocido: {known_issue['description']}")
            print(f"   💡 Solución: {known_issue['solution']}")
        
        try:
            start_time = time.time()
            
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=params, timeout=10)
            else:
                response = self.session.request(method, url, json=params, timeout=10)
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            result = {
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response_time_ms": round(response_time, 2),
                "success": response.status_code == expected_status,
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "known_issue": known_issue
            }
            
            # Analizar respuesta
            try:
                if response.headers.get('content-type', '').startswith('application/json'):
                    result["response_data"] = response.json()
                    result["data_type"] = "JSON"
                    result["data_size"] = len(str(result["response_data"]))
                else:
                    result["response_text"] = response.text[:500]
                    result["data_type"] = "TEXT"
                    result["data_size"] = len(response.text)
            except Exception as e:
                result["parse_error"] = str(e)
                result["response_text"] = response.text[:500]
                result["data_type"] = "TEXT"
            
            # Determinar resultado
            if result["success"]:
                result["status"] = "✅ ÉXITO"
                self.results["working"].append(result)
                print(f"   ✅ {result['status']} - {response.status_code} ({response_time:.2f}ms)")
                
                if "response_data" in result:
                    data = result["response_data"]
                    if isinstance(data, list):
                        print(f"   📊 Datos: {len(data)} elementos")
                    elif isinstance(data, dict):
                        print(f"   🔑 Campos: {', '.join(data.keys())}")
            else:
                result["status"] = "❌ FALLO"
                result["error"] = f"Esperado {expected_status}, obtenido {response.status_code}"
                self.results["failing"].append(result)
                print(f"   ❌ {result['status']} - {response.status_code} (esperado {expected_status})")
                
                # Diagnóstico específico
                self.diagnose_failure(result, response)
            
            return result
            
        except requests.exceptions.ConnectionError:
            error_result = {
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "status": "❌ CONEXIÓN",
                "error": "No se puede conectar al servicio",
                "success": False,
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            self.results["failing"].append(error_result)
            print(f"   ❌ CONEXIÓN - No se puede conectar al servicio")
            return error_result
            
        except Exception as e:
            error_result = {
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "status": "❌ ERROR",
                "error": str(e),
                "success": False,
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            self.results["failing"].append(error_result)
            print(f"   ❌ ERROR - {str(e)}")
            return error_result
    
    def check_known_issue(self, endpoint: str) -> Optional[Dict]:
        """Verifica si un endpoint tiene un problema conocido."""
        for issue_name, issue_data in self.known_issues.items():
            if endpoint in issue_data["affected_endpoints"]:
                return issue_data
        return None
    
    def diagnose_failure(self, result: Dict, response) -> None:
        """Proporciona diagnóstico específico para fallos."""
        status_code = result["status_code"]
        endpoint = result["endpoint"]
        
        if status_code == 422 and endpoint.startswith("/ingredientes/"):
            print(f"   🔍 Diagnóstico: FastAPI interpreta '{endpoint.split('/')[-1]}' como parámetro de ruta")
            print(f"   💡 Solución: Verificar orden de rutas en ingrediente_handler.py")
        
        elif status_code == 500 and "tipo" in str(result.get("response_data", "")):
            print(f"   🔍 Diagnóstico: Campo 'tipo' faltante en validación Pydantic")
            print(f"   💡 Solución: Verificar método to_domain() en item_model.py")
        
        elif status_code == 500 and "UNIQUE constraint" in str(result.get("response_data", "")):
            print(f"   🔍 Diagnóstico: Datos duplicados en base de datos")
            print(f"   💡 Solución: Manejar graciosamente datos existentes")
        
        else:
            if "response_data" in result:
                print(f"   📄 Error: {result['response_data']}")
            elif "response_text" in result:
                print(f"   📄 Error: {result['response_text'][:200]}...")
    
    def test_critical_endpoints(self):
        """Prueba endpoints críticos con diagnósticos."""
        print("\n" + "="*60)
        print("🎯 PROBANDO ENDPOINTS CRÍTICOS CON DIAGNÓSTICOS")
        print("="*60)
        
        # Health checks
        self.test_endpoint_with_diagnosis("GET", "/health", "Health Check")
        self.test_endpoint_with_diagnosis("GET", "/", "Root endpoint")
        self.test_endpoint_with_diagnosis("GET", "/info", "Información del servicio")
        
        # Endpoints que funcionan bien
        self.test_endpoint_with_diagnosis("GET", "/ingredientes/", "Listar ingredientes")
        self.test_endpoint_with_diagnosis("GET", "/items/with-ingredientes", "Ítems con ingredientes")
        self.test_endpoint_with_diagnosis("GET", "/items/1", "Obtener ítem por ID")
        
        # Endpoints con problemas conocidos
        self.test_endpoint_with_diagnosis("GET", "/ingredientes/verduras", "Obtener verduras")
        self.test_endpoint_with_diagnosis("GET", "/ingredientes/carnes", "Obtener carnes")
        self.test_endpoint_with_diagnosis("GET", "/items/", "Listar ítems")
        self.test_endpoint_with_diagnosis("POST", "/seed-data", "Sembrar datos")
    
    def generate_improved_report(self):
        """Genera reporte mejorado con diagnósticos."""
        end_time = datetime.now()
        duration = (end_time - self.results['start_time']).total_seconds()
        
        print("\n" + "="*80)
        print("📊 REPORTE MEJORADO CON DIAGNÓSTICOS")
        print("="*80)
        
        total = self.results["total_tests"]
        working = len(self.results["working"])
        failing = len(self.results["failing"])
        success_rate = (working / total * 100) if total > 0 else 0
        
        print(f"⏱️ Duración total: {duration:.2f} segundos")
        print(f"📊 Total de pruebas: {total}")
        print(f"✅ Exitosas: {working} ({success_rate:.1f}%)")
        print(f"❌ Fallidas: {failing} ({100-success_rate:.1f}%)")
        
        # Análisis de problemas conocidos
        print(f"\n🔍 ANÁLISIS DE PROBLEMAS CONOCIDOS:")
        for issue_name, issue_data in self.known_issues.items():
            affected_count = sum(1 for fail in self.results["failing"] 
                               if any(ep in fail["endpoint"] for ep in issue_data["affected_endpoints"]))
            status_icon = "✅" if issue_data["status"] == "fixed_in_code" else "⚠️"
            print(f"   {status_icon} {issue_data['description']}: {affected_count} endpoints afectados")
        
        # Endpoints que fallan con diagnóstico
        if self.results["failing"]:
            print(f"\n❌ ENDPOINTS QUE FALLAN CON DIAGNÓSTICO:")
            for fail in self.results["failing"]:
                issue_info = ""
                if fail.get("known_issue"):
                    issue_info = f" - {fail['known_issue']['description']}"
                print(f"   • {fail['method']} {fail['endpoint']}{issue_info}")
        
        # Recomendaciones específicas
        print(f"\n💡 RECOMENDACIONES ESPECÍFICAS:")
        print("   🔧 Para problemas de rutas de ingredientes:")
        print("      - Verificar que las rutas específicas estén antes que /{ingrediente_id}")
        print("      - Reiniciar el servidor después de cambios")
        print("   🔧 Para problemas de validación Pydantic:")
        print("      - Verificar que el campo 'tipo' se agregue dinámicamente")
        print("      - Revisar método to_domain() en item_model.py")
        print("   🔧 Para problemas de datos duplicados:")
        print("      - El endpoint ya maneja graciosamente datos existentes")
        print("      - No es necesario acción adicional")
        
        # Guardar reporte
        self.save_improved_report()
    
    def save_improved_report(self):
        """Guarda reporte mejorado."""
        filename = f"improved_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            "summary": {
                "total_tests": self.results["total_tests"],
                "working": len(self.results["working"]),
                "failing": len(self.results["failing"]),
                "success_rate": (len(self.results["working"]) / self.results["total_tests"] * 100) if self.results["total_tests"] > 0 else 0,
                "start_time": self.results["start_time"].isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - self.results["start_time"]).total_seconds()
            },
            "known_issues": self.known_issues,
            "working_endpoints": self.results["working"],
            "failing_endpoints": self.results["failing"]
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Reporte mejorado guardado en: {filename}")
        except Exception as e:
            print(f"\n⚠️ No se pudo guardar el reporte: {e}")
    
    def run_improved_tests(self):
        """Ejecuta pruebas mejoradas."""
        print("🚀 INICIANDO PRUEBAS MEJORADAS CON DIAGNÓSTICOS")
        print("="*80)
        print(f"🌐 URL Base: {self.base_url}")
        print(f"⏰ Inicio: {self.results['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Verificar conectividad
        print("\n🔌 Verificando conectividad...")
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Servicio disponible")
            else:
                print(f"⚠️ Servicio responde pero con código {response.status_code}")
        except Exception as e:
            print(f"❌ No se puede conectar al servicio: {e}")
            return
        
        # Ejecutar pruebas críticas
        self.test_critical_endpoints()
        
        # Generar reporte
        self.generate_improved_report()

def main():
    """Función principal."""
    print("🧪 TESTER MEJORADO DE ENDPOINTS CON DIAGNÓSTICOS")
    print("="*60)
    
    base_url = "http://localhost:8002"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
        print(f"🌐 Usando URL personalizada: {base_url}")
    
    tester = ImprovedMenuServiceTester(base_url)
    tester.run_improved_tests()
    
    print("\n🎉 ¡Pruebas mejoradas completadas!")
    print("\n💡 Para usar el tester mejorado:")
    print("   python test_endpoints_improved.py")
    print("   python test_endpoints_improved.py http://localhost:8002")

if __name__ == "__main__":
    main()
