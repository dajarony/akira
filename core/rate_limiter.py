"""
SUME DOCBLOCK

Nombre: Sistema de Rate Limiting Akira
Tipo: Core/Seguridad

Entradas:
- Requests HTTP
- Identificadores de usuario/IP
- Configuración de límites

Acciones:
- Cuenta requests por usuario/IP
- Aplica límites de tasa
- Bloquea requests excesivos
- Resetea contadores periódicamente

Salidas:
- Permite/Bloquea requests
- Headers de rate limit
- Logs de requests bloqueados
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from typing import Callable
import time
from collections import defaultdict
from datetime import datetime, timedelta

from core import get_settings, get_logger

class AdvancedRateLimiter:
    """Rate limiter avanzado con múltiples estrategias"""

    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger()

        # Configuración de límites
        self.rate_limit_enabled = getattr(self.settings, 'rate_limit_enabled', True)
        self.per_minute = getattr(self.settings, 'rate_limit_per_minute', 60)
        self.per_hour = getattr(self.settings, 'rate_limit_per_hour', 1000)
        self.scan_per_hour = getattr(self.settings, 'rate_limit_scan_per_hour', 10)

        # Almacenamiento de contadores
        self._minute_counters = defaultdict(list)
        self._hour_counters = defaultdict(list)
        self._scan_counters = defaultdict(list)

        # Slowapi limiter
        self.limiter = Limiter(
            key_func=self._get_identifier,
            default_limits=[f"{self.per_minute}/minute", f"{self.per_hour}/hour"]
        )

    def _get_identifier(self, request: Request) -> str:
        """Obtiene identificador único para rate limiting"""
        # Intentar obtener usuario autenticado
        if hasattr(request.state, 'user') and request.state.user:
            return f"user:{request.state.user.username}"

        # Si no hay usuario, usar IP
        return get_remote_address(request)

    def _clean_old_entries(self, counter: dict, max_age_seconds: int):
        """Limpia entradas antiguas de un contador"""
        cutoff_time = datetime.utcnow() - timedelta(seconds=max_age_seconds)

        for key in list(counter.keys()):
            counter[key] = [
                timestamp for timestamp in counter[key]
                if timestamp > cutoff_time
            ]

            if not counter[key]:
                del counter[key]

    def check_rate_limit(self, identifier: str, limit_type: str = "general") -> tuple[bool, dict]:
        """
        Verifica si se excede el rate limit

        Args:
            identifier: Identificador del usuario/IP
            limit_type: Tipo de límite (general, scan, etc.)

        Returns:
            (is_allowed, info_dict)
        """
        if not self.rate_limit_enabled:
            return True, {"allowed": True, "reason": "rate_limiting_disabled"}

        now = datetime.utcnow()

        if limit_type == "scan":
            # Límite especial para escaneos
            self._clean_old_entries(self._scan_counters, 3600)  # 1 hora

            scan_count = len(self._scan_counters[identifier])

            if scan_count >= self.scan_per_hour:
                self.logger.warning(
                    f"Scan rate limit exceeded for {identifier}: {scan_count}/{self.scan_per_hour}"
                )
                return False, {
                    "allowed": False,
                    "reason": "scan_rate_limit_exceeded",
                    "limit": self.scan_per_hour,
                    "current": scan_count,
                    "reset_in_seconds": 3600 - int((now - min(self._scan_counters[identifier])).total_seconds())
                }

            self._scan_counters[identifier].append(now)
            return True, {
                "allowed": True,
                "remaining": self.scan_per_hour - scan_count - 1
            }

        else:
            # Límite general por minuto
            self._clean_old_entries(self._minute_counters, 60)

            minute_count = len(self._minute_counters[identifier])

            if minute_count >= self.per_minute:
                self.logger.warning(
                    f"Rate limit exceeded for {identifier}: {minute_count}/{self.per_minute} per minute"
                )
                return False, {
                    "allowed": False,
                    "reason": "rate_limit_exceeded",
                    "limit": self.per_minute,
                    "current": minute_count,
                    "reset_in_seconds": 60
                }

            self._minute_counters[identifier].append(now)
            return True, {
                "allowed": True,
                "remaining": self.per_minute - minute_count - 1
            }

    async def log_rate_limit_violation(self, identifier: str, endpoint: str, limit_type: str):
        """Registra violaciones de rate limit"""
        await self.logger.log_activity(
            activity_type="rate_limit_violation",
            details={
                "identifier": identifier,
                "endpoint": endpoint,
                "limit_type": limit_type,
                "timestamp": datetime.utcnow().isoformat()
            },
            level="warning",
            save_to_firebase=True
        )

    def get_rate_limit_info(self, identifier: str) -> dict:
        """Obtiene información sobre el estado del rate limit de un identificador"""
        self._clean_old_entries(self._minute_counters, 60)
        self._clean_old_entries(self._hour_counters, 3600)
        self._clean_old_entries(self._scan_counters, 3600)

        return {
            "identifier": identifier,
            "limits": {
                "per_minute": self.per_minute,
                "per_hour": self.per_hour,
                "scans_per_hour": self.scan_per_hour
            },
            "current_usage": {
                "last_minute": len(self._minute_counters.get(identifier, [])),
                "last_hour": len(self._hour_counters.get(identifier, [])),
                "scans_last_hour": len(self._scan_counters.get(identifier, []))
            },
            "remaining": {
                "per_minute": self.per_minute - len(self._minute_counters.get(identifier, [])),
                "per_hour": self.per_hour - len(self._hour_counters.get(identifier, [])),
                "scans_per_hour": self.scan_per_hour - len(self._scan_counters.get(identifier, []))
            }
        }

# Instancia global del rate limiter
_rate_limiter = None

def get_rate_limiter() -> AdvancedRateLimiter:
    """Obtiene la instancia del rate limiter"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = AdvancedRateLimiter()
    return _rate_limiter
