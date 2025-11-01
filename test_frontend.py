#!/usr/bin/env python3
"""
Script para probar el frontend de Akira
Inicia el servidor HTTP para el frontend
"""

import http.server
import socketserver
import os
import webbrowser
import time
from threading import Thread

# Configuración
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')
PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def end_headers(self):
        # Agregar headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Log personalizado
        print(f"📡 {args[0]} - {args[1]}")

def open_browser():
    """Abre el navegador después de un pequeño delay"""
    time.sleep(2)
    url = f"http://localhost:{PORT}"
    print(f"\n🌐 Abriendo navegador en {url}...")
    webbrowser.open(url)

def main():
    print("=" * 60)
    print("🛡️⚔️  AKIRA SASE CYBERWAR MVP - FRONTEND TEST")
    print("=" * 60)
    print()
    print(f"📁 Directorio frontend: {FRONTEND_DIR}")
    print(f"🌐 Puerto: {PORT}")
    print()

    # Verificar que el directorio existe
    if not os.path.exists(FRONTEND_DIR):
        print(f"❌ Error: Directorio frontend no encontrado: {FRONTEND_DIR}")
        return

    # Verificar archivos principales
    files = ['index.html', 'styles.css', 'script.js']
    for file in files:
        filepath = os.path.join(FRONTEND_DIR, file)
        if os.path.exists(filepath):
            print(f"✅ {file} encontrado")
        else:
            print(f"❌ {file} NO encontrado")

    print()
    print("⚠️  NOTA: El backend NO está corriendo.")
    print("   El frontend funcionará en MODO SIMULACIÓN.")
    print("   Para funcionalidad completa, ejecuta:")
    print("   python main.py")
    print()
    print("=" * 60)
    print()

    # Abrir navegador en un thread separado
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Iniciar servidor
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Servidor frontend iniciado en http://localhost:{PORT}")
        print()
        print("📊 Funcionalidades disponibles en modo simulación:")
        print("   ✅ Dashboard con métricas simuladas")
        print("   ✅ Interfaz Red Team (Nmap, OSINT, Exploits)")
        print("   ✅ Interfaz Blue Team (Firewall, Honeypots, AI)")
        print("   ✅ Logs del sistema")
        print("   ⚠️  Las llamadas API fallarán pero mostrarán datos simulados")
        print()
        print("🛑 Presiona Ctrl+C para detener el servidor")
        print("=" * 60)
        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Deteniendo servidor...")
            print("✅ Servidor detenido correctamente")
            print("\n👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()
