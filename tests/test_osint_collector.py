#!/usr/bin/env python3
"""
Test específico para el OSINT Collector de Akira
"""

import asyncio
import sys
from datetime import datetime
import pytest

# Agregar el directorio raíz al path
sys.path.append('.')

from models import OSINTRequest, OSINTType, OSINTSources, ReconDepth
from modules.offense import get_osint_collector

@pytest.mark.asyncio
async def test_osint_collector():
    """Test del OSINT collector"""
    print("🔍 Testing Akira OSINT Collector...")
    
    # Obtener collector
    collector = get_osint_collector()
    
    # Crear request de prueba
    osint_request = OSINTRequest(
        target_domain="example.com",
        osint_type=OSINTType.PASSIVE,
        sources=[
            OSINTSources.DNS_RECORDS,
            OSINTSources.WHOIS,
            OSINTSources.SUBDOMAIN_ENUM,
            OSINTSources.EMAIL_HARVEST
        ],
        depth_level=ReconDepth.SURFACE,
        ai_analysis=False,
        save_results=False
    )
    
    print(f"🎯 Target: {osint_request.target_domain}")
    print(f"🔧 OSINT type: {osint_request.osint_type.value}")
    print(f"📊 Sources: {[s.value for s in osint_request.sources]}")
    print(f"📏 Depth: {osint_request.depth_level.value}")
    
    # Ejecutar recolección OSINT
    start_time = datetime.now()
    print("\n⏳ Ejecutando recolección OSINT...")
    
    try:
        results = await collector.collect_osint(osint_request)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Recolección completada en {duration:.2f} segundos")
        print(f"📊 Resultados:")
        print(f"   - Target: {results.target}")
        print(f"   - OSINT Type: {results.osint_type.value}")
        print(f"   - Execution time: {results.execution_time_seconds:.2f}s")
        print(f"   - Sources used: {len(results.sources_used)}")
        
        # Mostrar dominios encontrados
        if results.domains:
            print(f"\n🌐 Dominios encontrados ({len(results.domains)}):")
            for domain in results.domains[:5]:  # Mostrar solo los primeros 5
                print(f"   - {domain}")
        
        # Mostrar subdominios encontrados
        if results.subdomains:
            print(f"\n🔗 Subdominios encontrados ({len(results.subdomains)}):")
            for subdomain in results.subdomains[:5]:  # Mostrar solo los primeros 5
                print(f"   - {subdomain}")
        
        # Mostrar emails encontrados
        if results.emails:
            print(f"\n📧 Emails encontrados ({len(results.emails)}):")
            for email in results.emails[:5]:  # Mostrar solo los primeros 5
                print(f"   - {email}")
        
        # Mostrar registros DNS
        if results.dns_records:
            print(f"\n🔍 Registros DNS:")
            for record_type, records in results.dns_records.items():
                if records:
                    print(f"   - {record_type}: {len(records)} registros")
        
        # Mostrar información WHOIS
        if results.whois_info:
            print(f"\n📋 WHOIS Info: Disponible")
        
        # Mostrar perfiles sociales
        if results.social_profiles:
            print(f"\n📱 Perfiles sociales ({len(results.social_profiles)}):")
            for profile in results.social_profiles:
                print(f"   - {profile.get('platform', 'N/A')}: {profile.get('url', 'N/A')}")
        
        # Mostrar certificados
        if results.certificates:
            print(f"\n🔐 Certificados ({len(results.certificates)}):")
            for cert in results.certificates:
                print(f"   - CN: {cert.get('common_name', 'N/A')}")
                print(f"     Issuer: {cert.get('issuer', 'N/A')}")
        
        # Mostrar resumen
        if results.summary:
            print(f"\n📝 Resumen:")
            for key, value in results.summary.items():
                print(f"   - {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en recolección OSINT: {str(e)}")
        return False

@pytest.mark.asyncio
async def test_osint_statistics():
    """Test de estadísticas OSINT"""
    print("\n📊 Testing OSINT statistics...")
    
    collector = get_osint_collector()
    
    try:
        stats = await collector.get_osint_statistics()
        print(f"✅ Estadísticas obtenidas:")
        for key, value in stats.items():
            print(f"   - {key}: {value}")
        return True
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {str(e)}")
        return False

@pytest.mark.asyncio
async def test_supported_sources():
    """Test de fuentes soportadas"""
    print("\n🔧 Testing supported sources...")
    
    collector = get_osint_collector()
    
    try:
        sources = collector.get_supported_sources()
        print(f"✅ Fuentes soportadas ({len(sources)}):")
        for source in sources:
            print(f"   - {source['source']}: {source['description']}")
        return True
    except Exception as e:
        print(f"❌ Error obteniendo fuentes: {str(e)}")
        return False

async def main():
    """Función principal de test"""
    print("🚀 Iniciando tests del OSINT Collector de Akira\n")
    
    tests = [
        ("OSINT Collection", test_osint_collector),
        ("OSINT Statistics", test_osint_statistics),
        ("Supported Sources", test_supported_sources),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 Test: {test_name}")
        print('='*60)
        
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
    
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN FINAL")
    print('='*60)
    print(f"Tests pasados: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎉 OSINT Collector funcionando correctamente!")
        return 0
    else:
        print("⚠️ Algunos tests fallaron - revisar implementación")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)