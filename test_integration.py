#!/usr/bin/env python3
"""
Test de integración Frontend-Backend
Verifica que la comunicación funcione correctamente
"""

import requests
import json
import time

# Configuración
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8080"
API_TOKEN = "akira-dev-token-2024"

def test_backend_connection():
    """Prueba conexión con backend"""
    print("🔧 Testing Backend Connection...")
    
    try:
        # Test ping endpoint
        response = requests.get(f"{BACKEND_URL}/ping", timeout=5)
        if response.status_code == 200:
            print("✅ Backend ping: OK")
            return True
        else:
            print(f"❌ Backend ping failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_authenticated_endpoints():
    """Prueba endpoints autenticados"""
    print("🔐 Testing Authenticated Endpoints...")
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test health endpoint
        response = requests.get(f"{BACKEND_URL}/status/health", headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Authentication: OK")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def test_nmap_endpoint():
    """Prueba endpoint de Nmap"""
    print("🌐 Testing Nmap Endpoint...")
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "target": "127.0.0.1",
        "scan_type": "basic",
        "port_range": "80,443,22",
        "ai_analysis": True
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/offense/nmap", 
                               headers=headers, 
                               json=data, 
                               timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Nmap endpoint: OK")
            print(f"   Target: {result.get('target', 'N/A')}")
            return True
        else:
            print(f"❌ Nmap endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Nmap test failed: {e}")
        return False

def test_osint_endpoint():
    """Prueba endpoint de OSINT"""
    print("🔍 Testing OSINT Endpoint...")
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "target": "example.com",
        "osint_type": "domain",
        "sources": ["dns", "whois"],
        "ai_analysis": True
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/offense/osint", 
                               headers=headers, 
                               json=data, 
                               timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ OSINT endpoint: OK")
            print(f"   Target: {result.get('target', 'N/A')}")
            return True
        else:
            print(f"❌ OSINT endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OSINT test failed: {e}")
        return False

def test_frontend_connection():
    """Prueba conexión con frontend"""
    print("🎨 Testing Frontend Connection...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            if "AKIRA SASE CYBERWAR MVP" in response.text:
                print("✅ Frontend accessible: OK")
                print("✅ Frontend content: OK")
                return True
            else:
                print("❌ Frontend content invalid")
                return False
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🧪 AKIRA INTEGRATION TEST")
    print("="*50)
    
    # Test backend
    backend_ok = test_backend_connection()
    auth_ok = test_authenticated_endpoints() if backend_ok else False
    nmap_ok = test_nmap_endpoint() if auth_ok else False
    osint_ok = test_osint_endpoint() if auth_ok else False
    
    # Test frontend
    frontend_ok = test_frontend_connection()
    
    # Resultados
    print("\n📊 TEST RESULTS:")
    print("="*50)
    print(f"Backend Connection: {'✅ OK' if backend_ok else '❌ FAILED'}")
    print(f"Authentication: {'✅ OK' if auth_ok else '❌ FAILED'}")
    print(f"Nmap Endpoint: {'✅ OK' if nmap_ok else '❌ FAILED'}")
    print(f"OSINT Endpoint: {'✅ OK' if osint_ok else '❌ FAILED'}")
    print(f"Frontend: {'✅ OK' if frontend_ok else '❌ FAILED'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 INTEGRATION TEST PASSED!")
        print("🚀 Frontend and Backend are properly integrated")
        print("🌐 Open http://localhost:8080 to use Akira")
    else:
        print("\n❌ INTEGRATION TEST FAILED!")
        print("🔧 Please check that both servers are running:")
        print("   Backend: python main.py")
        print("   Frontend: cd frontend && python -m http.server 8080")

if __name__ == "__main__":
    main()