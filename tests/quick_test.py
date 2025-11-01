# quick_test.py - Prueba rápida de Akira

"""
SUME DOCBLOCK

Nombre: Testing Rápido de Akira
Tipo: Herramienta

Entradas:
- Sistema Akira corriendo

Acciones:
- Prueba endpoints básicos rápidamente
- Verifica funcionalidad core

Salidas:
- Reporte rápido de estado
"""

import requests
import json
import time

def test_akira_quick():
    """Test rápido del sistema Akira"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 AKIRA QUICK TEST")
    print("=" * 50)
    
    tests = [
        # Test básico de salud
        ("Sistema Base", "GET", "/"),
        
        # Documentación
        ("Documentación", "GET", "/docs"),
        
        # Status endpoints
        ("Health Check", "GET", "/status/health"),
        ("System Status", "GET", "/status/"),
        
        # Offense endpoints (básicos)
        ("Network Scan", "POST", "/offense/scan/network", {
            "target": "192.168.1.1",
            "scan_type": "network"
        }),
        
        ("OSINT Request", "POST", "/offense/osint/domain", {
            "target": "example.com",
            "osint_type": "domain_recon"
        }),
        
        # Defense endpoints (básicos)
        ("Firewall Status", "GET", "/defense/firewall/status"),
        
        ("Honeypot Status", "GET", "/defense/honeypot/status"),
    ]
    
    results = []
    
    for name, method, endpoint, *data in tests:
        try:
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                payload = data[0] if data else {}
                response = requests.post(f"{base_url}{endpoint}", json=payload, timeout=10)
            
            duration = time.time() - start_time
            success = response.status_code in [200, 201, 202]
            
            # Intentar obtener JSON
            try:
                response_data = response.json()
                # Detectar si es real o simulado
                is_real = detect_real_data(response_data)
            except:
                response_data = response.text[:100]
                is_real = "unknown"
            
            results.append({
                "test": name,
                "success": success,
                "status_code": response.status_code,
                "duration": round(duration, 3),
                "is_real": is_real
            })
            
            status = "✅" if success else "❌"
            real_indicator = "🟢" if is_real else "🟡" if is_real == "partial" else "🔵"
            
            print(f"{status} {real_indicator} {name}: {response.status_code} ({duration:.3f}s)")
            
        except requests.exceptions.ConnectionError:
            print(f"❌ ⚠️  {name}: Conexión rechazada - ¿Sistema corriendo?")
            results.append({"test": name, "success": False, "error": "Connection refused"})
            
        except Exception as e:
            print(f"❌ ⚠️  {name}: Error - {str(e)[:50]}")
            results.append({"test": name, "success": False, "error": str(e)[:50]})
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN RÁPIDO")
    print("=" * 50)
    
    successful = len([r for r in results if r.get("success", False)])
    total = len(results)
    success_rate = (successful / total * 100) if total > 0 else 0
    
    real_count = len([r for r in results if r.get("is_real") == True])
    partial_real = len([r for r in results if r.get("is_real") == "partial"])
    
    print(f"✅ Tests Exitosos: {successful}/{total} ({success_rate:.1f}%)")
    print(f"🟢 Funcionalidad Real: {real_count}")
    print(f"🟡 Funcionalidad Híbrida: {partial_real}")
    
    if success_rate > 80:
        print("🎉 ¡Sistema funcionando excelente!")
    elif success_rate > 50:
        print("👍 Sistema funcionando bien")
    else:
        print("⚠️  Sistema tiene problemas")
    
    # Indicar qué hacer para más funcionalidad real
    if real_count < 3:
        print("\n💡 Para más funcionalidad real:")
        print("   1. python make_akira_real.py")
        print("   2. Configura APIs en .env")
        print("   3. Instala nmap")
    
    return results

def detect_real_data(data):
    """Detecta si los datos son reales o simulados"""
    data_str = str(data).lower()
    
    # Indicadores de simulación
    simulation_keywords = ["simulation", "mock", "example", "test", "demo"]
    if any(keyword in data_str for keyword in simulation_keywords):
        return False
    
    # Indicadores de datos reales
    real_indicators = [
        "timestamp" in data_str,
        "uuid" in data_str or "_id" in data_str,
        len(data_str) > 200,  # Respuestas detalladas
        "execution_time" in data_str,
        "metadata" in data_str
    ]
    
    if sum(real_indicators) >= 2:
        return True
    elif sum(real_indicators) >= 1:
        return "partial"
    else:
        return False

if __name__ == "__main__":
    print("Asegúrate de que Akira esté corriendo: python main.py")
    print("Presiona Enter para continuar...")
    input()
    
    test_akira_quick()