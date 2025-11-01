#!/usr/bin/env python3
"""
Script de despliegue para Akira SASE Cyberwar MVP
Automatiza la configuración y despliegue del sistema
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
from datetime import datetime

class AkiraDeployer:
    """Desplegador automático de Akira"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.requirements_file = self.project_root / "requirements.txt"
        self.env_file = self.project_root / ".env"
        
    def print_banner(self):
        """Imprime banner de Akira"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🛡️⚔️  AKIRA SASE CYBERWAR MVP DEPLOYER  ⚔️🛡️           ║
║                                                              ║
║     Sistema Híbrido de Ciberseguridad Ofensiva/Defensiva    ║
║     Arquitectura SUME + STDG                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"📅 Deployment started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Project root: {self.project_root}")
        print()
    
    def check_system_requirements(self):
        """Verifica requisitos del sistema"""
        print("🔍 Checking system requirements...")
        
        # Verificar Python
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            raise Exception("Python 3.8+ is required")
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Verificar pip
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            print("✅ pip is available")
        except subprocess.CalledProcessError:
            raise Exception("pip is not available")
        
        # Verificar git (opcional)
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            print("✅ git is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  git not found (optional)")
        
        print()
    
    def create_virtual_environment(self):
        """Crea entorno virtual"""
        print("🐍 Setting up virtual environment...")
        
        if self.venv_path.exists():
            print("⚠️  Virtual environment already exists, removing...")
            shutil.rmtree(self.venv_path)
        
        # Crear venv
        subprocess.run([
            sys.executable, "-m", "venv", str(self.venv_path)
        ], check=True)
        
        print(f"✅ Virtual environment created at: {self.venv_path}")
        print()
    
    def get_venv_python(self):
        """Obtiene path del Python del venv"""
        if os.name == 'nt':  # Windows
            return self.venv_path / "Scripts" / "python.exe"
        else:  # Unix/Linux/macOS
            return self.venv_path / "bin" / "python"
    
    def get_venv_pip(self):
        """Obtiene path del pip del venv"""
        if os.name == 'nt':  # Windows
            return self.venv_path / "Scripts" / "pip.exe"
        else:  # Unix/Linux/macOS
            return self.venv_path / "bin" / "pip"
    
    def install_dependencies(self):
        """Instala dependencias"""
        print("📦 Installing dependencies...")
        
        pip_path = self.get_venv_pip()
        
        # Actualizar pip
        subprocess.run([
            str(pip_path), "install", "--upgrade", "pip"
        ], check=True)
        
        # Instalar dependencias básicas
        basic_deps = [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "pydantic>=2.5.0",
            "python-dotenv>=1.0.0",
            "aiohttp>=3.9.0",
            "requests>=2.31.0",
            "python-nmap>=0.7.1",
            "dnspython>=2.4.0",
            "python-whois>=0.8.0",
            "openai>=1.3.0",
            "firebase-admin>=6.2.0",
            "structlog>=23.2.0",
            "colorama>=0.4.6"
        ]
        
        for dep in basic_deps:
            print(f"   Installing {dep}...")
            subprocess.run([
                str(pip_path), "install", dep
            ], check=True, capture_output=True)
        
        print("✅ Dependencies installed successfully")
        print()
    
    def create_env_file(self):
        """Crea archivo .env"""
        print("⚙️  Creating environment configuration...")
        
        env_template = """# Akira SASE Cyberwar MVP Configuration
# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
API_ACCESS_TOKEN=akira-dev-token-2024

# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000

# Firebase Configuration (REQUIRED)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# Security Configuration
MAX_REQUEST_SIZE=10485760
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Logging Configuration
LOG_TO_FILE=true
LOG_FILE_PATH=./logs/akira.log
LOG_TO_FIREBASE=true

# Feature Flags
ENABLE_AI_ANALYSIS=true
ENABLE_FIREBASE_LOGGING=true
ENABLE_NMAP_SCANNING=true
ENABLE_OSINT_COLLECTION=true
ENABLE_EXPLOIT_VERIFICATION=true
ENABLE_FIREWALL_MANAGEMENT=true
ENABLE_HONEYPOT_DEPLOYMENT=true
ENABLE_THREAT_DETECTION=true
"""
        
        if not self.env_file.exists():
            with open(self.env_file, 'w') as f:
                f.write(env_template)
            print(f"✅ Environment file created: {self.env_file}")
        else:
            print(f"⚠️  Environment file already exists: {self.env_file}")
        
        print()
    
    def create_directory_structure(self):
        """Crea estructura de directorios"""
        print("📁 Creating directory structure...")
        
        directories = [
            "logs",
            "data",
            "temp",
            "backups",
            "uploads"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(exist_ok=True)
            print(f"   ✅ {directory}/")
        
        print()
    
    def create_systemd_service(self):
        """Crea servicio systemd (Linux)"""
        if os.name == 'nt':
            print("⚠️  Systemd service creation skipped (Windows)")
            return
        
        print("🔧 Creating systemd service...")
        
        service_content = f"""[Unit]
