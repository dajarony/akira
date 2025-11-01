# models/additional_models.py

"""
SUME DOCBLOCK

Nombre: Modelos Adicionales para Operaciones Comunes
Tipo: Contrato

Entradas:
- Peticiones para operaciones frecuentes del sistema

Acciones:
- Define contratos para operaciones adicionales
- Valida peticiones de reconocimiento y análisis

Salidas:
- Modelos validados para operaciones diversas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from enum import Enum

# Alias común para ReconRequest
class ReconRequest(BaseModel):
    """Alias para peticiones de reconocimiento (apunta a OSINTRequest)"""
    target: str = Field(..., description="Objetivo del reconocimiento")
    recon_type: str = Field(default="passive", description="Tipo de reconocimiento")
    depth: str = Field(default="basic", description="Profundidad del reconocimiento")
    passive_only: bool = Field(default=True, description="Solo reconocimiento pasivo")
    
    # Opciones comunes
    include_subdomains: bool = Field(default=True, description="Incluir subdominios")
    extract_emails: bool = Field(default=True, description="Extraer emails")
    technology_detection: bool = Field(default=True, description="Detectar tecnologías")
    
    # Metadatos
    description: Optional[str] = Field(None, description="Descripción del reconocimiento")
    tags: List[str] = Field(default_factory=list, description="Tags")

# Modelos para respuestas comunes
class ReconResponse(BaseModel):
    """Respuesta para operaciones de reconocimiento"""
    target: str = Field(..., description="Objetivo analizado")
    recon_type: str = Field(..., description="Tipo de reconocimiento realizado")
    results: Dict[str, Any] = Field(default_factory=dict, description="Resultados del reconocimiento")
    execution_time: Optional[float] = Field(None, description="Tiempo de ejecución")
    
class AnalysisRequest(BaseModel):
    """Petición para análisis general"""
    target: str = Field(..., description="Objetivo del análisis")
    analysis_type: str = Field(..., description="Tipo de análisis")
    depth: str = Field(default="standard", description="Profundidad del análisis")
    include_recommendations: bool = Field(default=True, description="Incluir recomendaciones")

class AnalysisResponse(BaseModel):
    """Respuesta para análisis general"""
    target: str = Field(..., description="Objetivo analizado")
    analysis_type: str = Field(..., description="Tipo de análisis")
    findings: List[Dict[str, Any]] = Field(default_factory=list, description="Hallazgos")
    recommendations: List[str] = Field(default_factory=list, description="Recomendaciones")
    severity_summary: Dict[str, int] = Field(default_factory=dict, description="Resumen por severidad")

# Modelos para operaciones de datos
class DataExtractionRequest(BaseModel):
    """Petición para extracción de datos"""
    source: str = Field(..., description="Fuente de datos")
    extraction_type: str = Field(..., description="Tipo de extracción")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Filtros a aplicar")
    output_format: str = Field(default="json", description="Formato de salida")

class DataExtractionResponse(BaseModel):
    """Respuesta para extracción de datos"""
    source: str = Field(..., description="Fuente de datos")
    extraction_type: str = Field(..., description="Tipo de extracción")
    data: List[Dict[str, Any]] = Field(default_factory=list, description="Datos extraídos")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadatos")
    
# Modelos para búsquedas
class SearchRequest(BaseModel):
    """Petición para búsquedas"""
    query: str = Field(..., description="Query de búsqueda")
    search_type: str = Field(default="general", description="Tipo de búsqueda")
    sources: List[str] = Field(default_factory=list, description="Fuentes a buscar")
    max_results: int = Field(default=50, ge=1, le=1000, description="Máximo resultados")
    
class SearchResponse(BaseModel):
    """Respuesta para búsquedas"""
    query: str = Field(..., description="Query ejecutada")
    search_type: str = Field(..., description="Tipo de búsqueda")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="Resultados")
    total_found: int = Field(default=0, description="Total encontrado")
    execution_time: Optional[float] = Field(None, description="Tiempo de ejecución")

# Modelos para reportes
class ReportRequest(BaseModel):
    """Petición para generación de reportes"""
    report_type: str = Field(..., description="Tipo de reporte")
    target: Optional[str] = Field(None, description="Objetivo del reporte")
    data_sources: List[str] = Field(default_factory=list, description="Fuentes de datos")
    format: str = Field(default="pdf", description="Formato del reporte")
    include_charts: bool = Field(default=True, description="Incluir gráficos")
    
class ReportResponse(BaseModel):
    """Respuesta para reportes generados"""
    report_id: str = Field(..., description="ID del reporte")
    report_type: str = Field(..., description="Tipo de reporte")
    file_path: Optional[str] = Field(None, description="Ruta del archivo generado")
    download_url: Optional[str] = Field(None, description="URL de descarga")
    status: str = Field(..., description="Estado del reporte")

# Modelos para configuración
class ConfigRequest(BaseModel):
    """Petición para configuración"""
    config_type: str = Field(..., description="Tipo de configuración")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Configuraciones")
    apply_immediately: bool = Field(default=False, description="Aplicar inmediatamente")
    
class ConfigResponse(BaseModel):
    """Respuesta para configuración"""
    config_type: str = Field(..., description="Tipo de configuración")
    status: str = Field(..., description="Estado de la configuración")
    applied_settings: Dict[str, Any] = Field(default_factory=dict, description="Configuraciones aplicadas")
    
# Modelos para monitoreo
class MonitoringRequest(BaseModel):
    """Petición para monitoreo"""
    target: str = Field(..., description="Objetivo a monitorear")
    monitoring_type: str = Field(..., description="Tipo de monitoreo")
    interval: int = Field(default=300, ge=60, le=86400, description="Intervalo en segundos")
    alerts_enabled: bool = Field(default=True, description="Alertas habilitadas")
    
class MonitoringResponse(BaseModel):
    """Respuesta para operaciones de monitoreo"""
    monitoring_id: str = Field(..., description="ID del monitoreo")
    target: str = Field(..., description="Objetivo monitoreado")
    status: str = Field(..., description="Estado del monitoreo")
    last_check: Optional[str] = Field(None, description="Última verificación")
    next_check: Optional[str] = Field(None, description="Próxima verificación")