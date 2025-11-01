#!/usr/bin/env python3
"""
Script de inicio completo para Akira SASE Cyberwar MVP
Inicia backend y frontend automáticamente
"""

import subprocess
import threading
import time
import os
import sys
import webbrowser
from pathlib import Path

def print_banner():
    """Imprime banner de Akira"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🛡️⚔️  AKIRA SASE CYBERWAR MVP LAUNCHER  ⚔️🛡️           ║
║                                                              ║
║     Sistema Híbrido de Ciberseguridad Completo              ║
║     Backend + Frontend Integrados                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def start_backend():
    """Inicia el servidor backend"""
    print("🚀 Starting Akira Backend API...")
    try:
        # Cambiar al directorio raíz
        os.chdir(Path(__file__).parent)
        
        # Iniciar servidor FastAPI
        subprocess.run([
            sys.executable, "main.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\\n🛑 Backend stopped by user")
    except Exception as e:
        print(f"❌ Backend error: {str(e)}")

def start_frontend():
    """Inicia el servidor frontend"""
    print("🌐 Starting Akira Frontend...")
    try:
        # Cambiar al directorio frontend
        frontend_dir = Path(__file__).parent / "frontend"
        os.chdir(frontend_dir)
        
        # Iniciar servidor HTTP
        subprocess.run([
            sys.executable, "-m", "http.server", "3000", "--bind", "127.0.0.1"
        ], check=True)
    except KeyboardInterrupt:
        print("\\n🛑 Frontend stopped by user")
    except Exception as e:
        print(f"❌ Frontend error: {str(e)}")

def main():
    """Función principal"""
    print_banner()
    
    print("🔧 Initializing Akira SASE Cyberwar MVP...")
    print("📡 Backend API: http://localhost:8000")
    print("🌐 Frontend UI: http://localhost:3000")
    print("📚 API Docs: http://localhost:8000/docs")
    print()
    
    # Iniciar backend en thread separado
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Esperar un poco para que el backend inicie
    print("⏳ Waiting for backend to start...")
    time.sleep(3)
    
    # Iniciar frontend en thread separado
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    # Esperar un poco para que el frontend inicie
    print("⏳ Waiting for frontend to start...")
    time.sleep(2)
    
    # Abrir navegador automáticamente
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:3000")
    
    print("\\n✅ Akira SASE Cyberwar MVP is running!")
    print("🔗 Frontend: http://localhost:3000")
    print("🔗 Backend: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("\\n⚠️  Press Ctrl+C to stop all services")
    
    try:
        # Mantener el script corriendo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n🛑 Shutting down Akira SASE Cyberwar MVP...")
        print("✅ All services stopped")

if __name__ == "__main__":
    main()