# models/requests.py

"""
SUME DOCBLOCK

Nombre: Modelos de Peticiones
Tipo: Contrato

Entradas:
- Definiciones de todas las peticiones del sistema

Acciones:
- Define estructuras para peticiones HTTP
- Valida datos de entrada

Salidas:
- Modelos Pydantic validados para peticiones
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

# Enums para requests
class ScanType(str, Enum):
    TCP_SYN = "tcp_syn"
    TCP_CONNECT = "tcp_connect"
    UDP = "udp"
    STEALTH = "stealth"
    AGGRESSIVE = "aggressive"
    PING_SWEEP = "ping_sweep"
    VERSION_DETECTION = "version_detection"
    OS_DETECTION = "os_detection"
    VULNERABILITY_SCAN = "vulnerability_scan"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PortRange(BaseModel):
    """Rango de puertos"""
    start: int = Field(..., ge=1, le=65535, description="Puerto inicial")
    end: int = Field(..., ge=1, le=65535, description="Puerto final")
    
    @validator('end')
    def validate_range(cls, v, values):
        if 'start' in values and v < values['start']:
            raise ValueError('End port must be greater than or equal to start port')
        return v

class ScanOptions(BaseModel):
    """Opciones de escaneo"""
    timing_template: int = Field(default=3, ge=0, le=5, description="Template de timing (0-5)")
    max_retries: int = Field(default=3, ge=0, le=10, description="Máximo número de reintentos")
    timeout_seconds: int = Field(default=30, ge=1, le=300, description="Timeout en segundos")
    parallel_processes: int = Field(default=1, ge=1, le=10, description="Procesos paralelos")
    stealth_mode: bool = Field(default=False, description="Modo sigiloso")
    fragment_packets: bool = Field(default=False, description="Fragmentar paquetes")

class ScanTarget(BaseModel):
    """Objetivo de escaneo"""
    ip: Optional[str] = Field(None, description="Dirección IP")
    hostname: Optional[str] = Field(None, description="Nombre del host")
    
    @validator('ip', 'hostname')
    def validate_target(cls, v, values):
        if not v and not values.get('ip') and not values.get('hostname'):
            raise ValueError('Either IP or hostname must be provided')
        return v

class ScanRequest(BaseModel):
    """Petición de escaneo general"""
    target: ScanTarget = Field(..., description="Objetivo del escaneo")
    scan_type: ScanType = Field(..., description="Tipo de escaneo")
    port_range: Optional[str] = Field(None, description="Rango de puertos (ej: '1-1000' o '80,443,22')")
    options: ScanOptions = Field(default_factory=ScanOptions, description="Opciones de escaneo")
    priority: Priority = Field(default=Priority.MEDIUM, description="Prioridad del escaneo")
    ai_analysis: bool = Field(default=False, description="Incluir análisis con IA")
    save_results: bool = Field(default=True, description="Guardar resultados en Firebase")
    tags: List[str] = Field(default_factory=list, description="Tags para categorización")

class NetworkScanRequest(ScanRequest):
    """Petición específica para escaneo de red"""
    network_range: str = Field(..., description="Rango de red (ej: '192.168.1.0/24')")
    discover_hosts: bool = Field(default=True, description="Descubrir hosts activos")
    port_scan_active_hosts: bool = Field(default=False, description="Escanear puertos en hosts activos")

class PortScanRequest(ScanRequest):
    """Petición específica para escaneo de puertos"""
    port_list: Optional[List[int]] = Field(None, description="Lista específica de puertos")
    service_detection: bool = Field(default=True, description="Detectar servicios")
    version_detection: bool = Field(default=False, description="Detectar versiones")

class VulnerabilityScanRequest(ScanRequest):
    """Petición específica para escaneo de vulnerabilidades"""
    vulnerability_db: str = Field(default="nmap_scripts", description="Base de datos de vulnerabilidades")
    scan_intensity: int = Field(default=3, ge=1, le=5, description="Intensidad del escaneo")
    exclude_plugins: List[str] = Field(default_factory=list, description="Plugins a excluir")

class WebAppScanRequest(ScanRequest):
    """Petición específica para escaneo de aplicaciones web"""
    url: str = Field(..., description="URL de la aplicación web")
    crawl_depth: int = Field(default=2, ge=1, le=5, description="Profundidad de crawling")
    check_forms: bool = Field(default=True, description="Verificar formularios")
    check_cookies: bool = Field(default=True, description="Verificar cookies")
    user_agent: str = Field(default="Akira-Scanner/1.0", description="User agent")

class ExploitRequest(BaseModel):
    """Petición para lanzar exploit"""
    target: ScanTarget = Field(..., description="Objetivo del exploit")
    exploit_id: str = Field(..., description="ID del exploit a usar")
    verification_only: bool = Field(default=True, description="Solo verificar vulnerabilidad")
    category: str = Field(..., description="Categoría del exploit")
    timeout_seconds: int = Field(default=60, ge=1, le=300, description="Timeout en segundos")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parámetros específicos")
    save_results: bool = Field(default=True, description="Guardar resultados")

class DefenseRequest(BaseModel):
    """Petición base para operaciones defensivas"""
    operation_type: str = Field(..., description="Tipo de operación defensiva")
    priority: Priority = Field(default=Priority.MEDIUM, description="Prioridad")
    auto_execute: bool = Field(default=False, description="Ejecutar automáticamente")
    notification_enabled: bool = Field(default=True, description="Habilitar notificaciones")

class SystemRequest(BaseModel):
    """Petición para operaciones del sistema"""
    command: str = Field(..., description="Comando del sistema")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parámetros del comando")
    async_execution: bool = Field(default=False, description="Ejecución asíncrona")

class AuthenticatedRequest(BaseModel):
    """Petición base autenticada"""
    user_id: Optional[str] = Field(None, description="ID del usuario")
    session_id: Optional[str] = Field(None, description="ID de sesión")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de la petición")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }