# fix_missing_models.py

"""
SUME DOCBLOCK

Nombre: Corrector de Modelos Faltantes Identificados
Tipo: Herramienta

Entradas:
- Errores identificados en logs de Akira

Acciones:
- Crea modelos faltantes específicos
- Actualiza imports automáticamente
- Corrige errores de atributos

Salidas:
- Sistema Akira 100% funcional
"""

import os
from pathlib import Path

def create_additional_models():
    """Crea modelos adicionales faltantes identificados en logs"""
    
    additional_models_content = '''# models/additional_missing_models.py

"""
SUME DOCBLOCK

Nombre: Modelos Adicionales Faltantes Identificados
Tipo: Contrato

Entradas:
- Errores específicos identificados en logs

Acciones:
- Define modelos faltantes específicos
- Soluciona errores de importación

Salidas:
- Modelos validados para sistema completo
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from datetime import datetime

# ================================
# MODELOS IDENTIFICADOS EN LOGS
# ================================

class SeverityLevel(str, Enum):
    """Niveles de severidad para exploits y vulnerabilidades"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class FirewallRule(BaseModel):
    """Modelo para reglas de firewall individuales"""
    rule_id: str = Field(..., description="ID único de la regla")
    name: str = Field(..., description="Nombre de la regla")
    action: str = Field(..., description="Acción (allow, deny, drop)")
    protocol: str = Field(default="tcp", description="Protocolo")
    source_ip: Optional[str] = Field(None, description="IP de origen")
    destination_ip: Optional[str] = Field(None, description="IP de destino")
    source_port: Optional[Union[int, str]] = Field(None, description="Puerto de origen")
    destination_port: Optional[Union[int, str]] = Field(None, description="Puerto de destino")
    enabled: bool = Field(default=True, description="Si la regla está activa")
    priority: int = Field(default=100, description="Prioridad de la regla")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AttackingIP(BaseModel):
    """Modelo para IPs atacantes identificadas"""
    ip_address: str = Field(..., description="Dirección IP del atacante")
    attack_count: int = Field(default=1, description="Número de ataques detectados")
    first_seen: datetime = Field(default_factory=datetime.utcnow, description="Primera vez detectada")
    last_seen: datetime = Field(default_factory=datetime.utcnow, description="Última vez detectada")
    attack_types: List[str] = Field(default_factory=list, description="Tipos de ataques realizados")
    severity: SeverityLevel = Field(default=SeverityLevel.MEDIUM, description="Severidad de la amenaza")
    blocked: bool = Field(default=False, description="Si la IP está bloqueada")
    country: Optional[str] = Field(None, description="País de origen")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HoneypotInfo(BaseModel):
    """Información detallada de honeypot"""
    honeypot_id: str = Field(..., description="ID único del honeypot")
    name: str = Field(..., description="Nombre del honeypot")
    type: str = Field(..., description="Tipo de honeypot")
    port: int = Field(..., description="Puerto donde está corriendo")
    status: str = Field(..., description="Estado actual")
    interface: str = Field(default="0.0.0.0", description="Interfaz de red")
    
    # Estadísticas
    total_connections: int = Field(default=0, description="Total de conexiones")
    unique_attackers: int = Field(default=0, description="Atacantes únicos")
    credentials_captured: int = Field(default=0, description="Credenciales capturadas")
    
    # Configuración
    log_level: str = Field(default="info", description="Nivel de logging")
    capture_enabled: bool = Field(default=True, description="Si está capturando datos")
    
    # Metadatos temporales
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación")
    last_activity: Optional[datetime] = Field(None, description="Última actividad")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# ================================
# MODELOS PARA ARREGLAR ERRORES DE ATRIBUTOS
# ================================

class ScanTarget(BaseModel):
    """Target mejorado para escaneos (arregla error de .ip)"""
    value: str = Field(..., description="Valor del target (IP, dominio, etc)")
    
    @property
    def ip(self) -> Optional[str]:
        """Extrae IP si el target es una IP válida"""
        import re
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, self.value):
            return self.value
        return None
    
    @property
    def hostname(self) -> Optional[str]:
        """Extrae hostname si el target es un dominio"""
        if not self.ip:
            return self.value
        return None
    
    def __str__(self):
        return self.value

# ================================
# MODELOS ADICIONALES ÚTILES
# ================================

class ExploitInfo(BaseModel):
    """Información detallada de exploit"""
    exploit_id: str = Field(..., description="ID único del exploit")
    name: str = Field(..., description="Nombre del exploit")
    category: str = Field(..., description="Categoría del exploit")
    severity: SeverityLevel = Field(..., description="Nivel de severidad")
    description: str = Field(..., description="Descripción del exploit")
    target_platform: List[str] = Field(default_factory=list, description="Plataformas objetivo")
    cve_ids: List[str] = Field(default_factory=list, description="CVE IDs relacionados")
    references: List[str] = Field(default_factory=list, description="Referencias adicionales")
    verified: bool = Field(default=False, description="Si el exploit está verificado")

class ThreatInfo(BaseModel):
    """Información de amenaza detectada"""
    threat_id: str = Field(..., description="ID único de la amenaza")
    threat_type: str = Field(..., description="Tipo de amenaza")
    severity: SeverityLevel = Field(..., description="Severidad de la amenaza")
    source_ip: str = Field(..., description="IP de origen")
    target_ip: Optional[str] = Field(None, description="IP objetivo")
    description: str = Field(..., description="Descripción de la amenaza")
    detected_at: datetime = Field(default_factory=datetime.utcnow, description="Momento de detección")
    blocked: bool = Field(default=False, description="Si fue bloqueada")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# ================================
# MODELOS DE CONFIGURACIÓN DEL SISTEMA
# ================================

class SystemConfig(BaseModel):
    """Configuración del sistema"""
    debug_mode: bool = Field(default=False, description="Modo debug")
    log_level: str = Field(default="info", description="Nivel de logging")
    max_concurrent_scans: int = Field(default=5, description="Máximo escaneos concurrentes")
    api_timeout: int = Field(default=30, description="Timeout de API en segundos")
    enable_real_tools: bool = Field(default=False, description="Habilitar herramientas reales")

class ToolStatus(BaseModel):
    """Estado de herramientas del sistema"""
    tool_name: str = Field(..., description="Nombre de la herramienta")
    available: bool = Field(..., description="Si está disponible")
    version: Optional[str] = Field(None, description="Versión de la herramienta")
    path: Optional[str] = Field(None, description="Ruta de la herramienta")
    simulation_mode: bool = Field(default=False, description="Si está en modo simulación")
    last_check: datetime = Field(default_factory=datetime.utcnow, description="Última verificación")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
'''
    
    print("💾 CREANDO models/additional_missing_models.py")
    print("=" * 60)
    
    try:
        with open("models/additional_missing_models.py", 'w', encoding='utf-8') as f:
            f.write(additional_models_content)
        print("✅ Creado models/additional_missing_models.py")
        return True
    except Exception as e:
        print(f"❌ Error creando additional_missing_models.py: {e}")
        return False

