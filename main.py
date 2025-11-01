"""
SUME DOCBLOCK

Nombre: Aplicación Principal Akira SASE Cyberwar MVP
Tipo: Entrada

Entradas:
- Configuración del sistema (.env)
- Requests HTTP de clientes
- Conexiones WebSocket (futuro)

Acciones:
- Inicializa servicios (OpenAI, Firebase)
- Configura FastAPI con routers
- Gestiona autenticación y CORS
- Maneja lifecycle de la aplicación
- Configura middleware de logging

Salidas:
- API REST completamente funcional
- Documentación automática (Swagger)
- Servicios inicializados y operativos
- Sistema de logging activo
"""

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
import time
from typing import Optional
import sys
import os

# Agregar el directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core import (
    get_settings, get_logger, get_services, get_error_handler,
    AkiraBaseException, AkiraConfigurationError
)
from api import offense_router, defense_router, status_router

# Configuración global
settings = get_settings()
logger = get_logger()
services = get_services()
error_handler = get_error_handler()

# Esquema de autenticación
security = HTTPBearer(auto_error=False)

async def verify_api_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica token de autenticación API"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Authentication required",
                "message": "API token must be provided in Authorization header"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if credentials.credentials != settings.api_access_token:
        await logger.log_activity(
            activity_type="security_alert",
            details={
                "event": "invalid_api_token",
                "provided_token": credentials.credentials[:10] + "...",
                "source": "api_authentication"
            },
            save_to_firebase=True
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid authentication",
                "message": "Invalid API token provided"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación"""
    # Startup
    try:
        logger.info("🚀 Akira SASE Cyberwar MVP starting up...")
        
        # Verificar configuración crítica
        logger.info("🔧 Validating configuration...")
        if not settings.openai_api_key or settings.openai_api_key == "sk-proj-your-key-here":
            raise AkiraConfigurationError("OpenAI API key not configured")
        
        if not settings.firebase_project_id:
            raise AkiraConfigurationError("Firebase project ID not configured")
        
        # Inicializar servicios
        logger.info("🔗 Initializing services...")
        await services.initialize()
        
        # Log de inicio exitoso
        await logger.log_activity(
            activity_type="system_startup",
            details={
                "version": "1.0.0-MVP",
                "environment": settings.environment,
                "services": ["openai", "firebase", "logging"],
                "api_host": settings.api_host,
                "api_port": settings.api_port
            },
            save_to_firebase=True
        )
        
        logger.info("✅ Akira SASE Cyberwar MVP initialized successfully")
        logger.info(f"🌐 API running on {settings.api_host}:{settings.api_port}")
        logger.info(f"📚 Documentation available at http://{settings.api_host}:{settings.api_port}/docs")
        
        yield
        
    except Exception as e:
        logger.critical(f"❌ Failed to initialize Akira: {str(e)}")
        raise
    
    # Shutdown
    try:
        logger.info("🛑 Akira SASE Cyberwar MVP shutting down...")
        
        # Log de shutdown
        await logger.log_activity(
            activity_type="system_shutdown",
            details={
                "reason": "normal_shutdown",
                "environment": settings.environment
            },
            save_to_firebase=True
        )
        
        logger.info("✅ Akira shutdown completed")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")

# Crear aplicación FastAPI
app = FastAPI(
    title="Akira SASE Cyberwar MVP",
    description="""
    ## 🛡️⚔️ Akira SASE Cyberwar MVP - Sistema Híbrido de Ciberseguridad
    
    **Arquitectura SUME + STDG** - Sistema modular para operaciones ofensivas y defensivas éticas.
    
    ### 🎯 Funcionalidades Principales:
    
    #### 🔴 Operaciones Ofensivas:
    - **Escaneo Nmap**: Escaneos de red completos con análisis IA
    - **Recolección OSINT**: Inteligencia de fuentes abiertas automatizada  
    - **Exploits Éticos**: Verificación de vulnerabilidades controlada
    
    #### 🔵 Operaciones Defensivas:
    - **Gestión Firewall**: Reglas automáticas y bloqueo de amenazas
    - **Honeypots**: Señuelos inteligentes para detectar atacantes
    - **Detección IA**: Análisis de amenazas con OpenAI GPT-4
    
    #### 📊 Monitoreo y Control:
    - **Estado del Sistema**: Salud de servicios y recursos
    - **Logs Centralizados**: Auditoría completa de actividades
    - **Estadísticas**: Métricas de seguridad en tiempo real
    
    ### 🔧 Tecnologías:
    - **FastAPI**: API REST de alto rendimiento
    - **OpenAI GPT-4**: Análisis inteligente de seguridad
    - **Firebase**: Almacenamiento y analytics en tiempo real
    - **Nmap**: Escaneo de red profesional
    - **Python**: Backend robusto y escalable
    
    ### 🔐 Autenticación:
    Incluir header: Authorization: Bearer {tu_api_token}
    
    ### ⚠️ Uso Ético:
    Este sistema está diseñado exclusivamente para:
    - Pruebas de penetración autorizadas
    - Auditorías de seguridad internas
    - Investigación de ciberseguridad ética
    - Entrenamiento y educación
    
    **NUNCA usar contra sistemas sin autorización explícita.**
    """,
    version="1.0.0-MVP",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    contact={
        "name": "Akira Security Team",
        "email": "security@akira-cyber.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware de hosts confiables (seguridad)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.environment == "development" else ["localhost", "127.0.0.1"]
)

# Middleware de logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de todas las requests"""
    start_time = time.time()
    
    # Obtener información de la request
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    url = str(request.url)
    user_agent = request.headers.get("user-agent", "unknown")
    
    try:
        # Procesar request
        response = await call_next(request)
        
        # Calcular tiempo de procesamiento
        process_time = time.time() - start_time
        
        # Log de la request
        if response.status_code >= 400:
            log_level = "warning" if response.status_code < 500 else "error"
        else:
            log_level = "info"
        
        await logger.log_activity(
            activity_type="api_request",
            details={
                "method": method,
                "url": url,
                "status_code": response.status_code,
                "client_ip": client_ip,
                "user_agent": user_agent,
                "process_time_ms": round(process_time * 1000, 2)
            },
            level=log_level,
            save_to_firebase=False  # No spam Firebase con todas las requests
        )
        
        # Agregar headers de respuesta
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Akira-Version"] = "1.0.0-MVP"
        
        return response
        
    except Exception as e:
        # Log de error
        process_time = time.time() - start_time
        
        await logger.log_activity(
            activity_type="api_error",
            details={
                "method": method,
                "url": url,
                "client_ip": client_ip,
                "error": str(e),
                "process_time_ms": round(process_time * 1000, 2)
            },
            level="error",
            save_to_firebase=True
        )
        
        # Re-lanzar excepción
        raise

# Manejadores de errores globales
@app.exception_handler(AkiraBaseException)
async def akira_exception_handler(request: Request, exc: AkiraBaseException):
    """Maneja excepciones personalizadas de Akira"""
    return JSONResponse(
        status_code=400,
        content={
            "error": type(exc).__name__,
            "message": exc.message,
            "details": exc.details,
            "timestamp": time.time()
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic"""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": exc.errors(),
            "timestamp": time.time()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Maneja excepciones HTTP estándar"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"HTTP {exc.status_code}",
            "message": exc.detail,
            "timestamp": time.time()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones no capturadas"""
    await logger.log_activity(
        activity_type="unhandled_error",
        details={
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "url": str(request.url),
            "method": request.method
        },
        level="critical",
        save_to_firebase=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "timestamp": time.time()
        }
    )

# Incluir routers con autenticación
app.include_router(
    offense_router, 
    dependencies=[Depends(verify_api_token)]
)
app.include_router(
    defense_router, 
    dependencies=[Depends(verify_api_token)]
)
app.include_router(
    status_router, 
    dependencies=[Depends(verify_api_token)]
)

# Incluir endpoints de defensa adicionales
from api.defense_endpoints import defense_router as defense_endpoints_router
app.include_router(
    defense_endpoints_router,
    dependencies=[Depends(verify_api_token)]
)

# Incluir nuevos endpoints de defensa
from api.defense_endpoints import defense_router as defense_endpoints_router
app.include_router(
    defense_endpoints_router,
    dependencies=[Depends(verify_api_token)]
)

# Endpoints públicos (sin autenticación)
@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz - Información básica de Akira"""
    return {
        "name": "Akira SASE Cyberwar MVP",
        "version": "1.0.0-MVP",
        "architecture": "SUME + STDG",
        "description": "Sistema híbrido de ciberseguridad ofensiva y defensiva",
        "status": "operational",
        "documentation": "/docs",
        "health_check": "/status/health",
        "authentication": "Bearer token required for all operations",
        "ethical_use_only": True,
        "contact": "security@akira-cyber.com"
    }

@app.get("/ping", tags=["Root"])
async def ping():
    """Health check simple sin autenticación"""
    return {
        "status": "pong",
        "timestamp": time.time(),
        "service": "akira-api"
    }

# Punto de entrada para ejecución directa
if __name__ == "__main__":
    try:
        logger.info("🔥 Starting Akira SASE Cyberwar MVP...")
        
        # Configuración de uvicorn
        uvicorn.run(
            "main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=settings.api_reload and settings.environment == "development",
            log_level=settings.log_level.lower(),
            access_log=True,
            server_header=False,  # Ocultar header del servidor por seguridad
            date_header=False     # Ocultar fecha por seguridad
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Akira stopped by user")
    except Exception as e:
        logger.critical(f"❌ Failed to start Akira: {str(e)}")
        sys.exit(1)
