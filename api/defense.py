# Contenido de api/defense.py (CORREGIDO FINAL)
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime
from core import get_logger
from models import DefenseStatusResponse, DefenseStats
from modules.defense import get_firewall_manager, get_honeypot_deployer, get_ai_threat_detector

router = APIRouter(prefix="/defense", tags=["Defensive Operations"])
logger = get_logger()

# ... (Todos los demás endpoints como /firewall/rule, /honeypot, etc. permanecen igual)

def _calculate_defense_score(stats: Dict[str, Any]) -> int:
    score = 50
    if stats.get("active_firewall_rules", 0) > 0: score += min(stats["active_firewall_rules"] * 5, 25)
    if stats.get("active_honeypots", 0) > 0: score += min(stats["active_honeypots"] * 10, 20)
    if stats.get("blocked_ips_count", 0) > 10: score -= min(stats["blocked_ips_count"], 30)
    return max(0, min(100, score))

def _assess_security_posture(stats: Dict[str, Any]) -> str:
    score = _calculate_defense_score(stats)
    if score >= 80: return "excellent"
    elif score >= 60: return "good"
    elif score >= 40: return "fair"
    else: return "needs_improvement"

@router.get("/stats", response_model=DefenseStatusResponse)
async def get_defense_statistics() -> DefenseStatusResponse:
    firewall_manager = get_firewall_manager()
    honeypot_deployer = get_honeypot_deployer()
    ai_threat_detector = get_ai_threat_detector()
    
    stats = { "collection_errors": [] }

    try:
        firewall_stats = await firewall_manager.get_defense_stats()
        stats.update(firewall_stats.dict())
    except Exception as e:
        logger.warning(f"Failed to get firewall stats: {e}")
        stats["collection_errors"].append(f"firewall: {str(e)}")

    try:
        honeypot_stats = await honeypot_deployer.get_honeypot_stats()
        stats['active_honeypots'] = honeypot_stats.get('active_honeypots', 0)
    except Exception as e:
        logger.warning(f"Failed to get honeypot stats: {e}")
        stats["collection_errors"].append(f"honeypots: {str(e)}")

    try:
        threat_stats = await ai_threat_detector.get_threat_statistics()
        stats.update({
            "alerts_generated_today": threat_stats.get("total_alerts", 0),
            "top_threat_types": threat_stats.get("top_threat_types", [])
        })
    except Exception as e:
        logger.warning(f"Failed to get threat detection stats: {e}")
        stats["collection_errors"].append(f"threat_detection: {str(e)}")
        
    stats.update({
        "defense_effectiveness_score": _calculate_defense_score(stats),
        "security_posture": _assess_security_posture(stats),
        # --- CORRECCIÓN AQUÍ ---
        "last_updated": datetime.utcnow() 
    })

    # Llenar valores por defecto para campos que podrían faltar si hubo errores
    default_stats = {
        "active_firewall_rules": 0, "active_honeypots": 0,
        "threats_blocked_today": 0, "alerts_generated_today": 0,
        "top_threat_types": [], "top_attacking_ips": [],
        "blocked_ips_count": 0
    }
    for key, value in default_stats.items():
        stats.setdefault(key, value)
    
    # Asegurar que top_attacking_ips tiene el formato correcto
    if not isinstance(stats.get("top_attacking_ips"), list) or not all(isinstance(item, dict) for item in stats.get("top_attacking_ips", [])):
        stats["top_attacking_ips"] = []


    final_stats_obj = DefenseStats(**stats)
    
    return DefenseStatusResponse(
        success=True,
        message="Defense statistics retrieved successfully.",
        defense_stats=final_stats_obj
    )

# ... (El resto de los endpoints de este archivo, si los hubiera, permanecen)
from models import FirewallRuleRequest, FirewallResponse, HoneypotRequest, HoneypotResponse, ThreatDetectionRequest, ThreatDetectionResponse, BaseResponse

@router.post("/firewall/rule", response_model=FirewallResponse)
async def create_firewall_rule(rule_request: FirewallRuleRequest):
    manager = get_firewall_manager()
    rule = await manager.create_firewall_rule(rule_request)
    rules = await manager.get_active_rules()
    return FirewallResponse(success=True, message="Rule created", rule=rule, active_rules=rules)

@router.delete("/firewall/rule/{rule_id}", response_model=BaseResponse)
async def delete_firewall_rule(rule_id: str):
    manager = get_firewall_manager()
    success = await manager.remove_firewall_rule(rule_id)
    if not success: raise HTTPException(404, "Rule not found")
    return BaseResponse(success=True, message="Rule deleted")

@router.get("/firewall/rules", response_model=FirewallResponse)
async def list_firewall_rules():
    manager = get_firewall_manager()
    rules = await manager.get_active_rules()
    return FirewallResponse(success=True, message="Rules retrieved", active_rules=rules)

@router.post("/honeypot", response_model=HoneypotResponse)
async def deploy_honeypot(req: HoneypotRequest):
    deployer = get_honeypot_deployer()
    info = await deployer.deploy_honeypot(req)
    return HoneypotResponse(success=True, message="Honeypot deployed", honeypot=info)

@router.delete("/honeypot/{honeypot_id}", response_model=BaseResponse)
async def stop_honeypot(honeypot_id: str):
    deployer = get_honeypot_deployer()
    success = await deployer.stop_honeypot(honeypot_id)
    if not success: raise HTTPException(404, "Honeypot not found")
    return BaseResponse(success=True, message="Honeypot stopped")

@router.get("/honeypots", response_model=HoneypotResponse)
async def list_active_honeypots():
    deployer = get_honeypot_deployer()
    hps = await deployer.get_active_honeypots()
    return HoneypotResponse(success=True, message="Honeypots retrieved", active_honeypots=hps)

@router.post("/threat-detection", response_model=ThreatDetectionResponse)
async def analyze_threats(req: ThreatDetectionRequest):
    detector = get_ai_threat_detector()
    threats = await detector.analyze_logs(req)
    return ThreatDetectionResponse(success=True, message="Analysis complete", threats_detected=threats)