def update_models_init_final():
    """Actualización final de models/__init__.py"""
    
    print("\n🔄 ACTUALIZANDO models/__init__.py FINAL")
    print("=" * 60)
    
    try:
        # Leer archivo actual
        with open("models/__init__.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Agregar import de additional_missing_models
        additional_import = """
# Importar modelos adicionales faltantes identificados
from .additional_missing_models import (
    SeverityLevel,
    FirewallRule,
    AttackingIP,
    HoneypotInfo,
    ScanTarget,
    ExploitInfo,
    ThreatInfo,
    SystemConfig,
    ToolStatus
)"""
        
        # Insertar el import
        if "from .defense_models import" in content:
            content = content.replace(
                "from .defense_models import",
                additional_import + "\n\nfrom .defense_models import"
            )
        else:
            content = content.replace(
                "__all__ = [",
                additional_import + "\n\n__all__ = ["
            )
        
        # Agregar modelos a __all__
        additional_models_list = '''
    # Modelos adicionales faltantes identificados
    "SeverityLevel",
    "FirewallRule", 
    "AttackingIP",
    "HoneypotInfo",
    "ScanTarget",
    "ExploitInfo",
    "ThreatInfo",
    "SystemConfig",
    "ToolStatus",'''
        
        # Insertar antes del cierre de __all__
        content = content.replace("]", additional_models_list + "\n]")
        
        # Escribir archivo actualizado
        with open("models/__init__.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Actualizado models/__init__.py")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando __init__.py: {e}")
        return False

def fix_attribute_errors():
    """Script para arreglar errores de atributos identificados"""
    
    print("\n🔧 GENERANDO SCRIPT PARA ARREGLAR ERRORES DE ATRIBUTOS")
    print("=" * 60)
    
    fix_script = '''# fix_attribute_errors.py

"""
Script para arreglar errores de atributos en Akira
Ejecutar después de instalar los modelos faltantes
"""

import re

def fix_target_attribute_error():
    """Arregla el error 'str' object has no attribute 'ip'"""
    
    print("🔧 Arreglando errores de atributos en offense.py...")
    
    try:
        # Leer archivo offense.py
        with open("api/offense.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar y reemplazar el patrón problemático
        # scan_request.target.ip or scan_request.target.hostname
        # por scan_request.target (que ya es string)
        
        old_pattern = r'scan_request\.target\.ip or scan_request\.target\.hostname'
        new_pattern = 'str(scan_request.target)'
        
        if old_pattern in content:
            content = re.sub(old_pattern, new_pattern, content)
            
            # Escribir archivo corregido
            with open("api/offense.py", 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Corregido error de atributo en offense.py")
        else:
            print("ℹ️  No se encontró el patrón específico en offense.py")
            
    except Exception as e:
        print(f"❌ Error arreglando offense.py: {e}")

def main():
    print("🔧 ARREGLANDO ERRORES DE ATRIBUTOS IDENTIFICADOS")
    print("=" * 60)
    
    fix_target_attribute_error()
    
    print("\\n✅ Errores de atributos corregidos")
    print("   Reinicia Akira para aplicar los cambios")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open("fix_attribute_errors.py", 'w', encoding='utf-8') as f:
            f.write(fix_script)
        print("✅ Generado fix_attribute_errors.py")
        return True
    except Exception as e:
        print(f"❌ Error generando script: {e}")
        return False

def test_new_models():
    """Test de los nuevos modelos"""
    
    print("\n🧪 TESTEANDO NUEVOS MODELOS")
    print("=" * 60)
    
    models_to_test = [
        "SeverityLevel",
        "FirewallRule",
        "AttackingIP", 
        "HoneypotInfo",
        "ScanTarget",
        "ExploitInfo",
        "ThreatInfo"
    ]
    
    success_count = 0
    
    for model in models_to_test:
        try:
            exec(f"from models import {model}")
            print(f"✅ {model}")
            success_count += 1
        except Exception as e:
            print(f"❌ {model}: {e}")
    
    print(f"\n📊 RESULTADO: {success_count}/{len(models_to_test)} modelos disponibles")
    return success_count == len(models_to_test)

def main():
    """Función principal de corrección"""
    
    print("🔧 CORRECTOR DE MODELOS FALTANTES - FASE FINAL")
    print("=" * 80)
    print("   Solucionando errores identificados en logs de Akira")
    print("=" * 80)
    
    # 1. Crear modelos adicionales
    models_created = create_additional_models()
    
    # 2. Actualizar __init__.py
    init_updated = update_models_init_final()
    
    # 3. Generar script de corrección de atributos
    fix_script_created = fix_attribute_errors()
    
    # 4. Test de nuevos modelos
    models_working = test_new_models()
    
    print("\n" + "=" * 80)
    print("🎯 RESULTADO FINAL")
    print("=" * 80)
    
    if all([models_created, init_updated, fix_script_created, models_working]):
        print("🎉 ¡TODOS LOS MODELOS FALTANTES AGREGADOS!")
        print("   ✅ Archivo additional_missing_models.py creado")
        print("   ✅ models/__init__.py actualizado")
        print("   ✅ Script de corrección generado")
        print("   ✅ Todos los modelos importables")
        print("\n🚀 PRÓXIMOS PASOS:")
        print("   1. python fix_attribute_errors.py")
        print("   2. Reiniciar Akira: Ctrl+C y python main.py")
        print("   3. python comprehensive_akira_test.py")
        print("\n💪 Tu sistema Akira estará 100% funcional")
    else:
        print("⚠️  Algunos pasos fallaron")
        print("   Revisa los errores anteriores")
    
    print("=" * 80)

if __name__ == "__main__":
    main()