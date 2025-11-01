"""
SUME DOCBLOCK

Nombre: Defense Module Initializer
Tipo: Lógica

Entradas:
- Importaciones de módulos defensivos

Acciones:
- Expone herramientas defensivas
- Facilita acceso a firewall y honeypots

Salidas:
- Módulos defensivos disponibles
"""

# Import functions directly from modules
def get_firewall_manager():
    from .firewall_manager import get_firewall_manager as _get_firewall_manager
    return _get_firewall_manager()

def get_honeypot_deployer():
    from .honeypot_deployer import get_honeypot_deployer as _get_honeypot_deployer
    return _get_honeypot_deployer()

def get_ai_threat_detector():
    from .ai_threat_detector import get_ai_threat_detector as _get_ai_threat_detector
    return _get_ai_threat_detector()

# Import classes for type hints
try:
    from .firewall_manager import FirewallManager
    from .honeypot_deployer import HoneypotDeployer
    from .ai_threat_detector import AIThreatDetector
except ImportError:
    # Fallback if modules have issues
    pass

__all__ = [
    'get_firewall_manager',
    'get_honeypot_deployer',
    'get_ai_threat_detector'
]
