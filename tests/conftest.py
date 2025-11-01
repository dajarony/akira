"""
Test Configuration and Fixtures
Configura el entorno de pruebas antes de ejecutar los tests
"""

import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv

# Obtener el directorio raíz del proyecto
ROOT_DIR = Path(__file__).parent.parent
TESTS_DIR = Path(__file__).parent

# Agregar el directorio raíz al path ANTES de cualquier import
sys.path.insert(0, str(ROOT_DIR))

# Cargar variables de entorno de test
env_test_path = TESTS_DIR / ".env.test"
if env_test_path.exists():
    load_dotenv(env_test_path, override=True)
else:
    # Configurar variables de entorno mínimas para tests
    os.environ.setdefault("OPENAI_API_KEY", "sk-test-fake-key-for-testing")
    os.environ.setdefault("FIREBASE_PROJECT_ID", "akira-test")
    os.environ.setdefault("FIREBASE_CREDENTIALS_PATH", str(TESTS_DIR / "firebase-credentials-test.json"))
    os.environ.setdefault("API_SECRET_KEY", "test-secret-key")
    os.environ.setdefault("API_ACCESS_TOKEN", "test-access-token")
    os.environ.setdefault("ENVIRONMENT", "testing")
    os.environ.setdefault("DEBUG", "false")
    os.environ.setdefault("LOG_TO_CONSOLE", "false")
    os.environ.setdefault("LOG_TO_FILE", "false")

# Cambiar al directorio de tests para paths relativos
os.chdir(TESTS_DIR)

@pytest.fixture(scope="session")
def test_env():
    """Fixture que provee configuración de test"""
    return {
        "api_token": os.getenv("API_ACCESS_TOKEN", "test-access-token"),
        "api_base_url": "http://localhost:8000",
        "environment": "testing"
    }

@pytest.fixture(scope="function")
def mock_firebase_service():
    """Mock del servicio Firebase para tests"""
    from unittest.mock import AsyncMock, MagicMock

    mock_service = MagicMock()
    mock_service.save_activity = AsyncMock(return_value=True)
    mock_service.save_scan_results = AsyncMock(return_value=True)
    mock_service.save_defense_action = AsyncMock(return_value=True)
    mock_service.get_scan_history = AsyncMock(return_value=[])
    mock_service.health_check = AsyncMock(return_value={
        "status": "healthy",
        "message": "Firebase service is operational."
    })

    return mock_service

@pytest.fixture(scope="function")
def mock_openai_service():
    """Mock del servicio OpenAI para tests"""
    from unittest.mock import AsyncMock, MagicMock

    mock_service = MagicMock()
    mock_service.analyze_scan_results = AsyncMock(return_value={
        "analysis": "Test analysis from AI"
    })
    mock_service.health_check = AsyncMock(return_value={
        "status": "healthy",
        "message": "OpenAI service is operational."
    })

    return mock_service

@pytest.fixture(scope="function")
async def mock_services(mock_firebase_service, mock_openai_service):
    """Mock completo de AkiraServices"""
    from unittest.mock import MagicMock

    mock = MagicMock()
    mock._initialized = True
    mock.firebase_service = mock_firebase_service
    mock.openai_service = mock_openai_service
    mock.health_check = AsyncMock(return_value={
        "overall_status": "healthy",
        "services": {
            "openai": {"status": "healthy"},
            "firebase": {"status": "healthy"}
        }
    })

    return mock

# Configurar pytest-asyncio
def pytest_configure(config):
    """Configuración global de pytest"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
