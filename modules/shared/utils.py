# modules/shared/utils.py

"""
SUME DOCBLOCK

Nombre: Utilidades Compartidas Akira
Tipo: Lógica

Entradas:
- Datos para validación y procesamiento
- Configuraciones del sistema
- Información de red y sistema

Acciones:
- Proporciona utilidades de red, seguridad y sistema
- Valida y procesa datos
- Gestiona operaciones comunes

Salidas:
- Funciones utilitarias para toda la aplicación
- Validaciones y transformaciones de datos
"""

import socket
import ipaddress
import psutil
import platform
import hashlib
import secrets
import json
import re
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

class NetworkUtils:
    """Utilidades de red"""
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """Valida si una IP es válida"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_hostname(hostname: str) -> bool:
        """Valida si un hostname es válido"""
        if len(hostname) > 255:
            return False
        
        # Regex para hostname válido
        hostname_regex = re.compile(
            r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*$'
        )
        return bool(hostname_regex.match(hostname))
    
    @staticmethod
    def is_valid_port(port: Union[int, str]) -> bool:
        """Valida si un puerto es válido"""
        try:
            port_int = int(port)
            return 1 <= port_int <= 65535
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def parse_port_range(port_range: str) -> List[int]:
        """Parsea un rango de puertos"""
        ports = []
        
        # Manejar diferentes formatos: "80", "80,443,22", "1-1000"
        if ',' in port_range:
            # Lista de puertos separados por coma
            for port_str in port_range.split(','):
                port_str = port_str.strip()
                if '-' in port_str:
                    # Rango dentro de la lista
                    start, end = map(int, port_str.split('-'))
                    ports.extend(range(start, end + 1))
                else:
                    ports.append(int(port_str))
        elif '-' in port_range:
            # Rango simple
            start, end = map(int, port_range.split('-'))
            ports.extend(range(start, end + 1))
        else:
            # Puerto único
            ports.append(int(port_range))
        
        return sorted(list(set(ports)))  # Eliminar duplicados y ordenar
    
    @staticmethod
    def is_port_open(host: str, port: int, timeout: int = 3) -> bool:
        """Verifica si un puerto está abierto"""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, socket.error):
            return False
    
    @staticmethod
    def resolve_hostname(hostname: str) -> Optional[str]:
        """Resuelve un hostname a IP"""
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None
    
    @staticmethod
    def reverse_dns(ip: str) -> Optional[str]:
        """Resuelve una IP a hostname"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return None
    
    @staticmethod
    def get_local_ip() -> str:
        """Obtiene la IP local"""
        try:
            # Conectar a un servidor externo para obtener la IP local
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
    
    @staticmethod
    def is_private_ip(ip: str) -> bool:
        """Verifica si una IP es privada"""
        try:
            return ipaddress.ip_address(ip).is_private
        except ValueError:
            return False

class SecurityUtils:
    """Utilidades de seguridad"""
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Genera un token seguro"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_string(data: str, algorithm: str = 'sha256') -> str:
        """Hashea una cadena"""
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(data.encode('utf-8'))
        return hash_obj.hexdigest()
    
    @staticmethod
    def is_safe_filename(filename: str) -> bool:
        """Verifica si un nombre de archivo es seguro"""
        # Caracteres peligrosos
        dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        return not any(char in filename for char in dangerous_chars)
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitiza entrada de usuario"""
        # Remover caracteres peligrosos
        sanitized = re.sub(r'[<>"\']', '', input_str)
        return sanitized.strip()
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Valida formato de email"""
        email_regex = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        return bool(email_regex.match(email))

