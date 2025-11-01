# models/additional_missing_models.py

"""
SUME DOCBLOCK

Nombre: Modelos Adicionales Faltantes
Tipo: Contrato

Entradas:
- Definiciones de modelos adicionales identificados

Acciones:
- Define modelos específicos para componentes del sistema
- Proporciona estructuras de datos detalladas

Salidas:
- Modelos Pydantic validados para componentes específicos
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum


# Enums adicionales
class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ToolStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


# Modelos específicos
class ScanTarget(BaseModel):
    """Objetivo de escaneo"""

    ip: Optional[str] = Field(None, description="Dirección IP")
    hostname: Optional[str] = Field(None, description="Nombre del host")
    port_range: Optional[str] = Field(None, description="Rango de puertos")

    @validator("ip", "hostname")
    def validate_target(cls, v, values):
        if not v and not values.get("ip") and not values.get("hostname"):
            raise ValueError("Either IP or hostname must be provided")
        return v


class FirewallRule(BaseModel):
    """Regla de firewall"""

    rule_id: str = Field(..., description="ID único de la regla")
    rule_name: str = Field(..., description="Nombre de la regla")
    action: str = Field(..., description="Acción (allow/deny/drop)")
    source_ip: Optional[str] = Field(None, description="IP de origen")
    destination_ip: Optional[str] = Field(None, description="IP de destino")
    source_port: Optional[Union[int, str]] = Field(None, description="Puerto de origen")
    destination_port: Optional[Union[int, str]] = Field(
        None, description="Puerto de destino"
    )
    protocol: str = Field(default="tcp", description="Protocolo")
    enabled: bool = Field(default=True, description="Si está habilitada")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Fecha de creación"
    )
    expires_at: Optional[datetime] = Field(None, description="Fecha de expiración")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class AttackingIP(BaseModel):
    """IP atacante"""

    ip_address: str = Field(..., description="Dirección IP")
    attack_count: int = Field(default=1, description="Número de ataques")
    first_seen: datetime = Field(
        default_factory=datetime.utcnow, description="Primera vez vista"
    )
    last_seen: datetime = Field(
        default_factory=datetime.utcnow, description="Última vez vista"
    )
    threat_level: SeverityLevel = Field(
        default=SeverityLevel.MEDIUM, description="Nivel de amenaza"
    )
    attack_types: List[str] = Field(default_factory=list, description="Tipos de ataque")
    blocked: bool = Field(default=False, description="Si está bloqueada")
    country: Optional[str] = Field(None, description="País de origen")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class HoneypotInfo(BaseModel):
    """Información de honeypot"""

    honeypot_id: str = Field(..., description="ID único del honeypot")
    honeypot_name: str = Field(..., description="Nombre del honeypot")
    honeypot_type: str = Field(..., description="Tipo de honeypot")
    port: int = Field(..., ge=1, le=65535, description="Puerto")
    interface: str = Field(default="0.0.0.0", description="Interfaz")
    status: ToolStatus = Field(default=ToolStatus.ACTIVE, description="Estado")
    connections_received: int = Field(default=0, description="Conexiones recibidas")
    credentials_captured: int = Field(default=0, description="Credenciales capturadas")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Fecha de creación"
    )
    last_activity: Optional[datetime] = Field(None, description="Última actividad")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class ExploitInfo(BaseModel):
    """Información de exploit"""

    exploit_id: str = Field(..., description="ID único del exploit")
    name: str = Field(..., description="Nombre del exploit")
    description: str = Field(..., description="Descripción")
    category: str = Field(..., description="Categoría")
    risk_level: SeverityLevel = Field(..., description="Nivel de riesgo")
    cve_ids: List[str] = Field(
        default_factory=list, description="IDs de CVE relacionados"
    )
    affected_systems: List[str] = Field(
        default_factory=list, description="Sistemas afectados"
    )
    verification_method: str = Field(
        default="manual", description="Método de verificación"
    )
    remediation: str = Field(..., description="Pasos de remediación")
    references: List[str] = Field(default_factory=list, description="Referencias")
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Última actualización"
    )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class ThreatInfo(BaseModel):
    """Información de amenaza"""

    threat_id: str = Field(..., description="ID único de la amenaza")
    threat_type: str = Field(..., description="Tipo de amenaza")
    severity: SeverityLevel = Field(..., description="Severidad")
    source_ip: Optional[str] = Field(None, description="IP de origen")
    target_ip: Optional[str] = Field(None, description="IP objetivo")
    description: str = Field(..., description="Descripción de la amenaza")
    indicators: List[str] = Field(
        default_factory=list, description="Indicadores de compromiso"
    )
    mitigation_steps: List[str] = Field(
        default_factory=list, description="Pasos de mitigación"
    )
    detected_at: datetime = Field(
        default_factory=datetime.utcnow, description="Fecha de detección"
    )
    resolved: bool = Field(default=False, description="Si está resuelta")
    resolved_at: Optional[datetime] = Field(None, description="Fecha de resolución")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class SystemConfig(BaseModel):
    """Configuración del sistema"""

    config_id: str = Field(..., description="ID de configuración")
    component: str = Field(..., description="Componente del sistema")
    settings: Dict[str, Any] = Field(..., description="Configuraciones")
    environment: str = Field(default="development", description="Entorno")
    version: str = Field(default="1.0.0", description="Versión")
    last_modified: datetime = Field(
        default_factory=datetime.utcnow, description="Última modificación"
    )
    modified_by: str = Field(default="system", description="Modificado por")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


# Modelos de exploit
class ExploitCategory(str, Enum):
    WEB_APP = "web_app"
    NETWORK = "network"
    SYSTEM = "system"
    DATABASE = "database"
    WIRELESS = "wireless"
    SOCIAL_ENGINEERING = "social_engineering"


class ExploitRequest(BaseModel):
    """Petición de ejecución de exploit"""

    exploit_id: str = Field(..., description="ID del exploit a ejecutar")
    target: ScanTarget = Field(..., description="Objetivo del exploit")
    category: ExploitCategory = Field(..., description="Categoría del exploit")
    verification_only: bool = Field(
        default=True, description="Solo verificación, no explotación"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Parámetros específicos"
    )
    timeout_seconds: int = Field(
        default=300, ge=1, le=3600, description="Timeout en segundos"
    )
    save_results: bool = Field(default=True, description="Guardar resultados")
    ai_analysis: bool = Field(default=True, description="Análisis con IA")


class ExploitResults(BaseModel):
    """Resultados de ejecución de exploit"""

    exploit_id: str = Field(..., description="ID del exploit ejecutado")
    target: str = Field(..., description="Objetivo del exploit")
    category: ExploitCategory = Field(..., description="Categoría del exploit")
    success: bool = Field(..., description="Si la ejecución fue exitosa")
    vulnerability_confirmed: bool = Field(
        ..., description="Si se confirmó la vulnerabilidad"
    )
    execution_time: datetime = Field(..., description="Tiempo de ejecución")
    output: str = Field(..., description="Salida del exploit")
    risk_level: SeverityLevel = Field(..., description="Nivel de riesgo")
    remediation: Optional[str] = Field(None, description="Pasos de remediación")
    evidence: List[str] = Field(
        default_factory=list, description="Evidencia recolectada"
    )
    ai_analysis: Optional[Dict[str, Any]] = Field(None, description="Análisis con IA")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
