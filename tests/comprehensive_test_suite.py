# comprehensive_test_suite.py

"""
SUME DOCBLOCK

Nombre: Suite de Testing Comprensivo para Sistema Akira
Tipo: Herramienta

Entradas:
- Sistema Akira funcionando en localhost:8000

Acciones:
- Prueba todos los endpoints de la API
- Verifica funcionalidad real vs simulada
- Analiza respuestas y performance
- Detecta qué servicios son reales vs mocks

Salidas:
- Reporte completo de funcionalidad del sistema
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import asyncio
import concurrent.futures

class AkiraSystemTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        self.performance_metrics = {}
        self.real_vs_mock_analysis = {}
        
    def log_test(self, test_name: str, success: bool, response_data: Any = None, 
                 duration: float = 0, notes: str = ""):
        """Registra resultado de un test"""
        self.test_results.append({
            "test": test_name,
            "success": success,
            "duration_ms": round(duration * 1000, 2),
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data,
            "notes": notes
        })
        
        status = "✅" if success else "❌"
        print(f"   {status} {test_name} ({duration:.3f}s) - {notes}")

    def test_system_health(self):
        """Test básico de salud del sistema"""
        print("\n🏥 TESTING SYSTEM HEALTH")
        print("=" * 50)
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("System Health Check", True, response.json(), duration, "API respondiendo")
                return True
            else:
                self.log_test("System Health Check", False, None, duration, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test("System Health Check", False, None, 0, "Conexión rechazada - ¿Sistema corriendo?")
            return False
        except Exception as e:
            self.log_test("System Health Check", False, None, 0, f"Error: {e}")
            return False

    def test_docs_availability(self):
        """Test de disponibilidad de documentación"""
        print("\n📚 TESTING DOCUMENTATION")
        print("=" * 50)
        
        docs_endpoints = [
            ("/docs", "Swagger UI"),
            ("/redoc", "ReDoc"),
            ("/openapi.json", "OpenAPI Schema")
        ]
        
        for endpoint, name in docs_endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                duration = time.time() - start_time
                
                success = response.status_code == 200
                self.log_test(f"Documentation - {name}", success, None, duration,
                            "Disponible" if success else f"HTTP {response.status_code}")
                            
            except Exception as e:
                self.log_test(f"Documentation - {name}", False, None, 0, f"Error: {e}")

    def test_status_endpoints(self):
        """Test de endpoints de status"""
        print("\n📊 TESTING STATUS ENDPOINTS")
        print("=" * 50)
        
        status_tests = [
            ("/status/", "GET", {}, "Status Base"),
            ("/status/health", "GET", {}, "Health Check"),
            ("/status/metrics", "GET", {}, "System Metrics"),
        ]
        
        for endpoint, method, data, name in status_tests:
            try:
                start_time = time.time()
                
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=15)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=15)
                
                duration = time.time() - start_time
                
                success = response.status_code in [200, 201]
                response_data = None
                
                if success:
                    try:
                        response_data = response.json()
                        # Analizar si es real o mock
                        self.analyze_response_authenticity("status", response_data)
                    except:
                        response_data = response.text[:200]
                
                self.log_test(f"Status - {name}", success, response_data, duration,
                            f"HTTP {response.status_code}")
                            
            except Exception as e:
                self.log_test(f"Status - {name}", False, None, 0, f"Error: {e}")

    def test_offense_endpoints(self):
        """Test de endpoints ofensivos"""
        print("\n🎯 TESTING OFFENSE ENDPOINTS")
        print("=" * 50)
        
        offense_tests = [
            # Scans
            ("/offense/scan/network", "POST", {
                "target": "192.168.1.0/24",
                "scan_type": "network",
                "priority": "medium"
            }, "Network Scan"),
            
            ("/offense/scan/port", "POST", {
                "target": "192.168.1.1",
                "scan_type": "port",
                "ports": [22, 80, 443]
            }, "Port Scan"),
            
            # OSINT
            ("/offense/osint/domain", "POST", {
                "target": "example.com",
                "osint_type": "domain_recon",
                "depth": "basic"
            }, "OSINT Domain Recon"),
            
            ("/offense/osint/email", "POST", {
                "target": "example.com",
                "osint_type": "email_harvest"
            }, "Email Harvesting"),
            
            # Exploits (modo verificación)
            ("/offense/exploit/web", "POST", {
                "target": "http://example.com",
                "exploit_type": "web_application",
                "verify_only": True
            }, "Web Exploit Verification"),
        ]
        
        for endpoint, method, data, name in offense_tests:
            try:
                start_time = time.time()
                
                headers = {"Content-Type": "application/json"}
                response = requests.post(f"{self.base_url}{endpoint}", 
                                       json=data, headers=headers, timeout=30)
                
                duration = time.time() - start_time
                
                success = response.status_code in [200, 201, 202]  # 202 for async operations
                response_data = None
                
                if success:
                    try:
                        response_data = response.json()
                        self.analyze_response_authenticity("offense", response_data)
                    except:
                        response_data = response.text[:200]
                
                self.log_test(f"Offense - {name}", success, response_data, duration,
                            f"HTTP {response.status_code}")
                            
            except Exception as e:
                self.log_test(f"Offense - {name}", False, None, 0, f"Error: {e}")

    def test_defense_endpoints(self):
        """Test de endpoints defensivos"""
        print("\n🛡️ TESTING DEFENSE ENDPOINTS")
        print("=" * 50)
        
        defense_tests = [
            # Firewall
            ("/defense/firewall/rule", "POST", {
                "rule_name": "test_rule",
                "action": "allow",
                "source_ip": "192.168.1.100",
                "destination_port": 80
            }, "Firewall Rule Creation"),
            
            ("/defense/firewall/status", "GET", {}, "Firewall Status"),
            
            # Honeypot
            ("/defense/honeypot/deploy", "POST", {
                "honeypot_name": "test_ssh_honeypot",
                "honeypot_type": "ssh",
                "port": 2222
            }, "Honeypot Deployment"),
            
            ("/defense/honeypot/status", "GET", {}, "Honeypot Status"),
            
            # Threat Detection
            ("/defense/threat/configure", "POST", {
                "detection_name": "test_malware_detection",
                "threat_types": ["malware", "intrusion"],
                "ai_enhanced": True
            }, "Threat Detection Config"),
            
            ("/defense/threat/status", "GET", {}, "Threat Detection Status"),
        ]
        
        for endpoint, method, data, name in defense_tests:
            try:
                start_time = time.time()
                
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=20)
                else:
                    headers = {"Content-Type": "application/json"}
                    response = requests.post(f"{self.base_url}{endpoint}", 
                                           json=data, headers=headers, timeout=20)
                
                duration = time.time() - start_time
                
                success = response.status_code in [200, 201, 202]
                response_data = None
                
                if success:
                    try:
                        response_data = response.json()
                        self.analyze_response_authenticity("defense", response_data)
                    except:
                        response_data = response.text[:200]
                
                self.log_test(f"Defense - {name}", success, response_data, duration,
                            f"HTTP {response.status_code}")
                            
            except Exception as e:
                self.log_test(f"Defense - {name}", False, None, 0, f"Error: {e}")

    def analyze_response_authenticity(self, category: str, response_data: Dict[str, Any]):
        """Analiza si una respuesta es real o simulada"""
        
        if category not in self.real_vs_mock_analysis:
            self.real_vs_mock_analysis[category] = {
                "real_indicators": [],
                "mock_indicators": [],
                "confidence_real": 0,
                "confidence_mock": 0
            }
        
        analysis = self.real_vs_mock_analysis[category]
        
        # Indicadores de datos reales
        real_indicators = [
            "timestamp" in str(response_data),
            "uuid" in str(response_data) or "id" in str(response_data),
            len(str(response_data)) > 100,  # Respuestas detalladas
            "metadata" in str(response_data),
            "execution_time" in str(response_data)
        ]
        
        # Indicadores de simulación/mock
        mock_indicators = [
            "simulation" in str(response_data).lower(),
            "mock" in str(response_data).lower(),
            "test" in str(response_data).lower(),
            "example" in str(response_data).lower(),
            len(str(response_data)) < 50  # Respuestas muy cortas
        ]
        
        analysis["real_indicators"].extend([i for i in real_indicators if i])
        analysis["mock_indicators"].extend([i for i in mock_indicators if i])

    def test_performance_stress(self):
        """Test de performance bajo carga"""
        print("\n⚡ TESTING PERFORMANCE")
        print("=" * 50)
        
        def make_request():
            try:
                start = time.time()
                response = requests.get(f"{self.base_url}/status/health", timeout=5)
                return time.time() - start, response.status_code == 200
            except:
                return 0, False
        
        # Test de 10 requests concurrentes
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        durations = [r[0] for r in results if r[1]]
        success_rate = len(durations) / len(results) * 100
        
        if durations:
            avg_response = sum(durations) / len(durations)
            max_response = max(durations)
            min_response = min(durations)
            
            self.performance_metrics = {
                "concurrent_requests": 10,
                "success_rate": success_rate,
                "avg_response_time": avg_response,
                "max_response_time": max_response,
                "min_response_time": min_response
            }
            
            self.log_test("Performance - Concurrent Load", success_rate > 80, 
                         self.performance_metrics, avg_response,
                         f"{success_rate:.1f}% success rate")
        else:
            self.log_test("Performance - Concurrent Load", False, None, 0, "No successful requests")

    def generate_comprehensive_report(self):
        """Genera reporte comprensivo del sistema"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE SYSTEM ANALYSIS REPORT")
        print("=" * 80)
        
        # Estadísticas generales
        total_tests = len(self.test_results)
        successful_tests = len([t for t in self.test_results if t["success"]])
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n🎯 GENERAL STATISTICS:")
        print(f"   Total Tests Executed: {total_tests}")
        print(f"   Successful Tests: {successful_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        # Análisis de autenticidad (Real vs Mock)
        print(f"\n🔍 AUTHENTICITY ANALYSIS (Real vs Mock):")
        for category, analysis in self.real_vs_mock_analysis.items():
            real_score = len(analysis["real_indicators"])
            mock_score = len(analysis["mock_indicators"])
            
            if real_score > mock_score:
                verdict = "🟢 MOSTLY REAL"
            elif mock_score > real_score:
                verdict = "🟡 MOSTLY SIMULATED"
            else:
                verdict = "🔵 MIXED/UNKNOWN"
            
            print(f"   {category.upper()}: {verdict}")
            print(f"      Real indicators: {real_score}")
            print(f"      Mock indicators: {mock_score}")
        
        # Performance
        if self.performance_metrics:
            print(f"\n⚡ PERFORMANCE METRICS:")
            metrics = self.performance_metrics
            print(f"   Average Response Time: {metrics['avg_response_time']:.3f}s")
            print(f"   Success Rate: {metrics['success_rate']:.1f}%")
            print(f"   Max Response Time: {metrics['max_response_time']:.3f}s")
        
        # Tests fallidos
        failed_tests = [t for t in self.test_results if not t["success"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test in failed_tests[:5]:  # Mostrar solo los primeros 5
                print(f"   - {test['test']}: {test['notes']}")
        
        # Recomendaciones
        print(f"\n💡 RECOMMENDATIONS:")
        if success_rate < 50:
            print("   🚨 Critical: Sistema tiene problemas serios")
        elif success_rate < 80:
            print("   ⚠️  Warning: Algunos endpoints no funcionan")
        else:
            print("   ✅ System is functioning well")
            
        # Detectar qué necesita instalación
        nmap_needed = any("nmap" in t["notes"].lower() for t in failed_tests)
        if nmap_needed:
            print("   🔧 Install nmap for real scanning capabilities")
            
        return {
            "total_tests": total_tests,
            "success_rate": success_rate,
            "authenticity_analysis": self.real_vs_mock_analysis,
            "performance_metrics": self.performance_metrics,
            "failed_tests": failed_tests
        }

    def run_full_test_suite(self):
        """Ejecuta la suite completa de tests"""
        print("🚀 STARTING COMPREHENSIVE AKIRA SYSTEM TEST")
        print("=" * 80)
        print(f"Target: {self.base_url}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # Verificar que el sistema esté corriendo
        if not self.test_system_health():
            print("\n❌ CRITICAL: Sistema no está respondiendo")
            print("   Asegúrate de que 'python main.py' esté corriendo")
            return False
        
        # Ejecutar todos los tests
        self.test_docs_availability()
        self.test_status_endpoints()
        self.test_offense_endpoints()
        self.test_defense_endpoints()
        self.test_performance_stress()
        
        # Generar reporte final
        report = self.generate_comprehensive_report()
        
        # Guardar reporte en archivo
        try:
            with open(f"akira_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
                json.dump({
                    "summary": report,
                    "detailed_results": self.test_results
                }, f, indent=2, default=str)
            print("\n💾 Detailed report saved to file")
        except Exception as e:
            print(f"\n⚠️  Could not save report: {e}")
        
        return report["success_rate"] > 70

def main():
    """Función principal"""
    tester = AkiraSystemTester()
    success = tester.run_full_test_suite()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 AKIRA SYSTEM TEST COMPLETED SUCCESSFULLY")
    else:
        print("⚠️  AKIRA SYSTEM TEST COMPLETED WITH ISSUES")
    print("=" * 80)

if __name__ == "__main__":
    main()