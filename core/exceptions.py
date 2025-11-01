"""
SUME DOCBLOCK

Nombre: Sistema de Excepciones Akira
Tipo: Lógica

Entradas:
- Errores de servicios externos (OpenAI, Firebase, nmap)
- Errores de validación y lógica de negocio
- Excepciones del sistema

Acciones:
- Define excepciones personalizadas
- Maneja errores con contexto específico
- Formatea respuestas de error para API

Salidas:
- Excepciones tipadas y descriptivas
- Respuestas HTTP estructuradas
- Logging automático de errores
"""

from typing import Optional, Dict, Any
from fastapi import HTTPException
from core.logger import get_logger

logger = get_logger()

class AkiraBaseException(Exception):
    """Excepción base para todas las excepciones de Akira"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class AkiraConfigurationError(AkiraBaseException):
    """Error de configuración del sistema"""
    pass

class AkiraServiceError(AkiraBaseException):
    """Error en servicios externos (Firebase, OpenAI)"""
    pass

class AkiraNetworkError(AkiraBaseException):
    """Error en operaciones de red (nmap, conectividad)"""
    pass

class AkiraValidationError(AkiraBaseException):
    """Error de validación de datos"""
    pass

class AkiraSecurityError(AkiraBaseException):
    """Error de seguridad o acceso no autorizado"""
    pass

class AkiraOperationError(AkiraBaseException):
    """Error en operaciones ofensivas/defensivas"""
    pass

class ErrorHandler:
    """Manejador centralizado de errores"""
    
    @staticmethod
    async def handle_service_error(error: Exception, service_name: str) -> HTTPException:
        """Maneja errores de servicios externos"""
        
        error_details = {
            "service": service_name,
            "error_type": type(error).__name__,
            "error_message": str(error)
        }
        
        # Log del error
        await logger.log_activity(
            activity_type="error",
            details=error_details,
            level="error",
            save_to_firebase=True
        )
        
        # Mapeo de errores específicos
        if "firebase" in service_name.lower():
            return HTTPException(
                status_code=503,
                detail={
                    "error": "Firebase service unavailable",
                    "message": "Unable to connect to Firebase. Please try again later.",
                    "service": service_name
                }
            )
        elif "openai" in service_name.lower():
            return HTTPException(
                status_code=503,
                detail={
                    "error": "AI service unavailable",
                    "message": "Unable to connect to OpenAI. Please try again later.",
                    "service": service_name
                }
            )
        else:
            return HTTPException(
                status_code=500,
                detail={
                    "error": "Service error",
                    "message": f"Error in {service_name} service",
                    "service": service_name
                }
            )
    
    @staticmethod
    async def handle_validation_error(error: Exception, context: str) -> HTTPException:
        """Maneja errores de validación"""
        
        error_details = {
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error)
        }
        
        await logger.log_activity(
            activity_type="validation_error",
            details=error_details,
            level="warning",
            save_to_firebase=False
        )
        
        return HTTPException(
            status_code=422,
            detail={
                "error": "Validation error",
                "message": str(error),
                "context": context
            }
        )
    
    @staticmethod
    async def handle_security_error(error: Exception, context: str) -> HTTPException:
        """Maneja errores de seguridad"""
        
        error_details = {
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error)
        }
        
        await logger.log_activity(
            activity_type="security_alert",
            details=error_details,
            level="critical",
            save_to_firebase=True
        )
        
        return HTTPException(
            status_code=403,
            detail={
                "error": "Security error",
                "message": "Access denied or security violation detected",
                "context": context
            }
        )
    
    @staticmethod
    async def handle_network_error(error: Exception, target: str) -> HTTPException:
        """Maneja errores de red"""
        
        error_details = {
            "target": target,
            "error_type": type(error).__name__,
            "error_message": str(error)
        }
        
        await logger.log_activity(
            activity_type="network_error",
            details=error_details,
            level="warning",
            save_to_firebase=True
        )
        
        return HTTPException(
            status_code=400,
            detail={
                "error": "Network error",
                "message": f"Unable to reach target: {target}",
                "target": target
            }
        )
    
    @staticmethod
    async def handle_operation_error(error: Exception, operation: str, target: str) -> HTTPException:
        """Maneja errores de operaciones ofensivas/defensivas"""
        
        error_details = {
            "operation": operation,
            "target": target,
            "error_type": type(error).__name__,
            "error_message": str(error)
        }
        
        await logger.log_activity(
            activity_type="operation_error",
            details=error_details,
            level="error",
            save_to_firebase=True
        )
        
        return HTTPException(
            status_code=400,
            detail={
                "error": "Operation failed",
                "message": f"Failed to execute {operation} on {target}",
                "operation": operation,
                "target": target
            }
        )

# Instancia global del manejador de errores
error_handler = ErrorHandler()

def get_error_handler() -> ErrorHandler:
    """Obtiene la instancia del manejador de errores"""
    return error_handler
