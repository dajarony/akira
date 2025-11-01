# models/__init__.py

"""
SUME DOCBLOCK

Nombre: Módulo de Modelos Centralizados
Tipo: Contrato

Entradas:
- Importaciones de todos los modelos del sistema

Acciones:
- Centraliza todas las definiciones de modelos
- Exporta interfaces consistentes

Salidas:
- Modelos Pydantic validados y listos para uso
"""

# Importar modelos base y respuestas
from .responses import (
    BaseResponse, 
    ErrorResponse, 
    SuccessResponse,
    ScanResponse,
    ExploitResponse,
    DefenseResponse,
    StatusResponse,
    ToolExecutionResponse,
    AIAnalysisResponse
)

# Importar modelos de escaneo
from .scan_models import (
    ScanResults,
    ScanStatus,
    VulnerabilitySeverity,
    PortInfo,
    Vulnerability,
    HostInfo,
    NetworkScanResults,
    VulnerabilityScanResults,
    WebAppScanResults
)

# Importar modelos de requests
from .requests import (
    ScanRequest,
    ScanType,
    Priority,
    PortRange,
    ScanOptions,
    NetworkScanRequest,
    PortScanRequest,
    VulnerabilityScanRequest,
    WebAppScanRequest,
    ExploitRequest,
    DefenseRequest,
    SystemRequest,
    AuthenticatedRequest
)

# Importar modelos OSINT
from .osint_models import (
    OSINTRequest,
    OSINTType,
    OSINTSources,
    ReconDepth,
    SubdomainEnumRequest,
    EmailHarvestRequest,
    ShodanSearchRequest,
    ThreatIntelRequest,
    ReconnaissanceRequest,
    FootprintingRequest,
    EnumerationRequest,
    OSINTResult,
    OSINTResults
)

# Importar modelos adicionales
from .additional_models import (
    ReconRequest,
    ReconResponse,
    AnalysisRequest,
    AnalysisResponse,
    DataExtractionRequest,
    DataExtractionResponse,
    SearchRequest,
    SearchResponse,
    ReportRequest,
    ReportResponse,
    ConfigRequest,
    ConfigResponse,
    MonitoringRequest,
    MonitoringResponse
)

# Importar modelos faltantes identificados
from .missing_models import (
    OSINTResponse,
    OSINTResults,
    ExploitResults,
    ExploitCategory,
    DefenseStatusResponse,
    DefenseStats,
    HealthStatus,
    SystemMetrics,
    ServiceStatus
)

__all__ = [
    # Respuestas base
    "BaseResponse",
    "ErrorResponse", 
    "SuccessResponse",
    "ScanResponse",
    "ExploitResponse", 
    "DefenseResponse",
    "StatusResponse",
    "ToolExecutionResponse",
    "AIAnalysisResponse",
    
    # Modelos de escaneo (responses)
    "ScanResults",
    "ScanStatus",
    "VulnerabilitySeverity",
    "PortInfo",
    "Vulnerability",
    "HostInfo",
    "NetworkScanResults",
    "VulnerabilityScanResults",
    "WebAppScanResults",
    
    # Modelos de peticiones (requests)
    "ScanRequest",
    "ScanType",
    "Priority", 
    "PortRange",
    "ScanOptions",
    "NetworkScanRequest",
    "PortScanRequest",
    "VulnerabilityScanRequest",
    "WebAppScanRequest",
    "ExploitRequest",
    "DefenseRequest",
    "SystemRequest",
    "AuthenticatedRequest",
    
    # Modelos OSINT
    "OSINTRequest",
    "OSINTType",
    "OSINTSources", 
    "ReconDepth",
    "SubdomainEnumRequest",
    "EmailHarvestRequest",
    "ShodanSearchRequest",
    "ThreatIntelRequest",
    "ReconnaissanceRequest",
    "FootprintingRequest",
    "EnumerationRequest",
    "OSINTResult",
    "OSINTResults",
    
    # Modelos adicionales
    "ReconRequest",
    "ReconResponse",
    "AnalysisRequest",
    "AnalysisResponse",
    "DataExtractionRequest",
    "DataExtractionResponse",
    "SearchRequest",
    "SearchResponse",
    "ReportRequest",
    "ReportResponse",
    "ConfigRequest",
    "ConfigResponse",
    "MonitoringRequest",
    "MonitoringResponse",
    
    # Modelos faltantes identificados
    "OSINTResponse",
    "OSINTResults",
    "ExploitResults",
    "ExploitCategory",
    "DefenseStatusResponse",
    "DefenseStats",
    "HealthStatus",
    "SystemMetrics",
    "ServiceStatus",
]