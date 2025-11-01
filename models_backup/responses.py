# models/responses.py

"""
SUME DOCBLOCK

Nombre: Modelos de Respuestas del Sistema
Tipo: Contrato

Entradas:
- Datos de respuesta de la API

Acciones:
- Define estructuras estándar para respuestas
- Valida formato de salida de la API

Salidas:
- Respuestas JSON consistentes y validadas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class BaseResponse(BaseModel):
    """Modelo base para todas las respuestas"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo de la respuesta")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de la respuesta")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ErrorResponse(BaseResponse):
    """Modelo para respuestas de error"""
    success: bool = Field(default=False, description="Siempre False para errores")
    error_code: Optional[str] = Field(None, description="Código de error específico")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Detalles adicionales del error")
    
    @classmethod
    def create_error(cls, message: str, error_code: str = None, details: Dict[str, Any] = None):
        """Factory method para crear errores consistentes"""
        return cls(
            message=message,
            error_code=error_code,
            details=details or {}
        )

class SuccessResponse(BaseResponse):
    """Modelo para respuestas exitosas"""
    success: bool = Field(default=True, description="Siempre True para respuestas exitosas")
    data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Datos de la respuesta")

class ScanResponse(BaseResponse):
    """Respuesta específica para operaciones de escaneo"""
    scan_results: Optional[Dict[str, Any]] = Field(None, description="Resultados del escaneo")
    ai_analysis: Optional[Dict[str, Any]] = Field(None, description="Análisis de IA de los resultados")
    recommendations: Optional[List[str]] = Field(default_factory=list, description="Recomendaciones basadas en el escaneo")
    
    def add_recommendation(self, recommendation: str):
        """Agregar recomendación a la respuesta"""
        if self.recommendations is None:
            self.recommendations = []
        self.recommendations.append(recommendation)

class ExploitResponse(BaseResponse):
    """Respuesta para operaciones de exploit"""
    exploit_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Datos del exploit")
    target_info: Optional[Dict[str, str]] = Field(default_factory=dict, description="Información del objetivo")
    success_rate: Optional[float] = Field(None, ge=0.0, le=1.0, description="Tasa de éxito del exploit")
    payload_executed: Optional[bool] = Field(None, description="Si el payload fue ejecutado")
    vulnerability_exploited: Optional[str] = Field(None, description="Vulnerabilidad explotada")
    evidence: Optional[List[str]] = Field(default_factory=list, description="Evidencia del exploit")
    
    def add_evidence(self, evidence: str):
        """Agregar evidencia al exploit"""
        if self.evidence is None:
            self.evidence = []
        self.evidence.append(evidence)

class DefenseResponse(BaseResponse):
    """Respuesta para operaciones defensivas"""
    protection_status: str = Field(..., description="Estado de la protección aplicada")
    blocked_attempts: Optional[int] = Field(None, description="Intentos bloqueados")
    security_measures: Optional[List[str]] = Field(default_factory=list, description="Medidas de seguridad aplicadas")
    firewall_rules: Optional[List[str]] = Field(default_factory=list, description="Reglas de firewall aplicadas")
    monitoring_enabled: Optional[bool] = Field(None, description="Si el monitoreo está habilitado")
    
    def add_security_measure(self, measure: str):
        """Agregar medida de seguridad"""
        if self.security_measures is None:
            self.security_measures = []
        self.security_measures.append(measure)

class StatusResponse(BaseResponse):
    """Respuesta para consultas de estado del sistema"""
    system_status: str = Field(..., description="Estado del sistema")
    uptime: Optional[float] = Field(None, description="Tiempo de actividad en segundos")
    active_scans: Optional[int] = Field(None, description="Escaneos activos")
    system_resources: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Estado de recursos del sistema")
    services_status: Optional[Dict[str, str]] = Field(default_factory=dict, description="Estado de servicios")
    last_update: Optional[str] = Field(None, description="Última actualización")

class ToolExecutionResponse(BaseResponse):
    """Respuesta para ejecución de herramientas"""
    tool_name: str = Field(..., description="Nombre de la herramienta ejecutada")
    execution_time: Optional[float] = Field(None, description="Tiempo de ejecución en segundos")
    output: Optional[str] = Field(None, description="Salida de la herramienta")
    exit_code: Optional[int] = Field(None, description="Código de salida")
    command_executed: Optional[str] = Field(None, description="Comando ejecutado")
    
class AIAnalysisResponse(BaseResponse):
    """Respuesta para análisis de IA"""
    analysis_type: str = Field(..., description="Tipo de análisis realizado")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Puntuación de confianza")
    insights: Optional[List[str]] = Field(default_factory=list, description="Insights del análisis")
    raw_analysis: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Análisis completo en formato raw")
    recommendations: Optional[List[str]] = Field(default_factory=list, description="Recomendaciones de la IA")
    model_used: Optional[str] = Field(None, description="Modelo de IA utilizado")