"""
SUME DOCBLOCK

Nombre: Offense Module Initializer
Tipo: Lógica

Entradas:
- Importaciones de módulos ofensivos

Acciones:
- Expone herramientas ofensivas
- Facilita acceso a escáneres y exploits

Salidas:
- Módulos ofensivos disponibles
"""

# Import functions directly from modules
def get_nmap_scanner():
    from .nmap_scanner import get_nmap_scanner as _get_nmap_scanner
    return _get_nmap_scanner()

def get_osint_collector():
    from .osint_collector import get_osint_collector as _get_osint_collector
    return _get_osint_collector()

def get_exploit_launcher():
    from .exploit_launcher import get_exploit_launcher as _get_exploit_launcher
    return _get_exploit_launcher()

# Import classes for type hints
try:
    from .nmap_scanner import NmapScanner
    from .osint_collector import OSINTCollector
    from .exploit_launcher import ExploitLauncher
except ImportError:
    # Fallback if modules have issues
    pass

__all__ = [
    'get_nmap_scanner',
    'get_osint_collector',
    'get_exploit_launcher'
]
