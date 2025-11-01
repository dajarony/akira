#!/usr/bin/env python3
"""
Script de prueba rápida para verificar endpoints básicos de Akira
"""

import requests
import time
import subprocess
import sys
from threading import Thread
import signal

def start_server():
    """Inicia el servidor en background"""
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        pass

def test_endpoints():
    """Prueba endpoints básicos"""
    base_url = "http://localhost:8000"
    headers = {"Authorization": "Bearer akira-access-token-2025-MVP-cyberwar"}
    
    # Esperar a que el servidor arranque
    print("⏳ Esperando que el servidor arranque...")
    time.sleep(3)
    
    tests = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/ping", "Ping endpoint"),
        ("GET", "/docs", "Documentation"),
        ("GET", "/status/health", "Health check"),
        ("GET", "/status/version", "Version info"),
    ]
    
    results = []
    
    for method, endpoint, description in tests:
        try:
            url = f"{base_url}{endpoint}"
            
            if endpoint in ["/", "/ping", "/docs"]:
                # Endpoints públicos
                response = requests.get(url, timeout=5)
            else:
                # Endpoints con autenticación
                response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {description}: {response.status_code}")
                results.append(True)
            else:
                print(f"❌ {description}: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)}")
            results.append(False)
    
    success_rate = (sum(results) / len(results)) * 100
    print(f"\n📊 Resultados: {sum(results)}/{len(results)} tests pasaron ({success_rate:.1f}%)")
    
    return success_rate > 80

if __name__ == "__main__":
    print("🚀 Iniciando test de endpoints básicos de Akira...")
    
    # Iniciar servidor en background
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    try:
        # Ejecutar tests
        success = test_endpoints()
        
        if success:
            print("🎉 Tests básicos PASARON - API funcionando correctamente!")
            sys.exit(0)
        else:
            print("⚠️ Algunos tests fallaron - revisar configuración")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Tests interrumpidos por usuario")
        sys.exit(1)