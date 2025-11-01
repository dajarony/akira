#!/usr/bin/env python3
"""
Test específico para el Nmap Scanner de Akira
"""

import asyncio
import sys
from datetime import datetime
import pytest

# Agregar el directorio raíz al path
sys.path.append('.')

from models import ScanRequest, ScanType, ScanTarget
from modules.offense import get_nmap_scanner

@pytest.mark.asyncio
async def test_nmap_scanner():
    """Test del nmap scanner en modo simulación"""
    print("🔍 Testing Akira Nmap Scanner...")
    
    # Obtener scanner
    scanner = get_nmap_scanner()
    
    print(f"📡 Nmap disponible: {'✅ Sí' if scanner.nmap_available else '❌ No (modo simulación)'}")
    
    # Crear request de prueba
    scan_request = ScanRequest(
        target={"hostname": "example.com"},
        scan_type=ScanType.TCP_SYN,
        port_range="80,443,22,3306",
        ai_analysis=False,
        save_results=False
    )
    
    print(f"🎯 Target: {scan_request.target.hostname}")
    print(f"🔧 Scan type: {scan_request.scan_type.value}")
    print(f"🚪 Ports: {scan_request.port_range}")
    
    # Ejecutar escaneo
    start_time = datetime.now()
    print("\n⏳ Ejecutando escaneo...")
    
    try:
        results = await scanner.scan_target(scan_request)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Escaneo completado en {duration:.2f} segundos")
        print(f"📊 Resultados:")
        print(f"   - Scan ID: {results.scan_id}")
        print(f"   - Target: {results.target}")
        print(f"   - Status: {results.status.value}")
        print(f"   - Hosts encontrados: {len(results.hosts_discovered)}")
        print(f"   - Puertos encontrados: {len(results.ports_found)}")
        print(f"   - Vulnerabilidades: {len(results.vulnerabilities)}")
        
        if results.hosts_discovered:
            print(f"\n🖥️ Detalles del host:")
            host = results.hosts_discovered[0]
            print(f"   - IP: {host.ip}")
            print(f"   - Hostname: {host.hostname}")
            print(f"   - Status: {host.status}")
            
            print(f"\n🚪 Puertos encontrados:")
            for port in results.ports_found:
                status_icon = "🟢" if port.state == "open" else "🟡" if port.state == "filtered" else "🔴"
                print(f"   {status_icon} {port.port}/{port.protocol} - {port.service} ({port.state})")
        
        print(f"\n📝 Escaneo completado exitosamente")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en escaneo: {str(e)}")
        return False

@pytest.mark.asyncio
async def test_scan_history():
    """Test del historial de escaneos"""
    print("\n📚 Testing scan history...")
    
    scanner = get_nmap_scanner()
    
    try:
        history = await scanner.get_scan_history("example.com", limit=5)
        print(f"✅ Historial obtenido: {len(history)} registros")
        return True
    except Exception as e:
        print(f"❌ Error obteniendo historial: {str(e)}")
        return False

async def main():
    """Función principal de test"""
    print("🚀 Iniciando tests del Nmap Scanner de Akira\n")
    
    tests = [
        ("Nmap Scanner", test_nmap_scanner),
        ("Scan History", test_scan_history),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 Test: {test_name}")
        print('='*50)
        
        try:
            result = await test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_name} falló: {str(e)}")
            results.append(False)
    
    # Resumen final
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"\n{'='*50}")
    print(f"📊 RESUMEN FINAL")
    print('='*50)
    print(f"Tests pasados: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎉 Nmap Scanner funcionando correctamente!")
        return 0
    else:
        print("⚠️ Algunos tests fallaron - revisar implementación")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)