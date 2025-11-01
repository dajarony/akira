# modules/shared/validators.py

"""
SUME DOCBLOCK

Nombre: Validadores Compartidos Akira
Tipo: Lógica

Entradas:
- Datos para validación de red, seguridad y negocio
- Parámetros de configuración
- Inputs de usuario

Acciones:
- Valida datos de entrada
- Verifica formatos y rangos
- Aplica reglas de negocio

Salidas:
- Validaciones booleanas con mensajes de error
- Datos sanitizados y normalizados
"""

import re
import ipaddress
import socket
from typing import Dict, Any, List, Optional, Tuple, Union
from urllib.parse import urlparse
from datetime import datetime

from .utils import NetworkUtils, SecurityUtils

class NetworkValidators:
    """Validadores de red"""
    
    @staticmethod
    def validate_ip_address(ip: str) -> Tuple[bool, str]:
        """Valida dirección IP"""
        if not ip:
            return False, "IP address cannot be empty"
        
        try:
            ipaddress.ip_address(ip)
            return True, "Valid IP address"
        except ValueError:
            return False, "Invalid IP address format"
    
    @staticmethod
    def validate_hostname(hostname: str) -> Tuple[bool, str]:
        """Valida hostname"""
        if not hostname:
            return False, "Hostname cannot be empty"
        
        if len(hostname) > 255:
            return False, "Hostname too long (max 255 characters)"
        
        # Regex para hostname válido
        hostname_regex = re.compile(
            r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*$'
        )
        
        if not hostname_regex.match(hostname):
            return False, "Invalid hostname format"
        
        return True, "Valid hostname"
    
    @staticmethod
    def validate_port(port: Union[int, str]) -> Tuple[bool, str]:
        """Valida puerto"""
        try:
            port_int = int(port)
            if 1 <= port_int <= 65535:
                return True, "Valid port"
            else:
                return False, "Port must be between 1 and 65535"
        except (ValueError, TypeError):
            return False, "Port must be a valid integer"
    
    @staticmethod
    def validate_port_range(port_range: str) -> Tuple[bool, str]:
        """Valida rango de puertos"""
        if not port_range:
            return False, "Port range cannot be empty"
        
        try:
            # Manejar diferentes formatos
            if ',' in port_range:
                # Lista de puertos
                for port_str in port_range.split(','):
                    port_str = port_str.strip()
                    if '-' in port_str:
                        # Rango dentro de la lista
                        start, end = map(int, port_str.split('-'))
                        if not (1 <= start <= 65535 and 1 <= end <= 65535):
                            return False, f"Invalid port range: {port_str}"
                        if start > end:
                            return False, f"Invalid range (start > end): {port_str}"
                    else:
                        # Puerto individual
                        port = int(port_str)
                        if not (1 <= port <= 65535):
                            return False, f"Invalid port: {port}"
            elif '-' in port_range:
                # Rango simple
                start, end = map(int, port_range.split('-'))
                if not (1 <= start <= 65535 and 1 <= end <= 65535):
                    return False, "Ports must be between 1 and 65535"
                if start > end:
                    return False, "Start port cannot be greater than end port"
            else:
                # Puerto único
                port = int(port_range)
                if not (1 <= port <= 65535):
                    return False, "Port must be between 1 and 65535"
            
            return True, "Valid port range"
            
        except ValueError:
            return False, "Invalid port range format"
    
    @staticmethod
    def validate_network_range(network: str) -> Tuple[bool, str]:
        """Valida rango de red CIDR"""
        if not network:
            return False, "Network range cannot be empty"
        
        try:
            ipaddress.ip_network(network, strict=False)
            return True, "Valid network range"
        except ValueError:
            return False, "Invalid network range format (use CIDR notation)"
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, str]:
        """Valida URL"""
        if not url:
            return False, "URL cannot be empty"
        
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False, "Invalid URL format"
            
            if parsed.scheme not in ['http', 'https']:
                return False, "URL must use HTTP or HTTPS"
            
            return True, "Valid URL"
        except Exception:
            return False, "Invalid URL format"

