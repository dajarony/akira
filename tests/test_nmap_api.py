#!/usr/bin/env python3
"""
Test del endpoint /offense/nmap via API
"""

import requests
import time
import subprocess
import sys
from threading import Thread
import json

def start_server():
    """Inicia el servidor en background"""
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        pass

def test_nmap_endpoint():
    """Prueba el endpoint /offense/nmap"""
    base_url = "http://localhost:8000"
    headers = {
        "Authorization": "Bearer akira-access-token-2025-MVP-cyberwar",
        "Content-Type": "application/json"
    }
    
    # Esperar a que el servidor arranque
    print("⏳ Esperando que el servidor arranque...")
    time.sleep(3)
    
    # Datos de prueba para el escaneo
    scan_data = {
        "target": {"hostname": "example.com"},
        "scan_type": "tcp_syn",
        "port_range": "80,443,22,3306",
        "ai_analysis": True,
        "save_results": False
    }
    
    print("🔍 Testing /offense/nmap endpoint...")
    print(f"🎯 Target: {scan_data['target']['hostname']}")
    print(f"🔧 Scan type: {scan_data['scan_type']}")
    print(f"🚪 Ports: {scan_data['port_range']}")
    print(f"🤖 AI Analysis: {scan_data['ai_analysis']}")
    
    try:
        print("\n⏳ Enviando request de escaneo...")
        start_time = time.time()
        
        response = requests.post(
            f"{base_url}/offense/nmap",
            headers=headers,
            json=scan_data,
            timeout=30
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"⏱️ Request Duration: {duration:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ Escaneo completado exitosamente!")
            print(f"📊 Resultados:")
            print(f"   - Success: {result.get('success', False)}")
            print(f"   - Message: {result.get('message', 'N/A')}")
            print(f"   - Execution time: {result.get('execution_time_ms', 0):.2f}ms")
            
            # Verificar scan_results
            scan_results = result.get('scan_results')
            if scan_results:
                print(f"   - Scan ID: {scan_results.get('scan_id', 'N/A')}")
                print(f"   - Target: {scan_results.get('target', 'N/A')}")
                print(f"   - Status: {scan_results.get('status', 'N/A')}")
                print(f"   - Hosts found: {len(scan_results.get('hosts_discovered', []))}")
                print(f"   - Ports found: {len(scan_results.get('ports_found', []))}")
                
                # Mostrar puertos encontrados
                ports = scan_results.get('ports_found', [])
                if ports:
                    print(f"\n🚪 Puertos detectados:")
                    for port in ports[:5]:  # Mostrar solo los primeros 5
                        status_icon = "🟢" if port.get('state') == "open" else "🟡" if port.get('state') == "filtered" else "🔴"
                        print(f"   {status_icon} {port.get('port', 'N/A')}/{port.get('protocol', 'N/A')} - {port.get('service', 'N/A')} ({port.get('state', 'N/A')})")
            
            # Verificar AI analysis
            ai_analysis = result.get('ai_analysis')
            if ai_analysis:
                print(f"\n🤖 AI Analysis:")
                print(f"   - Model: {ai_analysis.get('model_used', 'N/A')}")
                print(f"   - Confidence: {ai_analysis.get('confidence_score', 0)}")
                print(f"   - Risk Level: {ai_analysis.get('risk_level', 'N/A')}")
            else:
                print(f"\n🤖 AI Analysis: No disponible (esperado en modo simulación)")
            
            return True
            
        else:
            print(f"❌ Error en request: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   Error details: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"   Raw response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - el escaneo tomó demasiado tiempo")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - servidor no disponible")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_other_offense_endpoints():
    """Prueba otros endpoints ofensivos básicos"""
    base_url = "http://localhost:8000"
    headers = {"Authorization": "Bearer akira-access-token-2025-MVP-cyberwar"}
    
    endpoints = [
        ("GET", "/offense/exploits", "List available exploits"),
        ("GET", "/offense/scan-history/example.com", "Get scan history"),
    ]
    
    results = []
    
    for method, endpoint, description in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description}: {response.status_code}")
                results.append(True)
            else:
                print(f"❌ {description}: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)}")
            results.append(False)
    
    return results

def main():
    """Función principal"""
    print("🚀 Testing Akira Nmap API Endpoint\n")
    
    # Iniciar servidor en background
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    try:
        # Test principal del endpoint nmap
        print("="*60)
        print("🧪 Test: /offense/nmap endpoint")
        print("="*60)
        
        nmap_success = test_nmap_endpoint()
        
        # Test de otros endpoints
        print("\n" + "="*60)
        print("🧪 Test: Other offense endpoints")
        print("="*60)
        
        other_results = test_other_offense_endpoints()
        
        # Resumen final
        total_tests = 1 + len(other_results)
        passed_tests = int(nmap_success) + sum(other_results)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\n{'='*60}")
        print(f"📊 RESUMEN FINAL")
        print('='*60)
        print(f"Tests pasados: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print("🎉 Nmap API endpoint funcionando correctamente!")
            return 0
        else:
            print("⚠️ Algunos tests fallaron - revisar implementación")
            return 1
            
    except KeyboardInterrupt:
        print("\n🛑 Tests interrumpidos por usuario")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)