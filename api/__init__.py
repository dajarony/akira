"""
SUME DOCBLOCK

Nombre: API Module Initializer
Tipo: Entrada

Entradas:
- Importaciones de routers API

Acciones:
- Expone routers de endpoints
- Facilita configuración de FastAPI

Salidas:
- Routers API disponibles para app principal
"""

from .offense import router as offense_router
from .defense import router as defense_router
from .status import router as status_router
from .defense_endpoints import defense_router as defense_endpoints_router

__all__ = [
    'offense_router',
    'defense_router', 
    'status_router',
    'defense_endpoints_router'
]