class SecurityValidators:
    """Validadores de seguridad"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Valida email"""
        if not email:
            return False, "Email cannot be empty"
        
        email_regex = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        if not email_regex.match(email):
            return False, "Invalid email format"
        
        if len(email) > 254:
            return False, "Email too long (max 254 characters)"
        
        return True, "Valid email"
    
    @staticmethod
    def validate_domain(domain: str) -> Tuple[bool, str]:
        """Valida dominio"""
        if not domain:
            return False, "Domain cannot be empty"
        
        # Remover protocolo si está presente
        if domain.startswith(('http://', 'https://')):
            domain = urlparse(domain).netloc
        
        return NetworkValidators.validate_hostname(domain)
    
    @staticmethod
    def validate_api_token(token: str) -> Tuple[bool, str]:
        """Valida token de API"""
        if not token:
            return False, "API token cannot be empty"
        
        if len(token) < 16:
            return False, "API token too short (minimum 16 characters)"
        
        if len(token) > 512:
            return False, "API token too long (maximum 512 characters)"
        
        # Verificar caracteres válidos
        if not re.match(r'^[A-Za-z0-9_-]+$', token):
            return False, "API token contains invalid characters"
        
        return True, "Valid API token"
    
    @staticmethod
    def validate_filename(filename: str) -> Tuple[bool, str]:
        """Valida nombre de archivo"""
        if not filename:
            return False, "Filename cannot be empty"
        
        # Caracteres peligrosos
        dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(char in filename for char in dangerous_chars):
            return False, "Filename contains dangerous characters"
        
        if len(filename) > 255:
            return False, "Filename too long (max 255 characters)"
        
        return True, "Valid filename"

