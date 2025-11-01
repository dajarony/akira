# models/responses.py

"""
SUME DOCBLOCK

Nombre: Modelos de Respuestas
Tipo: Contrato

Entradas:
- Definiciones de todas las respuestas del sistema

Acciones:
- Define estructuras para respuestas HTTP
- Estandariza formato de respuestas

Salidas:
- Modelos Pydantic validados para respuestas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

# Respuestas base
class BaseResponse(BaseModel):
    """Respuesta base para todas las operaciones"""
    success: bool = Field(..., description="Si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de resultado")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")
    execution_time_ms: Optional[float] = Field(None, description="Tiempo de ejecución en ms")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ErrorResponse(BaseResponse):
    """Respuesta para errores"""
    error_code: str = Field(..., description="Código de error")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Detalles del error")
    stack_trace: Optional[str] = Field(None, description="Stack trace (solo en desarrollo)")

class SuccessResponse(BaseResponse):
    """Respuesta para operaciones exitosas"""
    data: Optional[Dict[str, Any]] = Field(None, description="Datos de respuesta")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadatos adicionales")

class ScanResponse(BaseResponse):
    """Respuesta para operaciones de escaneo"""
    scan_id: Optional[str] = Field(None, description="ID único del escaneo")
    scan_results: Optional[Dict[str, Any]] = Field(None, description="Resultados del escaneo")
    ai_analysis: Optional[Dict[str, Any]] = Field(None, description="Análisis con IA")
    saved_to_firebase: bool = Field(default=False, description="Si se guardó en Firebase")
    recommendations: List[str] = Field(default_factory=list, description="Recomendaciones")

class ExploitResponse(BaseResponse):
    """Respuesta para operaciones de exploit"""
    exploit_id: Optional[str] = Field(None, description="ID del exploit")
    exploit_results: Optional[Dict[str, Any]] = Field(None, description="Resultados del exploit")
    vulnerability_confirmed: bool = Field(default=False, description="Si se confirmó vulnerabilidad")
    security_recommendations: List[str] = Field(default_factory=list, description="Recomendaciones de seguridad")
    saved_to_firebase: bool = Field(default=False, description="Si se guardó en Firebase")

class DefenseResponse(BaseResponse):
    """Respuesta para operaciones defensivas"""
    operation_id: Optional[str] = Field(None, description="ID de la operación")
    defense_status: Optional[Dict[str, Any]] = Field(None, description="Estado de defensa")
    actions_taken: List[str] = Field(default_factory=list, description="Acciones tomadas")
    effectiveness_score: Optional[int] = Field(None, description="Puntuación de efectividad")

class StatusResponse(BaseResponse):
    """Respuesta para consultas de estado"""
    system_status: Optional[Dict[str, Any]] = Field(None, description="Estado del sistema")
    service_health: Optional[Dict[str, Any]] = Field(None, description="Salud de servicios")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Métricas del sistema")

class ToolExecutionResponse(BaseResponse):
    """Respuesta para ejecución de herramientas"""
    tool_name: str = Field(..., description="Nombre de la herramienta")
    tool_version: Optional[str] = Field(None, description="Versión de la herramienta")
    output: Optional[str] = Field(None, description="Salida de la herramienta")
    exit_code: Optional[int] = Field(None, description="Código de salida")
    warnings: List[str] = Field(default_factory=list, description="Advertencias")

class AIAnalysisResponse(BaseResponse):
    """Respuesta para análisis con IA"""
    analysis_id: str = Field(..., description="ID único del análisis")
    model_used: str = Field(..., description="Modelo de IA utilizado")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Puntuación de confianza")
    analysis_text: str = Field(..., description="Texto del análisis")
    recommendations: List[str] = Field(default_factory=list, description="Recomendaciones")
    risk_assessment: Optional[str] = Field(None, description="Evaluación de riesgo")
    tokens_used: Optional[int] = Field(None, description="Tokens utilizados")
    cost_estimate: Optional[float] = Field(None, description="Estimación de costo")