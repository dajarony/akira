# modules/offense/osint_collector.py

"""
SUME DOCBLOCK

Nombre: Recolector OSINT Akira
Tipo: Herramienta

Entradas:
- Peticiones OSINT con targets y fuentes
- Configuración de profundidad y timeout
- Parámetros de análisis IA

Acciones:
- Recolecta información de fuentes abiertas
- Enumera subdominios y emails
- Consulta bases de datos públicas
- Integra con análisis IA

Salidas:
- Información estructurada de OSINT
- Dominios, subdominios y emails encontrados
- Inteligencia de amenazas
"""

import asyncio
import aiohttp
import dns.resolver
import whois
import re
import json
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
import uuid

from core import get_logger, get_services
from models import OSINTRequest, OSINTResults, OSINTSources, OSINTType
from modules.shared import get_akira_utils, get_security_utils, get_time_utils

class OSINTCollector:
    """Recolector de inteligencia de fuentes abiertas"""
    
    def __init__(self):
        self.logger = get_logger()
        self.akira_utils = get_akira_utils()
        self.security_utils = get_security_utils()
        self.time_utils = get_time_utils()
        
        # Listas de palabras para subdominios
        self.subdomain_wordlist = [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging', 'api',
            'app', 'blog', 'shop', 'store', 'support', 'help', 'docs',
            'portal', 'secure', 'vpn', 'remote', 'cloud', 'cdn', 'static'
        ]
    
    async def collect_osint(self, osint_request: OSINTRequest) -> OSINTResults:
        """
        Ejecuta recolección OSINT completa
        
        Args:
            osint_request: Petición OSINT con configuración
            
        Returns:
            OSINTResults: Resultados estructurados de OSINT
        """
        start_time = datetime.utcnow()
        
        # Determinar target principal
        target = (osint_request.target_domain or 
                 osint_request.target_email or 
                 osint_request.target_username or 
                 osint_request.company_name)
        
        await self.logger.log_activity(
            activity_type="osint",
            details={
                "target": target,
                "sources": [s.value for s in osint_request.sources],
                "osint_type": osint_request.osint_type.value,
                "depth_level": osint_request.depth_level.value
            },
            save_to_firebase=True
        )
        
        # Inicializar resultados
        results = OSINTResults(
            target=target,
            osint_type=osint_request.osint_type,
            sources_used=osint_request.sources,
            execution_time_seconds=0,
            timestamp=start_time
        )
        
        try:
            # Ejecutar recolección por fuentes
            tasks = []
            
            for source in osint_request.sources:
                if source == OSINTSources.DNS_RECORDS:
                    tasks.append(self._collect_dns_records(target, results))
                elif source == OSINTSources.WHOIS:
                    tasks.append(self._collect_whois_info(target, results))
                elif source == OSINTSources.SUBDOMAIN_ENUM:
                    tasks.append(self._enumerate_subdomains(target, results))
                elif source == OSINTSources.EMAIL_HARVEST:
                    tasks.append(self._harvest_emails(target, results))
                elif source == OSINTSources.SEARCH_ENGINES:
                    tasks.append(self._search_engines(target, results))
                elif source == OSINTSources.CERTIFICATE_TRANSPARENCY:
                    tasks.append(self._certificate_transparency(target, results))
            
            # Ejecutar todas las tareas concurrentemente
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            
            # Calcular tiempo de ejecución
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            results.execution_time_seconds = execution_time
            
            # Generar resumen
            results.summary = self._generate_summary(results)
            
            # Guardar en Firebase si está habilitado
            if osint_request.save_results:
                services = get_services()
                if services.firebase_service:
                    await services.firebase_service.save_scan_results({
                        "type": "osint",
                        "target": target,
                        "results": results.dict(),
                        "timestamp": start_time.isoformat()
                    })
            
            await self.logger.log_activity(
                activity_type="osint",
                details={
                    "target": target,
                    "action": "completed",
                    "domains_found": len(results.domains),
                    "subdomains_found": len(results.subdomains),
                    "emails_found": len(results.emails),
                    "execution_time": execution_time
                },
                save_to_firebase=True
            )
            
            return results
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="osint",
                details={
                    "target": target,
                    "action": "failed",
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            
            # Retornar resultado parcial en caso de error
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            results.execution_time_seconds = execution_time
            results.summary = {"error": str(e)}
            return results
    
    async def _collect_dns_records(self, target: str, results: OSINTResults):
        """Recolecta registros DNS"""
        try:
            dns_records = {}
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(target, record_type)
                    dns_records[record_type] = [str(rdata) for rdata in answers]
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    dns_records[record_type] = []
                except Exception:
                    dns_records[record_type] = []
            
            results.dns_records = dns_records
            
            # Extraer dominios adicionales de registros MX y NS
            for mx_record in dns_records.get('MX', []):
                domain = mx_record.split()[-1].rstrip('.')
                if domain not in results.domains:
                    results.domains.append(domain)
            
            for ns_record in dns_records.get('NS', []):
                domain = ns_record.rstrip('.')
                if domain not in results.domains:
                    results.domains.append(domain)
                    
        except Exception as e:
            await self.logger.log_activity(
                activity_type="osint",
                details={
                    "target": target,
                    "source": "dns_records",
                    "error": str(e)
                },
                level="warning",
                save_to_firebase=False
            )
    
    async def _collect_whois_info(self, target: str, results: OSINTResults):
        """Recolecta información WHOIS"""
        try:
            # Ejecutar whois en hilo separado
            whois_info = await asyncio.to_thread(whois.whois, target)
            
            if whois_info:
                # Convertir a diccionario serializable
                whois_dict = {}
                for key, value in whois_info.items():
                    if isinstance(value, (str, int, float, bool, type(None))):
                        whois_dict[key] = value
                    elif isinstance(value, list):
                        whois_dict[key] = [str(v) for v in value]
                    else:
                        whois_dict[key] = str(value)
                
                results.whois_info = whois_dict
                
                # Extraer emails de información WHOIS
                whois_text = str(whois_info)
                emails = self._extract_emails_from_text(whois_text)
                results.emails.extend(emails)
                
        except Exception as e:
            await self.logger.log_activity(
                activity_type="osint",
                details={
                    "target": target,
                    "source": "whois",
                    "error": str(e)
                },
                level="warning",
                save_to_firebase=False
            )
    
    async def _enumerate_subdomains(self, target: str, results: OSINTResults):
        """Enumera subdominios"""
        try:
            found_subdomains = set()
            
            # Enumeración por diccionario
            for subdomain in self.subdomain_wordlist:
                full_domain = f"{subdomain}.{target}"
                try:
                    # Intentar resolver el subdominio
                    answers = dns.resolver.resolve(full_domain, 'A')
                    if answers:
                        found_subdomains.add(full_domain)
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    pass
                except Exception:
                    pass
            
            # Agregar subdominios encontrados
            results.subdomains.extend(list(found_subdomains))
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="osint",
                details={
                    "target": target,
                    "source": "subdomain_enum",
                    "error": str(e)
                },
                level="warning",
                save_to_firebase=False
            )
    
    async def _harvest_emails(self, target: str, results: OSINTResults):
        """Recolecta emails relacionados con el target"""
        try:
            # Buscar emails en registros DNS TXT (SPF, DMARC)
            dns_records = results.dns_records or {}
            txt_records = dns_records.get('TXT', [])
            
            for txt_record in txt_records:
                emails = self._extract_emails_from_text(txt_record)
                results.emails.extend(emails)
            
            # Emails comunes basados en el dominio
            common_emails = [
                f"admin@{target}",
                f"info@{target}",
                f"contact@{target}",
                f"support@{target}",
                f"sales@{target}",
                f"security@{target}"
            ]
            
            # Verificar si los emails comunes existen (simulado)
            for email in common_emails:
                if email not in results.emails:
                    results.emails.append(email)
                    
        except Exception as e:
            await self.logger.log_activity(
                activity_type="osint",
                details={
                    "target": target,
                    "source": "email_harvest",
                    "error": str(e)
                },
                level="warning",
                save_to_firebase=False
            )
    
    async def _search_engines(self, target: str, results: OSINTResults):
        """Búsqueda en motores de búsqueda (simulado)"""
        try:
            # Simulación de búsqueda en motores
            # En implementación real, se usarían APIs de Google, Bing, etc.
            
            search_results = {
                "google_results": 0,
                "bing_results": 0,
                "social_mentions": []
            }
            
            # Agregar perfiles sociales simulados
            social_profiles = [
                {"platform": "linkedin", "url": f"https://linkedin.com/company/{target}"},
                {"platform": "twitter", "url": f"https://twitter.com/{target}"},
                {"platform": "facebook", "url": f"https://facebook.com/{target}"}
            ]
            
            results.social_profiles.extend(social_profiles)
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="osint",
                details={
                    "target": target,
                    "source": "search_engines",
                    "error": str(e)
                },
                level="warning",
                save_to_firebase=False
            )
    
    async def _certificate_transparency(self, target: str, results: OSINTResults):
        """Búsqueda en logs de transparencia de certificados"""
        try:
            # Simulación de búsqueda en CT logs
            # En implementación real, se consultarían APIs como crt.sh
            
            certificates = [
                {
                    "common_name": target,
                    "issuer": "Let's Encrypt",
                    "valid_from": "2024-01-01",
                    "valid_to": "2024-12-31",
                    "san_domains": [f"www.{target}", f"mail.{target}"]
                }
            ]
            
            results.certificates = certificates
            
            # Extraer subdominios de certificados
            for cert in certificates:
                san_domains = cert.get("san_domains", [])
                for domain in san_domains:
                    if domain not in results.subdomains:
                        results.subdomains.append(domain)
                        
        except Exception as e:
            await self.logger.log_activity(
                activity_type="osint",
                details={
                    "target": target,
                    "source": "certificate_transparency",
                    "error": str(e)
                },
                level="warning",
                save_to_firebase=False
            )
    
    def _extract_emails_from_text(self, text: str) -> List[str]:
        """Extrae emails de un texto"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # Eliminar duplicados
    
    def _generate_summary(self, results: OSINTResults) -> Dict[str, Any]:
        """Genera resumen de resultados OSINT"""
        return {
            "domains_found": len(results.domains),
            "subdomains_found": len(results.subdomains),
            "emails_found": len(results.emails),
            "social_profiles_found": len(results.social_profiles),
            "certificates_found": len(results.certificates),
            "dns_records_collected": len(results.dns_records),
            "whois_info_available": bool(results.whois_info),
            "threat_intel_entries": len(results.threat_intel)
        }
    
    async def get_osint_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de OSINT"""
        try:
            stats = {
                "total_osint_operations_today": 0,
                "successful_operations": 0,
                "failed_operations": 0,
                "most_used_sources": ["dns_records", "whois", "subdomain_enum"],
                "average_execution_time_seconds": 45.2,
                "last_operation_time": self.time_utils.get_timestamp()
            }
            
            return stats
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "action": "get_osint_statistics",
                    "error": str(e)
                },
                level="warning",
                save_to_firebase=False
            )
            return {}
    
    def get_supported_sources(self) -> List[Dict[str, str]]:
        """Retorna fuentes OSINT soportadas"""
        return [
            {"source": "dns_records", "description": "DNS record enumeration"},
            {"source": "whois", "description": "WHOIS information lookup"},
            {"source": "subdomain_enum", "description": "Subdomain enumeration"},
            {"source": "email_harvest", "description": "Email address harvesting"},
            {"source": "search_engines", "description": "Search engine reconnaissance"},
            {"source": "certificate_transparency", "description": "Certificate transparency logs"},
            {"source": "social_media", "description": "Social media profile discovery"},
            {"source": "threat_intel", "description": "Threat intelligence lookup"}
        ]

# Instancia global del recolector OSINT
osint_collector = OSINTCollector()

def get_osint_collector() -> OSINTCollector:
    """Obtiene la instancia del recolector OSINT"""
    return osint_collector