class DataUtils:
    """Utilidades de datos"""
    
    @staticmethod
    def safe_json_loads(json_str: str) -> Optional[Dict[str, Any]]:
        """Carga JSON de forma segura"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    
    @staticmethod
    def safe_json_dumps(data: Any) -> str:
        """Serializa a JSON de forma segura"""
        try:
            return json.dumps(data, default=str, ensure_ascii=False)
        except (TypeError, ValueError):
            return "{}"
    
    @staticmethod
    def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """Aplana un diccionario anidado"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataUtils.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
        """Fusiona múltiples diccionarios"""
        result = {}
        for d in dicts:
            result.update(d)
        return result
    
    @staticmethod
    def filter_dict_keys(d: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
        """Filtra diccionario por claves permitidas"""
        return {k: v for k, v in d.items() if k in allowed_keys}

class TimeUtils:
    """Utilidades de tiempo"""
    
    @staticmethod
    def get_timestamp() -> str:
        """Obtiene timestamp actual en formato ISO"""
        return datetime.utcnow().isoformat()
    
    @staticmethod
    def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
        """Parsea timestamp desde string"""
        try:
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except ValueError:
            return None
    
    @staticmethod
    def time_ago(timestamp: datetime) -> str:
        """Calcula tiempo transcurrido"""
        now = datetime.utcnow()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"
    
    @staticmethod
    def is_expired(timestamp: datetime, expiry_hours: int) -> bool:
        """Verifica si un timestamp ha expirado"""
        now = datetime.utcnow()
        expiry_time = timestamp + timedelta(hours=expiry_hours)
        return now > expiry_time

class SystemUtils:
    """Utilidades del sistema"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Obtiene información del sistema"""
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }
    
    @staticmethod
    def get_cpu_usage() -> float:
        """Obtiene uso de CPU"""
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Obtiene uso de memoria"""
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percentage": memory.percent
        }
    
    @staticmethod
    def get_disk_usage(path: str = "/") -> Dict[str, Any]:
        """Obtiene uso de disco"""
        try:
            disk = psutil.disk_usage(path)
            return {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percentage": (disk.used / disk.total) * 100
            }
        except Exception:
            return {"total": 0, "used": 0, "free": 0, "percentage": 0}
    
    @staticmethod
    def get_network_interfaces() -> List[Dict[str, Any]]:
        """Obtiene interfaces de red"""
        interfaces = []
        for interface, addrs in psutil.net_if_addrs().items():
            interface_info = {"name": interface, "addresses": []}
            for addr in addrs:
                interface_info["addresses"].append({
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
            interfaces.append(interface_info)
        return interfaces
    
    @staticmethod
    def run_command(command: List[str], timeout: int = 30) -> Tuple[int, str, str]:
        """Ejecuta comando del sistema"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

class AkiraUtils:
    """Utilidades específicas de Akira"""
    
    @staticmethod
    def generate_scan_id() -> str:
        """Genera ID único para escaneo"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        random_suffix = secrets.token_hex(4)
        return f"scan_{timestamp}_{random_suffix}"
    
    @staticmethod
    def generate_exploit_id() -> str:
        """Genera ID único para exploit"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        random_suffix = secrets.token_hex(4)
        return f"exploit_{timestamp}_{random_suffix}"
    
    @staticmethod
    def generate_defense_id() -> str:
        """Genera ID único para operación defensiva"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        random_suffix = secrets.token_hex(4)
        return f"defense_{timestamp}_{random_suffix}"
    
    @staticmethod
    def validate_target_format(target: str) -> Tuple[bool, str]:
        """Valida formato de objetivo"""
        network_utils = NetworkUtils()
        
        if network_utils.is_valid_ip(target):
            return True, "ip"
        elif network_utils.is_valid_hostname(target):
            return True, "hostname"
        else:
            return False, "invalid"
    
    @staticmethod
    def parse_nmap_output(output: str) -> Dict[str, Any]:
        """Parsea salida de nmap (básico)"""
        # Implementación básica - se puede mejorar con python-nmap
        lines = output.split('\n')
        result = {
            "hosts": [],
            "ports": [],
            "summary": ""
        }
        
        for line in lines:
            if "Nmap scan report for" in line:
                host = line.split("for ")[-1]
                result["hosts"].append(host)
            elif "/tcp" in line or "/udp" in line:
                parts = line.split()
                if len(parts) >= 3:
                    port_info = {
                        "port": parts[0],
                        "state": parts[1],
                        "service": parts[2] if len(parts) > 2 else "unknown"
                    }
                    result["ports"].append(port_info)
        
        return result

# Funciones de factory para obtener instancias
def get_network_utils() -> NetworkUtils:
    return NetworkUtils()

def get_security_utils() -> SecurityUtils:
    return SecurityUtils()

def get_data_utils() -> DataUtils:
    return DataUtils()

def get_time_utils() -> TimeUtils:
    return TimeUtils()

def get_system_utils() -> SystemUtils:
    return SystemUtils()

def get_akira_utils() -> AkiraUtils:
    return AkiraUtils()