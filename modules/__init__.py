"""
SUME DOCBLOCK

Nombre: Modules Package Initializer
Tipo: Lógica

Entradas:
- Importaciones de todos los módulos

Acciones:
- Expone módulos ofensivos, defensivos y compartidos
- Facilita importaciones centralizadas

Salidas:
- Todos los módulos de Akira disponibles
"""

# Import modules safely
from . import offense
from . import defense  
from . import shared

__all__ = ['offense', 'defense', 'shared']
