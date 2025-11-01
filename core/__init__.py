"""
SUME DOCBLOCK

Nombre: Core Module Initializer
Tipo: Lógica

Entradas:
- Importaciones de módulos core

Acciones:
- Expone interfaces principales
- Facilita importaciones

Salidas:
- Módulos core disponibles
"""

from .config import get_settings, AkiraConfig
from .logger import get_logger, AkiraLogger
from .services import get_services, AkiraServices
from .exceptions import (
    AkiraBaseException,
    AkiraConfigurationError,
    AkiraServiceError,
    AkiraNetworkError,
    AkiraValidationError,
    AkiraSecurityError,
    AkiraOperationError,
    get_error_handler
)
from .auth import get_auth_manager, AuthManager, User, Token, TokenData
from .rate_limiter import get_rate_limiter, AdvancedRateLimiter
from .target_authorization import get_target_auth_manager, TargetAuthorizationManager

__all__ = [
    'get_settings',
    'AkiraConfig',
    'get_logger',
    'AkiraLogger',
    'get_services',
    'AkiraServices',
    'AkiraBaseException',
    'AkiraConfigurationError',
    'AkiraServiceError',
    'AkiraNetworkError',
    'AkiraValidationError',
    'AkiraSecurityError',
    'AkiraOperationError',
    'get_error_handler',
    'get_auth_manager',
    'AuthManager',
    'User',
    'Token',
    'TokenData',
    'get_rate_limiter',
    'AdvancedRateLimiter',
    'get_target_auth_manager',
    'TargetAuthorizationManager'
]
