"""
SUME DOCBLOCK

Nombre: Configuración Central Akira
Tipo: Lógica

Entradas:
- Variables de entorno (.env)
- Firebase credentials JSON
- Configuración por defecto

Acciones:
- Carga y valida todas las configuraciones
- Inicializa settings globales
- Valida credenciales críticas

Salidas:
- Objeto settings configurado
- Validación exitosa o error específico
"""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional
import os
from pathlib import Path

class AkiraConfig(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API Key")
    
    # Firebase Configuration
    firebase_project_id: str = Field(..., description="Firebase Project ID")
    firebase_credentials_path: str = Field(default="firebase-credentials.json", description="Path to Firebase credentials")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API Host")
    api_port: int = Field(default=8000, description="API Port")
    api_reload: bool = Field(default=True, description="Auto-reload in development")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_to_console: bool = Field(default=True, description="Log to console")
    log_to_file: bool = Field(default=True, description="Log to file")
    log_file_path: str = Field(default="akira.log", description="Log file path")
    
    # Security
    api_secret_key: str = Field(..., description="API Secret Key")
    api_access_token: str = Field(..., description="API Access Token")
    
    # Environment
    environment: str = Field(default="development", description="Environment")
    debug: bool = Field(default=True, description="Debug mode")
    
    @field_validator('firebase_credentials_path')
    def validate_firebase_credentials(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Firebase credentials file not found: {v}")
        return v
    
    @field_validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of: {valid_levels}")
        return v.upper()
    
    @field_validator('environment')
    def validate_environment(cls, v):
        valid_envs = ['development', 'staging', 'production', 'testing']
        if v.lower() not in valid_envs:
            raise ValueError(f"Invalid environment. Must be one of: {valid_envs}")
        return v.lower()
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = AkiraConfig()

def get_settings() -> AkiraConfig:
    """Get application settings"""
    return settings
