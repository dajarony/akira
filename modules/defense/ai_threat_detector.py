# modules/defense/ai_threat_detector.py

"""
SUME DOCBLOCK

Nombre: Detector de Amenazas con IA Akira
Tipo: Herramienta

Entradas:
- Logs de sistema y aplicaciones
- Patrones de tráfico de red
- Eventos de seguridad
- Datos de honeypots y firewall

Acciones:
- Analiza logs con OpenAI GPT-4
- Detecta patrones maliciosos
- Correlaciona eventos de seguridad
- Genera alertas automáticas

Salidas:
- Alertas de amenazas clasificadas
- Análisis de comportamiento
- Recomendaciones de respuesta
- Métricas de seguridad
"""

import asyncio
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import uuid

from core import get_logger, get_services
from models import ThreatInfo, SeverityLevel, AttackingIP
from modules.shared import get_akira_utils, get_security_utils, get_network_utils
from modules.defense.firewall_manager import get_firewall_manager
from modules.defense.honeypot_deployer import get_honeypot_deployer
from core.exceptions import AkiraOperationError, AkiraSecurityError

class AIThreatDetector:
    """Detector de amenazas inteligente con análisis IA"""
    
    def __init__(self):
        self.logger = get_logger()
        self.services = get_services()
        self.akira_utils = get_akira_utils()
        self.security_utils = get_security_utils()
        self.network_utils = get_network_utils()
        self.firewall_manager = get_firewall_manager()
        self.honeypot_deployer = get_honeypot_deployer()
        
        # Amenazas detectadas
        self.detected_threats: Dict[str, ThreatInfo] = {}
        self.threat_patterns = self._initialize_threat_patterns()
        
        # Configuración
        self.ai_analysis_enabled = True
        self.auto_response_enabled = True
        self.threat_correlation_window = 300  # 5 minutos
        
    def _initialize_threat_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Inicializa patrones de amenazas conocidos"""
        return {
            "brute_force_ssh": {
                "pattern": r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)",
                "threshold": 5,
                "time_window": 300,
                "severity": SeverityLevel.HIGH,
                "description": "SSH brute force attack detected"
            },
            "sql_injection": {
                "pattern": r"(UNION|SELECT|INSERT|DELETE|DROP|UPDATE).*FROM",
                "threshold": 1,
                "time_window": 60,
                "severity": SeverityLevel.CRITICAL,
                "description": "SQL injection attempt detected"
            },
            "xss_attempt": {
                "pattern": r"<script|javascript:|onload=|onerror=",
                "threshold": 1,
                "time_window": 60,
                "severity": SeverityLevel.HIGH,
                "description": "Cross-site scripting attempt detected"
            },
            "directory_traversal": {
                "pattern": r"\.\./|\.\.\\\|%2e%2e%2f|%2e%2e%5c",
                "threshold": 1,
                "time_window": 60,
                "severity": SeverityLevel.HIGH,
                "description": "Directory traversal attempt detected"
            },
            "port_scan": {
                "pattern": r"Connection attempt to port (\d+) from (\d+\.\d+\.\d+\.\d+)",
                "threshold": 10,
                "time_window": 60,
                "severity": SeverityLevel.MEDIUM,
                "description": "Port scanning activity detected"
            },
            "malware_signature": {
                "pattern": r"(eval\(|base64_decode|shell_exec|system\()",
                "threshold": 1,
                "time_window": 60,
                "severity": SeverityLevel.CRITICAL,
                "description": "Malware signature detected"
            }
        }
    
    async def analyze_logs(self, log_entries: List[str], source: str = "system") -> Dict[str, Any]:
        """Analiza logs en busca de amenazas"""
        try:
            start_time = datetime.utcnow()
            
            # Análisis con patrones
            pattern_threats = await self._analyze_with_patterns(log_entries, source)
            
            # Análisis con IA si está habilitado
            ai_threats = []
            if self.ai_analysis_enabled and self.services.openai_service:
                ai_threats = await self._analyze_with_ai(log_entries, source)
            
            # Combinar resultados
            all_threats = pattern_threats + ai_threats
            
            # Correlacionar amenazas
            correlated_threats = await self._correlate_threats(all_threats)
            
            # Generar respuestas automáticas
            if self.auto_response_enabled:
                await self._generate_automatic_responses(correlated_threats)
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="threat_analysis",
                details={
                    "source": source,
                    "log_entries_count": len(log_entries),
                    "threats_detected": len(all_threats),
                    "correlated_threats": len(correlated_threats),
                    "analysis_time_ms": (datetime.utcnow() - start_time).total_seconds() * 1000
                },
                save_to_firebase=True
            )
            
            return {
                "success": True,
                "analysis_results": {
                    "source": source,
                    "log_entries_analyzed": len(log_entries),
                    "threats_detected": len(all_threats),
                    "correlated_threats": len(correlated_threats),
                    "pattern_threats": len(pattern_threats),
                    "ai_threats": len(ai_threats),
                    "analysis_time_ms": (datetime.utcnow() - start_time).total_seconds() * 1000
                },
                "threats": [threat.dict() for threat in correlated_threats],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            await self.logger.log_activity(
                activity_type="error",
                details={
                    "operation": "analyze_logs",
                    "source": source,
                    "error": str(e)
                },
                level="error",
                save_to_firebase=True
            )
            raise AkiraOperationError(f"Failed to analyze logs: {str(e)}")
    
    async def _analyze_with_patterns(self, log_entries: List[str], source: str) -> List[ThreatInfo]:
        """Analiza logs usando patrones predefinidos"""
        threats = []
        
        for pattern_name, pattern_config in self.threat_patterns.items():
            pattern = pattern_config["pattern"]
            threshold = pattern_config["threshold"]
            severity = pattern_config["severity"]
            description = pattern_config["description"]
            
            matches = []
            for log_entry in log_entries:
                match = re.search(pattern, log_entry, re.IGNORECASE)
                if match:
                    matches.append({
                        "log_entry": log_entry,
                        "match": match.groups() if match.groups() else [match.group(0)],
                        "timestamp": datetime.utcnow()
                    })
            
            # Si supera el umbral, crear amenaza
            if len(matches) >= threshold:
                threat_id = f"{pattern_name}_{uuid.uuid4().hex[:8]}"
                
                # Extraer IPs si están disponibles
                source_ips = []
                for match in matches:
                    if match["match"]:
                        for group in match["match"]:
                            if self.network_utils.is_valid_ip(group):
                                source_ips.append(group)
                
                threat = ThreatInfo(
                    threat_id=threat_id,
                    threat_type=pattern_name,
                    severity=severity,
                    source_ip=source_ips[0] if source_ips else None,
                    description=f"{description} ({len(matches)} occurrences)",
                    indicators=[match["log_entry"][:100] for match in matches[:5]],  # Primeros 5
                    mitigation_steps=self._get_mitigation_steps(pattern_name)
                )
                
                threats.append(threat)
                self.detected_threats[threat_id] = threat
        
        return threats
    
    async def _analyze_with_ai(self, log_entries: List[str], source: str) -> List[ThreatInfo]:
        """Analiza logs usando IA (OpenAI GPT-4)"""
        try:
            # Preparar prompt para análisis
            log_sample = "\n".join(log_entries[:50])  # Primeros 50 logs
            
            prompt = f"""
            Analyze the following system logs for security threats and suspicious activities:
            
            Source: {source}
            Logs:
            {log_sample}
            
            Please identify:
            1. Security threats and their severity (CRITICAL, HIGH, MEDIUM, LOW)
            2. Suspicious IP addresses or patterns
            3. Attack types (brute force, injection, scanning, etc.)
            4. Recommended mitigation steps
            
            Respond in JSON format with this structure:
            {{
                "threats": [
                    {{
                        "threat_type": "string",
                        "severity": "CRITICAL|HIGH|MEDIUM|LOW",
                        "description": "string",
                        "source_ip": "string or null",
                        "indicators": ["string"],
                        "mitigation_steps": ["string"]
                    }}
                ]
            }}
            """
            
            # Llamar a OpenAI
            response = await self.services.openai_service.analyze_with_gpt4(
                prompt=prompt,
                context="security_threat_analysis"
            )
            
            # Parsear respuesta
            ai_analysis = json.loads(response.get("analysis", "{}"))
            threats = []
            
            for threat_data in ai_analysis.get("threats", []):
                threat_id = f"ai_{threat_data['threat_type']}_{uuid.uuid4().hex[:8]}"
                
                # Mapear severidad
                severity_map = {
                    "CRITICAL": SeverityLevel.CRITICAL,
                    "HIGH": SeverityLevel.HIGH,
                    "MEDIUM": SeverityLevel.MEDIUM,
                    "LOW": SeverityLevel.LOW
                }
                
                threat = ThreatInfo(
                    threat_id=threat_id,
                    threat_type=f"ai_{threat_data['threat_type']}",
                    severity=severity_map.get(threat_data['severity'], SeverityLevel.MEDIUM),
                    source_ip=threat_data.get('source_ip'),
                    description=threat_data['description'],
                    indicators=threat_data.get('indicators', []),
                    mitigation_steps=threat_data.get('mitigation_steps', [])
                )
                
                threats.append(threat)
                self.detected_threats[threat_id] = threat
            
            return threats
            
        except Exception as e:
            self.logger.error(f"AI threat analysis failed: {str(e)}")
            return []
    
    async def _correlate_threats(self, threats: List[ThreatInfo]) -> List[ThreatInfo]:
        """Correlaciona amenazas relacionadas"""
        # Agrupar amenazas por IP de origen
        ip_threats = {}
        for threat in threats:
            if threat.source_ip:
                if threat.source_ip not in ip_threats:
                    ip_threats[threat.source_ip] = []
                ip_threats[threat.source_ip].append(threat)
        
        # Crear amenazas correlacionadas para IPs con múltiples ataques
        correlated_threats = list(threats)  # Empezar con todas las amenazas
        
        for ip, ip_threat_list in ip_threats.items():
            if len(ip_threat_list) > 1:
                # Crear amenaza correlacionada
                threat_id = f"correlated_{ip}_{uuid.uuid4().hex[:8]}"
                
                # Determinar severidad máxima
                max_severity = max(threat.severity for threat in ip_threat_list)
                
                # Combinar indicadores
                all_indicators = []
                all_mitigation_steps = []
                threat_types = []
                
                for threat in ip_threat_list:
                    all_indicators.extend(threat.indicators)
                    all_mitigation_steps.extend(threat.mitigation_steps)
                    threat_types.append(threat.threat_type)
                
                correlated_threat = ThreatInfo(
                    threat_id=threat_id,
                    threat_type="correlated_attack",
                    severity=max_severity,
                    source_ip=ip,
                    description=f"Correlated attack from {ip}: {', '.join(set(threat_types))}",
                    indicators=list(set(all_indicators)),
                    mitigation_steps=list(set(all_mitigation_steps + [f"Block IP {ip} immediately"]))
                )
                
                correlated_threats.append(correlated_threat)
                self.detected_threats[threat_id] = correlated_threat
        
        return correlated_threats
    
    async def _generate_automatic_responses(self, threats: List[ThreatInfo]):
        """Genera respuestas automáticas a amenazas"""
        for threat in threats:
            try:
                # Bloquear IPs maliciosas automáticamente
                if threat.source_ip and threat.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
                    await self.firewall_manager.block_malicious_ip(
                        ip_address=threat.source_ip,
                        threat_level=threat.severity,
                        duration_hours=24 if threat.severity == SeverityLevel.CRITICAL else 12
                    )
                    
                    self.logger.warning(f"Auto-blocked malicious IP: {threat.source_ip} (threat: {threat.threat_type})")
                
                # Generar alerta
                await self.logger.log_activity(
                    activity_type="threat_detected",
                    details={
                        "threat_id": threat.threat_id,
                        "threat_type": threat.threat_type,
                        "severity": threat.severity.value,
                        "source_ip": threat.source_ip,
                        "description": threat.description,
                        "auto_response": "ip_blocked" if threat.source_ip else "alert_only"
                    },
                    level="warning" if threat.severity == SeverityLevel.MEDIUM else "error",
                    save_to_firebase=True
                )
                
            except Exception as e:
                self.logger.error(f"Failed to generate automatic response for threat {threat.threat_id}: {str(e)}")
    
    def _get_mitigation_steps(self, threat_type: str) -> List[str]:
        """Obtiene pasos de mitigación para un tipo de amenaza"""
        mitigation_map = {
            "brute_force_ssh": [
                "Block source IP immediately",
                "Implement fail2ban or similar protection",
                "Use key-based authentication",
                "Change default SSH port"
            ],
            "sql_injection": [
                "Block source IP immediately",
                "Review and sanitize input validation",
                "Use parameterized queries",
                "Update web application firewall rules"
            ],
            "xss_attempt": [
                "Block source IP",
                "Implement proper input sanitization",
                "Use Content Security Policy (CSP)",
                "Update web application security"
            ],
            "directory_traversal": [
                "Block source IP immediately",
                "Review file access permissions",
                "Implement proper input validation",
                "Update web server configuration"
            ],
            "port_scan": [
                "Monitor source IP closely",
                "Consider blocking if persistent",
                "Review firewall rules",
                "Enable intrusion detection"
            ],
            "malware_signature": [
                "Block source IP immediately",
                "Scan affected systems for malware",
                "Review file uploads and execution",
                "Update antivirus signatures"
            ]
        }
        
        return mitigation_map.get(threat_type, ["Investigate further", "Monitor closely"])
    
    async def get_threat_status(self) -> Dict[str, Any]:
        """Obtiene estado actual de amenazas"""
        try:
            # Estadísticas básicas
            total_threats = len(self.detected_threats)
            
            # Amenazas por severidad
            severity_counts = {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            }
            
            # Amenazas por tipo
            type_counts = {}
            
            # Amenazas recientes (últimas 24 horas)
            recent_threats = []
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            
            for threat in self.detected_threats.values():
                # Contar por severidad
                severity_counts[threat.severity.value] += 1
                
                # Contar por tipo
                if threat.threat_type not in type_counts:
                    type_counts[threat.threat_type] = 0
                type_counts[threat.threat_type] += 1
                
                # Amenazas recientes
                if threat.detected_at >= cutoff_time:
                    recent_threats.append(threat)
            
            # Top IPs atacantes
            ip_threat_counts = {}
            for threat in self.detected_threats.values():
                if threat.source_ip:
                    if threat.source_ip not in ip_threat_counts:
                        ip_threat_counts[threat.source_ip] = 0
                    ip_threat_counts[threat.source_ip] += 1
            
            top_attacking_ips = sorted(
                ip_threat_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
            
            return {
                "success": True,
                "threat_status": {
                    "total_threats": total_threats,
                    "severity_distribution": severity_counts,
                    "threat_types": type_counts,
                    "recent_threats_24h": len(recent_threats),
                    "ai_analysis_enabled": self.ai_analysis_enabled,
                    "auto_response_enabled": self.auto_response_enabled
                },
                "top_attacking_ips": [
                    {"ip": ip, "threat_count": count} 
                    for ip, count in top_attacking_ips
                ],
                "recent_threats": [
                    threat.dict() for threat in sorted(
                        recent_threats,
                        key=lambda x: x.detected_at,
                        reverse=True
                    )[:10]
                ],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise AkiraOperationError(f"Failed to get threat status: {str(e)}")
    
    def list_detected_threats(self, severity_filter: Optional[SeverityLevel] = None) -> List[Dict[str, Any]]:
        """Lista amenazas detectadas con filtro opcional"""
        threats = list(self.detected_threats.values())
        
        if severity_filter:
            threats = [t for t in threats if t.severity == severity_filter]
        
        return [threat.dict() for threat in sorted(threats, key=lambda x: x.detected_at, reverse=True)]
    
    async def resolve_threat(self, threat_id: str) -> Dict[str, Any]:
        """Marca una amenaza como resuelta"""
        try:
            if threat_id not in self.detected_threats:
                raise AkiraOperationError(f"Threat not found: {threat_id}")
            
            threat = self.detected_threats[threat_id]
            threat.resolved = True
            threat.resolved_at = datetime.utcnow()
            
            # Log de actividad
            await self.logger.log_activity(
                activity_type="threat_resolved",
                details={
                    "threat_id": threat_id,
                    "threat_type": threat.threat_type,
                    "severity": threat.severity.value,
                    "source_ip": threat.source_ip
                },
                save_to_firebase=True
            )
            
            return {
                "success": True,
                "message": f"Threat {threat_id} marked as resolved",
                "threat_info": threat.dict()
            }
            
        except Exception as e:
            raise AkiraOperationError(f"Failed to resolve threat: {str(e)}")

# Instancia global del detector de amenazas
ai_threat_detector = AIThreatDetector()

def get_ai_threat_detector() -> AIThreatDetector:
    """Obtiene la instancia del detector de amenazas IA"""
    return ai_threat_detector