# make_akira_real.py

"""
SUME DOCBLOCK

Nombre: Convertidor de Akira de Simulación a Sistema Real
Tipo: Herramienta

Entradas:
- Sistema Akira en modo híbrido/simulación

Acciones:
- Instala dependencias faltantes
- Configura APIs externas
- Habilita funcionalidades reales
- Verifica capacidades del sistema

Salidas:
- Sistema Akira 100% funcional y real
"""

import subprocess
import sys
import os
import platform
import json
from pathlib import Path

class AkiraRealizer:
    def __init__(self):
        self.system = platform.system().lower()
        self.installation_log = []
        self.config_changes = []
        
    def log_action(self, action: str, success: bool, details: str = ""):
        """Registra acciones realizadas"""
        self.installation_log.append({
            "action": action,
            "success": success,
            "details": details,
            "system": self.system
        })
        
        status = "✅" if success else "❌"
        print(f"   {status} {action}: {details}")

    def check_admin_rights(self):
        """Verifica si tiene permisos de administrador"""
        print("\n🔐 CHECKING ADMIN PRIVILEGES")
        print("=" * 50)
        
        try:
            if self.system == "windows":
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            else:
                is_admin = os.geteuid() == 0
            
            self.log_action("Admin Rights Check", is_admin, 
                          "Available" if is_admin else "Limited - some features may not work")
            return is_admin
            
        except Exception as e:
            self.log_action("Admin Rights Check", False, f"Error: {e}")
            return False

    def install_nmap(self):
        """Instala Nmap según el sistema operativo"""
        print("\n🗺️ INSTALLING NMAP")
        print("=" * 50)
        
        try:
            # Verificar si ya está instalado
            result = subprocess.run(["nmap", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_action("Nmap Installation", True, "Already installed")
                return True
        except:
            pass
        
        # Instalar según SO
        if self.system == "windows":
            self.log_action("Nmap Installation", False, 
                          "Manual installation required - Download from https://nmap.org/download.html")
            print("   💡 Para Windows:")
            print("      1. Ve a https://nmap.org/download.html")
            print("      2. Descarga 'Latest stable release self-installer'")
            print("      3. Ejecuta como administrador")
            print("      4. Reinicia la terminal")
            return False
            
        elif self.system == "linux":
            try:
                # Ubuntu/Debian
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "nmap"], check=True)
                self.log_action("Nmap Installation", True, "Installed via apt")
                return True
            except:
                try:
                    # CentOS/RHEL
                    subprocess.run(["sudo", "yum", "install", "-y", "nmap"], check=True)
                    self.log_action("Nmap Installation", True, "Installed via yum")
                    return True
                except:
                    self.log_action("Nmap Installation", False, "Failed - install manually")
                    return False
                    
        elif self.system == "darwin":  # macOS
            try:
                subprocess.run(["brew", "install", "nmap"], check=True)
                self.log_action("Nmap Installation", True, "Installed via brew")
                return True
            except:
                self.log_action("Nmap Installation", False, "Brew not found - install manually")
                return False

    def install_python_packages(self):
        """Instala paquetes Python para funcionalidad real"""
        print("\n📦 INSTALLING PYTHON PACKAGES")
        print("=" * 50)
        
        packages = [
            ("python-nmap", "Network scanning"),
            ("shodan", "Shodan API integration"),
            ("requests[security]", "Enhanced HTTP security"),
            ("scapy", "Packet manipulation"),
            ("netaddr", "Network address manipulation"),
            ("psutil", "System monitoring"),
            ("python-whois", "WHOIS lookups"),
            ("dnspython", "DNS operations"),
            ("python-virustotal-api", "VirusTotal integration"),
            ("paramiko", "SSH operations"),
        ]
        
        for package, description in packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True)
                self.log_action(f"Package: {package}", True, description)
            except Exception as e:
                self.log_action(f"Package: {package}", False, f"Failed: {str(e)[:50]}")

    def create_env_template(self):
        """Crea template de archivo .env para configuración"""
        print("\n⚙️ CREATING CONFIGURATION TEMPLATE")
        print("=" * 50)
        
        env_template = """# Akira Configuration - Real Mode
# Copia este archivo a .env y completa con tus valores reales

# OpenAI API (para análisis IA)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Firebase (para almacenamiento)
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\\nYOUR_PRIVATE_KEY\\n-----END PRIVATE KEY-----\\n"
FIREBASE_CLIENT_EMAIL=your_service_account@project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id

# APIs de Seguridad
SHODAN_API_KEY=your_shodan_api_key
VIRUSTOTAL_API_KEY=your_virustotal_api_key
HAVEIBEENPWNED_API_KEY=your_hibp_api_key

# Configuración de Red
DEFAULT_SCAN_TIMEOUT=30
MAX_CONCURRENT_SCANS=5
ENABLE_AGGRESSIVE_SCANS=false

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
ENABLE_FILE_LOGGING=true

# Seguridad
ENABLE_REAL_EXPLOITS=false  # PELIGROSO - solo para testing autorizado
HONEYPOT_DEFAULT_PORT_RANGE=8000-8100
FIREWALL_MANAGEMENT=false   # Requiere permisos admin

# APIs de OSINT
CENSYS_API_ID=your_censys_api_id
CENSYS_API_SECRET=your_censys_secret
SECURITYTRAILS_API_KEY=your_securitytrails_key
"""
        
        try:
            with open(".env.template", "w") as f:
                f.write(env_template)
            
            self.log_action("Configuration Template", True, ".env.template created")
            
            # Si no existe .env, crear uno básico
            if not os.path.exists(".env"):
                with open(".env", "w") as f:
                    f.write("# Akira Configuration\n")
                    f.write("LOG_LEVEL=INFO\n")
                    f.write("ENABLE_REAL_EXPLOITS=false\n")
                self.log_action("Basic .env file", True, "Created with safe defaults")
            
        except Exception as e:
            self.log_action("Configuration Template", False, f"Error: {e}")

    def setup_security_tools(self):
        """Configura herramientas de seguridad adicionales"""
        print("\n🛡️ SETTING UP SECURITY TOOLS")
        print("=" * 50)
        
        # Crear directorio para herramientas
        tools_dir = Path("tools")
        tools_dir.mkdir(exist_ok=True)
        
        # Scripts de instalación para herramientas adicionales
        tools_info = {
            "nikto": "Web vulnerability scanner",
            "dirb": "Web directory brute forcer", 
            "sqlmap": "SQL injection testing",
            "metasploit": "Penetration testing framework",
            "wireshark": "Network protocol analyzer"
        }
        
        installation_guide = f"""# Security Tools Installation Guide

## Core Tools (Install manually)

### 1. Nikto (Web Scanner)
```bash
# Ubuntu/Debian
sudo apt install nikto

# Windows
# Download from https://github.com/sullo/nikto
```

### 2. SQLMap (SQL Injection)
```bash
# Python package
pip install sqlmap-python

# Or download from https://github.com/sqlmapproject/sqlmap
```

### 3. Dirb (Directory Brute Force)
```bash
# Ubuntu/Debian
sudo apt install dirb

# Windows/macOS
# Download from http://dirb.sourceforge.net/
```

### 4. Metasploit (Advanced - Optional)
```bash
# Ubuntu/Debian
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
sudo ./msfinstall

# Windows
# Download installer from https://www.metasploit.com/download
```

## API Keys Needed

### Free APIs:
- Shodan: https://developer.shodan.io/api/requirements
- VirusTotal: https://developers.virustotal.com/reference
- HaveIBeenPwned: https://haveibeenpwned.com/API/v3

### Paid APIs (Optional):
- SecurityTrails: https://securitytrails.com/corp/apidocs
- Censys: https://search.censys.io/api

## Notes:
- Start with free APIs for basic functionality
- Install tools one by one and test
- Always get permission before scanning external targets
- Use in isolated environments for safety
"""
        
        try:
            with open(tools_dir / "installation_guide.md", "w") as f:
                f.write(installation_guide)
            
            self.log_action("Security Tools Guide", True, "Installation guide created")
            
        except Exception as e:
            self.log_action("Security Tools Guide", False, f"Error: {e}")

    def verify_real_capabilities(self):
        """Verifica qué capacidades están realmente funcionando"""
        print("\n🔍 VERIFYING REAL CAPABILITIES")
        print("=" * 50)
        
        capabilities = {
            "nmap": self.check_nmap(),
            "python_nmap": self.check_python_nmap(),
            "shodan": self.check_shodan(),
            "scapy": self.check_scapy(),
            "psutil": self.check_psutil(),
            "dns": self.check_dns(),
            "whois": self.check_whois()
        }
        
        real_count = sum(capabilities.values())
        total_count = len(capabilities)
        percentage = (real_count / total_count) * 100
        
        print(f"\n📊 REAL CAPABILITIES: {real_count}/{total_count} ({percentage:.1f}%)")
        
        return capabilities

    def check_nmap(self):
        """Verifica si nmap está disponible"""
        try:
            result = subprocess.run(["nmap", "--version"], 
                                  capture_output=True, timeout=5)
            success = result.returncode == 0
            self.log_action("Nmap Binary", success, "Available" if success else "Not found")
            return success
        except:
            self.log_action("Nmap Binary", False, "Not found")
            return False

    def check_python_nmap(self):
        """Verifica python-nmap"""
        try:
            import nmap
            self.log_action("Python-Nmap", True, "Available")
            return True
        except ImportError:
            self.log_action("Python-Nmap", False, "Not installed")
            return False

    def check_shodan(self):
        """Verifica Shodan"""
        try:
            import shodan
            self.log_action("Shodan Library", True, "Available")
            return True
        except ImportError:
            self.log_action("Shodan Library", False, "Not installed")
            return False

    def check_scapy(self):
        """Verifica Scapy"""
        try:
            import scapy
            self.log_action("Scapy", True, "Available")
            return True
        except ImportError:
            self.log_action("Scapy", False, "Not installed")
            return False

    def check_psutil(self):
        """Verifica psutil"""
        try:
            import psutil
            self.log_action("PSUtil", True, "Available")
            return True
        except ImportError:
            self.log_action("PSUtil", False, "Not installed")
            return False

    def check_dns(self):
        """Verifica dns"""
        try:
            import dns.resolver
            self.log_action("DNS Python", True, "Available")
            return True
        except ImportError:
            self.log_action("DNS Python", False, "Not installed")
            return False

    def check_whois(self):
        """Verifica whois"""
        try:
            import whois
            self.log_action("Python Whois", True, "Available")
            return True
        except ImportError:
            self.log_action("Python Whois", False, "Not installed")
            return False

    def generate_final_report(self, capabilities):
        """Genera reporte final"""
        print("\n" + "=" * 80)
        print("🎯 AKIRA REALIZATION REPORT")
        print("=" * 80)
        
        # Estado de instalaciones
        successful_actions = len([a for a in self.installation_log if a["success"]])
        total_actions = len(self.installation_log)
        success_rate = (successful_actions / total_actions * 100) if total_actions > 0 else 0
        
        print(f"\n📦 INSTALLATION SUMMARY:")
        print(f"   Successful Actions: {successful_actions}/{total_actions} ({success_rate:.1f}%)")
        
        # Capacidades reales
        real_capabilities = sum(capabilities.values())
        total_capabilities = len(capabilities)
        real_percentage = (real_capabilities / total_capabilities) * 100
        
        print(f"\n🔥 REAL CAPABILITIES:")
        print(f"   Real Functions: {real_capabilities}/{total_capabilities} ({real_percentage:.1f}%)")
        
        for capability, status in capabilities.items():
            emoji = "✅" if status else "❌"
            print(f"   {emoji} {capability}")
        
        # Próximos pasos
        print(f"\n🚀 NEXT STEPS:")
        
        if real_percentage < 30:
            print("   🚨 CRITICAL: Install basic dependencies first")
            print("   1. Install nmap manually")
            print("   2. Run: pip install -r requirements.txt")
            print("   3. Get free API keys (Shodan, VirusTotal)")
            
        elif real_percentage < 70:
            print("   ⚠️  GOOD START: Complete the setup")
            print("   1. Configure .env file with your API keys")
            print("   2. Install remaining security tools")
            print("   3. Test with safe targets")
            
        else:
            print("   ✅ EXCELLENT: System is mostly real!")
            print("   1. Fine-tune configuration")
            print("   2. Add advanced tools as needed")
            print("   3. Ready for professional use")
        
        print(f"\n💡 FILES CREATED:")
        print(f"   - .env.template (configuration template)")
        print(f"   - tools/installation_guide.md (security tools guide)")
        
        # Guardar reporte
        report = {
            "installation_log": self.installation_log,
            "capabilities": capabilities,
            "success_rate": success_rate,
            "real_percentage": real_percentage
        }
        
        try:
            with open("akira_realization_report.json", "w") as f:
                json.dump(report, f, indent=2)
            print(f"   - akira_realization_report.json (this report)")
        except Exception as e:
            print(f"   ⚠️  Could not save report: {e}")

    def run_full_realization(self):
        """Ejecuta el proceso completo de realización"""
        print("🚀 AKIRA SYSTEM REALIZATION - FROM SIMULATION TO REALITY")
        print("=" * 80)
        
        # Verificar permisos
        has_admin = self.check_admin_rights()
        
        # Instalar dependencias
        self.install_python_packages()
        
        # Intentar instalar nmap
        self.install_nmap()
        
        # Crear configuración
        self.create_env_template()
        
        # Configurar herramientas
        self.setup_security_tools()
        
        # Verificar capacidades
        capabilities = self.verify_real_capabilities()
        
        # Generar reporte
        self.generate_final_report(capabilities)
        
        return capabilities

def main():
    """Función principal"""
    realizer = AkiraRealizer()
    capabilities = realizer.run_full_realization()
    
    real_count = sum(capabilities.values())
    total_count = len(capabilities)
    
    print("\n" + "=" * 80)
    if real_count >= total_count * 0.7:
        print("🎉 AKIRA IS NOW SIGNIFICANTLY MORE REAL!")
    else:
        print("🔧 AKIRA REALIZATION IN PROGRESS - MANUAL STEPS NEEDED")
    print("=" * 80)

if __name__ == "__main__":
    main()