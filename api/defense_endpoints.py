# api/defense_endpoints.py

"""
SUME DOCBLOCK

Nombre: Endpoints API de Defensa Akira
Tipo: API

Entradas:
- Peticiones HTTP para gestión de defensa
- Configuración de firewall y honeypots
- Análisis de amenazas y logs

Acciones:
- Gestiona firewall automático
- Despliega y controla honeypots
- Analiza amenazas con IA
- Proporciona estadísticas defensivas

Salidas:
- Respuestas JSON con estado de defensa
- Métricas de seguridad
- Alertas y amenazas detectadas
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from datetime import datetime

from core import get_logger
from models import (
    FirewallRule, HoneypotInfo, SeverityLevel, ToolStatus,
    DefenseStatusResponse, DefenseStats
)
from modules.defense.firewall_manager import get_firewall_manager
from modules.defense.honeypot_deployer import get_honeypot_deployer
from modules.defense.ai_threat_detector import get_ai_threat_detector

# Router para endpoints de defensa
defense_router = APIRouter(prefix="/defense", tags=["Defense"])
logger = get_logger()

# === FIREWALL ENDPOINTS ===

@defense_router.post("/firewall/rules")
async def create_firewall_rule(rule: FirewallRule):
    """Crea una nueva regla de firewall"""
    try:
        firewall_manager = get_firewall_manager()
        result = await firewall_manager.create_firewall_rule(rule)
        return result
    except Exception as e:
        logger.error(f"Failed to create firewall rule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.delete("/firewall/rules/{rule_id}")
async def delete_firewall_rule(rule_id: str):
    """Elimina una regla de firewall"""
    try:
        firewall_manager = get_firewall_manager()
        result = await firewall_manager.delete_firewall_rule(rule_id)
        return result
    except Exception as e:
        logger.error(f"Failed to delete firewall rule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.get("/firewall/rules")
async def list_firewall_rules():
    """Lista todas las reglas de firewall activas"""
    try:
        firewall_manager = get_firewall_manager()
        rules = firewall_manager.list_active_rules()
        return {
            "success": True,
            "rules": rules,
            "total_rules": len(rules),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to list firewall rules: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.post("/firewall/block-ip")
async def block_malicious_ip(
    ip_address: str,
    threat_level: SeverityLevel = SeverityLevel.HIGH,
    duration_hours: int = 24
):
    """Bloquea una IP maliciosa"""
    try:
        firewall_manager = get_firewall_manager()
        result = await firewall_manager.block_malicious_ip(
            ip_address=ip_address,
            threat_level=threat_level,
            duration_hours=duration_hours
        )
        return result
    except Exception as e:
        logger.error(f"Failed to block IP: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.post("/firewall/unblock-ip")
async def unblock_ip(ip_address: str):
    """Desbloquea una IP"""
    try:
        firewall_manager = get_firewall_manager()
        result = await firewall_manager.unblock_ip(ip_address)
        return result
    except Exception as e:
        logger.error(f"Failed to unblock IP: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.post("/firewall/bulk-block")
async def bulk_block_ips(
    ip_list: List[str],
    threat_level: SeverityLevel = SeverityLevel.HIGH
):
    """Bloquea múltiples IPs en lote"""
    try:
        firewall_manager = get_firewall_manager()
        result = await firewall_manager.bulk_block_ips(ip_list, threat_level)
        return result
    except Exception as e:
        logger.error(f"Failed to bulk block IPs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.get("/firewall/status")
async def get_firewall_status():
    """Obtiene el estado del firewall"""
    try:
        firewall_manager = get_firewall_manager()
        status = await firewall_manager.get_firewall_status()
        return status
    except Exception as e:
        logger.error(f"Failed to get firewall status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.get("/firewall/blocked-ips")
async def get_blocked_ips():
    """Obtiene lista de IPs bloqueadas"""
    try:
        firewall_manager = get_firewall_manager()
        blocked_ips = firewall_manager.get_blocked_ips()
        return {
            "success": True,
            "blocked_ips": blocked_ips,
            "total_blocked": len(blocked_ips),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get blocked IPs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === HONEYPOT ENDPOINTS ===

@defense_router.post("/honeypot/deploy/ssh")
async def deploy_ssh_honeypot(
    port: int = 2222,
    interface: str = "0.0.0.0"
):
    """Despliega honeypot SSH"""
    try:
        honeypot_deployer = get_honeypot_deployer()
        result = await honeypot_deployer.deploy_ssh_honeypot(port, interface)
        return result
    except Exception as e:
        logger.error(f"Failed to deploy SSH honeypot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.post("/honeypot/deploy/http")
async def deploy_http_honeypot(
    port: int = 8080,
    interface: str = "0.0.0.0"
):
    """Despliega honeypot HTTP"""
    try:
        honeypot_deployer = get_honeypot_deployer()
        result = await honeypot_deployer.deploy_http_honeypot(port, interface)
        return result
    except Exception as e:
        logger.error(f"Failed to deploy HTTP honeypot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.post("/honeypot/deploy/ftp")
async def deploy_ftp_honeypot(
    port: int = 2121,
    interface: str = "0.0.0.0"
):
    """Despliega honeypot FTP"""
    try:
        honeypot_deployer = get_honeypot_deployer()
        result = await honeypot_deployer.deploy_ftp_honeypot(port, interface)
        return result
    except Exception as e:
        logger.error(f"Failed to deploy FTP honeypot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.delete("/honeypot/{honeypot_id}")
async def stop_honeypot(honeypot_id: str):
    """Detiene un honeypot específico"""
    try:
        honeypot_deployer = get_honeypot_deployer()
        result = await honeypot_deployer.stop_honeypot(honeypot_id)
        return result
    except Exception as e:
        logger.error(f"Failed to stop honeypot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.delete("/honeypot/stop-all")
async def stop_all_honeypots():
    """Detiene todos los honeypots"""
    try:
        honeypot_deployer = get_honeypot_deployer()
        result = await honeypot_deployer.stop_all_honeypots()
        return result
    except Exception as e:
        logger.error(f"Failed to stop all honeypots: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.get("/honeypot/status")
async def get_honeypot_status():
    """Obtiene estado de todos los honeypots"""
    try:
        honeypot_deployer = get_honeypot_deployer()
        status = await honeypot_deployer.get_honeypot_status()
        return status
    except Exception as e:
        logger.error(f"Failed to get honeypot status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.get("/honeypot/active")
async def list_active_honeypots():
    """Lista honeypots activos"""
    try:
        honeypot_deployer = get_honeypot_deployer()
        active_honeypots = honeypot_deployer.list_active_honeypots()
        return {
            "success": True,
            "active_honeypots": active_honeypots,
            "total_active": len(active_honeypots),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to list active honeypots: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === THREAT DETECTION ENDPOINTS ===

@defense_router.post("/threat-detection/analyze")
async def analyze_logs(
    log_entries: List[str],
    source: str = "system"
):
    """Analiza logs en busca de amenazas"""
    try:
        ai_threat_detector = get_ai_threat_detector()
        result = await ai_threat_detector.analyze_logs(log_entries, source)
        return result
    except Exception as e:
        logger.error(f"Failed to analyze logs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.get("/threat-detection/status")
async def get_threat_status():
    """Obtiene estado actual de amenazas"""
    try:
        ai_threat_detector = get_ai_threat_detector()
        status = await ai_threat_detector.get_threat_status()
        return status
    except Exception as e:
        logger.error(f"Failed to get threat status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.get("/threat-detection/threats")
async def list_detected_threats(
    severity_filter: Optional[SeverityLevel] = None
):
    """Lista amenazas detectadas"""
    try:
        ai_threat_detector = get_ai_threat_detector()
        threats = ai_threat_detector.list_detected_threats(severity_filter)
        return {
            "success": True,
            "threats": threats,
            "total_threats": len(threats),
            "severity_filter": severity_filter.value if severity_filter else None,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to list threats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@defense_router.post("/threat-detection/resolve/{threat_id}")
async def resolve_threat(threat_id: str):
    """Marca una amenaza como resuelta"""
    try:
        ai_threat_detector = get_ai_threat_detector()
        result = await ai_threat_detector.resolve_threat(threat_id)
        return result
    except Exception as e:
        logger.error(f"Failed to resolve threat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === DEFENSE STATISTICS ENDPOINT ===

@defense_router.get("/stats", response_model=DefenseStatusResponse)
async def get_defense_stats():
    """Obtiene estadísticas completas de defensa"""
    try:
        # Obtener datos de todos los módulos
        firewall_manager = get_firewall_manager()
        honeypot_deployer = get_honeypot_deployer()
        ai_threat_detector = get_ai_threat_detector()
        
        # Estadísticas de firewall
        firewall_status = await firewall_manager.get_firewall_status()
        blocked_ips = firewall_manager.get_blocked_ips()
        
        # Estadísticas de honeypots
        honeypot_status = await honeypot_deployer.get_honeypot_status()
        
        # Estadísticas de amenazas
        threat_status = await ai_threat_detector.get_threat_status()
        
        # Compilar estadísticas defensivas
        defense_stats = DefenseStats(
            active_firewall_rules=firewall_status['firewall_status']['total_rules'],
            active_honeypots=honeypot_status['honeypot_status']['active_honeypots'],
            threats_blocked_today=len([ip for ip in blocked_ips if ip['blocked']]),
            alerts_generated_today=threat_status['threat_status']['recent_threats_24h'],
            top_threat_types=list(threat_status['threat_status']['threat_types'].keys())[:5],
            blocked_ips_count=len(blocked_ips),
            defense_effectiveness_score=min(100, max(0, 
                80 - (threat_status['threat_status']['severity_distribution']['critical'] * 10) -
                (threat_status['threat_status']['severity_distribution']['high'] * 5)
            )),
            security_posture="excellent" if threat_status['threat_status']['severity_distribution']['critical'] == 0 else
                           "good" if threat_status['threat_status']['severity_distribution']['critical'] < 3 else
                           "fair" if threat_status['threat_status']['severity_distribution']['critical'] < 10 else "poor"
        )
        
        return DefenseStatusResponse(
            success=True,
            message="Defense statistics retrieved successfully",
            defense_stats=defense_stats
        )
        
    except Exception as e:
        logger.error(f"Failed to get defense stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# === BACKGROUND TASKS ===

@defense_router.post("/maintenance/cleanup")
async def run_defense_cleanup(background_tasks: BackgroundTasks):
    """Ejecuta tareas de limpieza de defensa en background"""
    try:
        async def cleanup_task():
            try:
                # Limpiar reglas de firewall expiradas
                firewall_manager = get_firewall_manager()
                await firewall_manager._cleanup_expired_rules()
                
                logger.info("Defense cleanup completed successfully")
                
            except Exception as e:
                logger.error(f"Defense cleanup failed: {str(e)}")
        
        background_tasks.add_task(cleanup_task)
        
        return {
            "success": True,
            "message": "Defense cleanup task started in background",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start cleanup task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))