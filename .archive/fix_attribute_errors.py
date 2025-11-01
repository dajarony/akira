# fix_attribute_errors.py

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
    
    print("\n✅ Errores de atributos corregidos")
    print("   Reinicia Akira para aplicar los cambios")

if __name__ == "__main__":
    main()
