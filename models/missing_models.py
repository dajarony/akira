# models/missing_models.py

"""
SUME DOCBLOCK

Nombre: Modelos Faltantes Identificados
Tipo: Contrato

Entradas:
- Definiciones de modelos que faltan en el sistema

Acciones:
- Define todos los modelos faltantes identificados en el análisis
- Proporciona estructuras de datos completas

Salidas:
- Modelos Pydantic validados para completar el sistema
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

# Enums necesarios
class ExploitCategory(str, Enum):
    WEB_APP = "web_app"
    NETWORK = "network"
    SYSTEM = "system"
    DATABASE = "database"
    WIRELESS = "wireless"
    SOCIAL_ENGINEERING = "social_engineering"

class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

# Modelos de respuesta OSINT
class OSINTResponse(BaseModel):
    """Respuesta para operaciones OSINT"""
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de resultado")
    execution_time_ms: float = Field(..., description="Tiempo de ejecución en ms")
    osint_results: Optional[Dict[str, Any]] = Field(None, description="Resultados OSINT")
    ai_analysis: Optional[Dict[str, Any]] = Field(None, description="Análisis con IA")
    saved_to_firebase: bool = Field(default=False, description="Si se guardó en Firebase")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Modelos de exploit
class ExploitResults(BaseModel):
    """Resultados de ejecución de exploit"""
    exploit_id: str = Field(..., description="ID del exploit ejecutado")
    target: str = Field(..., description="Objetivo del exploit")
    vulnerability_confirmed: bool = Field(..., description="Si se confirmó la vulnerabilidad")
    exploit_successful: bool = Field(..., description="Si el exploit fue exitoso")
    evidence: List[str] = Field(default_factory=list, description="Evidencia recolectada")
    risk_level: SeverityLevel = Field(..., description="Nivel de riesgo")
    remediation_steps: List[str] = Field(default_factory=list, description="Pasos de remediación")
    execution_time_seconds: float = Field(..., description="Tiempo de ejecución")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Modelos de defensa
class AttackingIP(BaseModel):
    """Información de IP atacante"""
    ip_address: str = Field(..., description="Dirección IP")
    attack_count: int = Field(..., description="Número de ataques")
    last_seen: datetime = Field(..., description="Última vez vista")
    threat_level: SeverityLevel = Field(..., description="Nivel de amenaza")
    blocked: bool = Field(default=False, description="Si está bloqueada")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class DefenseStats(BaseModel):
    """Estadísticas de defensa"""
    active_firewall_rules: int = Field(default=0, description="Reglas de firewall activas")
    active_honeypots: int = Field(default=0, description="Honeypots activos")
    threats_blocked_today: int = Field(default=0, description="Amenazas bloqueadas hoy")
    alerts_generated_today: int = Field(default=0, description="Alertas generadas hoy")
    top_threat_types: List[str] = Field(default_factory=list, description="Tipos de amenaza principales")
    top_attacking_ips: List[AttackingIP] = Field(default_factory=list, description="IPs atacantes principales")
    blocked_ips_count: int = Field(default=0, description="Número de IPs bloqueadas")
    defense_effectiveness_score: int = Field(default=50, description="Puntuación de efectividad")
    security_posture: str = Field(default="fair", description="Postura de seguridad")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Última actualización")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class DefenseStatusResponse(BaseModel):
    """Respuesta de estado de defensa"""
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de resultado")
    defense_stats: DefenseStats = Field(..., description="Estadísticas de defensa")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Modelos de sistema
class SystemMetrics(BaseModel):
    """Métricas del sistema"""
    cpu_usage_percent: float = Field(..., description="Uso de CPU en porcentaje")
    memory_usage_percent: float = Field(..., description="Uso de memoria en porcentaje")
    disk_usage_percent: float = Field(..., description="Uso de disco en porcentaje")
    network_connections: int = Field(default=0, description="Conexiones de red activas")
    uptime_seconds: int = Field(default=0, description="Tiempo de actividad en segundos")
    load_average: List[float] = Field(default_factory=list, description="Promedio de carga")

class HealthStatus(BaseModel):
    """Estado de salud del sistema"""
    overall_status: ServiceStatus = Field(..., description="Estado general")
    services: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Estado de servicios")
    system_metrics: Optional[SystemMetrics] = Field(None, description="Métricas del sistema")
    last_check: datetime = Field(default_factory=datetime.utcnow, description="Última verificación")
    issues: List[str] = Field(default_factory=list, description="Problemas detectados")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Modelos de análisis
class AnalysisRequest(BaseModel):
    """Petición de análisis"""
    analysis_type: str = Field(..., description="Tipo de análisis")
    target_data: Dict[str, Any] = Field(..., description="Datos a analizar")
    ai_enhanced: bool = Field(default=True, description="Usar IA para análisis")
    depth_level: int = Field(default=1, ge=1, le=3, description="Nivel de profundidad")

class AnalysisResponse(BaseModel):
    """Respuesta de análisis"""
    success: bool = Field(..., description="Si el análisis fue exitoso")
    analysis_id: str = Field(..., description="ID único del análisis")
    results: Dict[str, Any] = Field(..., description="Resultados del análisis")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Puntuación de confianza")
    recommendations: List[str] = Field(default_factory=list, description="Recomendaciones")
    execution_time_ms: float = Field(..., description="Tiempo de ejecución")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Modelos de reconocimiento
class ReconRequest(BaseModel):
    """Petición de reconocimiento"""
    target: str = Field(..., description="Objetivo del reconocimiento")
    recon_type: str = Field(..., description="Tipo de reconocimiento")
    passive_only: bool = Field(default=True, description="Solo reconocimiento pasivo")
    sources: List[str] = Field(default_factory=list, description="Fuentes a utilizar")

class ReconResponse(BaseModel):
    """Respuesta de reconocimiento"""
    success: bool = Field(..., description="Si el reconocimiento fue exitoso")
    recon_id: str = Field(..., description="ID único del reconocimiento")
    target: str = Field(..., description="Objetivo del reconocimiento")
    results: Dict[str, Any] = Field(..., description="Resultados del reconocimiento")
    sources_used: List[str] = Field(default_factory=list, description="Fuentes utilizadas")
    execution_time_ms: float = Field(..., description="Tiempo de ejecución")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }