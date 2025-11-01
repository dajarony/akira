# models/defense_models.py

"""
SUME DOCBLOCK

Nombre: Modelos Específicos de Defensa
Tipo: Contrato

Entradas:
- Peticiones específicas para operaciones defensivas

Acciones:
- Define contratos para firewall, honeypots y detección de amenazas

Salidas:
- Modelos validados para operaciones defensivas específicas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from datetime import datetime

class FirewallAction(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    DROP = "drop"
    REJECT = "reject"

class FirewallRuleRequest(BaseModel):
    """Petición para reglas de firewall"""
    rule_name: str = Field(..., description="Nombre de la regla")
    action: FirewallAction = Field(..., description="Acción a realizar")
    source_ip: Optional[str] = Field(None, description="IP de origen")
    destination_ip: Optional[str] = Field(None, description="IP de destino")
    source_port: Optional[Union[int, str]] = Field(None, description="Puerto de origen")
    destination_port: Optional[Union[int, str]] = Field(None, description="Puerto de destino")
    enabled: bool = Field(default=True, description="Si la regla está habilitada")

class FirewallResponse(BaseModel):
    """Respuesta para operaciones de firewall"""
    rule_id: str = Field(..., description="ID único de la regla")
    rule_name: str = Field(..., description="Nombre de la regla")
    status: str = Field(..., description="Estado de la operación")
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de resultado")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HoneypotType(str, Enum):
    SSH = "ssh"
    HTTP = "http"
    FTP = "ftp"
    TELNET = "telnet"

class HoneypotRequest(BaseModel):
    """Petición para operaciones de honeypot"""
    honeypot_name: str = Field(..., description="Nombre del honeypot")
    honeypot_type: HoneypotType = Field(..., description="Tipo de honeypot")
    port: int = Field(..., ge=1, le=65535, description="Puerto del honeypot")
    interface: str = Field(default="0.0.0.0", description="Interfaz de red")
    log_level: str = Field(default="info", description="Nivel de logging")

class HoneypotResponse(BaseModel):
    """Respuesta para operaciones de honeypot"""
    honeypot_id: str = Field(..., description="ID único del honeypot")
    honeypot_name: str = Field(..., description="Nombre del honeypot")
    status: str = Field(..., description="Estado del honeypot")
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de resultado")
    listening_port: Optional[int] = Field(None, description="Puerto donde está escuchando")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ThreatType(str, Enum):
    MALWARE = "malware"
    PHISHING = "phishing"
    BRUTE_FORCE = "brute_force"
    INTRUSION = "intrusion"
    ANOMALY = "anomaly"

class ThreatSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ThreatDetectionRequest(BaseModel):
    """Petición para detección de amenazas"""
    detection_name: str = Field(..., description="Nombre de la detección")
    threat_types: List[ThreatType] = Field(..., description="Tipos de amenazas a detectar")
    detection_sensitivity: str = Field(default="medium", description="Sensibilidad de detección")
    ai_enhanced: bool = Field(default=True, description="Usar detección mejorada con IA")
    auto_block: bool = Field(default=False, description="Bloqueo automático")

class ThreatDetectionResponse(BaseModel):
    """Respuesta para operaciones de detección de amenazas"""
    detection_id: str = Field(..., description="ID único de la detección")
    detection_name: str = Field(..., description="Nombre de la detección")
    status: str = Field(..., description="Estado del sistema de detección")
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de resultado")
    active_detections: Optional[int] = Field(None, description="Detecciones activas")
    threats_detected_today: Optional[int] = Field(None, description="Amenazas detectadas hoy")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
