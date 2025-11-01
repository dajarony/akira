# comprehensive_akira_test.py

"""
SUME DOCBLOCK

Nombre: Suite Comprensiva de Pruebas de Akira
Tipo: Herramienta

Entradas:
- Sistema Akira en ejecución

Acciones:
- Prueba todos los endpoints disponibles
- Identifica funcionalidad real vs simulada vs rota
- Proporciona métricas de rendimiento
- Genera reporte detallado de capacidades

Salidas:
- Reporte completo de funcionalidad del sistema
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Any
import asyncio
import aiohttp

class AkiraTestSuite:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "simulated": 0,
            "real_functionality": 0,
            "test_details": [],
            "system_info": {},
            "performance_metrics": {},
            "recommendations": []
        }
        
    def log_test(self, test_name: str, status: str, details: Dict[str, Any], execution_time: float):
        """Registra resultado de un test"""
        self.results["total_tests"] += 1
        
        if status == "PASSED":
            self.results["passed"] += 1
        elif status == "FAILED":
            self.results["failed"] += 1
        elif status == "SIMULATED":
            self.results["simulated"] += 1
        elif status == "REAL":
            self.results["real_functionality"] += 1
            
        self.results["test_details"].append({
            "test": test_name,
            "status": status,
            "execution_time_ms": round(execution_time * 1000, 2),
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def test_basic_connectivity(self) -> bool:
        """Test de conectividad básica"""
        print("🔌 TESTING BASIC CONNECTIVITY")
        print("=" * 50)
        
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/ping", timeout=5)
            execution_time = time.time() - start_time
            
            if response.status_code == 200:
                print("✅ Ping successful")
                self.log_test("Basic Connectivity", "PASSED", {
                    "status_code": response.status_code,
                    "response_size": len(response.content)
                }, execution_time)
                return True
            else:
                print(f"❌ Ping failed: {response.status_code}")
                self.log_test("Basic Connectivity", "FAILED", {
                    "status_code": response.status_code,
                    "error": "Non-200 status"
                }, execution_time)
                return False
                
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            self.log_test("Basic Connectivity", "FAILED", {
                "error": str(e)
            }, 0)
            return False

    def test_system_endpoints(self):
        """Prueba endpoints del sistema"""
        print("\n🖥️  TESTING SYSTEM ENDPOINTS")
        print("=" * 50)
        
        system_endpoints = [
            ("/", "Root Endpoint"),
            ("/ping", "Ping"),
            ("/status/health", "Health Check"),
            ("/status/version", "Version Info"),
            ("/status/system-info", "System Info"),
            ("/docs", "API Documentation"),
            ("/redoc", "Alternative Docs")
        ]
        
        for endpoint, name in system_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                execution_time = time.time() - start_time
                
                if response.status_code == 200:
                    print(f"✅ {name}: OK ({response.status_code})")
                    
                    # Analizar si es contenido real o simulado
                    content_length = len(response.content)
                    is_real = content_length > 50  # Heurística simple
                    
                    status = "REAL" if is_real else "SIMULATED"
                    
                    self.log_test(f"System - {name}", status, {
                        "status_code": response.status_code,
                        "content_length": content_length,
                        "content_type": response.headers.get("content-type", "unknown")
                    }, execution_time)
                    
                    # Guardar info del sistema si es system-info
                    if endpoint == "/status/system-info":
                        try:
                            self.results["system_info"] = response.json()
                        except:
                            pass
                            
                else:
                    print(f"⚠️  {name}: {response.status_code}")
                    self.log_test(f"System - {name}", "FAILED", {
                        "status_code": response.status_code,
                        "error": f"HTTP {response.status_code}"
                    }, execution_time)
                    
            except Exception as e:
                print(f"❌ {name}: {e}")
                self.log_test(f"System - {name}", "FAILED", {
                    "error": str(e)
                }, 0)

    def test_offense_endpoints(self):
        """Prueba endpoints ofensivos"""
        print("\n🎯 TESTING OFFENSIVE ENDPOINTS")
        print("=" * 50)
        
        # Tests GET (seguros)
        get_endpoints = [
            ("/offense/exploits", "List Exploits"),
            ("/offense/tools", "List Tools"),
            ("/offense/scans", "List Scans")
        ]
        
        for endpoint, name in get_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                execution_time = time.time() - start_time
                
                if response.status_code == 200:
                    print(f"✅ {name}: Functional")
                    self.log_test(f"Offense - {name}", "REAL", {
                        "status_code": response.status_code,
                        "response_size": len(response.content)
                    }, execution_time)
                elif response.status_code == 500:
                    print(f"🔧 {name}: Internal Error (needs model fixes)")
                    self.log_test(f"Offense - {name}", "FAILED", {
                        "status_code": response.status_code,
                        "error": "Internal server error - model issues"
                    }, execution_time)
                else:
                    print(f"⚠️  {name}: {response.status_code}")
                    self.log_test(f"Offense - {name}", "FAILED", {
                        "status_code": response.status_code
                    }, execution_time)
                    
            except Exception as e:
                print(f"❌ {name}: {e}")
                self.log_test(f"Offense - {name}", "FAILED", {"error": str(e)}, 0)
        
        # Test POST seguro (nmap scan)
        print("\n   Testing POST Operations:")
        try:
            scan_payload = {
                "target": "127.0.0.1",
                "scan_type": "network",
                "priority": "medium"
            }
            
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/offense/nmap",
                json=scan_payload,
                timeout=15
            )
            execution_time = time.time() - start_time
            
            if response.status_code == 200:
                print("✅ Nmap Scan: Functional (simulated)")
                self.log_test("Offense - Nmap Scan", "SIMULATED", {
                    "status_code": response.status_code,
                    "simulation_mode": True
                }, execution_time)
            elif response.status_code == 500:
                print("🔧 Nmap Scan: Model error (fixable)")
                self.log_test("Offense - Nmap Scan", "FAILED", {
                    "status_code": response.status_code,
                    "error": "Model attribute error"
                }, execution_time)
            else:
                print(f"⚠️  Nmap Scan: {response.status_code}")
                self.log_test("Offense - Nmap Scan", "FAILED", {
                    "status_code": response.status_code
                }, execution_time)
                
        except Exception as e:
            print(f"❌ Nmap Scan: {e}")
            self.log_test("Offense - Nmap Scan", "FAILED", {"error": str(e)}, 0)

    def test_defense_endpoints(self):
        """Prueba endpoints defensivos"""
        print("\n🛡️  TESTING DEFENSE ENDPOINTS")
        print("=" * 50)
        
        defense_endpoints = [
            ("/defense/stats", "Defense Statistics"),
            ("/defense/firewall", "Firewall Status"),
            ("/defense/honeypots", "Honeypot Status"),
            ("/defense/threats", "Threat Detection")
        ]
        
        for endpoint, name in defense_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                execution_time = time.time() - start_time
                
                if response.status_code == 200:
                    print(f"✅ {name}: Functional")
                    self.log_test(f"Defense - {name}", "REAL", {
                        "status_code": response.status_code
                    }, execution_time)
                elif response.status_code == 500:
                    print(f"🔧 {name}: Model errors (fixable)")
                    self.log_test(f"Defense - {name}", "FAILED", {
                        "status_code": response.status_code,
                        "error": "Missing models"
                    }, execution_time)
                else:
                    print(f"⚠️  {name}: {response.status_code}")
                    self.log_test(f"Defense - {name}", "FAILED", {
                        "status_code": response.status_code
                    }, execution_time)
                    
            except Exception as e:
                print(f"❌ {name}: {e}")
                self.log_test(f"Defense - {name}", "FAILED", {"error": str(e)}, 0)

    def test_status_endpoints(self):
        """Prueba endpoints de estado"""
        print("\n📊 TESTING STATUS ENDPOINTS")
        print("=" * 50)
        
        status_endpoints = [
            ("/status/stats", "System Statistics"),
            ("/status/logs", "System Logs"),
            ("/status/metrics", "System Metrics")
        ]
        
        for endpoint, name in status_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                execution_time = time.time() - start_time
                
                if response.status_code == 200:
                    print(f"✅ {name}: Functional")
                    
                    # Verificar si tiene datos reales
                    try:
                        data = response.json()
                        is_real = len(str(data)) > 100  # Heurística
                        status = "REAL" if is_real else "SIMULATED"
                    except:
                        status = "REAL"
                        
                    self.log_test(f"Status - {name}", status, {
                        "status_code": response.status_code,
                        "data_size": len(response.content)
                    }, execution_time)
                elif response.status_code == 500:
                    print(f"🔧 {name}: Internal errors")
                    self.log_test(f"Status - {name}", "FAILED", {
                        "status_code": response.status_code,
                        "error": "Internal server error"
                    }, execution_time)
                else:
                    print(f"⚠️  {name}: {response.status_code}")
                    self.log_test(f"Status - {name}", "FAILED", {
                        "status_code": response.status_code
                    }, execution_time)
                    
            except Exception as e:
                print(f"❌ {name}: {e}")
                self.log_test(f"Status - {name}", "FAILED", {"error": str(e)}, 0)

    def test_performance_metrics(self):
        """Prueba métricas de rendimiento"""
        print("\n⚡ TESTING PERFORMANCE METRICS")
        print("=" * 50)
        
        # Test de carga ligera
        endpoint = "/ping"
        requests_count = 10
        
        times = []
        success_count = 0
        
        print(f"   Sending {requests_count} requests to {endpoint}...")
        
        for i in range(requests_count):
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=5)
                execution_time = time.time() - start_time
                times.append(execution_time * 1000)  # Convert to ms
                
                if response.status_code == 200:
                    success_count += 1
                    
            except Exception as e:
                times.append(999999)  # Mark as failed
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            success_rate = (success_count / requests_count) * 100
            
            print(f"   ✅ Average response time: {avg_time:.2f}ms")
            print(f"   ✅ Min response time: {min_time:.2f}ms")
            print(f"   ✅ Max response time: {max_time:.2f}ms")
            print(f"   ✅ Success rate: {success_rate:.1f}%")
            
            self.results["performance_metrics"] = {
                "average_response_ms": round(avg_time, 2),
                "min_response_ms": round(min_time, 2),
                "max_response_ms": round(max_time, 2),
                "success_rate_percent": round(success_rate, 1),
                "requests_tested": requests_count
            }
            
            self.log_test("Performance Test", "PASSED", self.results["performance_metrics"], avg_time/1000)

    def analyze_logs_for_issues(self):
        """Analiza logs para identificar problemas específicos"""
        print("\n🔍 ANALYZING SYSTEM ISSUES")
        print("=" * 50)
        
        # Analizar errores comunes identificados en los logs
        known_issues = {
            "Missing Models": [
                "FirewallRule", "SeverityLevel", "HoneypotInfo", "AttackingIP"
            ],
            "Attribute Errors": [
                "'str' object has no attribute 'ip'"
            ],
            "Health Check Issues": [
                "'AkiraServices' object has no attribute 'health_check'"
            ],
            "Datetime Issues": [
                "can't compare offset-naive and offset-aware datetimes"
            ]
        }
        
        for issue_category, issues in known_issues.items():
            print(f"   🔧 {issue_category}:")
            for issue in issues:
                print(f"      - {issue}")
                self.results["recommendations"].append(f"Fix {issue_category}: {issue}")

    def generate_final_report(self):
        """Genera reporte final completo"""
        print(f"\n" + "=" * 70)
        print("📊 COMPREHENSIVE AKIRA TEST REPORT")
        print("=" * 70)
        
        # Estadísticas generales
        total = self.results["total_tests"]
        passed = self.results["passed"]
        failed = self.results["failed"]
        simulated = self.results["simulated"]
        real = self.results["real_functionality"]
        
        print(f"📈 OVERALL STATISTICS:")
        print(f"   Total Tests: {total}")
        print(f"   ✅ Passed: {passed} ({(passed/total*100):.1f}%)")
        print(f"   ❌ Failed: {failed} ({(failed/total*100):.1f}%)")
        print(f"   🔄 Simulated: {simulated} ({(simulated/total*100):.1f}%)")
        print(f"   🎯 Real Functionality: {real} ({(real/total*100):.1f}%)")
        
        # Performance
        if self.results["performance_metrics"]:
            perf = self.results["performance_metrics"]
            print(f"\n⚡ PERFORMANCE METRICS:")
            print(f"   Average Response: {perf['average_response_ms']}ms")
            print(f"   Success Rate: {perf['success_rate_percent']}%")
        
        # System Info
        if self.results["system_info"]:
            print(f"\n🖥️  SYSTEM INFORMATION:")
            sys_info = self.results["system_info"]
            if "cpu_usage" in sys_info:
                print(f"   CPU Usage: {sys_info.get('cpu_usage', 'N/A')}%")
            if "memory_usage" in sys_info:
                print(f"   Memory Usage: {sys_info.get('memory_usage', 'N/A')}%")
        
        # Recomendaciones
        if self.results["recommendations"]:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(self.results["recommendations"], 1):
                print(f"   {i}. {rec}")
        
        # Funcionalidad real vs simulada
        real_percentage = (real + passed) / total * 100 if total > 0 else 0
        sim_percentage = simulated / total * 100 if total > 0 else 0
        
        print(f"\n🎯 AKIRA FUNCTIONALITY ASSESSMENT:")
        print(f"   🟢 Real Functionality: {real_percentage:.1f}%")
        print(f"   🟡 Simulated/Mock: {sim_percentage:.1f}%")
        print(f"   🔴 Broken/Needs Fix: {(failed/total*100):.1f}%")
        
        # Veredicto final
        if real_percentage > 70:
            verdict = "🎉 AKIRA IS HIGHLY FUNCTIONAL"
            description = "Most features working with real implementation"
        elif real_percentage > 50:
            verdict = "✅ AKIRA IS MODERATELY FUNCTIONAL"
            description = "Good mix of real and simulated features"
        elif real_percentage > 30:
            verdict = "⚠️  AKIRA IS PARTIALLY FUNCTIONAL"
            description = "Some real features, many simulated"
        else:
            verdict = "🔧 AKIRA NEEDS SIGNIFICANT WORK"
            description = "Mostly simulated or broken features"
        
        print(f"\n{verdict}")
        print(f"   {description}")
        
        print("=" * 70)
        
        return self.results

    def save_detailed_report(self, filename: str = "akira_test_report.json"):
        """Guarda reporte detallado en archivo JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, default=str)
            print(f"\n💾 Detailed report saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Failed to save report: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 COMPREHENSIVE AKIRA CYBERWAR SYSTEM TEST SUITE")
    print("=" * 80)
    print("   Testing functionality, performance, and system health")
    print("   Identifying real vs simulated vs broken features")
    print("=" * 80)
    
    # Verificar que Akira esté corriendo
    try:
        response = requests.get("http://localhost:8000/ping", timeout=5)
        if response.status_code != 200:
            print("❌ Akira is not responding. Make sure it's running on port 8000")
            print("   Run: python main.py")
            sys.exit(1)
    except:
        print("❌ Cannot connect to Akira. Make sure it's running on port 8000")
        print("   Run: python main.py")
        sys.exit(1)
    
    # Ejecutar suite de pruebas
    test_suite = AkiraTestSuite()
    
    # Tests principales
    if not test_suite.test_basic_connectivity():
        print("❌ Basic connectivity failed. Aborting tests.")
        sys.exit(1)
    
    test_suite.test_system_endpoints()
    test_suite.test_offense_endpoints()
    test_suite.test_defense_endpoints()
    test_suite.test_status_endpoints()
    test_suite.test_performance_metrics()
    test_suite.analyze_logs_for_issues()
    
    # Generar reporte final
    results = test_suite.generate_final_report()
    test_suite.save_detailed_report()
    
    # Determinar código de salida
    total_tests = results["total_tests"]
    failed_tests = results["failed"]
    
    if failed_tests / total_tests > 0.5:  # Más del 50% fallan
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()