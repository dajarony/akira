# models/requests.py

"""
SUME DOCBLOCK

Nombre: Modelos de Peticiones (Versión Mínima Funcional)
Tipo: Entrada

Entradas:
- Datos de peticiones HTTP

Acciones:
- Define modelos básicos de request
- Incluye PortRange y otros modelos críticos

Salidas:
- Modelos validados de entrada
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from enum import Enum
import ipaddress
import re

class ScanType(str, Enum):
    """Tipos de escaneo"""
    NETWORK = "network"
    PORT = "port"
    VULNERABILITY = "vulnerability"
    WEB_APP = "web_app"
    SERVICE = "service"
    FULL = "full"

class Priority(str, Enum):
    """Niveles de prioridad"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PortRange(BaseModel):
    """Rango de puertos para escaneo"""
    start: int = Field(..., ge=1, le=65535, description="Puerto inicial")
    end: int = Field(..., ge=1, le=65535, description="Puerto final")
    
    @validator('end')
    def end_must_be_greater_than_start(cls, v, values):
        if 'start' in values and v < values['start']:
            raise ValueError('El puerto final debe ser mayor que el inicial')
        return v

class ScanOptions(BaseModel):
    """Opciones de configuración para escaneos"""
    timeout: Optional[int] = Field(default=30, ge=1, le=300, description="Timeout en segundos")
    max_threads: Optional[int] = Field(default=10, ge=1, le=100, description="Máximo número de threads")
    stealth_mode: Optional[bool] = Field(default=False, description="Modo sigiloso")
    save_raw_output: Optional[bool] = Field(default=True, description="Guardar salida raw")

class ScanRequest(BaseModel):
    """Petición base para operaciones de escaneo"""
    target: str = Field(..., min_length=1, description="Objetivo del escaneo")
    scan_type: ScanType = Field(..., description="Tipo de escaneo a realizar")
    priority: Priority = Field(default=Priority.MEDIUM, description="Prioridad del escaneo")
    ports: Optional[Union[List[int], PortRange, str]] = Field(None, description="Puertos a escanear")
    options: Optional[ScanOptions] = Field(default_factory=ScanOptions, description="Opciones del escaneo")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del escaneo")

class NetworkScanRequest(ScanRequest):
    """Petición específica para escaneo de red"""
    scan_type: ScanType = Field(default=ScanType.NETWORK, description="Tipo fijo para escaneo de red")
    network_range: Optional[str] = Field(None, description="Rango de red CIDR")
    discover_hosts: bool = Field(default=True, description="Descubrir hosts activos")

class PortScanRequest(ScanRequest):
    """Petición específica para escaneo de puertos"""
    scan_type: ScanType = Field(default=ScanType.PORT, description="Tipo fijo para escaneo de puertos")
    scan_technique: Optional[str] = Field(default="TCP_SYN", description="Técnica de escaneo")
    service_detection: bool = Field(default=True, description="Detectar servicios")

class VulnerabilityScanRequest(ScanRequest):
    """Petición específica para escaneo de vulnerabilidades"""
    scan_type: ScanType = Field(default=ScanType.VULNERABILITY, description="Tipo fijo para vulnerabilidades")
    vuln_categories: Optional[List[str]] = Field(default_factory=list, description="Categorías de vulnerabilidades")
    safe_checks_only: bool = Field(default=True, description="Solo verificaciones seguras")

class WebAppScanRequest(ScanRequest):
    """Petición específica para escaneo de aplicaciones web"""
    scan_type: ScanType = Field(default=ScanType.WEB_APP, description="Tipo fijo para escaneo web")
    scan_depth: int = Field(default=2, ge=1, le=5, description="Profundidad del escaneo")
    include_forms: bool = Field(default=True, description="Incluir análisis de formularios")

class ExploitRequest(BaseModel):
    """Petición para operaciones de exploit"""
    target: str = Field(..., description="Objetivo del exploit")
    exploit_type: str = Field(..., description="Tipo de exploit")
    payload: Optional[str] = Field(None, description="Payload personalizado")
    verify_only: bool = Field(default=True, description="Solo verificar, no ejecutar")
    
class DefenseRequest(BaseModel):
    """Petición para operaciones defensivas"""
    action: str = Field(..., description="Acción defensiva a realizar")
    target: Optional[str] = Field(None, description="Objetivo a proteger")
    rules: Optional[List[str]] = Field(default_factory=list, description="Reglas a aplicar")
    priority: Priority = Field(default=Priority.MEDIUM, description="Prioridad de la acción")

class SystemRequest(BaseModel):
    """Petición para operaciones del sistema"""
    action: str = Field(..., description="Acción del sistema")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Parámetros adicionales")

class AuthenticatedRequest(BaseModel):
    """Base para requests que requieren autenticación"""
    api_key: Optional[str] = Field(None, description="Clave API")
    token: Optional[str] = Field(None, description="Token de autenticación")
