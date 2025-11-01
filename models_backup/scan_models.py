# models/scan_models.py

"""
SUME DOCBLOCK

Nombre: Modelos de Escaneo (Versión Mínima Funcional)
Tipo: Contrato

Entradas:
- Datos de escaneos y resultados

Acciones:
- Define estructuras para resultados de escaneo
- Sin caracteres especiales o BOM

Salidas:
- Modelos validados para respuestas de escaneo
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ScanStatus(str, Enum):
    """Estados posibles del escaneo"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class VulnerabilitySeverity(str, Enum):
    """Niveles de severidad de vulnerabilidades"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class PortInfo(BaseModel):
    """Información de puerto detectado"""
    port: int = Field(..., ge=1, le=65535, description="Número de puerto")
    protocol: str = Field(..., description="Protocolo (TCP/UDP)")
    state: str = Field(..., description="Estado del puerto")
    service: Optional[str] = Field(None, description="Servicio detectado")

class Vulnerability(BaseModel):
    """Información de vulnerabilidad detectada"""
    id: str = Field(..., description="ID único de la vulnerabilidad")
    name: str = Field(..., description="Nombre de la vulnerabilidad")
    severity: VulnerabilitySeverity = Field(..., description="Nivel de severidad")
    description: str = Field(..., description="Descripción de la vulnerabilidad")

class HostInfo(BaseModel):
    """Información del host escaneado"""
    ip: str = Field(..., description="Dirección IP")
    hostname: Optional[str] = Field(None, description="Nombre del host")
    status: str = Field(..., description="Estado del host (up/down)")

class ScanResults(BaseModel):
    """Resultados completos del escaneo"""
    scan_id: str = Field(..., description="ID único del escaneo")
    target: str = Field(..., description="Objetivo del escaneo")
    scan_type: str = Field(..., description="Tipo de escaneo realizado")
    status: ScanStatus = Field(..., description="Estado actual del escaneo")
    started_at: datetime = Field(..., description="Timestamp de inicio")
    completed_at: Optional[datetime] = Field(None, description="Timestamp de finalización")
    hosts_discovered: List[HostInfo] = Field(default_factory=list, description="Hosts descubiertos")
    ports_found: List[PortInfo] = Field(default_factory=list, description="Puertos encontrados")
    vulnerabilities: List[Vulnerability] = Field(default_factory=list, description="Vulnerabilidades detectadas")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class NetworkScanResults(ScanResults):
    """Resultados específicos para escaneo de red"""
    network_range: str = Field(..., description="Rango de red escaneado")
    alive_hosts: int = Field(default=0, description="Hosts activos encontrados")

class VulnerabilityScanResults(ScanResults):
    """Resultados específicos para escaneo de vulnerabilidades"""
    scan_plugins: List[str] = Field(default_factory=list, description="Plugins utilizados")
    false_positives: List[str] = Field(default_factory=list, description="Posibles falsos positivos")

class WebAppScanResults(ScanResults):
    """Resultados específicos para escaneo de aplicaciones web"""
    url: str = Field(..., description="URL de la aplicación web")
    technologies: List[str] = Field(default_factory=list, description="Tecnologías detectadas")
    forms_found: int = Field(default=0, description="Formularios encontrados")
    cookies: Dict[str, str] = Field(default_factory=dict, description="Cookies detectadas")
