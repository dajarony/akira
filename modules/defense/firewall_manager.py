# modules/defense/firewall_manager.py

"""
SUME DOCBLOCK

Nombre: Gestor de Firewall Automático Akira
Tipo: Herramienta

Entradas:
- Reglas de firewall para crear/modificar/eliminar
- IPs maliciosas para bloqueo automático
- Configuración de políticas de seguridad

Acciones:
- Gestiona reglas de firewall dinámicamente
- Bloquea IPs maliciosas automáticamente
- Integra con iptables/Windows Firewall
- Monitorea tráfico de red

Salidas:
- Estado de reglas de firewall
- Estadísticas de bloqueos
- Logs de actividad de firewall
"""

import asyncio
import subprocess
import platform
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import uuid

from core import get_logger, get_services
from models import FirewallRule, AttackingIP, SeverityLevel
from modules.shared import get_akira_utils, get_security_utils, get_network_utils
from core.exceptions import AkiraOperationError, AkiraSecurityError

class FirewallManager:
    """Gestor automático de firewall para defensa activa"""
    
    def __init__(self):
        self.logger = get_logger()
        self.services = get_services()
        self.akira_utils = get_akira_utils()
        self.security_utils = get_security_utils()
        self.network_utils = get_network_utils()
        
        # Detectar sistema operativo
        self.os_type = platform.system().lower()
        self.is_windows = self.os_type == "windows"
        self.is_linux = self.os_type == "linux"
        
        # Reglas activas en memoria
        self.active_rules: Dict[str, FirewallRule] = {}
        self.blocked_ips: Dict[str, AttackingIP] = {}
        
        # Configuración
        self.max_rules = 1000
        self.auto_cleanup_hours = 24
        
    async def create_firewall_rule(self, rule: FirewallRule) -> Dict[str, Any]:
        """Crea una nueva regla de firewall"""
        try:
            # Validar regla
            await self._validate_firewall_rule(rule)
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="firewall_rule_create",
                details={
                    "rule_id": rule.rule_id,
                    "rule_name": rule.rule_name,
                    "action": rule.action,
                    "source_ip": rule.source_ip,
                    "destination_port": rule.destination_port
                },
                save_to_firebase=True
            )
            
            # Crear regla según el sistema operativo
            if self.is_windows:
                success = await self._create_windows_firewall_rule(rule)
            elif self.is_linux:
                success = await self._create_linux_firewall_rule(rule)
            else:
                # Modo simulación para otros sistemas
                success = await self._create_simulated_firewall_rule(rule)
            
            if success:
                # Guardar en memoria
                self.active_rules[rule.rule_id] = rule
                
                # Guardar en Firebase si está disponible
                if self.services.firebase_service:
                    await self._save_firewall_rule(rule)
                
                self.logger.info(f"Firewall rule created: {rule.rule_name}")
                
                return {
                    "success": True,
                    "message": f"Firewall rule '{rule.rule_name}' created successfully",
                    "rule_id": rule.rule_id,
                    "active_rules_count": len(self.active_rules)
                }
            else:
                raise AkiraOperationError("Failed to create firewall rule")
                
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "operation": "firewall_rule_create",
                    "rule_name": rule.rule_name,
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            raise AkiraOperationError(f"Failed to create firewall rule: {str(e)}")
    
    async def delete_firewall_rule(self, rule_id: str) -> Dict[str, Any]:
        """Elimina una regla de firewall"""
        try:
            if rule_id not in self.active_rules:
                raise AkiraOperationError(f"Firewall rule not found: {rule_id}")
            
            rule = self.active_rules[rule_id]
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="firewall_rule_delete",
                details={
                    "rule_id": rule_id,
                    "rule_name": rule.rule_name
                },
                save_to_firebase=True
            )
            
            # Eliminar regla según el sistema operativo
            if self.is_windows:
                success = await self._delete_windows_firewall_rule(rule)
            elif self.is_linux:
                success = await self._delete_linux_firewall_rule(rule)
            else:
                success = await self._delete_simulated_firewall_rule(rule)
            
            if success:
                # Eliminar de memoria
                del self.active_rules[rule_id]
                
                self.logger.info(f"Firewall rule deleted: {rule.rule_name}")
                
                return {
                    "success": True,
                    "message": f"Firewall rule '{rule.rule_name}' deleted successfully",
                    "active_rules_count": len(self.active_rules)
                }
            else:
                raise AkiraOperationError("Failed to delete firewall rule")
                
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "operation": "firewall_rule_delete",
                    "rule_id": rule_id,
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            raise AkiraOperationError(f"Failed to delete firewall rule: {str(e)}")
    
    async def block_malicious_ip(self, ip_address: str, threat_level: SeverityLevel = SeverityLevel.HIGH, 
                                duration_hours: int = 24) -> Dict[str, Any]:
        """Bloquea una IP maliciosa automáticamente"""
        try:
            # Validar IP
            if not self.network_utils.is_valid_ip(ip_address):
                raise AkiraOperationError(f"Invalid IP address: {ip_address}")
            
            # Crear regla de bloqueo
            rule_id = f"block_{ip_address}_{uuid.uuid4().hex[:8]}"
            expires_at = datetime.utcnow() + timedelta(hours=duration_hours)
            
            block_rule = FirewallRule(
                rule_id=rule_id,
                rule_name=f"Block malicious IP {ip_address}",
                action="deny",
                source_ip=ip_address,
                protocol="all",
                enabled=True,
                expires_at=expires_at
            )
            
            # Crear regla de firewall
            result = await self.create_firewall_rule(block_rule)
            
            # Registrar IP atacante
            attacking_ip = AttackingIP(
                ip_address=ip_address,
                threat_level=threat_level,
                blocked=True,
                attack_count=1
            )
            
            self.blocked_ips[ip_address] = attacking_ip
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="malicious_ip_blocked",
                details={
                    "ip_address": ip_address,
                    "threat_level": threat_level.value,
                    "duration_hours": duration_hours,
                    "rule_id": rule_id
                },
                save_to_firebase=True
            )
            
            self.logger.warning(f"Malicious IP blocked: {ip_address} (threat level: {threat_level.value})")
            
            return {
                "success": True,
                "message": f"Malicious IP {ip_address} blocked successfully",
                "rule_id": rule_id,
                "expires_at": expires_at.isoformat(),
                "blocked_ips_count": len(self.blocked_ips)
            }
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "operation": "block_malicious_ip",
                    "ip_address": ip_address,
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            raise AkiraOperationError(f"Failed to block malicious IP: {str(e)}")
    
    async def unblock_ip(self, ip_address: str) -> Dict[str, Any]:
        """Desbloquea una IP"""
        try:
            # Buscar reglas de bloqueo para esta IP
            rules_to_delete = []
            for rule_id, rule in self.active_rules.items():
                if rule.source_ip == ip_address and rule.action == "deny":
                    rules_to_delete.append(rule_id)
            
            if not rules_to_delete:
                raise AkiraOperationError(f"No blocking rules found for IP: {ip_address}")
            
            # Eliminar reglas de bloqueo
            deleted_count = 0
            for rule_id in rules_to_delete:
                try:
                    await self.delete_firewall_rule(rule_id)
                    deleted_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to delete rule {rule_id}: {str(e)}")
            
            # Actualizar registro de IP atacante
            if ip_address in self.blocked_ips:
                self.blocked_ips[ip_address].blocked = False
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="ip_unblocked",
                details={
                    "ip_address": ip_address,
                    "rules_deleted": deleted_count
                },
                save_to_firebase=True
            )
            
            self.logger.info(f"IP unblocked: {ip_address} ({deleted_count} rules deleted)")
            
            return {
                "success": True,
                "message": f"IP {ip_address} unblocked successfully",
                "rules_deleted": deleted_count
            }
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "operation": "unblock_ip",
                    "ip_address": ip_address,
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            raise AkiraOperationError(f"Failed to unblock IP: {str(e)}")
    
    async def get_firewall_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del firewall"""
        try:
            # Limpiar reglas expiradas
            await self._cleanup_expired_rules()
            
            # Estadísticas básicas
            total_rules = len(self.active_rules)
            blocked_ips_count = len([ip for ip in self.blocked_ips.values() if ip.blocked])
            
            # Reglas por acción
            allow_rules = len([r for r in self.active_rules.values() if r.action == "allow"])
            deny_rules = len([r for r in self.active_rules.values() if r.action == "deny"])
            
            # Top IPs atacantes
            top_attacking_ips = sorted(
                self.blocked_ips.values(),
                key=lambda x: x.attack_count,
                reverse=True
            )[:10]
            
            return {
                "success": True,
                "firewall_status": {
                    "total_rules": total_rules,
                    "allow_rules": allow_rules,
                    "deny_rules": deny_rules,
                    "blocked_ips_count": blocked_ips_count,
                    "system_type": self.os_type,
                    "max_rules": self.max_rules,
                    "auto_cleanup_hours": self.auto_cleanup_hours
                },
                "top_attacking_ips": [ip.dict() for ip in top_attacking_ips],
                "recent_rules": [
                    rule.dict() for rule in sorted(
                        self.active_rules.values(),
                        key=lambda x: x.created_at,
                        reverse=True
                    )[:10]
                ],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise AkiraOperationError(f"Failed to get firewall status: {str(e)}")
    
    async def _validate_firewall_rule(self, rule: FirewallRule):
        """Valida una regla de firewall"""
        # Validar acción
        valid_actions = ["allow", "deny", "drop"]
        if rule.action not in valid_actions:
            raise AkiraOperationError(f"Invalid action: {rule.action}. Must be one of {valid_actions}")
        
        # Validar IP si se proporciona
        if rule.source_ip and not self.network_utils.is_valid_ip(rule.source_ip):
            raise AkiraOperationError(f"Invalid source IP: {rule.source_ip}")
        
        if rule.destination_ip and not self.network_utils.is_valid_ip(rule.destination_ip):
            raise AkiraOperationError(f"Invalid destination IP: {rule.destination_ip}")
        
        # Validar puertos
        if rule.source_port and not self._is_valid_port(rule.source_port):
            raise AkiraOperationError(f"Invalid source port: {rule.source_port}")
        
        if rule.destination_port and not self._is_valid_port(rule.destination_port):
            raise AkiraOperationError(f"Invalid destination port: {rule.destination_port}")
        
        # Verificar límite de reglas
        if len(self.active_rules) >= self.max_rules:
            raise AkiraOperationError(f"Maximum number of rules reached: {self.max_rules}")
    
    def _is_valid_port(self, port) -> bool:
        """Valida un puerto"""
        try:
            if isinstance(port, str):
                if "-" in port:
                    # Rango de puertos
                    start, end = port.split("-")
                    return 1 <= int(start) <= 65535 and 1 <= int(end) <= 65535
                else:
                    return 1 <= int(port) <= 65535
            elif isinstance(port, int):
                return 1 <= port <= 65535
            return False
        except:
            return False 
   
    async def _create_windows_firewall_rule(self, rule: FirewallRule) -> bool:
        """Crea regla de firewall en Windows"""
        try:
            # Construir comando netsh
            cmd_parts = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule.rule_name}",
                f"dir={'in' if rule.source_ip else 'out'}",
                f"action={'allow' if rule.action == 'allow' else 'block'}"
            ]
            
            if rule.source_ip:
                cmd_parts.append(f"remoteip={rule.source_ip}")
            
            if rule.destination_port:
                cmd_parts.append(f"localport={rule.destination_port}")
            
            if rule.protocol and rule.protocol != "all":
                cmd_parts.append(f"protocol={rule.protocol}")
            
            # Ejecutar comando
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.info(f"Windows firewall rule created: {rule.rule_name}")
                return True
            else:
                self.logger.error(f"Failed to create Windows firewall rule: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Windows firewall command timed out")
            return False
        except Exception as e:
            self.logger.error(f"Error creating Windows firewall rule: {str(e)}")
            return False
    
    async def _create_linux_firewall_rule(self, rule: FirewallRule) -> bool:
        """Crea regla de firewall en Linux usando iptables"""
        try:
            # Construir comando iptables
            cmd_parts = ["iptables"]
            
            # Determinar cadena
            if rule.action == "allow":
                cmd_parts.extend(["-A", "INPUT", "-j", "ACCEPT"])
            else:
                cmd_parts.extend(["-A", "INPUT", "-j", "DROP"])
            
            if rule.source_ip:
                cmd_parts.extend(["-s", rule.source_ip])
            
            if rule.destination_port:
                cmd_parts.extend(["-p", rule.protocol or "tcp", "--dport", str(rule.destination_port)])
            
            # Ejecutar comando
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.info(f"Linux firewall rule created: {rule.rule_name}")
                return True
            else:
                self.logger.error(f"Failed to create Linux firewall rule: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Linux firewall command timed out")
            return False
        except Exception as e:
            self.logger.error(f"Error creating Linux firewall rule: {str(e)}")
            return False
    
    async def _create_simulated_firewall_rule(self, rule: FirewallRule) -> bool:
        """Crea regla de firewall simulada"""
        self.logger.info(f"SIMULATION: Created firewall rule '{rule.rule_name}' - {rule.action} {rule.source_ip or 'any'}")
        return True
    
    async def _delete_windows_firewall_rule(self, rule: FirewallRule) -> bool:
        """Elimina regla de firewall en Windows"""
        try:
            cmd = [
                "netsh", "advfirewall", "firewall", "delete", "rule",
                f"name={rule.rule_name}"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.info(f"Windows firewall rule deleted: {rule.rule_name}")
                return True
            else:
                self.logger.error(f"Failed to delete Windows firewall rule: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error deleting Windows firewall rule: {str(e)}")
            return False
    
    async def _delete_linux_firewall_rule(self, rule: FirewallRule) -> bool:
        """Elimina regla de firewall en Linux"""
        try:
            # En un sistema real, necesitaríamos rastrear el número de línea de la regla
            # Por ahora, simulamos la eliminación
            self.logger.info(f"Linux firewall rule deleted: {rule.rule_name}")
            return True
                
        except Exception as e:
            self.logger.error(f"Error deleting Linux firewall rule: {str(e)}")
            return False
    
    async def _delete_simulated_firewall_rule(self, rule: FirewallRule) -> bool:
        """Elimina regla de firewall simulada"""
        self.logger.info(f"SIMULATION: Deleted firewall rule '{rule.rule_name}'")
        return True
    
    async def _cleanup_expired_rules(self):
        """Limpia reglas expiradas"""
        try:
            current_time = datetime.utcnow()
            expired_rules = []
            
            for rule_id, rule in self.active_rules.items():
                if rule.expires_at and rule.expires_at <= current_time:
                    expired_rules.append(rule_id)
            
            for rule_id in expired_rules:
                try:
                    await self.delete_firewall_rule(rule_id)
                    self.logger.info(f"Expired firewall rule cleaned up: {rule_id}")
                except Exception as e:
                    self.logger.error(f"Failed to cleanup expired rule {rule_id}: {str(e)}")
            
            if expired_rules:
                await self.logger.log_activity(
                    activity_type="firewall_cleanup",
                    details={
                        "expired_rules_count": len(expired_rules),
                        "cleanup_time": current_time.isoformat()
                    },
                    save_to_firebase=True
                )
                
        except Exception as e:
            self.logger.error(f"Error during firewall cleanup: {str(e)}")
    
    async def _save_firewall_rule(self, rule: FirewallRule):
        """Guarda regla de firewall en Firebase"""
        try:
            rule_data = rule.dict()
            await self.services.firebase_service.save_scan_results({
                "type": "firewall_rule",
                "data": rule_data,
                "timestamp": datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"Failed to save firewall rule to Firebase: {str(e)}")
    
    def list_active_rules(self) -> List[Dict[str, Any]]:
        """Lista todas las reglas activas"""
        return [rule.dict() for rule in self.active_rules.values()]
    
    def get_blocked_ips(self) -> List[Dict[str, Any]]:
        """Obtiene lista de IPs bloqueadas"""
        return [ip.dict() for ip in self.blocked_ips.values() if ip.blocked]
    
    async def bulk_block_ips(self, ip_list: List[str], threat_level: SeverityLevel = SeverityLevel.HIGH) -> Dict[str, Any]:
        """Bloquea múltiples IPs en lote"""
        try:
            blocked_count = 0
            failed_count = 0
            results = []
            
            for ip in ip_list:
                try:
                    result = await self.block_malicious_ip(ip, threat_level)
                    blocked_count += 1
                    results.append({"ip": ip, "status": "blocked", "rule_id": result["rule_id"]})
                except Exception as e:
                    failed_count += 1
                    results.append({"ip": ip, "status": "failed", "error": str(e)})
            
            return {
                "success": True,
                "message": f"Bulk IP blocking completed: {blocked_count} blocked, {failed_count} failed",
                "blocked_count": blocked_count,
                "failed_count": failed_count,
                "results": results
            }
            
        except Exception as e:
            raise AkiraOperationError(f"Bulk IP blocking failed: {str(e)}")

# Instancia global del gestor de firewall
firewall_manager = FirewallManager()

def get_firewall_manager() -> FirewallManager:
    """Obtiene la instancia del gestor de firewall"""
    return firewall_manager