class BusinessValidators:
    """Validadores de lógica de negocio"""
    
    @staticmethod
    def validate_scan_target(ip: Optional[str], hostname: Optional[str]) -> Tuple[bool, str]:
        """Valida objetivo de escaneo"""
        if not ip and not hostname:
            return False, "Either IP address or hostname must be provided"
        
        if ip:
            is_valid, message = NetworkValidators.validate_ip_address(ip)
            if not is_valid:
                return False, f"Invalid IP: {message}"
            
            # Verificar que no sea IP privada en producción
            try:
                if ipaddress.ip_address(ip).is_loopback:
                    return False, "Loopback addresses are not allowed"
            except ValueError:
                pass
        
        if hostname:
            is_valid, message = NetworkValidators.validate_hostname(hostname)
            if not is_valid:
                return False, f"Invalid hostname: {message}"
        
        return True, "Valid scan target"
    
    @staticmethod
    def validate_scan_options(options: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida opciones de escaneo"""
        # Validar timing template
        timing = options.get('timing_template', 3)
        if not isinstance(timing, int) or not (0 <= timing <= 5):
            return False, "Timing template must be between 0 and 5"
        
        # Validar timeout
        timeout = options.get('timeout_seconds', 30)
        if not isinstance(timeout, int) or not (1 <= timeout <= 300):
            return False, "Timeout must be between 1 and 300 seconds"
        
        # Validar procesos paralelos
        parallel = options.get('parallel_processes', 1)
        if not isinstance(parallel, int) or not (1 <= parallel <= 10):
            return False, "Parallel processes must be between 1 and 10"
        
        return True, "Valid scan options"
    
    @staticmethod
    def validate_exploit_request(exploit_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida petición de exploit"""
        # Verificar campos requeridos
        required_fields = ['target', 'exploit_id', 'category']
        for field in required_fields:
            if field not in exploit_data:
                return False, f"Missing required field: {field}"
        
        # Validar target
        target = exploit_data['target']
        if isinstance(target, dict):
            ip = target.get('ip')
            hostname = target.get('hostname')
            is_valid, message = BusinessValidators.validate_scan_target(ip, hostname)
            if not is_valid:
                return False, message
        
        # Validar exploit_id
        exploit_id = exploit_data['exploit_id']
        if not isinstance(exploit_id, str) or len(exploit_id) < 3:
            return False, "Invalid exploit ID"
        
        # Validar timeout
        timeout = exploit_data.get('timeout_seconds', 60)
        if not isinstance(timeout, int) or not (1 <= timeout <= 300):
            return False, "Timeout must be between 1 and 300 seconds"
        
        return True, "Valid exploit request"
    
    @staticmethod
    def validate_firewall_rule(rule_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida regla de firewall"""
        # Verificar campos requeridos
        required_fields = ['rule_name', 'action']
        for field in required_fields:
            if field not in rule_data:
                return False, f"Missing required field: {field}"
        
        # Validar acción
        valid_actions = ['allow', 'deny', 'drop', 'reject']
        if rule_data['action'] not in valid_actions:
            return False, f"Action must be one of: {valid_actions}"
        
        # Validar IPs si están presentes
        for ip_field in ['source_ip', 'destination_ip']:
            if ip_field in rule_data and rule_data[ip_field]:
                is_valid, message = NetworkValidators.validate_ip_address(rule_data[ip_field])
                if not is_valid:
                    return False, f"Invalid {ip_field}: {message}"
        
        # Validar puertos si están presentes
        for port_field in ['source_port', 'destination_port']:
            if port_field in rule_data and rule_data[port_field]:
                port_value = rule_data[port_field]
                if isinstance(port_value, str):
                    is_valid, message = NetworkValidators.validate_port_range(port_value)
                else:
                    is_valid, message = NetworkValidators.validate_port(port_value)
                
                if not is_valid:
                    return False, f"Invalid {port_field}: {message}"
        
        return True, "Valid firewall rule"
    
    @staticmethod
    def validate_honeypot_config(config: Dict[str, Any]) -> Tuple[bool, str]:
        """Valida configuración de honeypot"""
        # Verificar campos requeridos
        required_fields = ['honeypot_name', 'honeypot_type', 'port']
        for field in required_fields:
            if field not in config:
                return False, f"Missing required field: {field}"
        
        # Validar tipo de honeypot
        valid_types = ['ssh', 'http', 'ftp', 'telnet']
        if config['honeypot_type'] not in valid_types:
            return False, f"Honeypot type must be one of: {valid_types}"
        
        # Validar puerto
        is_valid, message = NetworkValidators.validate_port(config['port'])
        if not is_valid:
            return False, f"Invalid port: {message}"
        
        # Validar interfaz si está presente
        if 'interface' in config and config['interface']:
            interface = config['interface']
            if interface != '0.0.0.0':
                is_valid, message = NetworkValidators.validate_ip_address(interface)
                if not is_valid:
                    return False, f"Invalid interface: {message}"
        
        return True, "Valid honeypot configuration"

class DataValidators:
    """Validadores de datos"""
    
    @staticmethod
    def validate_json_structure(data: Any, required_keys: List[str]) -> Tuple[bool, str]:
        """Valida estructura JSON"""
        if not isinstance(data, dict):
            return False, "Data must be a JSON object"
        
        for key in required_keys:
            if key not in data:
                return False, f"Missing required key: {key}"
        
        return True, "Valid JSON structure"
    
    @staticmethod
    def validate_string_length(value: str, min_length: int = 0, max_length: int = 1000) -> Tuple[bool, str]:
        """Valida longitud de string"""
        if not isinstance(value, str):
            return False, "Value must be a string"
        
        if len(value) < min_length:
            return False, f"String too short (minimum {min_length} characters)"
        
        if len(value) > max_length:
            return False, f"String too long (maximum {max_length} characters)"
        
        return True, "Valid string length"
    
    @staticmethod
    def validate_integer_range(value: int, min_value: int = 0, max_value: int = 1000000) -> Tuple[bool, str]:
        """Valida rango de entero"""
        if not isinstance(value, int):
            return False, "Value must be an integer"
        
        if value < min_value:
            return False, f"Value too small (minimum {min_value})"
        
        if value > max_value:
            return False, f"Value too large (maximum {max_value})"
        
        return True, "Valid integer range"

# Función principal de validación
def validate_input(input_type: str, value: Any, **kwargs) -> Tuple[bool, str]:
    """
    Función principal de validación
    
    Args:
        input_type: Tipo de validación (ip, hostname, port, email, etc.)
        value: Valor a validar
        **kwargs: Parámetros adicionales para validación
    
    Returns:
        Tuple[bool, str]: (es_válido, mensaje)
    """
    validators_map = {
        'ip': NetworkValidators.validate_ip_address,
        'hostname': NetworkValidators.validate_hostname,
        'port': NetworkValidators.validate_port,
        'port_range': NetworkValidators.validate_port_range,
        'network': NetworkValidators.validate_network_range,
        'url': NetworkValidators.validate_url,
        'email': SecurityValidators.validate_email,
        'domain': SecurityValidators.validate_domain,
        'api_token': SecurityValidators.validate_api_token,
        'filename': SecurityValidators.validate_filename
    }
    
    validator = validators_map.get(input_type)
    if not validator:
        return False, f"Unknown validation type: {input_type}"
    
    try:
        return validator(value)
    except Exception as e:
        return False, f"Validation error: {str(e)}"