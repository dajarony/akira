"""
SUME DOCBLOCK

Nombre: Sistema de Logging Híbrido Akira
Tipo: Lógica

Entradas:
- Configuración de logging (nivel, archivos, formato)
- Mensajes de log desde toda la aplicación
- Datos estructurados para Firebase

Acciones:
- Configura logging JSON estructurado
- Envía logs críticos a Firebase activities
- Mantiene logs detallados en archivo local
- Formatea salida a consola en desarrollo

Salidas:
- Logs estructurados en akira.log
- Actividades críticas en Firebase
- Salida formateada en consola
"""

import logging
import json
import structlog
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from core.config import get_settings

class AkiraLogger:
    def __init__(self):
        self.settings = get_settings()
        self.firebase_service = None  # Se inyecta después
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura el sistema de logging estructurado"""
        
        # Configurar structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="ISO"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        # Configurar logging estándar
        logging.basicConfig(
            level=getattr(logging, self.settings.log_level),
            format='%(message)s'
        )
        
        # Logger principal
        self.logger = structlog.get_logger("akira")
        
        # Configurar handlers
        self._setup_file_handler()
        if self.settings.log_to_console:
            self._setup_console_handler()
    
    def _setup_file_handler(self):
        """Configura el handler para archivo"""
        if self.settings.log_to_file:
            file_handler = logging.FileHandler(
                self.settings.log_file_path, 
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, self.settings.log_level))
            logging.getLogger().addHandler(file_handler)
    
    def _setup_console_handler(self):
        """Configura el handler para consola"""
        console_handler = logging.StreamHandler()
        
        # Solo warnings y errores en producción
        if self.settings.environment == 'production':
            console_handler.setLevel(logging.WARNING)
        else:
            console_handler.setLevel(getattr(logging, self.settings.log_level))
        
        logging.getLogger().addHandler(console_handler)
    
    def set_firebase_service(self, firebase_service):
        """Inyecta el servicio Firebase para logging crítico"""
        self.firebase_service = firebase_service
    
    async def log_activity(self, 
                          activity_type: str, 
                          details: Dict[str, Any], 
                          level: str = "info",
                          save_to_firebase: bool = True):
        """
        Log de actividad con envío opcional a Firebase
        
        Args:
            activity_type: Tipo de actividad (scan, exploit, defense, etc.)
            details: Detalles de la actividad
            level: Nivel de log (debug, info, warning, error)
            save_to_firebase: Si enviar a Firebase activities
        """
        
        log_data = {
            "activity_type": activity_type,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details,
            "environment": self.settings.environment
        }
        
        # Log local
        log_method = getattr(self.logger, level.lower())
        log_method("Activity logged", **log_data)
        
        # Log en Firebase para actividades críticas
        if save_to_firebase and self.firebase_service:
            critical_activities = ['scan', 'exploit', 'defense_action', 'error', 'security_alert']
            if activity_type in critical_activities:
                try:
                    await self.firebase_service.save_activity(log_data)
                except Exception as e:
                    self.logger.error("Failed to save activity to Firebase", error=str(e))
    
    def info(self, message: str, **kwargs):
        """Log nivel INFO"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log nivel WARNING"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log nivel ERROR"""
        self.logger.error(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log nivel DEBUG"""
        self.logger.debug(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log nivel CRITICAL"""
        self.logger.critical(message, **kwargs)

# Instancia global del logger
akira_logger = AkiraLogger()

def get_logger() -> AkiraLogger:
    """Obtiene la instancia del logger"""
    return akira_logger
