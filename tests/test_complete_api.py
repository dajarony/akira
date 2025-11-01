#!/usr/bin/env python3
"""
Test script completo para la API de Akira SASE Cyberwar MVP
Prueba todos los endpoints principales del sistema
"""

import asyncio
import aiohttp
import json
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuración de la API
API_BASE_URL = "http://localhost:8000"
API_TOKEN = "akira-dev-token-2024"  # Token de desarrollo

class AkiraAPITester:
    """Tester completo para la API de Akira"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        self.session = None
        self.test_results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Hace una request HTTP a la API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                async with self.session.get(url, headers=self.headers) as response:
                    return {
                        "status": response.status,
                        "data": await response.json() if response.content_type == "application/json" else await response.text()
                    }
            elif method.upper() == "POST":
                async with self.session.post(url, headers=self.headers, json=data) as response:
                    return {
                        "status": response.status,
                        "data": await response.json() if response.content_type == "application/json" else await response.text()
                    }
            elif method.upper() == "DELETE":
                async with self.session.delete(url, headers=self.headers) as response:
                    return {
                        "status": response.status,
                        "data": await response.json() if response.content_type == "application/json" else await response.text()
                    }
        except Exception as e:
            return {
                "status": 500,
                "data": {"error": str(e)}
            }
    
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Registra resultado de un test"""
        self.test_results["total_tests"] += 1
        if success:
            self.test_results["passed"] += 1
            print(f"✅ {test_name}: PASSED {details}")
        else:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"{test_name}: {details}")
            print(f"❌ {test_name}: FAILED {details}")
    
    async def test_basic_endpoints(self):
        """Prueba endpoints básicos"""
        print("\n=== Testing Basic Endpoints ===")
        
        # Test root endpoint
        response = await self.make_request("GET", "/")
        self.log_test_result(
            "Root Endpoint",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
        
        # Test ping endpoint
        response = await self.make_request("GET", "/ping")
        self.log_test_result(
            "Ping Endpoint",
            response["status"] == 200 and response["data"].get("status") == "pong",
            f"Status: {response['status']}"
        )
    
    async def test_status_endpoints(self):
        """Prueba endpoints de estado"""
        print("\n=== Testing Status Endpoints ===")
        
        # Test health check
        response = await self.make_request("GET", "/status/health")
        self.log_test_result(
            "Health Check",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
        
        # Test system info
        response = await self.make_request("GET", "/status/system")
        self.log_test_result(
            "System Info",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
    
    async def test_offense_endpoints(self):
        """Prueba endpoints ofensivos"""
        print("\n=== Testing Offense Endpoints ===")
        
        # Test Nmap scan
        nmap_data = {
            "target": "127.0.0.1",
            "scan_type": "basic",
            "port_range": "80,443,22",
            "ai_analysis": True
        }
        
        response = await self.make_request("POST", "/offense/nmap", nmap_data)
        self.log_test_result(
            "Nmap Scan",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
        
        # Test OSINT collection
        osint_data = {
            "target": "example.com",
            "osint_type": "domain",
            "sources": ["dns", "whois"],
            "ai_analysis": True
        }
        
        response = await self.make_request("POST", "/offense/osint", osint_data)
        self.log_test_result(
            "OSINT Collection",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
        
        # Test exploit list
        response = await self.make_request("GET", "/offense/exploits")
        self.log_test_result(
            "Exploit List",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
    
    async def test_defense_endpoints(self):
        """Prueba endpoints defensivos"""
        print("\n=== Testing Defense Endpoints ===")
        
        # Test firewall status
        response = await self.make_request("GET", "/defense/firewall/status")
        self.log_test_result(
            "Firewall Status",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
        
        # Test block IP
        block_data = {
            "ip_address": "192.168.1.100",
            "threat_level": "high",
            "duration_hours": 1
        }
        
        response = await self.make_request("POST", "/defense/firewall/block-ip", block_data)
        self.log_test_result(
            "Block IP",
            response["status"] in [200, 500],  # 500 expected if no admin rights
            f"Status: {response['status']}"
        )
        
        # Test honeypot status
        response = await self.make_request("GET", "/defense/honeypot/status")
        self.log_test_result(
            "Honeypot Status",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
        
        # Test deploy SSH honeypot
        honeypot_data = {
            "port": 2222,
            "interface": "127.0.0.1"
        }
        
        response = await self.make_request("POST", "/defense/honeypot/deploy/ssh", honeypot_data)
        self.log_test_result(
            "Deploy SSH Honeypot",
            response["status"] in [200, 500],  # May fail if port in use
            f"Status: {response['status']}"
        )
        
        # Test threat detection status
        response = await self.make_request("GET", "/defense/threat-detection/status")
        self.log_test_result(
            "Threat Detection Status",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
        
        # Test log analysis
        log_data = {
            "log_entries": [
                "Failed password for root from 192.168.1.100 port 22 ssh2",
                "Failed password for admin from 192.168.1.100 port 22 ssh2",
                "Failed password for user from 192.168.1.100 port 22 ssh2"
            ],
            "source": "test_system"
        }
        
        response = await self.make_request("POST", "/defense/threat-detection/analyze", log_data)
        self.log_test_result(
            "Log Analysis",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
        
        # Test defense stats
        response = await self.make_request("GET", "/defense/stats")
        self.log_test_result(
            "Defense Statistics",
            response["status"] == 200,
            f"Status: {response['status']}"
        )
    
    async def test_error_handling(self):
        """Prueba manejo de errores"""
        print("\n=== Testing Error Handling ===")
        
        # Test invalid endpoint
        response = await self.make_request("GET", "/invalid/endpoint")
        self.log_test_result(
            "Invalid Endpoint",
            response["status"] == 404,
            f"Status: {response['status']}"
        )
        
        # Test invalid method
        response = await self.make_request("PUT", "/status/health")
        self.log_test_result(
            "Invalid Method",
            response["status"] == 405,
            f"Status: {response['status']}"
        )
        
        # Test invalid JSON
        try:
            url = f"{self.base_url}/offense/nmap"
            async with self.session.post(url, headers=self.headers, data="invalid json") as response:
                self.log_test_result(
                    "Invalid JSON",
                    response.status == 422,
                    f"Status: {response.status}"
                )
        except Exception as e:
            self.log_test_result("Invalid JSON", False, str(e))
    
    async def test_authentication(self):
        """Prueba autenticación"""
        print("\n=== Testing Authentication ===")
        
        # Test without token
        headers_no_auth = {"Content-Type": "application/json"}
        try:
            url = f"{self.base_url}/status/health"
            async with self.session.get(url, headers=headers_no_auth) as response:
                self.log_test_result(
                    "No Authentication",
                    response.status == 401,
                    f"Status: {response.status}"
                )
        except Exception as e:
            self.log_test_result("No Authentication", False, str(e))
        
        # Test with invalid token
        headers_invalid = {
            "Authorization": "Bearer invalid-token",
            "Content-Type": "application/json"
        }
        try:
            url = f"{self.base_url}/status/health"
            async with self.session.get(url, headers=headers_invalid) as response:
                self.log_test_result(
                    "Invalid Token",
                    response.status == 401,
                    f"Status: {response.status}"
                )
        except Exception as e:
            self.log_test_result("Invalid Token", False, str(e))
    
    def print_summary(self):
        """Imprime resumen de resultados"""
        print("\n" + "="*50)
        print("🧪 AKIRA API TEST SUMMARY")
        print("="*50)
        print(f"📊 Total Tests: {self.test_results['total_tests']}")
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        
        if self.test_results['failed'] > 0:
            print(f"\n🔍 Failed Tests:")
            for error in self.test_results['errors']:
                print(f"   - {error}")
        
        success_rate = (self.test_results['passed'] / self.test_results['total_tests']) * 100
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 API is working well!")
        elif success_rate >= 60:
            print("⚠️  API has some issues but is functional")
        else:
            print("🚨 API has significant issues")

async def main():
    """Función principal de testing"""
    print("🚀 Starting Akira SASE Cyberwar MVP API Tests")
    print(f"🌐 Testing API at: {API_BASE_URL}")
    print(f"🔑 Using token: {API_TOKEN[:10]}...")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async with AkiraAPITester() as tester:
        try:
            # Ejecutar todas las pruebas
            await tester.test_basic_endpoints()
            await tester.test_authentication()
            await tester.test_status_endpoints()
            await tester.test_offense_endpoints()
            await tester.test_defense_endpoints()
            await tester.test_error_handling()
            
        except Exception as e:
            print(f"❌ Test execution failed: {str(e)}")
        
        finally:
            # Mostrar resumen
            tester.print_summary()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"❌ Test runner failed: {str(e)}")
        sys.exit(1)