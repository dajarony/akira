"""
SUME DOCBLOCK

Nombre: API Endpoints Ofensivos Akira
Tipo: Entrada

Entradas:
- Requests HTTP con parámetros de escaneo/exploit
- Headers de autenticación
- Datos JSON de configuración

Acciones:
- Procesa requests de operaciones ofensivas
- Ejecuta escaneos nmap reales
- Realiza recolección OSINT
- Lanza exploits éticos
- Integra análisis IA y Firebase

Salidas:
- Respuestas JSON estructuradas
- Resultados de escaneos y exploits
- Análisis de IA incluido
- Datos guardados en Firebase
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime

from core import get_logger, get_services, get_error_handler
from models import (
    ScanRequest, ScanResponse, ScanResults,
    OSINTRequest, OSINTResponse, OSINTResults,
    ExploitRequest, ExploitResponse, ExploitResults,
    BaseResponse, ErrorResponse, ExploitCategory
)
from modules.offense import get_nmap_scanner, get_osint_collector, get_exploit_launcher
from modules.shared import validate_input, BusinessValidators

router = APIRouter(prefix="/offense", tags=["Offensive Operations"])
logger = get_logger()
error_handler = get_error_handler()

@router.post("/nmap", response_model=ScanResponse)
async def execute_nmap_scan(
    scan_request: ScanRequest,
    background_tasks: BackgroundTasks
) -> ScanResponse:
    """
    Ejecuta escaneo Nmap real del target especificado
    
    - **target**: IP o hostname a escanear
    - **scan_type**: Tipo de escaneo (tcp_syn, stealth, aggressive, etc.)
    - **port_range**: Rango de puertos (ej: "1-1000" o "80,443,22")
    - **ai_analysis**: Si incluir análisis con IA
    - **save_results**: Si guardar en Firebase
    """
    start_time = datetime.utcnow()
    
    try:
        await logger.log_activity(
            activity_type="scan",
            details={
                "endpoint": "/offense/nmap",
                "target": scan_request.target.ip or scan_request.target.hostname,
                "scan_type": scan_request.scan_type.value
            },
            save_to_firebase=True
        )
        
        # Validar target
        target_data = {
            "ip": scan_request.target.ip,
            "hostname": scan_request.target.hostname
        }
        
        is_valid, validation_error = BusinessValidators.validate_scan_target(
            target_data.get("ip"), target_data.get("hostname")
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid scan target",
                    "message": validation_error,
                    "target": target_data
                }
            )
        
        # Obtener servicios
        services = get_services()
        if not services._initialized:
            await services.initialize()
        
        # Ejecutar escaneo
        nmap_scanner = get_nmap_scanner()
        scan_results = await nmap_scanner.scan_target(scan_request)
        
        # Análisis con IA si está habilitado
        ai_analysis = None
        if scan_request.ai_analysis and services.openai_service:
            try:
                # Obtener historial para contexto
                scan_history = await nmap_scanner.get_scan_history(
                    scan_results.target, limit=5
                )
                
                # Generar análisis IA
                ai_response = await services.openai_service.analyze_scan_results(
                    scan_results.dict(),
                    scan_results.target,
                    scan_history
                )
                
                ai_analysis = {
                    "model_used": "gpt-4",
                    "confidence_score": 0.85,
                    "analysis_text": ai_response["analysis"],
                    "recommendations": [],
                    "risk_level": "medium",
                    "timestamp": datetime.utcnow()
                }
                
            except Exception as e:
                logger.warning(f"AI analysis failed: {str(e)}")
        
        # Calcular tiempo de ejecución
        execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return ScanResponse(
            success=True,
            message=f"Nmap scan completed successfully. Found {scan_results.hosts_found} hosts with {sum(len(h.ports) for h in scan_results.hosts)} total ports.",
            execution_time_ms=execution_time,
            scan_results=scan_results,
            ai_analysis=ai_analysis,
            saved_to_firebase=scan_request.save_results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Nmap scan failed: {str(e)}")
        http_exception = await error_handler.handle_operation_error(
            e, "nmap_scan", scan_request.target.ip or scan_request.target.hostname
        )
        raise http_exception

@router.post("/osint", response_model=OSINTResponse)
async def execute_osint_collection(
    osint_request: OSINTRequest,
    background_tasks: BackgroundTasks
) -> OSINTResponse:
    """
    Ejecuta recolección OSINT del target especificado
    
    - **target_domain**: Dominio a investigar
    - **target_email**: Email a investigar
    - **sources**: Fuentes OSINT a consultar
    - **depth_level**: Profundidad de la investigación (1-3)
    - **ai_analysis**: Si incluir análisis con IA
    """
    start_time = datetime.utcnow()
    
    try:
        target = (osint_request.target_domain or 
                 osint_request.target_email or 
                 osint_request.target_username or 
                 osint_request.company_name)
        
        await logger.log_activity(
            activity_type="osint",
            details={
                "endpoint": "/offense/osint",
                "target": target,
                "sources": [s.value for s in osint_request.sources],
                "depth_level": osint_request.depth_level
            },
            save_to_firebase=True
        )
        
        # Validaciones básicas
        if not target:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Missing target",
                    "message": "At least one target (domain, email, username, or company) must be provided"
                }
            )
        
        # Validar email si está presente
        if osint_request.target_email:
            is_valid, validation_error = validate_input("email", osint_request.target_email)
            if not is_valid:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "Invalid email",
                        "message": validation_error
                    }
                )
        
        # Validar dominio si está presente
        if osint_request.target_domain:
            is_valid, validation_error = validate_input("hostname", osint_request.target_domain)
            if not is_valid:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "Invalid domain",
                        "message": validation_error
                    }
                )
        
        # Obtener servicios
        services = get_services()
        if not services._initialized:
            await services.initialize()
        
        # Ejecutar recolección OSINT
        osint_collector = get_osint_collector()
        osint_results = await osint_collector.collect_osint(osint_request)
        
        # Análisis con IA si está habilitado
        ai_analysis = None
        if osint_request.ai_analysis and services.openai_service:
            try:
                # Preparar datos para análisis IA
                osint_summary = {
                    "target": target,
                    "domains_found": len(osint_results.domains),
                    "subdomains_found": len(osint_results.subdomains),
                    "emails_found": len(osint_results.emails),
                    "technologies": osint_results.technologies,
                    "summary": osint_results.summary
                }
                
                ai_response = await services.openai_service.analyze_scan_results(
                    osint_summary,
                    target,
                    []  # Sin historial para OSINT
                )
                
                ai_analysis = {
                    "model_used": "gpt-4",
                    "confidence_score": 0.80,
                    "analysis_text": ai_response["analysis"],
                    "recommendations": [],
                    "risk_level": "low",
                    "timestamp": datetime.utcnow()
                }
                
            except Exception as e:
                logger.warning(f"OSINT AI analysis failed: {str(e)}")
        
        # Calcular tiempo de ejecución
        execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return OSINTResponse(
            success=True,
            message=f"OSINT collection completed. Found {osint_results.summary.get('domains_found', 0)} domains, {osint_results.summary.get('subdomains_found', 0)} subdomains, {osint_results.summary.get('emails_found', 0)} emails.",
            execution_time_ms=execution_time,
            osint_results=osint_results,
            ai_analysis=ai_analysis,
            saved_to_firebase=osint_request.save_results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OSINT collection failed: {str(e)}")
        http_exception = await error_handler.handle_operation_error(
            e, "osint_collection", target
        )
        raise http_exception

@router.post("/exploit", response_model=ExploitResponse)
async def launch_exploit(
    exploit_request: ExploitRequest,
    background_tasks: BackgroundTasks
) -> ExploitResponse:
    """
    Lanza exploit ético para verificación de vulnerabilidades
    
    - **target**: IP o hostname objetivo
    - **exploit_id**: ID del exploit a usar
    - **verification_only**: Solo verificar vulnerabilidad (recomendado)
    - **category**: Categoría del exploit
    - **timeout_seconds**: Timeout para la operación
    """
    start_time = datetime.utcnow()
    
    try:
        target = exploit_request.target.ip or exploit_request.target.hostname
        
        await logger.log_activity(
            activity_type="exploit",
            details={
                "endpoint": "/offense/exploit",
                "target": target,
                "exploit_id": exploit_request.exploit_id,
                "verification_only": exploit_request.verification_only,
                "category": exploit_request.category.value
            },
            save_to_firebase=True
        )
        
        # Validar request
        exploit_data = exploit_request.dict()
        is_valid, validation_error = BusinessValidators.validate_exploit_request(exploit_data)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid exploit request",
                    "message": validation_error
                }
            )
        
        # Forzar verificación únicamente para seguridad
        if not exploit_request.verification_only:
            logger.warning(f"Forcing verification_only mode for exploit {exploit_request.exploit_id}")
            exploit_request.verification_only = True
        
        # Obtener servicios
        services = get_services()
        if not services._initialized:
            await services.initialize()
        
        # Ejecutar exploit
        exploit_launcher = get_exploit_launcher()
        exploit_results = await exploit_launcher.launch_exploit(exploit_request)
        
        # Generar recomendaciones de seguridad
        security_recommendations = [
            "Review and patch identified vulnerabilities immediately",
            "Implement proper network segmentation",
            "Enable monitoring and alerting for suspicious activities",
            "Conduct regular security assessments"
        ]
        
        if exploit_results.vulnerability_confirmed:
            security_recommendations.insert(0, "CRITICAL: Vulnerability confirmed - apply patches immediately")
        
        # Calcular tiempo de ejecución
        execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return ExploitResponse(
            success=True,
            message=f"Exploit verification completed. Vulnerability {'confirmed' if exploit_results.vulnerability_confirmed else 'not confirmed'}.",
            execution_time_ms=execution_time,
            exploit_results=exploit_results,
            security_recommendations=security_recommendations,
            saved_to_firebase=exploit_request.save_results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Exploit launch failed: {str(e)}")
        http_exception = await error_handler.handle_operation_error(
            e, "exploit_launch", target
        )
        raise http_exception

@router.get("/exploits", response_model=Dict[str, Any])
async def list_available_exploits() -> Dict[str, Any]:
    """
    Lista todos los exploits disponibles en el sistema
    
    Retorna información detallada de cada exploit incluyendo:
    - Nombre y descripción
    - Categoría y nivel de riesgo
    - Método de verificación
    - Recomendaciones de remediación
    """
    try:
        await logger.log_activity(
            activity_type="system_event",
            details={
                "endpoint": "/offense/exploits",
                "action": "list_exploits"
            },
            save_to_firebase=False
        )
        
        exploit_launcher = get_exploit_launcher()
        exploits_db = exploit_launcher.list_available_exploits()
        
        # Organizar por categoría
        exploits_by_category = {}
        for exploit_id, exploit_info in exploits_db.items():
            category = exploit_info.get("category", "unknown")
            if category not in exploits_by_category:
                exploits_by_category[category] = {}
            
            exploits_by_category[category][exploit_id] = {
                "name": exploit_info.get("name", "Unknown"),
                "description": exploit_info.get("description", "No description"),
                "risk_level": exploit_info.get("risk_level", "unknown"),
                "verification_method": exploit_info.get("verification_method", "manual"),
                "remediation": exploit_info.get("remediation", "Contact security team")
            }
        
        return {
            "success": True,
            "message": f"Found {len(exploits_db)} available exploits",
            "total_exploits": len(exploits_db),
            "exploits_by_category": exploits_by_category,
            "categories": list(exploits_by_category.keys()),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to list exploits: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve exploits",
                "message": str(e)
            }
        )

@router.get("/exploits/{category}", response_model=Dict[str, Any])
async def list_exploits_by_category(category: ExploitCategory) -> Dict[str, Any]:
    """
    Lista exploits por categoría específica
    
    - **category**: Categoría de exploits (web_app, network, system, etc.)
    """
    try:
        await logger.log_activity(
            activity_type="system_event",
            details={
                "endpoint": f"/offense/exploits/{category.value}",
                "action": "list_exploits_by_category",
                "category": category.value
            },
            save_to_firebase=False
        )
        
        exploit_launcher = get_exploit_launcher()
        category_exploits = exploit_launcher.get_exploit_by_category(category)
        
        if not category_exploits:
            return {
                "success": True,
                "message": f"No exploits found for category: {category.value}",
                "category": category.value,
                "exploits": {},
                "count": 0,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Formatear exploits para respuesta
        formatted_exploits = {}
        for exploit_id, exploit_info in category_exploits.items():
            formatted_exploits[exploit_id] = {
                "name": exploit_info.get("name", "Unknown"),
                "description": exploit_info.get("description", "No description"),
                "risk_level": exploit_info.get("risk_level", "unknown"),
                "verification_method": exploit_info.get("verification_method", "manual"),
                "remediation": exploit_info.get("remediation", "Contact security team")
            }
        
        return {
            "success": True,
            "message": f"Found {len(category_exploits)} exploits in category: {category.value}",
            "category": category.value,
            "exploits": formatted_exploits,
            "count": len(category_exploits),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to list exploits by category: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve exploits by category",
                "message": str(e),
                "category": category.value
            }
        )

@router.get("/scan-history/{target}", response_model=Dict[str, Any])
async def get_scan_history(
    target: str,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Obtiene historial de escaneos para un target específico
    
    - **target**: IP o hostname del cual obtener historial
    - **limit**: Número máximo de escaneos a retornar
    """
    try:
        # Validar target
        if not target:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid target",
                    "message": "Target cannot be empty"
                }
            )
        
        # Validar limit
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid limit",
                    "message": "Limit must be between 1 and 100"
                }
            )
        
        await logger.log_activity(
            activity_type="system_event",
            details={
                "endpoint": f"/offense/scan-history/{target}",
                "action": "get_scan_history",
                "target": target,
                "limit": limit
            },
            save_to_firebase=False
        )
        
        nmap_scanner = get_nmap_scanner()
        scan_history = await nmap_scanner.get_scan_history(target, limit)
        
        return {
            "success": True,
            "message": f"Retrieved {len(scan_history)} scan records for target: {target}",
            "target": target,
            "scan_history": scan_history,
            "count": len(scan_history),
            "limit": limit,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get scan history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve scan history",
                "message": str(e),
                "target": target
            }
        )
