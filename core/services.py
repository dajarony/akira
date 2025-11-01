# Contenido de core/services.py (Con tus fixes de import y métodos)
import json
import openai
import firebase_admin
import asyncio
from firebase_admin import credentials, firestore
from datetime import datetime
from typing import Dict, Any
from core.config import get_settings
from core.logger import get_logger
from core.exceptions import AkiraServiceError, AkiraConfigurationError

class OpenAIService:
    # ... (código sin cambios) ...
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    async def analyze_scan_results(self, scan_data: dict, target: str) -> dict:
        context = f"""Target: {target}
Scan results: {json.dumps(scan_data, indent=2, default=str)}"""
        prompt = "Analyze this data."
        response = self.client.chat.completions.create(model="gpt-4", messages=[{"role": "system", "content": "You are a cybersecurity expert."}, {"role": "user", "content": prompt}])
        return {"analysis": response.choices[0].message.content}

    async def health_check(self) -> Dict[str, Any]:
        try:
            # Intenta una llamada simple a la API para verificar la conectividad y la clave
            await self.client.models.list()
            return {"status": "healthy", "message": "OpenAI service is operational."}
        except openai.AuthenticationError:
            return {"status": "unhealthy", "message": "OpenAI authentication failed. Check API key."}
        except openai.APIConnectionError as e:
            return {"status": "unhealthy", "message": f"OpenAI connection error: {e}"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"OpenAI service error: {e}"}

class FirebaseService:
    def __init__(self, credentials_path: str, project_id: str):
        cred = credentials.Certificate(credentials_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {'projectId': project_id})
        self.db = firestore.client()
        self.logger = get_logger()
        self.environment = get_settings().environment

    async def save_activity(self, activity_data: Dict[str, Any]):
        try:
            doc_ref = self.db.collection('activities').document()
            await asyncio.to_thread(doc_ref.set, activity_data)
        except Exception as e:
            self.logger.warning(f"Failed to save activity to Firebase: {e}")

    # MÉTODO AÑADIDO (TU FIX #3)
    async def save_defense_action(self, action_data: Dict[str, Any]) -> bool:
        try:
            doc_ref = self.db.collection('defense_actions').document()
            await asyncio.to_thread(doc_ref.set, {'payload': action_data, 'timestamp': datetime.utcnow()})
            return True
        except Exception as e:
            self.logger.warning(f"Failed to save defense action: {e}")
            return False

    # MÉTODO MEJORADO (TU FIX #3)
    async def save_scan_results(self, scan_data: Dict[str, Any]) -> bool:
        try:
            doc_ref = self.db.collection('scan_results').document()
            await asyncio.to_thread(doc_ref.set, {'payload': scan_data, 'timestamp': datetime.utcnow()})
            return True
        except Exception as e:
            self.logger.warning(f"Failed to save scan results: {e}")
            return False
            
    async def get_scan_history(self, target: str, limit: int = 5) -> list:
        try:
            query = self.db.collection('scan_results').where('payload.target', '==', target).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
            docs = await asyncio.to_thread(query.stream)
            return [doc.to_dict() for doc in docs]
        except Exception as e:
             self.logger.error(f"Firestore query failed, possibly requires an index: {e}")
             return []

    async def health_check(self) -> Dict[str, Any]:
        try:
            # Intenta una operación simple de lectura/escritura para verificar la conectividad
            test_doc_ref = self.db.collection('health_checks').document('test_doc')
            await asyncio.to_thread(test_doc_ref.set, {'timestamp': datetime.utcnow()})
            await asyncio.to_thread(test_doc_ref.get)
            return {"status": "healthy", "message": "Firebase service is operational."}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Firebase service error: {e}"}


class AkiraServices:
    # ... (código sin cambios) ...
    def __init__(self):
        self.settings = get_settings(); self.logger = get_logger(); self._initialized = False
    async def initialize(self):
        if self._initialized: return
        self.openai_service = OpenAIService(self.settings.openai_api_key)
        self.firebase_service = FirebaseService(self.settings.firebase_credentials_path, self.settings.firebase_project_id)
        self.logger.set_firebase_service(self.firebase_service)
        self._initialized = True

    async def health_check(self) -> Dict[str, Any]:
        results = {}
        overall_status = "healthy"

        # Check OpenAI Service
        if hasattr(self, 'openai_service') and self.openai_service:
            openai_health = await self.openai_service.health_check()
            results["openai"] = openai_health
            if openai_health["status"] != "healthy":
                overall_status = "degraded"
        else:
            results["openai"] = {"status": "uninitialized", "message": "OpenAI service not initialized."}
            overall_status = "degraded"

        # Check Firebase Service
        if hasattr(self, 'firebase_service') and self.firebase_service:
            firebase_health = await self.firebase_service.health_check()
            results["firebase"] = firebase_health
            if firebase_health["status"] != "healthy":
                overall_status = "degraded"
        else:
            results["firebase"] = {"status": "uninitialized", "message": "Firebase service not initialized."}
            overall_status = "degraded"

        return {"overall_status": overall_status, "services": results}

akira_services = AkiraServices()
def get_services() -> AkiraServices:
    return akira_services
