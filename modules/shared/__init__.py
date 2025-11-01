"""
SUME DOCBLOCK

Nombre: Shared Module Initializer
Tipo: Lógica

Entradas:
- Importaciones de utilidades compartidas

Acciones:
- Expone utilidades y validadores
- Facilita acceso a funciones comunes

Salidas:
- Utilidades compartidas disponibles
"""

# Import functions safely
def get_network_utils():
    from .utils import get_network_utils as _get_network_utils
    return _get_network_utils()

def get_security_utils():
    from .utils import get_security_utils as _get_security_utils
    return _get_security_utils()

def get_data_utils():
    from .utils import get_data_utils as _get_data_utils
    return _get_data_utils()

def get_time_utils():
    from .utils import get_time_utils as _get_time_utils
    return _get_time_utils()

def get_system_utils():
    from .utils import get_system_utils as _get_system_utils
    return _get_system_utils()

def get_akira_utils():
    from .utils import get_akira_utils as _get_akira_utils
    return _get_akira_utils()

def validate_input(*args, **kwargs):
    from .validators import validate_input as _validate_input
    return _validate_input(*args, **kwargs)

# Import classes
try:
    from .utils import NetworkUtils, SecurityUtils, DataUtils, TimeUtils, SystemUtils, AkiraUtils
    from .validators import NetworkValidators, SecurityValidators, BusinessValidators, DataValidators
except ImportError:
    pass

__all__ = [
    'get_network_utils', 'get_security_utils', 'get_data_utils',
    'get_time_utils', 'get_system_utils', 'get_akira_utils',
    'validate_input'
]
