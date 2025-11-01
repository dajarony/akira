#!/usr/bin/env python3
"""
Script de inicio integrado para Akira SASE Cyberwar MVP
Inicia backend y frontend automáticamente con integración real
"""

import subprocess
import threading
import time
import os
import sys
import webbrowser
import signal
from pathlib import Path

# Variables globales para procesos
backend_process = None
frontend_process = None

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
    global backend_process
    print("🚀 Starting Akira Backend API...")
    
    try:
        # Cambiar al directorio raíz
        project_root = Path(__file__).parent
        
        # Iniciar servidor FastAPI
        backend_process = subprocess.Popen([
            sys.executable, "main.py"
        ], cwd=project_root)
        
        return backend_process
        
    except Exception as e:
        print(f"❌ Backend error: {str(e)}")
        return None

def start_frontend():
    """Inicia el servidor frontend"""
    global frontend_process
    print("🌐 Starting Akira Frontend...")
    
    try:
        # Cambiar al directorio frontend
        frontend_dir = Path(__file__).parent / "frontend"
        
        # Iniciar servidor HTTP
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8080", "--bind", "127.0.0.1"
        ], cwd=frontend_dir)
        
        return frontend_process
        
    except Exception as e:
        print(f"❌ Frontend error: {str(e)}")
        return None

def wait_for_service(url, timeout=30):
    """Espera a que un servicio esté disponible"""
    import requests
    
    for i in range(timeout):
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def signal_handler(signum, frame):
    """Maneja señales de interrupción"""
    print("\n🛑 Shutting down Akira SASE Cyberwar MVP...")
    cleanup()
    sys.exit(0)

def cleanup():
    """Limpia procesos al salir"""
    global backend_process, frontend_process
    
    if backend_process:
        print("🔄 Stopping backend...")
        backend_process.terminate()
        backend_process.wait()
    
    if frontend_process:
        print("🔄 Stopping frontend...")
        frontend_process.terminate()
        frontend_process.wait()
    
    print("✅ All services stopped")

def main():
    """Función principal"""
    # Configurar manejo de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print_banner()
    
    print("🔧 Initializing Akira SASE Cyberwar MVP...")
    print("📡 Backend API: http://localhost:8000")
    print("🌐 Frontend UI: http://localhost:8080")
    print("📚 API Docs: http://localhost:8000/docs")
    print()
    
    # Verificar archivos necesarios
    if not Path("main.py").exists():
        print("❌ Error: main.py not found. Please run from project root.")
        sys.exit(1)
    
    if not Path("frontend/index.html").exists():
        print("❌ Error: frontend/index.html not found.")
        sys.exit(1)
    
    # Iniciar backend
    backend_proc = start_backend()
    if not backend_proc:
        print("❌ Failed to start backend")
        sys.exit(1)
    
    # Esperar a que el backend esté listo
    print("⏳ Waiting for backend to start...")
    if not wait_for_service("http://localhost:8000/ping"):
        print("❌ Backend failed to start within timeout")
        cleanup()
        sys.exit(1)
    
    print("✅ Backend started successfully")
    
    # Iniciar frontend
    frontend_proc = start_frontend()
    if not frontend_proc:
        print("❌ Failed to start frontend")
        cleanup()
        sys.exit(1)
    
    # Esperar a que el frontend esté listo
    print("⏳ Waiting for frontend to start...")
    if not wait_for_service("http://localhost:8080"):
        print("❌ Frontend failed to start within timeout")
        cleanup()
        sys.exit(1)
    
    print("✅ Frontend started successfully")
    
    # Abrir navegador automáticamente
    print("🌐 Opening browser...")
    time.sleep(2)
    webbrowser.open("http://localhost:8080")
    
    print("\n" + "="*60)
    print("🎉 AKIRA SASE CYBERWAR MVP IS RUNNING!")
    print("="*60)
    print("🔗 Frontend: http://localhost:8080")
    print("🔗 Backend: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("💚 Health Check: http://localhost:8000/ping")
    print("="*60)
    print("🛑 Press Ctrl+C to stop all services")
    print("="*60)
    
    try:
        # Mantener el script corriendo
        while True:
            # Verificar que los procesos sigan vivos
            if backend_proc.poll() is not None:
                print("❌ Backend process died")
                break
            if frontend_proc.poll() is not None:
                print("❌ Frontend process died")
                break
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        pass
    
    finally:
        cleanup()

if __name__ == "__main__":
    main()