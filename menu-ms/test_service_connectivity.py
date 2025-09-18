#!/usr/bin/env python3
"""
Script para verificar la conectividad y estado del microservicio de menú.
"""

import requests
import time
import json
from typing import Dict, Any, Optional

class ServiceConnectivityTester:
    """Tester de conectividad del servicio."""
    
    def __init__(self, base_url: str = "http://localhost:8002"):
        self.base_url = base_url
        self.timeout = 10
    
    def test_basic_connectivity(self) -> bool:
        """Prueba la conectividad básica al servicio."""
        print("🔌 PROBANDO CONECTIVIDAD BÁSICA")
        print("="*40)
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
            if response.status_code == 200:
                print("✅ Servicio responde correctamente")
                return True
            else:
                print(f"⚠️ Servicio responde pero con código {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar al servicio")
            print("💡 Verifica que el microservicio esté ejecutándose en el puerto 8002")
            return False
        except requests.exceptions.Timeout:
            print("❌ Timeout de conexión")
            print("💡 El servicio puede estar sobrecargado o no responder")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def test_service_info(self) -> Optional[Dict[str, Any]]:
        """Obtiene información del servicio."""
        print("\n📋 INFORMACIÓN DEL SERVICIO")
        print("="*40)
        
        try:
            response = requests.get(f"{self.base_url}/info", timeout=self.timeout)
            if response.status_code == 200:
                info = response.json()
                print("✅ Información del servicio obtenida:")
                for key, value in info.items():
                    print(f"   • {key}: {value}")
                return info
            else:
                print(f"❌ Error al obtener información: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error al obtener información: {e}")
            return None
    
    def test_database_connectivity(self) -> bool:
        """Prueba la conectividad a la base de datos a través de la API."""
        print("\n🗄️ PROBANDO CONECTIVIDAD A BASE DE DATOS")
        print("="*40)
        
        try:
            # Probar endpoint de ingredientes (más simple)
            response = requests.get(f"{self.base_url}/ingredientes/", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Base de datos accesible - {len(data)} ingredientes encontrados")
                return True
            else:
                print(f"❌ Error al acceder a la base de datos: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error al probar base de datos: {e}")
            return False
    
    def test_critical_endpoints(self) -> Dict[str, bool]:
        """Prueba endpoints críticos del servicio."""
        print("\n🎯 PROBANDO ENDPOINTS CRÍTICOS")
        print("="*40)
        
        critical_endpoints = [
            ("/health", "Health Check"),
            ("/", "Root"),
            ("/info", "Información del servicio"),
            ("/ingredientes/", "Listar ingredientes"),
            ("/items/", "Listar ítems"),
            ("/items/with-ingredientes", "Ítems con ingredientes"),
        ]
        
        results = {}
        
        for endpoint, description in critical_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=self.timeout)
                if response.status_code == 200:
                    print(f"✅ {description}")
                    results[endpoint] = True
                else:
                    print(f"❌ {description} - Código: {response.status_code}")
                    results[endpoint] = False
            except Exception as e:
                print(f"❌ {description} - Error: {str(e)[:50]}...")
                results[endpoint] = False
        
        return results
    
    def test_performance(self) -> Dict[str, Any]:
        """Prueba el rendimiento del servicio."""
        print("\n⚡ PROBANDO RENDIMIENTO")
        print("="*40)
        
        performance_tests = [
            ("/health", "Health Check"),
            ("/ingredientes/", "Listar ingredientes"),
            ("/items/", "Listar ítems"),
            ("/items/with-ingredientes", "Ítems con ingredientes"),
        ]
        
        results = {}
        
        for endpoint, description in performance_tests:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=self.timeout)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # ms
                
                if response.status_code == 200:
                    print(f"✅ {description}: {response_time:.2f}ms")
                    results[endpoint] = {
                        "success": True,
                        "response_time_ms": response_time,
                        "status_code": response.status_code
                    }
                else:
                    print(f"❌ {description}: {response.status_code} ({response_time:.2f}ms)")
                    results[endpoint] = {
                        "success": False,
                        "response_time_ms": response_time,
                        "status_code": response.status_code
                    }
            except Exception as e:
                print(f"❌ {description}: Error - {str(e)[:50]}...")
                results[endpoint] = {
                    "success": False,
                    "error": str(e)
                }
        
        return results
    
    def generate_diagnosis(self, connectivity: bool, db_ok: bool, 
                          critical_results: Dict[str, bool], 
                          performance: Dict[str, Any]) -> str:
        """Genera un diagnóstico basado en los resultados."""
        print("\n🔍 DIAGNÓSTICO FINAL")
        print("="*40)
        
        issues = []
        recommendations = []
        
        # Analizar conectividad
        if not connectivity:
            issues.append("❌ El servicio no responde")
            recommendations.append("• Verificar que el microservicio esté ejecutándose")
            recommendations.append("• Comprobar que el puerto 8002 esté disponible")
        else:
            print("✅ Conectividad básica: OK")
        
        # Analizar base de datos
        if not db_ok:
            issues.append("❌ Problemas con la base de datos")
            recommendations.append("• Verificar que la base de datos esté creada")
            recommendations.append("• Ejecutar el script de datos de prueba")
        else:
            print("✅ Base de datos: OK")
        
        # Analizar endpoints críticos
        failed_endpoints = [ep for ep, ok in critical_results.items() if not ok]
        if failed_endpoints:
            issues.append(f"❌ {len(failed_endpoints)} endpoints críticos fallan")
            recommendations.append("• Revisar los logs del microservicio")
            recommendations.append("• Verificar la configuración de la base de datos")
        else:
            print("✅ Endpoints críticos: OK")
        
        # Analizar rendimiento
        slow_endpoints = [ep for ep, data in performance.items() 
                         if data.get("success") and data.get("response_time_ms", 0) > 1000]
        if slow_endpoints:
            issues.append(f"⚠️ {len(slow_endpoints)} endpoints son lentos (>1s)")
            recommendations.append("• Considerar optimizaciones de base de datos")
            recommendations.append("• Implementar cache si es necesario")
        
        # Mostrar resumen
        if not issues:
            print("🎉 ¡El servicio está funcionando perfectamente!")
        else:
            print("⚠️ Problemas encontrados:")
            for issue in issues:
                print(f"   {issue}")
        
        if recommendations:
            print("\n💡 Recomendaciones:")
            for rec in recommendations:
                print(f"   {rec}")
        
        return "OK" if not issues else "ISSUES_FOUND"
    
    def run_full_test(self) -> str:
        """Ejecuta todas las pruebas de conectividad."""
        print("🚀 INICIANDO PRUEBAS DE CONECTIVIDAD")
        print("="*50)
        print(f"🌐 URL Base: {self.base_url}")
        print(f"⏱️ Timeout: {self.timeout}s")
        
        # Pruebas básicas
        connectivity = self.test_basic_connectivity()
        if not connectivity:
            return "NO_CONNECTIVITY"
        
        # Información del servicio
        service_info = self.test_service_info()
        
        # Base de datos
        db_ok = self.test_database_connectivity()
        
        # Endpoints críticos
        critical_results = self.test_critical_endpoints()
        
        # Rendimiento
        performance = self.test_performance()
        
        # Diagnóstico final
        diagnosis = self.generate_diagnosis(connectivity, db_ok, critical_results, performance)
        
        return diagnosis

def main():
    """Función principal."""
    print("🔧 TESTER DE CONECTIVIDAD - MICROSERVICIO DE MENÚ")
    print("="*60)
    
    # Verificar argumentos
    import sys
    base_url = "http://localhost:8002"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    # Crear tester y ejecutar
    tester = ServiceConnectivityTester(base_url)
    result = tester.run_full_test()
    
    print(f"\n🏁 RESULTADO FINAL: {result}")
    
    if result == "OK":
        print("✅ El servicio está listo para usar")
    elif result == "NO_CONNECTIVITY":
        print("❌ No se puede conectar al servicio")
        print("💡 Ejecuta: python main.py")
    else:
        print("⚠️ El servicio tiene algunos problemas")
        print("💡 Revisa las recomendaciones anteriores")

if __name__ == "__main__":
    main()
