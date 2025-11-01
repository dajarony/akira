# endpoint_discovery.py

"""
SUME DOCBLOCK

Nombre: Descubridor de Endpoints Reales de Akira
Tipo: Herramienta

Entradas:
- Sistema Akira funcionando
- Schema OpenAPI del sistema

Acciones:
- Descubre endpoints reales implementados
- Prueba cada endpoint con métodos correctos
- Detecta autenticación requerida

Salidas:
- Lista de endpoints reales funcionando
- Tests ajustados a la implementación real
"""

import requests
import json
import time
from typing import Dict, List, Any

class AkiraEndpointDiscovery:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.discovered_endpoints = []
        self.working_endpoints = []
        self.auth_required_endpoints = []
        
    def discover_from_openapi(self):
        """Descubre endpoints desde el schema OpenAPI"""
        print("🔍 DISCOVERING REAL ENDPOINTS FROM OPENAPI SCHEMA")
        print("=" * 60)
        
        try:
            response = requests.get(f"{self.base_url}/openapi.json", timeout=10)
            if response.status_code != 200:
                print(f"❌ No se pudo obtener schema OpenAPI: {response.status_code}")
                return False
            
            schema = response.json()
            paths = schema.get("paths", {})
            
            print(f"📋 Endpoints encontrados en schema: {len(paths)}")
            
            for path, methods in paths.items():
                for method, details in methods.items():
                    endpoint_info = {
                        "path": path,
                        "method": method.upper(),
                        "summary": details.get("summary", ""),
                        "tags": details.get("tags", []),
                        "requires_auth": self.check_auth_required(details),
                        "parameters": details.get("parameters", []),
                        "request_body": details.get("requestBody", {})
                    }
                    self.discovered_endpoints.append(endpoint_info)
                    
                    tag = endpoint_info["tags"][0] if endpoint_info["tags"] else "general"
                    auth = "🔒" if endpoint_info["requires_auth"] else "🔓"
                    print(f"   {auth} {method.upper():6} {path:30} [{tag}] {details.get('summary', '')[:40]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error obteniendo schema: {e}")
            return False
    
    def check_auth_required(self, endpoint_details):
        """Verifica si un endpoint requiere autenticación"""
        security = endpoint_details.get("security", [])
        return len(security) > 0
    
    def test_discovered_endpoints(self):
        """Prueba todos los endpoints descubiertos"""
        print(f"\n🧪 TESTING {len(self.discovered_endpoints)} DISCOVERED ENDPOINTS")
        print("=" * 60)
        
        # Agrupar por categorías
        categories = {}
        for endpoint in self.discovered_endpoints:
            tag = endpoint["tags"][0] if endpoint["tags"] else "general"
            if tag not in categories:
                categories[tag] = []
            categories[tag].append(endpoint)
        
        # Probar por categoría
        for category, endpoints in categories.items():
            print(f"\n📂 CATEGORY: {category.upper()}")
            print("-" * 40)
            
            for endpoint in endpoints:
                self.test_single_endpoint(endpoint)
    
    def test_single_endpoint(self, endpoint_info):
        """Prueba un endpoint individual"""
        path = endpoint_info["path"]
        method = endpoint_info["method"]
        requires_auth = endpoint_info["requires_auth"]
        
        try:
            start_time = time.time()
            
            # Preparar headers
            headers = {"Content-Type": "application/json"}
            
            # Preparar datos de prueba según el endpoint
            test_data = self.generate_test_data(endpoint_info)
            
            # Hacer la petición
            url = f"{self.base_url}{path}"
            
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=test_data, headers=headers, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=test_data, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                print(f"   ⚠️  {method:6} {path:30} - Método no soportado en test")
                return
            
            duration = time.time() - start_time
            
            # Analizar respuesta
            success = response.status_code < 400
            auth_issue = response.status_code == 401
            
            if success:
                self.working_endpoints.append(endpoint_info)
                try:
                    response_data = response.json()
                    is_real = self.analyze_response_realness(response_data)
                    real_indicator = "🟢" if is_real else "🟡"
                except:
                    real_indicator = "🔵"
                
                print(f"   ✅ {real_indicator} {method:6} {path:30} - {response.status_code} ({duration:.3f}s)")
                
            elif auth_issue and requires_auth:
                self.auth_required_endpoints.append(endpoint_info)
                print(f"   🔒 🟡 {method:6} {path:30} - Auth required (expected)")
                
            elif auth_issue:
                print(f"   🔒 ❌ {method:6} {path:30} - Unexpected auth required")
                
            else:
                error_detail = f"{response.status_code}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_detail = f"{response.status_code}: {error_data['detail'][:30]}"
                except:
                    pass
                
                print(f"   ❌ 🔴 {method:6} {path:30} - {error_detail}")
        
        except Exception as e:
            print(f"   ❌ ⚠️  {method:6} {path:30} - Error: {str(e)[:30]}")
    
    def generate_test_data(self, endpoint_info):
        """Genera datos de prueba para un endpoint"""
        path = endpoint_info["path"]
        method = endpoint_info["method"]
        
        # Datos de prueba básicos según el tipo de endpoint
        if "scan" in path.lower():
            return {
                "target": "192.168.1.1",
                "scan_type": "network",
                "priority": "medium"
            }
        elif "osint" in path.lower():
            return {
                "target": "example.com",
                "osint_type": "domain_recon",
                "depth": "basic"
            }
        elif "firewall" in path.lower():
            return {
                "rule_name": "test_rule",
                "action": "allow",
                "source_ip": "192.168.1.100"
            }
        elif "honeypot" in path.lower():
            return {
                "honeypot_name": "test_honeypot",
                "honeypot_type": "ssh",
                "port": 2222
            }
        elif "threat" in path.lower():
            return {
                "detection_name": "test_detection",
                "threat_types": ["malware"]
            }
        else:
            # Datos genéricos
            return {
                "target": "test.example.com",
                "type": "test"
            }
    
    def analyze_response_realness(self, response_data):
        """Analiza si una respuesta contiene datos reales"""
        data_str = str(response_data).lower()
        
        # Indicadores de datos reales
        real_indicators = [
            len(data_str) > 100,
            "timestamp" in data_str,
            "id" in data_str,
            "uuid" in data_str,
            "execution_time" in data_str,
            "metadata" in data_str
        ]
        
        # Indicadores de simulación
        mock_indicators = [
            "simulation" in data_str,
            "mock" in data_str,
            "example" in data_str,
            "test" in data_str and len(data_str) < 50
        ]
        
        real_score = sum(real_indicators)
        mock_score = sum(mock_indicators)
        
        return real_score > mock_score
    
    def test_with_simple_auth(self):
        """Prueba endpoints que requieren auth con tokens simples"""
        print(f"\n🔑 TESTING AUTH REQUIRED ENDPOINTS")
        print("=" * 60)
        
        # Tokens de prueba comunes
        test_tokens = [
            "Bearer test",
            "Bearer demo",
            "test-api-key",
            "demo-key"
        ]
        
        if not self.auth_required_endpoints:
            print("   ℹ️  No se encontraron endpoints que requieran autenticación")
            return
        
        for endpoint in self.auth_required_endpoints[:3]:  # Probar solo los primeros 3
            path = endpoint["path"]
            method = endpoint["method"]
            
            print(f"\n   Testing {method} {path}:")
            
            for token in test_tokens:
                try:
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": token,
                        "X-API-Key": token.replace("Bearer ", "")
                    }
                    
                    url = f"{self.base_url}{path}"
                    test_data = self.generate_test_data(endpoint)
                    
                    if method == "GET":
                        response = requests.get(url, headers=headers, timeout=5)
                    else:
                        response = requests.post(url, json=test_data, headers=headers, timeout=5)
                    
                    if response.status_code != 401:
                        status = "✅" if response.status_code < 400 else "⚠️ "
                        print(f"      {status} {token[:15]:15} - {response.status_code}")
                        if response.status_code < 400:
                            break
                    
                except Exception as e:
                    continue
    
    def generate_comprehensive_report(self):
        """Genera reporte comprensivo de descubrimiento"""
        print(f"\n" + "=" * 80)
        print("📊 COMPREHENSIVE ENDPOINT DISCOVERY REPORT")
        print("=" * 80)
        
        total_discovered = len(self.discovered_endpoints)
        working_count = len(self.working_endpoints)
        auth_required_count = len(self.auth_required_endpoints)
        
        # Estadísticas generales
        working_percentage = (working_count / total_discovered * 100) if total_discovered > 0 else 0
        
        print(f"\n🎯 DISCOVERY STATISTICS:")
        print(f"   Total Endpoints Discovered: {total_discovered}")
        print(f"   Working Endpoints: {working_count}")
        print(f"   Auth Required Endpoints: {auth_required_count}")
        print(f"   Success Rate: {working_percentage:.1f}%")
        
        # Endpoints por categoría
        categories = {}
        for endpoint in self.discovered_endpoints:
            tag = endpoint["tags"][0] if endpoint["tags"] else "general"
            if tag not in categories:
                categories[tag] = {"total": 0, "working": 0}
            categories[tag]["total"] += 1
            if endpoint in self.working_endpoints:
                categories[tag]["working"] += 1
        
        print(f"\n📂 ENDPOINTS BY CATEGORY:")
        for category, stats in categories.items():
            percentage = (stats["working"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"   {category:15}: {stats['working']:2}/{stats['total']:2} ({percentage:5.1f}%)")
        
        # Endpoints que funcionan sin autenticación
        print(f"\n✅ WORKING ENDPOINTS (No Auth Required):")
        for endpoint in self.working_endpoints[:10]:  # Mostrar primeros 10
            path = endpoint["path"]
            method = endpoint["method"]
            summary = endpoint["summary"][:40] if endpoint["summary"] else ""
            print(f"   {method:6} {path:30} - {summary}")
        
        if len(self.working_endpoints) > 10:
            print(f"   ... and {len(self.working_endpoints) - 10} more")
        
        # Recomendaciones
        print(f"\n💡 RECOMMENDATIONS:")
        
        if working_percentage > 70:
            print("   🎉 Excellent! Most endpoints are working")
            print("   📝 Focus on testing the working endpoints")
        elif working_percentage > 40:
            print("   👍 Good coverage of working endpoints")
            print("   🔑 Configure authentication for protected endpoints")
        else:
            print("   ⚠️  Many endpoints require setup or authentication")
            print("   🔧 Check server logs for detailed error information")
        
        if auth_required_count > 0:
            print(f"   🔑 {auth_required_count} endpoints need authentication setup")
        
        # Generar script de test personalizado
        self.generate_custom_test_script()
        
        return {
            "total_discovered": total_discovered,
            "working_count": working_count,
            "success_rate": working_percentage,
            "categories": categories
        }
    
    def generate_custom_test_script(self):
        """Genera un script de test personalizado con los endpoints reales"""
        print(f"\n💾 GENERATING CUSTOM TEST SCRIPT...")
        
        if not self.working_endpoints:
            print("   ⚠️  No working endpoints found - cannot generate test script")
            return
        
        script_content = f'''# akira_real_endpoints_test.py
# Generated automatically from endpoint discovery

import requests
import json
import time

def test_real_akira_endpoints():
    """Test con endpoints reales descubiertos"""
    
    base_url = "http://localhost:8000"
    
    print("🎯 TESTING REAL AKIRA ENDPOINTS")
    print("=" * 50)
    
    # Endpoints que sabemos que funcionan
    working_endpoints = [
'''
        
        for endpoint in self.working_endpoints[:15]:  # Máximo 15 para no hacer el script muy largo
            method = endpoint["method"]
            path = endpoint["path"]
            summary = endpoint["summary"].replace('"', '\\"') if endpoint["summary"] else ""
            
            test_data = json.dumps(self.generate_test_data(endpoint))
            
            script_content += f'''        {{
            "name": "{summary[:30] or f'{method} {path}'}",
            "method": "{method}",
            "path": "{path}",
            "data": {test_data}
        }},
'''
        
        script_content += '''    ]
    
    results = []
    
    for test in working_endpoints:
        try:
            start_time = time.time()
            
            if test["method"] == "GET":
                response = requests.get(f"{base_url}{test['path']}", timeout=10)
            else:
                response = requests.post(f"{base_url}{test['path']}", 
                                       json=test["data"], timeout=10)
            
            duration = time.time() - start_time
            success = response.status_code < 400
            
            status = "✅" if success else "❌"
            print(f"{status} {test['name'][:30]:30} - {response.status_code} ({duration:.3f}s)")
            
            results.append({
                "test": test["name"],
                "success": success,
                "status_code": response.status_code,
                "duration": duration
            })
            
        except Exception as e:
            print(f"❌ {test['name'][:30]:30} - Error: {str(e)[:30]}")
    
    # Resumen
    successful = len([r for r in results if r["success"]])
    total = len(results)
    success_rate = (successful / total * 100) if total > 0 else 0
    
    print(f"\\n📊 REAL ENDPOINTS TEST SUMMARY:")
    print(f"   Success Rate: {successful}/{total} ({success_rate:.1f}%)")
    
    return results

if __name__ == "__main__":
    test_real_akira_endpoints()
'''
        
        try:
            with open("akira_real_endpoints_test.py", "w") as f:
                f.write(script_content)
            print("   ✅ Generated: akira_real_endpoints_test.py")
        except Exception as e:
            print(f"   ❌ Error generating script: {e}")
    
    def run_full_discovery(self):
        """Ejecuta el descubrimiento completo"""
        print("🚀 AKIRA ENDPOINT DISCOVERY & REAL TESTING")
        print("=" * 80)
        
        # Verificar conexión básica
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code != 200:
                print(f"❌ Sistema no responde correctamente: {response.status_code}")
                return False
        except:
            print("❌ No se puede conectar al sistema - ¿Está corriendo 'python main.py'?")
            return False
        
        # Descubrir endpoints
        if not self.discover_from_openapi():
            print("❌ No se pudieron descubrir endpoints")
            return False
        
        # Probar endpoints
        self.test_discovered_endpoints()
        
        # Probar autenticación simple
        self.test_with_simple_auth()
        
        # Generar reporte
        report = self.generate_comprehensive_report()
        
        return report

def main():
    """Función principal"""
    discovery = AkiraEndpointDiscovery()
    result = discovery.run_full_discovery()
    
    if result and result["working_count"] > 0:
        print(f"\n🎉 DISCOVERY COMPLETED - {result['working_count']} WORKING ENDPOINTS FOUND!")
        print("   Run: python akira_real_endpoints_test.py")
    else:
        print(f"\n⚠️  DISCOVERY COMPLETED - LIMITED FUNCTIONALITY DETECTED")

if __name__ == "__main__":
    main()