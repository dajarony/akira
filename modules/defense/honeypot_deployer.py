# modules/defense/honeypot_deployer.py

"""
SUME DOCBLOCK

Nombre: Desplegador de Honeypots Akira
Tipo: Herramienta

Entradas:
- Configuración de honeypots (SSH, HTTP, FTP)
- Puertos y servicios a simular
- Políticas de respuesta a atacantes

Acciones:
- Despliega honeypots simulados
- Detecta intentos de ataque
- Registra actividad maliciosa
- Integra con sistema de bloqueo

Salidas:
- Estado de honeypots activos
- Logs de intentos de ataque
- Credenciales capturadas
- Alertas de seguridad
"""

import asyncio
import socket
import threading
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from core import get_logger, get_services
from models import HoneypotInfo, AttackingIP, SeverityLevel, ToolStatus
from modules.shared import get_akira_utils, get_security_utils, get_network_utils
from modules.defense.firewall_manager import get_firewall_manager
from core.exceptions import AkiraOperationError, AkiraSecurityError

class HoneypotDeployer:
    """Desplegador de honeypots inteligentes para detección de atacantes"""
    
    def __init__(self):
        self.logger = get_logger()
        self.services = get_services()
        self.akira_utils = get_akira_utils()
        self.security_utils = get_security_utils()
        self.network_utils = get_network_utils()
        self.firewall_manager = get_firewall_manager()
        
        # Honeypots activos
        self.active_honeypots: Dict[str, HoneypotInfo] = {}
        self.honeypot_servers: Dict[str, Any] = {}
        
        # Configuración
        self.max_honeypots = 10
        self.auto_block_attackers = True
        
    async def deploy_ssh_honeypot(self, port: int = 2222, interface: str = "0.0.0.0") -> Dict[str, Any]:
        """Despliega honeypot SSH"""
        try:
            honeypot_id = f"ssh_{port}_{uuid.uuid4().hex[:8]}"
            
            # Validar puerto
            if not self._is_port_available(port, interface):
                raise AkiraOperationError(f"Port {port} is already in use")
            
            # Crear información del honeypot
            honeypot_info = HoneypotInfo(
                honeypot_id=honeypot_id,
                honeypot_name=f"SSH Honeypot on port {port}",
                honeypot_type="ssh",
                port=port,
                interface=interface,
                status=ToolStatus.ACTIVE
            )
            
            # Iniciar servidor SSH honeypot
            server_task = asyncio.create_task(
                self._run_ssh_honeypot(honeypot_info)
            )
            
            # Registrar honeypot
            self.active_honeypots[honeypot_id] = honeypot_info
            self.honeypot_servers[honeypot_id] = server_task
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="honeypot_deployed",
                details={
                    "honeypot_id": honeypot_id,
                    "type": "ssh",
                    "port": port,
                    "interface": interface
                },
                save_to_firebase=True
            )
            
            self.logger.info(f"SSH honeypot deployed: {honeypot_info.honeypot_name}")
            
            return {
                "success": True,
                "message": f"SSH honeypot deployed on port {port}",
                "honeypot_id": honeypot_id,
                "honeypot_info": honeypot_info.dict()
            }
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "operation": "deploy_ssh_honeypot",
                    "port": port,
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            raise AkiraOperationError(f"Failed to deploy SSH honeypot: {str(e)}")
    
    async def deploy_http_honeypot(self, port: int = 8080, interface: str = "0.0.0.0") -> Dict[str, Any]:
        """Despliega honeypot HTTP"""
        try:
            honeypot_id = f"http_{port}_{uuid.uuid4().hex[:8]}"
            
            # Validar puerto
            if not self._is_port_available(port, interface):
                raise AkiraOperationError(f"Port {port} is already in use")
            
            # Crear información del honeypot
            honeypot_info = HoneypotInfo(
                honeypot_id=honeypot_id,
                honeypot_name=f"HTTP Honeypot on port {port}",
                honeypot_type="http",
                port=port,
                interface=interface,
                status=ToolStatus.ACTIVE
            )
            
            # Iniciar servidor HTTP honeypot
            server_task = asyncio.create_task(
                self._run_http_honeypot(honeypot_info)
            )
            
            # Registrar honeypot
            self.active_honeypots[honeypot_id] = honeypot_info
            self.honeypot_servers[honeypot_id] = server_task
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="honeypot_deployed",
                details={
                    "honeypot_id": honeypot_id,
                    "type": "http",
                    "port": port,
                    "interface": interface
                },
                save_to_firebase=True
            )
            
            self.logger.info(f"HTTP honeypot deployed: {honeypot_info.honeypot_name}")
            
            return {
                "success": True,
                "message": f"HTTP honeypot deployed on port {port}",
                "honeypot_id": honeypot_id,
                "honeypot_info": honeypot_info.dict()
            }
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "operation": "deploy_http_honeypot",
                    "port": port,
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            raise AkiraOperationError(f"Failed to deploy HTTP honeypot: {str(e)}")
    
    async def deploy_ftp_honeypot(self, port: int = 2121, interface: str = "0.0.0.0") -> Dict[str, Any]:
        """Despliega honeypot FTP"""
        try:
            honeypot_id = f"ftp_{port}_{uuid.uuid4().hex[:8]}"
            
            # Validar puerto
            if not self._is_port_available(port, interface):
                raise AkiraOperationError(f"Port {port} is already in use")
            
            # Crear información del honeypot
            honeypot_info = HoneypotInfo(
                honeypot_id=honeypot_id,
                honeypot_name=f"FTP Honeypot on port {port}",
                honeypot_type="ftp",
                port=port,
                interface=interface,
                status=ToolStatus.ACTIVE
            )
            
            # Iniciar servidor FTP honeypot
            server_task = asyncio.create_task(
                self._run_ftp_honeypot(honeypot_info)
            )
            
            # Registrar honeypot
            self.active_honeypots[honeypot_id] = honeypot_info
            self.honeypot_servers[honeypot_id] = server_task
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="honeypot_deployed",
                details={
                    "honeypot_id": honeypot_id,
                    "type": "ftp",
                    "port": port,
                    "interface": interface
                },
                save_to_firebase=True
            )
            
            self.logger.info(f"FTP honeypot deployed: {honeypot_info.honeypot_name}")
            
            return {
                "success": True,
                "message": f"FTP honeypot deployed on port {port}",
                "honeypot_id": honeypot_id,
                "honeypot_info": honeypot_info.dict()
            }
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "operation": "deploy_ftp_honeypot",
                    "port": port,
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            raise AkiraOperationError(f"Failed to deploy FTP honeypot: {str(e)}")
    
    async def stop_honeypot(self, honeypot_id: str) -> Dict[str, Any]:
        """Detiene un honeypot"""
        try:
            if honeypot_id not in self.active_honeypots:
                raise AkiraOperationError(f"Honeypot not found: {honeypot_id}")
            
            honeypot_info = self.active_honeypots[honeypot_id]
            
            # Detener servidor
            if honeypot_id in self.honeypot_servers:
                server_task = self.honeypot_servers[honeypot_id]
                server_task.cancel()
                del self.honeypot_servers[honeypot_id]
            
            # Actualizar estado
            honeypot_info.status = ToolStatus.INACTIVE
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="honeypot_stopped",
                details={
                    "honeypot_id": honeypot_id,
                    "type": honeypot_info.honeypot_type,
                    "connections_received": honeypot_info.connections_received,
                    "credentials_captured": honeypot_info.credentials_captured
                },
                save_to_firebase=True
            )
            
            self.logger.info(f"Honeypot stopped: {honeypot_info.honeypot_name}")
            
            return {
                "success": True,
                "message": f"Honeypot {honeypot_info.honeypot_name} stopped successfully",
                "final_stats": {
                    "connections_received": honeypot_info.connections_received,
                    "credentials_captured": honeypot_info.credentials_captured
                }
            }
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "operation": "stop_honeypot",
                    "honeypot_id": honeypot_id,
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            raise AkiraOperationError(f"Failed to stop honeypot: {str(e)}")
    
    async def get_honeypot_status(self) -> Dict[str, Any]:
        """Obtiene estado de todos los honeypots"""
        try:
            active_count = len([h for h in self.active_honeypots.values() if h.status == ToolStatus.ACTIVE])
            total_connections = sum(h.connections_received for h in self.active_honeypots.values())
            total_credentials = sum(h.credentials_captured for h in self.active_honeypots.values())
            
            # Estadísticas por tipo
            stats_by_type = {}
            for honeypot in self.active_honeypots.values():
                if honeypot.honeypot_type not in stats_by_type:
                    stats_by_type[honeypot.honeypot_type] = {
                        "count": 0,
                        "connections": 0,
                        "credentials": 0
                    }
                
                stats_by_type[honeypot.honeypot_type]["count"] += 1
                stats_by_type[honeypot.honeypot_type]["connections"] += honeypot.connections_received
                stats_by_type[honeypot.honeypot_type]["credentials"] += honeypot.credentials_captured
            
            return {
                "success": True,
                "honeypot_status": {
                    "total_honeypots": len(self.active_honeypots),
                    "active_honeypots": active_count,
                    "total_connections_received": total_connections,
                    "total_credentials_captured": total_credentials,
                    "max_honeypots": self.max_honeypots,
                    "auto_block_attackers": self.auto_block_attackers
                },
                "stats_by_type": stats_by_type,
                "active_honeypots": [h.dict() for h in self.active_honeypots.values()],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise AkiraOperationError(f"Failed to get honeypot status: {str(e)}")
    
    def _is_port_available(self, port: int, interface: str) -> bool:
        """Verifica si un puerto está disponible"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            result = sock.bind((interface, port))
            sock.close()
            return True
        except:
            return False  
  
    async def _run_ssh_honeypot(self, honeypot_info: HoneypotInfo):
        """Ejecuta honeypot SSH"""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((honeypot_info.interface, honeypot_info.port))
            server_socket.listen(5)
            server_socket.settimeout(1.0)  # Timeout para permitir cancelación
            
            self.logger.info(f"SSH honeypot listening on {honeypot_info.interface}:{honeypot_info.port}")
            
            while honeypot_info.status == ToolStatus.ACTIVE:
                try:
                    client_socket, client_address = server_socket.accept()
                    
                    # Registrar conexión
                    honeypot_info.connections_received += 1
                    honeypot_info.last_activity = datetime.utcnow()
                    
                    # Procesar conexión SSH en background
                    asyncio.create_task(
                        self._handle_ssh_connection(client_socket, client_address, honeypot_info)
                    )
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if honeypot_info.status == ToolStatus.ACTIVE:
                        self.logger.error(f"SSH honeypot error: {str(e)}")
                    break
            
            server_socket.close()
            
        except Exception as e:
            self.logger.error(f"SSH honeypot failed: {str(e)}")
            honeypot_info.status = ToolStatus.ERROR
    
    async def _handle_ssh_connection(self, client_socket, client_address, honeypot_info: HoneypotInfo):
        """Maneja conexión SSH"""
        try:
            client_ip = client_address[0]
            
            # Log del intento de conexión
            await self.logger.log_activity(
                activity_type="honeypot_connection",
                details={
                    "honeypot_id": honeypot_info.honeypot_id,
                    "type": "ssh",
                    "client_ip": client_ip,
                    "client_port": client_address[1]
                },
                save_to_firebase=True
            )
            
            # Simular banner SSH
            banner = b"SSH-2.0-OpenSSH_7.4\r\n"
            client_socket.send(banner)
            
            # Leer datos del cliente
            try:
                data = client_socket.recv(1024)
                if data:
                    # Simular intercambio de claves
                    client_socket.send(b"Protocol mismatch.\r\n")
                    
                    # Si parece un intento de autenticación, registrar credenciales
                    if b"ssh-userauth" in data or b"password" in data:
                        honeypot_info.credentials_captured += 1
                        
                        await self.logger.log_activity(
                            activity_type="credentials_captured",
                            details={
                                "honeypot_id": honeypot_info.honeypot_id,
                                "type": "ssh",
                                "client_ip": client_ip,
                                "data_length": len(data)
                            },
                            save_to_firebase=True
                        )
            except:
                pass
            
            # Bloquear IP atacante si está habilitado
            if self.auto_block_attackers:
                await self._block_attacker_ip(client_ip, "SSH honeypot interaction")
            
        except Exception as e:
            self.logger.error(f"Error handling SSH connection: {str(e)}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    async def _run_http_honeypot(self, honeypot_info: HoneypotInfo):
        """Ejecuta honeypot HTTP"""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((honeypot_info.interface, honeypot_info.port))
            server_socket.listen(5)
            server_socket.settimeout(1.0)
            
            self.logger.info(f"HTTP honeypot listening on {honeypot_info.interface}:{honeypot_info.port}")
            
            while honeypot_info.status == ToolStatus.ACTIVE:
                try:
                    client_socket, client_address = server_socket.accept()
                    
                    # Registrar conexión
                    honeypot_info.connections_received += 1
                    honeypot_info.last_activity = datetime.utcnow()
                    
                    # Procesar conexión HTTP en background
                    asyncio.create_task(
                        self._handle_http_connection(client_socket, client_address, honeypot_info)
                    )
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if honeypot_info.status == ToolStatus.ACTIVE:
                        self.logger.error(f"HTTP honeypot error: {str(e)}")
                    break
            
            server_socket.close()
            
        except Exception as e:
            self.logger.error(f"HTTP honeypot failed: {str(e)}")
            honeypot_info.status = ToolStatus.ERROR
    
    async def _handle_http_connection(self, client_socket, client_address, honeypot_info: HoneypotInfo):
        """Maneja conexión HTTP"""
        try:
            client_ip = client_address[0]
            
            # Log del intento de conexión
            await self.logger.log_activity(
                activity_type="honeypot_connection",
                details={
                    "honeypot_id": honeypot_info.honeypot_id,
                    "type": "http",
                    "client_ip": client_ip,
                    "client_port": client_address[1]
                },
                save_to_firebase=True
            )
            
            # Leer request HTTP
            try:
                data = client_socket.recv(4096).decode('utf-8', errors='ignore')
                
                if data:
                    # Analizar request
                    lines = data.split('\n')
                    if lines:
                        request_line = lines[0]
                        
                        # Buscar patrones maliciosos
                        malicious_patterns = [
                            '/admin', '/wp-admin', '/phpmyadmin', '/.env',
                            '/config', '/backup', '/shell', '/cmd',
                            'SELECT', 'UNION', '<script>', 'javascript:'
                        ]
                        
                        is_malicious = any(pattern.lower() in data.lower() for pattern in malicious_patterns)
                        
                        if is_malicious:
                            honeypot_info.credentials_captured += 1
                            
                            await self.logger.log_activity(
                                activity_type="malicious_http_request",
                                details={
                                    "honeypot_id": honeypot_info.honeypot_id,
                                    "client_ip": client_ip,
                                    "request_line": request_line,
                                    "full_request": data[:500]  # Primeros 500 chars
                                },
                                save_to_firebase=True
                            )
                    
                    # Responder con página falsa
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        "Content-Length: 200\r\n"
                        "\r\n"
                        "<html><head><title>Server Status</title></head>"
                        "<body><h1>System Online</h1>"
                        "<p>Server is running normally.</p>"
                        "<form><input type='password' placeholder='Admin Password'></form>"
                        "</body></html>"
                    )
                    
                    client_socket.send(response.encode())
            except:
                pass
            
            # Bloquear IP atacante si está habilitado
            if self.auto_block_attackers:
                await self._block_attacker_ip(client_ip, "HTTP honeypot interaction")
            
        except Exception as e:
            self.logger.error(f"Error handling HTTP connection: {str(e)}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    async def _run_ftp_honeypot(self, honeypot_info: HoneypotInfo):
        """Ejecuta honeypot FTP"""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((honeypot_info.interface, honeypot_info.port))
            server_socket.listen(5)
            server_socket.settimeout(1.0)
            
            self.logger.info(f"FTP honeypot listening on {honeypot_info.interface}:{honeypot_info.port}")
            
            while honeypot_info.status == ToolStatus.ACTIVE:
                try:
                    client_socket, client_address = server_socket.accept()
                    
                    # Registrar conexión
                    honeypot_info.connections_received += 1
                    honeypot_info.last_activity = datetime.utcnow()
                    
                    # Procesar conexión FTP en background
                    asyncio.create_task(
                        self._handle_ftp_connection(client_socket, client_address, honeypot_info)
                    )
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if honeypot_info.status == ToolStatus.ACTIVE:
                        self.logger.error(f"FTP honeypot error: {str(e)}")
                    break
            
            server_socket.close()
            
        except Exception as e:
            self.logger.error(f"FTP honeypot failed: {str(e)}")
            honeypot_info.status = ToolStatus.ERROR
    
    async def _handle_ftp_connection(self, client_socket, client_address, honeypot_info: HoneypotInfo):
        """Maneja conexión FTP"""
        try:
            client_ip = client_address[0]
            
            # Log del intento de conexión
            await self.logger.log_activity(
                activity_type="honeypot_connection",
                details={
                    "honeypot_id": honeypot_info.honeypot_id,
                    "type": "ftp",
                    "client_ip": client_ip,
                    "client_port": client_address[1]
                },
                save_to_firebase=True
            )
            
            # Enviar banner FTP
            client_socket.send(b"220 FTP Server Ready\r\n")
            
            # Manejar comandos FTP
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    command = data.decode('utf-8', errors='ignore').strip().upper()
                    
                    if command.startswith('USER'):
                        client_socket.send(b"331 Password required\r\n")
                    elif command.startswith('PASS'):
                        honeypot_info.credentials_captured += 1
                        
                        await self.logger.log_activity(
                            activity_type="ftp_credentials_captured",
                            details={
                                "honeypot_id": honeypot_info.honeypot_id,
                                "client_ip": client_ip,
                                "command": command[:50]  # Primeros 50 chars
                            },
                            save_to_firebase=True
                        )
                        
                        client_socket.send(b"530 Login incorrect\r\n")
                    elif command.startswith('QUIT'):
                        client_socket.send(b"221 Goodbye\r\n")
                        break
                    else:
                        client_socket.send(b"500 Unknown command\r\n")
            except:
                pass
            
            # Bloquear IP atacante si está habilitado
            if self.auto_block_attackers:
                await self._block_attacker_ip(client_ip, "FTP honeypot interaction")
            
        except Exception as e:
            self.logger.error(f"Error handling FTP connection: {str(e)}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    async def _block_attacker_ip(self, ip_address: str, reason: str):
        """Bloquea IP atacante automáticamente"""
        try:
            await self.firewall_manager.block_malicious_ip(
                ip_address=ip_address,
                threat_level=SeverityLevel.HIGH,
                duration_hours=24
            )
            
            self.logger.warning(f"Attacker IP blocked automatically: {ip_address} (reason: {reason})")
            
        except Exception as e:
            self.logger.error(f"Failed to block attacker IP {ip_address}: {str(e)}")
    
    def list_active_honeypots(self) -> List[Dict[str, Any]]:
        """Lista honeypots activos"""
        return [h.dict() for h in self.active_honeypots.values() if h.status == ToolStatus.ACTIVE]
    
    async def stop_all_honeypots(self) -> Dict[str, Any]:
        """Detiene todos los honeypots"""
        try:
            stopped_count = 0
            failed_count = 0
            
            for honeypot_id in list(self.active_honeypots.keys()):
                try:
                    await self.stop_honeypot(honeypot_id)
                    stopped_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to stop honeypot {honeypot_id}: {str(e)}")
                    failed_count += 1
            
            return {
                "success": True,
                "message": f"Stopped {stopped_count} honeypots, {failed_count} failed",
                "stopped_count": stopped_count,
                "failed_count": failed_count
            }
            
        except Exception as e:
            raise AkiraOperationError(f"Failed to stop all honeypots: {str(e)}")

# Instancia global del desplegador de honeypots
honeypot_deployer = HoneypotDeployer()

def get_honeypot_deployer() -> HoneypotDeployer:
    """Obtiene la instancia del desplegador de honeypots"""
    return honeypot_deployer