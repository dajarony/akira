# models/scan_models.py - VERSIÓN MÍNIMA CORREGIDA

"""
SUME DOCBLOCK

Nombre: Modelos de Escaneo (Versión Mínima)
Tipo: Contrato

Entradas:
- Datos de escaneos básicos

Acciones:
- Define estructuras mínimas para escaneos

Salidas:
- Modelos validados básicos
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ScanStatus(str, Enum):
    """Estados del escaneo"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class VulnerabilitySeverity(str, Enum):
    """Severidades de vulnerabilidades"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class PortInfo(BaseModel):
    """Información básica de puerto"""
    port: int = Field(..., description="Número de puerto")
    protocol: str = Field(..., description="Protocolo")
    state: str = Field(..., description="Estado")

class Vulnerability(BaseModel):
    """Información básica de vulnerabilidad"""
    id: str = Field(..., description="ID de vulnerabilidad")
    severity: VulnerabilitySeverity = Field(..., description="Severidad")
    description: str = Field(..., description="Descripción")

class HostInfo(BaseModel):
    """Información básica de host"""
    ip: str = Field(..., description="IP del host")
    status: str = Field(..., description="Estado")

class ScanResults(BaseModel):
    """Resultados básicos de escaneo"""
    scan_id: str = Field(..., description="ID del escaneo")
    target: str = Field(..., description="Objetivo")
    status: ScanStatus = Field(..., description="Estado")
    started_at: datetime = Field(..., description="Inicio")
    hosts_discovered: List[HostInfo] = Field(default_factory=list, description="Hosts")
    ports_found: List[PortInfo] = Field(default_factory=list, description="Puertos")
    vulnerabilities: List[Vulnerability] = Field(default_factory=list, description="Vulnerabilidades")

class NetworkScanResults(ScanResults):
    """Resultados específicos para escaneo de red"""
    network_range: str = Field(..., description="Rango de red")
    alive_hosts: int = Field(default=0, description="Hosts activos")

class VulnerabilityScanResults(ScanResults):
    """Resultados específicos para vulnerabilidades"""
    scan_plugins: List[str] = Field(default_factory=list, description="Plugins")

class WebAppScanResults(ScanResults):
    """Resultados específicos para web apps"""
    url: str = Field(..., description="URL")
    technologies: List[str] = Field(default_factory=list, description="Tecnologías")
