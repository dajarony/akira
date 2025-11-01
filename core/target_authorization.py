"""
SUME DOCBLOCK

Nombre: Sistema de Autorización de Targets Akira
Tipo: Core/Seguridad

Entradas:
- IPs y dominios target
- Configuración de whitelist
- Requests de autorización

Acciones:
- Valida targets contra whitelist
- Verifica rangos de red permitidos
- Bloquea infraestructura crítica
- Registra intentos de acceso no autorizado

Salidas:
- Autorización permitida/denegada
- Razones de bloqueo
- Logs de seguridad
"""

import ipaddress
import socket
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from core import get_settings, get_logger
from core.exceptions import AkiraSecurityError

class TargetAuthorizationManager:
    """Gestor de autorización de targets"""

    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger()

        # Configuración
        self.require_authorization = getattr(self.settings, 'require_target_authorization', True)
        self.strict_mode = getattr(self.settings, 'strict_security_mode', True)

        # Cargar whitelist de configuración
        whitelist_str = getattr(self.settings, 'whitelisted_targets', '')
        self.whitelisted_targets = [
            target.strip() for target in whitelist_str.split(',') if target.strip()
        ]

        # Infraestructura crítica SIEMPRE bloqueada
        self.critical_infrastructure = [
            # DNS Públicos
            "8.8.8.8", "8.8.4.4",  # Google DNS
            "1.1.1.1", "1.0.0.1",  # Cloudflare DNS
            "208.67.222.222", "208.67.220.220",  # OpenDNS
            # Redes gubernamentales (ejemplos)
            "*.gov", "*.mil",
            # Servicios críticos
            "*.emergency.gov", "*.911.gov",
        ]

        # Dominios públicos grandes BLOQUEADOS por defecto
        self.blocked_public_domains = [
            "google.com", "facebook.com", "amazon.com", "microsoft.com",
            "apple.com", "netflix.com", "twitter.com", "instagram.com",
            "linkedin.com", "youtube.com", "yahoo.com", "reddit.com",
            "github.com", "gitlab.com", "bitbucket.org",
            "aws.amazon.com", "azure.microsoft.com", "cloud.google.com",
        ]

        # Rangos privados permitidos por defecto
        self.private_ranges = [
            ipaddress.ip_network("10.0.0.0/8"),
            ipaddress.ip_network("172.16.0.0/12"),
            ipaddress.ip_network("192.168.0.0/16"),
            ipaddress.ip_network("127.0.0.0/8"),
        ]

    def is_private_ip(self, ip: str) -> bool:
        """Verifica si una IP es privada"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return any(ip_obj in network for network in self.private_ranges)
        except ValueError:
            return False

    def is_valid_ip(self, ip: str) -> bool:
        """Verifica si es una IP válida"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def resolve_domain(self, domain: str) -> Optional[str]:
        """Resuelve un dominio a IP"""
        try:
            # Limpiar dominio
            parsed = urlparse(f"http://{domain}")
            clean_domain = parsed.hostname or domain

            ip = socket.gethostbyname(clean_domain)
            return ip
        except socket.gaierror:
            return None

    def is_in_whitelist(self, target: str) -> bool:
        """Verifica si un target está en la whitelist"""
        if not self.whitelisted_targets:
            return False

        # Verificar coincidencia exacta
        if target in self.whitelisted_targets:
            return True

        # Verificar si es IP en rango CIDR de whitelist
        if self.is_valid_ip(target):
            target_ip = ipaddress.ip_address(target)
            for whitelisted in self.whitelisted_targets:
                if '/' in whitelisted:  # Es un CIDR
                    try:
                        network = ipaddress.ip_network(whitelisted, strict=False)
                        if target_ip in network:
                            return True
                    except ValueError:
                        continue

        # Verificar dominios
        for whitelisted in self.whitelisted_targets:
            if '*' in whitelisted:  # Wildcard
                pattern = whitelisted.replace('.', r'\.').replace('*', '.*')
                import re
                if re.match(pattern, target):
                    return True
            elif target.endswith(whitelisted) or whitelisted.endswith(target):
                return True

        return False

    def is_critical_infrastructure(self, target: str) -> Tuple[bool, Optional[str]]:
        """Verifica si es infraestructura crítica"""
        # Verificar IPs críticas
        if target in self.critical_infrastructure:
            return True, f"Target {target} is critical infrastructure"

        # Verificar dominios críticos
        for critical in self.critical_infrastructure:
            if '*' in critical:
                pattern = critical.replace('.', r'\.').replace('*', '.*')
                import re
                if re.match(pattern, target):
                    return True, f"Target matches critical pattern {critical}"
            elif critical in target or target in critical:
                return True, f"Target contains critical domain {critical}"

        return False, None

    def is_blocked_public_domain(self, target: str) -> Tuple[bool, Optional[str]]:
        """Verifica si es un dominio público bloqueado"""
        for blocked in self.blocked_public_domains:
            if blocked in target or target.endswith(blocked):
                return True, f"Target {target} is a blocked public service"
        return False, None

    async def authorize_target(self, target: str, user_id: Optional[str] = None) -> Tuple[bool, dict]:
        """
        Autoriza un target para escaneo/ataque

        Args:
            target: IP o dominio a verificar
            user_id: ID del usuario solicitante

        Returns:
            (is_authorized, details_dict)
        """
        # Log del intento
        await self.logger.log_activity(
            activity_type="target_authorization_check",
            details={
                "target": target,
                "user_id": user_id,
                "require_authorization": self.require_authorization,
                "strict_mode": self.strict_mode
            },
            save_to_firebase=False
        )

        # Si no se requiere autorización y no está en modo estricto
        if not self.require_authorization and not self.strict_mode:
            return True, {"authorized": True, "reason": "authorization_disabled"}

        # SIEMPRE bloquear infraestructura crítica
        is_critical, reason = self.is_critical_infrastructure(target)
        if is_critical:
            await self.logger.log_activity(
                activity_type="security_alert",
                details={
                    "event": "critical_infrastructure_target_blocked",
                    "target": target,
                    "user_id": user_id,
                    "reason": reason
                },
                level="critical",
                save_to_firebase=True
            )
            return False, {
                "authorized": False,
                "reason": "critical_infrastructure",
                "message": reason
            }

        # Bloquear dominios públicos grandes
        is_blocked, reason = self.is_blocked_public_domain(target)
        if is_blocked:
            await self.logger.log_activity(
                activity_type="security_alert",
                details={
                    "event": "blocked_public_domain_target",
                    "target": target,
                    "user_id": user_id,
                    "reason": reason
                },
                level="warning",
                save_to_firebase=True
            )
            return False, {
                "authorized": False,
                "reason": "blocked_public_domain",
                "message": reason
            }

        # Si es IP privada, permitir (red interna)
        if self.is_valid_ip(target) and self.is_private_ip(target):
            return True, {
                "authorized": True,
                "reason": "private_network",
                "message": f"Target {target} is in private network range"
            }

        # Verificar whitelist
        if self.is_in_whitelist(target):
            return True, {
                "authorized": True,
                "reason": "whitelisted",
                "message": f"Target {target} is in whitelist"
            }

        # Si llegamos aquí y se requiere autorización, denegar
        if self.require_authorization:
            await self.logger.log_activity(
                activity_type="security_alert",
                details={
                    "event": "unauthorized_target_blocked",
                    "target": target,
                    "user_id": user_id,
                    "reason": "not_in_whitelist"
                },
                level="warning",
                save_to_firebase=True
            )
            return False, {
                "authorized": False,
                "reason": "not_whitelisted",
                "message": f"Target {target} is not in whitelist and authorization is required"
            }

        # Por defecto, permitir si no hay restricciones
        return True, {
            "authorized": True,
            "reason": "no_restrictions"
        }

    async def add_to_whitelist(self, target: str, admin_user_id: str) -> dict:
        """Añade un target a la whitelist (solo admin)"""
        if target not in self.whitelisted_targets:
            self.whitelisted_targets.append(target)

            await self.logger.log_activity(
                activity_type="whitelist_update",
                details={
                    "action": "add",
                    "target": target,
                    "admin_user_id": admin_user_id
                },
                save_to_firebase=True
            )

            return {
                "success": True,
                "message": f"Target {target} added to whitelist",
                "whitelist_count": len(self.whitelisted_targets)
            }

        return {
            "success": False,
            "message": f"Target {target} already in whitelist"
        }

    async def remove_from_whitelist(self, target: str, admin_user_id: str) -> dict:
        """Elimina un target de la whitelist (solo admin)"""
        if target in self.whitelisted_targets:
            self.whitelisted_targets.remove(target)

            await self.logger.log_activity(
                activity_type="whitelist_update",
                details={
                    "action": "remove",
                    "target": target,
                    "admin_user_id": admin_user_id
                },
                save_to_firebase=True
            )

            return {
                "success": True,
                "message": f"Target {target} removed from whitelist",
                "whitelist_count": len(self.whitelisted_targets)
            }

        return {
            "success": False,
            "message": f"Target {target} not in whitelist"
        }

    def get_whitelist(self) -> List[str]:
        """Obtiene la whitelist actual"""
        return self.whitelisted_targets.copy()

# Instancia global
_target_auth_manager = None

def get_target_auth_manager() -> TargetAuthorizationManager:
    """Obtiene la instancia del gestor de autorización de targets"""
    global _target_auth_manager
    if _target_auth_manager is None:
        _target_auth_manager = TargetAuthorizationManager()
    return _target_auth_manager
