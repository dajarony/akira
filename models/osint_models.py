# models/osint_models.py

"""
SUME DOCBLOCK

Nombre: Modelos OSINT
Tipo: Contrato

Entradas:
- Definiciones para operaciones OSINT

Acciones:
- Define estructuras para recolección de inteligencia
- Valida fuentes y tipos de OSINT

Salidas:
- Modelos Pydantic validados para OSINT
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

# Enums para OSINT
class OSINTType(str, Enum):
    PASSIVE = "passive"
    ACTIVE = "active"
    SEMI_PASSIVE = "semi_passive"

class OSINTSources(str, Enum):
    DNS_RECORDS = "dns_records"
    WHOIS = "whois"
    SUBDOMAIN_ENUM = "subdomain_enum"
    EMAIL_HARVEST = "email_harvest"
    SOCIAL_MEDIA = "social_media"
    SEARCH_ENGINES = "search_engines"
    SHODAN = "shodan"
    CENSYS = "censys"
    THREAT_INTEL = "threat_intel"
    CERTIFICATE_TRANSPARENCY = "certificate_transparency"

class ReconDepth(int, Enum):
    SURFACE = 1
    MODERATE = 2
    DEEP = 3

# Modelos de peticiones OSINT
class OSINTRequest(BaseModel):
    """Petición base para operaciones OSINT"""
    target_domain: Optional[str] = Field(None, description="Dominio objetivo")
    target_email: Optional[str] = Field(None, description="Email objetivo")
    target_username: Optional[str] = Field(None, description="Usuario objetivo")
    company_name: Optional[str] = Field(None, description="Nombre de empresa")
    sources: List[OSINTSources] = Field(..., description="Fuentes OSINT a utilizar")
    osint_type: OSINTType = Field(default=OSINTType.PASSIVE, description="Tipo de OSINT")
    depth_level: ReconDepth = Field(default=ReconDepth.MODERATE, description="Nivel de profundidad")
    ai_analysis: bool = Field(default=False, description="Incluir análisis con IA")
    save_results: bool = Field(default=True, description="Guardar resultados")
    timeout_minutes: int = Field(default=30, ge=1, le=120, description="Timeout en minutos")
    
    @validator('target_domain', 'target_email', 'target_username', 'company_name')
    def validate_at_least_one_target(cls, v, values):
        targets = [v, values.get('target_domain'), values.get('target_email'), 
                  values.get('target_username'), values.get('company_name')]
        if not any(targets):
            raise ValueError('At least one target must be provided')
        return v

class SubdomainEnumRequest(BaseModel):
    """Petición para enumeración de subdominios"""
    domain: str = Field(..., description="Dominio principal")
    wordlist: Optional[str] = Field(None, description="Lista de palabras personalizada")
    recursive: bool = Field(default=False, description="Búsqueda recursiva")
    max_depth: int = Field(default=2, ge=1, le=5, description="Profundidad máxima")

class EmailHarvestRequest(BaseModel):
    """Petición para recolección de emails"""
    domain: str = Field(..., description="Dominio objetivo")
    search_engines: List[str] = Field(default_factory=lambda: ["google", "bing"], description="Motores de búsqueda")
    social_networks: bool = Field(default=False, description="Buscar en redes sociales")
    limit: int = Field(default=100, ge=1, le=1000, description="Límite de resultados")

class ShodanSearchRequest(BaseModel):
    """Petición para búsqueda en Shodan"""
    query: str = Field(..., description="Query de búsqueda")
    facets: List[str] = Field(default_factory=list, description="Facetas a incluir")
    limit: int = Field(default=100, ge=1, le=1000, description="Límite de resultados")

class ThreatIntelRequest(BaseModel):
    """Petición para inteligencia de amenazas"""
    indicators: List[str] = Field(..., description="Indicadores a investigar")
    sources: List[str] = Field(default_factory=lambda: ["virustotal", "otx"], description="Fuentes de threat intel")
    include_context: bool = Field(default=True, description="Incluir contexto")

class ReconnaissanceRequest(BaseModel):
    """Petición para reconocimiento general"""
    target: str = Field(..., description="Objetivo del reconocimiento")
    techniques: List[str] = Field(..., description="Técnicas de reconocimiento")
    passive_only: bool = Field(default=True, description="Solo técnicas pasivas")

class FootprintingRequest(BaseModel):
    """Petición para footprinting"""
    organization: str = Field(..., description="Organización objetivo")
    include_employees: bool = Field(default=False, description="Incluir empleados")
    include_infrastructure: bool = Field(default=True, description="Incluir infraestructura")

class EnumerationRequest(BaseModel):
    """Petición para enumeración"""
    target: str = Field(..., description="Objetivo de enumeración")
    services: List[str] = Field(default_factory=list, description="Servicios específicos")
    aggressive: bool = Field(default=False, description="Enumeración agresiva")

# Modelos de resultados OSINT
class OSINTResult(BaseModel):
    """Resultado individual de OSINT"""
    source: OSINTSources = Field(..., description="Fuente del resultado")
    data_type: str = Field(..., description="Tipo de dato")
    value: str = Field(..., description="Valor encontrado")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadatos adicionales")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class OSINTResults(BaseModel):
    """Resultados completos de OSINT"""
    target: str = Field(..., description="Objetivo investigado")
    osint_type: OSINTType = Field(..., description="Tipo de OSINT realizado")
    sources_used: List[OSINTSources] = Field(..., description="Fuentes utilizadas")
    domains: List[str] = Field(default_factory=list, description="Dominios encontrados")
    subdomains: List[str] = Field(default_factory=list, description="Subdominios encontrados")
    emails: List[str] = Field(default_factory=list, description="Emails encontrados")
    social_profiles: List[Dict[str, str]] = Field(default_factory=list, description="Perfiles sociales")
    technologies: List[str] = Field(default_factory=list, description="Tecnologías detectadas")
    certificates: List[Dict[str, Any]] = Field(default_factory=list, description="Certificados encontrados")
    dns_records: Dict[str, List[str]] = Field(default_factory=dict, description="Registros DNS")
    whois_info: Dict[str, Any] = Field(default_factory=dict, description="Información WHOIS")
    threat_intel: List[Dict[str, Any]] = Field(default_factory=list, description="Inteligencia de amenazas")
    summary: Dict[str, Any] = Field(default_factory=dict, description="Resumen de resultados")
    execution_time_seconds: float = Field(..., description="Tiempo de ejecución")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }