"""
SUME DOCBLOCK

Nombre: API Endpoints de Estado Akira
Tipo: Entrada

Entradas:
- Requests HTTP de monitoreo
- Headers de autenticación
- Parámetros de consulta

Acciones:
- Monitorea salud del sistema
- Proporciona logs del sistema
- Retorna información del sistema
- Gestiona estadísticas generales

Salidas:
- Estado de salud de servicios
- Logs estructurados
- Métricas del sistema
- Información de configuración
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

from core import get_logger, get_services, get_settings
from models import HealthStatus, BaseResponse
from modules.shared import get_system_utils, get_time_utils

router = APIRouter(prefix="/status", tags=["System Status"])
logger = get_logger()

@router.get("/health", response_model=Dict[str, Any])
async def get_system_health() -> Dict[str, Any]:
    """
    Verifica el estado de salud de todos los servicios del sistema
    
    Retorna información sobre:
    - Estado de servicios (OpenAI, Firebase)
    - Conectividad de red
    - Recursos del sistema
    - Tiempo de actividad
    """
    try:
        services = get_services()
        system_utils = get_system_utils()
        settings = get_settings()
        
        # Verificar salud de servicios
        services_health = await services.health_check()
        
        # Información del sistema
        system_info = system_utils.get_system_info()
        
        # Uso de recursos
        cpu_usage = system_utils.get_cpu_usage()
        memory_usage = system_utils.get_memory_usage()
        disk_usage = system_utils.get_disk_usage()
        
        # Determinar estado general
        overall_status = "healthy"
        if services_health.get("overall_status") == "degraded":
            overall_status = "degraded"
        elif cpu_usage > 90 or memory_usage.get("percentage", 0) > 90:
            overall_status = "warning"
        
        health_data = {
            "overall_status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "services": services_health.get("services", {}),
            "system": {
                "platform": system_info.get("platform", "unknown"),
                "python_version": system_info.get("python_version", "unknown"),
                "hostname": system_info.get("hostname", "unknown")
            },
            "resources": {
                "cpu_usage_percent": cpu_usage,
                "memory_usage_percent": memory_usage.get("percentage", 0),
                "memory_total_gb": round(memory_usage.get("total", 0) / (1024**3), 2),
                "memory_available_gb": round(memory_usage.get("available", 0) / (1024**3), 2),
                "disk_usage_percent": disk_usage.get("percentage", 0),
                "disk_total_gb": round(disk_usage.get("total", 0) / (1024**3), 2),
                "disk_free_gb": round(disk_usage.get("free", 0) / (1024**3), 2)
            },
            "configuration": {
                "environment": settings.environment,
                "debug_mode": settings.debug,
                "log_level": settings.log_level,
                "api_host": settings.api_host,
                "api_port": settings.api_port
            }
        }
        
        # Log del health check
        await logger.log_activity(
            activity_type="system_event",
            details={
                "endpoint": "/status/health",
                "overall_status": overall_status,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage.get("percentage", 0)
            },
            save_to_firebase=False
        )
        
        return health_data
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "overall_status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "services": {"all": "error"},
            "system": {"status": "error"},
            "resources": {"status": "error"}
        }

@router.get("/logs", response_model=Dict[str, Any])
async def get_system_logs(
    limit: int = Query(default=100, ge=1, le=1000, description="Number of log entries to return"),
    level: Optional[str] = Query(default=None, description="Filter by log level (DEBUG, INFO, WARNING, ERROR)"),
    hours: int = Query(default=24, ge=1, le=168, description="Hours back to search")
) -> Dict[str, Any]:
    """
    Obtiene logs recientes del sistema
    
    - **limit**: Número máximo de entradas a retornar (1-1000)
    - **level**: Filtrar por nivel de log (DEBUG, INFO, WARNING, ERROR)
    - **hours**: Horas hacia atrás para buscar (1-168)
    """
    try:
        await logger.log_activity(
            activity_type="system_event",
            details={
                "endpoint": "/status/logs",
                "limit": limit,
                "level": level,
                "hours": hours
            },
            save_to_firebase=False
        )
        
        # Validar nivel de log
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level and level.upper() not in valid_levels:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid log level",
                    "message": f"Level must be one of: {valid_levels}",
                    "provided": level
                }
            )
        
        # Leer logs del archivo
        settings = get_settings()
        log_file_path = settings.log_file_path
        
        logs = []
        try:
            # Leer líneas del archivo de log
            with open(log_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Procesar últimas líneas (más recientes)
            recent_lines = lines[-limit*2:] if len(lines) > limit*2 else lines
            
            for line in reversed(recent_lines):  # Más recientes primero
                if line.strip():
                    try:
                        # Intentar parsear como JSON (logs estructurados)
                        import json
                        log_entry = json.loads(line.strip())
                        
                        # Filtrar por nivel si se especifica
                        if level and log_entry.get("level", "").upper() != level.upper():
                            continue
                        
                        # Filtrar por tiempo
                        log_time_str = log_entry.get("timestamp")
                        if log_time_str:
                            try:
                                log_time = datetime.fromisoformat(log_time_str.replace('Z', '+00:00'))
                                cutoff_time = datetime.utcnow() - timedelta(hours=hours)
                                if log_time < cutoff_time:
                                    continue
                            except ValueError:
                                pass  # No filtrar si no se puede parsear el tiempo
                        
                        logs.append(log_entry)
                        
                        if len(logs) >= limit:
                            break
                            
                    except json.JSONDecodeError:
                        # Si no es JSON, tratar como texto plano
                        if level:  # Si se filtra por nivel, skip logs de texto plano
                            continue
                        
                        logs.append({
                            "timestamp": datetime.utcnow().isoformat(),
                            "level": "INFO",
                            "message": line.strip(),
                            "type": "plain_text"
                        })
                        
                        if len(logs) >= limit:
                            break
            
        except FileNotFoundError:
            logger.warning(f"Log file not found: {log_file_path}")
        except Exception as e:
            logger.error(f"Error reading log file: {str(e)}")
        
        return {
            "success": True,
            "message": f"Retrieved {len(logs)} log entries",
            "logs": logs,
            "count": len(logs),
            "limit": limit,
            "level_filter": level,
            "hours": hours,
            "log_file": log_file_path,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get logs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve logs",
                "message": str(e)
            }
        )

@router.get("/system-info", response_model=Dict[str, Any])
async def get_system_information() -> Dict[str, Any]:
    """
    Obtiene información detallada del sistema
    """
    try:
        await logger.log_activity(
            activity_type="system_event",
            details={
                "endpoint": "/status/system-info",
                "action": "get_system_info"
            },
            save_to_firebase=False
        )
        
        system_utils = get_system_utils()
        settings = get_settings()
        
        # Información básica del sistema
        system_info = system_utils.get_system_info()
        
        # Recursos del sistema
        cpu_usage = system_utils.get_cpu_usage()
        memory_usage = system_utils.get_memory_usage()
        disk_usage = system_utils.get_disk_usage()
        
        # Interfaces de red
        network_interfaces = system_utils.get_network_interfaces()
        
        # Configuración de Akira
        akira_config = {
            "environment": settings.environment,
            "debug_mode": settings.debug,
            "log_level": settings.log_level,
            "api_host": settings.api_host,
            "api_port": settings.api_port,
            "firebase_project": settings.firebase_project_id,
            "log_file_path": settings.log_file_path
        }
        
        return {
            "success": True,
            "message": "System information retrieved successfully",
            "timestamp": datetime.utcnow().isoformat(),
            "system": system_info,
            "resources": {
                "cpu": {
                    "usage_percent": cpu_usage,
                    "status": "high" if cpu_usage > 80 else "normal" if cpu_usage > 50 else "low"
                },
                "memory": {
                    **memory_usage,
                    "status": "high" if memory_usage.get("percentage", 0) > 80 else "normal" if memory_usage.get("percentage", 0) > 50 else "low"
                },
                "disk": {
                    **disk_usage,
                    "status": "high" if disk_usage.get("percentage", 0) > 80 else "normal" if disk_usage.get("percentage", 0) > 50 else "low"
                }
            },
            "network": {
                "interfaces": network_interfaces,
                "interface_count": len(network_interfaces)
            },
            "configuration": akira_config
        }
        
    except Exception as e:
        logger.error(f"Failed to get system info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve system information",
                "message": str(e)
            }
        )

@router.get("/stats", response_model=Dict[str, Any])
async def get_system_statistics() -> Dict[str, Any]:
    """
    Obtiene estadísticas generales del sistema Akira
    """
    try:
        await logger.log_activity(
            activity_type="system_event",
            details={
                "endpoint": "/status/stats",
                "action": "get_stats"
            },
            save_to_firebase=False
        )
        
        # Obtener estadísticas de módulos defensivos
        from modules.defense import get_firewall_manager, get_honeypot_deployer, get_ai_threat_detector
        
        firewall_manager = get_firewall_manager()
        honeypot_deployer = get_honeypot_deployer()
        ai_threat_detector = get_ai_threat_detector()
        
        # Estadísticas de firewall
        active_rules = await firewall_manager.get_active_rules()
        blocked_ips = await firewall_manager.get_blocked_ips()
        
        # Estadísticas de honeypots
        active_honeypots = await honeypot_deployer.get_active_honeypots()
        honeypot_stats = await honeypot_deployer.get_honeypot_stats()
        
        # Estadísticas de amenazas
        threat_stats = await ai_threat_detector.get_threat_statistics()
        recent_alerts = await ai_threat_detector.get_recent_alerts(hours=24)
        
        # Estadísticas del sistema
        system_utils = get_system_utils()
        cpu_usage = system_utils.get_cpu_usage()
        memory_usage = system_utils.get_memory_usage()
        
        return {
            "success": True,
            "message": "System statistics retrieved successfully",
            "timestamp": datetime.utcnow().isoformat(),
            "overview": {
                "system_health": "healthy" if cpu_usage < 80 and memory_usage.get("percentage", 0) < 80 else "warning",
                "active_firewall_rules": len(active_rules),
                "blocked_ips": len(blocked_ips),
                "active_honeypots": len(active_honeypots),
                "alerts_24h": len(recent_alerts),
                "critical_alerts_24h": len([a for a in recent_alerts if a.severity.value == "critical"])
            },
            "defense": {
                "firewall": {
                    "active_rules": len(active_rules),
                    "blocked_ips": len(blocked_ips),
                    "auto_block_enabled": firewall_manager.auto_block_enabled
                },
                "honeypots": {
                    "active_count": len(active_honeypots),
                    "total_connections": honeypot_stats.get("total_connections", 0),
                    "credentials_captured": honeypot_stats.get("credentials_captured", 0)
                },
                "threat_detection": {
                    "total_alerts_24h": threat_stats.get("total_alerts", 0),
                    "critical_alerts": threat_stats.get("critical_alerts", 0),
                    "alerts_last_hour": threat_stats.get("alerts_last_hour", 0),
                    "top_threat_types": threat_stats.get("threat_types", {}),
                    "top_attacking_ips": threat_stats.get("top_threatening_ips", {})
                }
            },
            "system": {
                "cpu_usage_percent": cpu_usage,
                "memory_usage_percent": memory_usage.get("percentage", 0),
                "memory_total_gb": round(memory_usage.get("total", 0) / (1024**3), 2),
                "uptime_info": "Available via /status/health"
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get system statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve system statistics",
                "message": str(e)
            }
        )

@router.post("/command", response_model=BaseResponse)
async def execute_system_command(
    command: str,
    parameters: Optional[Dict[str, Any]] = None
) -> BaseResponse:
    """
    Ejecuta comandos del sistema Akira
    
    Comandos disponibles:
    - cleanup_logs: Limpia logs antiguos
    - cleanup_expired_rules: Limpia reglas de firewall expiradas
    - reload_config: Recarga configuración
    - gc_collect: Fuerza recolección de basura
    """
    start_time = datetime.utcnow()
    
    try:
        await logger.log_activity(
            activity_type="system_event",
            details={
                "endpoint": "/status/command",
                "command": command,
                "parameters": parameters or {}
            },
            save_to_firebase=True
        )
        
        # Comandos disponibles
        available_commands = [
            "cleanup_logs", "cleanup_expired_rules", "reload_config", 
            "gc_collect", "health_check", "restart_services"
        ]
        
        if command not in available_commands:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Unknown command",
                    "message": f"Command must be one of: {available_commands}",
                    "provided": command
                }
            )
        
        result_message = ""
        
        if command == "cleanup_logs":
            # Limpiar logs antiguos (placeholder - implementar según necesidades)
            result_message = "Log cleanup completed (placeholder implementation)"
            
        elif command == "cleanup_expired_rules":
            # Limpiar reglas de firewall expiradas
            firewall_manager = get_firewall_manager()
            await firewall_manager.cleanup_expired_rules()
            result_message = "Expired firewall rules cleaned up"
            
        elif command == "reload_config":
            # Recargar configuración (placeholder)
            result_message = "Configuration reloaded (placeholder implementation)"
            
        elif command == "gc_collect":
            # Forzar recolección de basura
            import gc
            collected = gc.collect()
            result_message = f"Garbage collection completed. Collected {collected} objects"
            
        elif command == "health_check":
            # Ejecutar health check completo
            services = get_services()
            health_result = await services.health_check()
            result_message = f"Health check completed. Status: {health_result.get('overall_status', 'unknown')}"
            
        elif command == "restart_services":
            # Reiniciar servicios (placeholder)
            result_message = "Services restart initiated (placeholder implementation)"
        
        execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return BaseResponse(
            success=True,
            message=f"Command '{command}' executed successfully. {result_message}",
            execution_time_ms=execution_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Command execution failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Command execution failed",
                "message": str(e),
                "command": command
            }
        )

@router.get("/version", response_model=Dict[str, Any])
async def get_version_info() -> Dict[str, Any]:
    """
    Obtiene información de versión de Akira
    """
    try:
        return {
            "success": True,
            "akira_version": "1.0.0-MVP",
            "api_version": "v1",
            "architecture": "SUME + STDG",
            "build_date": "2025-06-18",
            "features": [
                "Nmap Scanning",
                "OSINT Collection", 
                "Ethical Exploitation",
                "Firewall Management",
                "Honeypot Deployment",
                "AI Threat Detection",
                "Real-time Analytics"
            ],
            "modules": {
                "offense": ["nmap_scanner", "osint_collector", "exploit_launcher"],
                "defense": ["firewall_manager", "honeypot_deployer", "ai_threat_detector"],
                "shared": ["utils", "validators"]
            },
            "services": {
                "openai": "OpenAI GPT-4 Integration",
                "firebase": "Firebase Realtime Database & Analytics",
                "logging": "Structured JSON Logging"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get version info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve version information",
                "message": str(e)
            }
        )