Description=Akira SASE Cyberwar MVP
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'akira')}
WorkingDirectory={self.project_root}
Environment=PATH={self.venv_path}/bin
ExecStart={self.get_venv_python()} main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        
        service_file = self.project_root / "akira.service"
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        print(f"✅ Systemd service file created: {service_file}")
        print("   To install: sudo cp akira.service /etc/systemd/system/")
        print("   To enable: sudo systemctl enable akira")
        print("   To start: sudo systemctl start akira")
        print()
    
    def create_docker_files(self):
        """Crea archivos Docker"""
        print("🐳 Creating Docker configuration...")
        
        # Dockerfile
        dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    nmap \\
    dnsutils \\
    whois \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data temp backups uploads

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
"""
        
        dockerfile_path = self.project_root / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        # docker-compose.yml
        compose_content = """version: '3.8'

services:
  akira:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - ./firebase-credentials.json:/app/firebase-credentials.json
    restart: unless-stopped
    
  # Optional: Add Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
    
  # Optional: Add PostgreSQL for data storage
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: akira
      POSTGRES_USER: akira
      POSTGRES_PASSWORD: akira_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
"""
        
        compose_path = self.project_root / "docker-compose.yml"
        with open(compose_path, 'w') as f:
            f.write(compose_content)
        
        print(f"✅ Dockerfile created: {dockerfile_path}")
        print(f"✅ docker-compose.yml created: {compose_path}")
        print("   To build: docker-compose build")
        print("   To run: docker-compose up -d")
        print()
    
    def create_requirements_file(self):
        """Crea archivo requirements.txt"""
        print("📋 Creating requirements.txt...")
        
        requirements = """# Akira SASE Cyberwar MVP Dependencies
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
requests>=2.31.0
python-nmap>=0.7.1
dnspython>=2.4.0
python-whois>=0.8.0
openai>=1.3.0
firebase-admin>=6.2.0
structlog>=23.2.0
colorama>=0.4.6
"""
        
        with open(self.requirements_file, 'w') as f:
            f.write(requirements)
        
        print(f"✅ Requirements file created: {self.requirements_file}")
        print()
    
    def run_tests(self):
        """Ejecuta tests básicos"""
        print("🧪 Running basic tests...")
        
        python_path = self.get_venv_python()
        
        # Test imports
        test_script = """
import sys
sys.path.append('.')

try:
    from core import get_logger, get_services, get_settings
    from models import ScanRequest, ScanResults
    from modules.offense.nmap_scanner import get_nmap_scanner
    from modules.defense.firewall_manager import get_firewall_manager
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
"""
        
        test_file = self.project_root / "test_imports.py"
        with open(test_file, 'w') as f:
            f.write(test_script)
        
        try:
            subprocess.run([str(python_path), str(test_file)], check=True)
            test_file.unlink()  # Remove test file
            print("✅ Basic tests passed")
        except subprocess.CalledProcessError:
            print("❌ Basic tests failed")
        
        print()
    
    def print_next_steps(self):
        """Imprime próximos pasos"""
        print("🎉 Deployment completed successfully!")
        print()
        print("📋 NEXT STEPS:")
        print("1. Configure your API keys in .env file:")
        print("   - Set your OpenAI API key")
        print("   - Set your Firebase project ID and credentials")
        print()
        print("2. Start the application:")
        if os.name == 'nt':
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("   python main.py")
        print()
        print("3. Access the API:")
        print("   - API: http://localhost:8000")
        print("   - Documentation: http://localhost:8000/docs")
        print("   - Health check: http://localhost:8000/ping")
        print()
        print("4. Run tests:")
        print("   python test_complete_api.py")
        print()
        print("🔐 SECURITY REMINDERS:")
        print("- Change the default API token in .env")
        print("- Use HTTPS in production")
        print("- Restrict API access to authorized IPs")
        print("- Regularly update dependencies")
        print()
        print("📚 DOCUMENTATION:")
        print("- README.md: Project overview")
        print("- ROADMAP.md: Development roadmap")
        print("- /docs: Interactive API documentation")
        print()
    
    def deploy(self):
        """Ejecuta despliegue completo"""
        try:
            self.print_banner()
            self.check_system_requirements()
            self.create_virtual_environment()
            self.install_dependencies()
            self.create_requirements_file()
            self.create_env_file()
            self.create_directory_structure()
            self.create_systemd_service()
            self.create_docker_files()
            self.run_tests()
            self.print_next_steps()
            
        except Exception as e:
            print(f"❌ Deployment failed: {str(e)}")
            sys.exit(1)

def main():
    """Función principal"""
    deployer = AkiraDeployer()
    deployer.deploy()

if __name__ == "__main__":
    main()