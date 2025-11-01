"""
SUME DOCBLOCK

Nombre: Sistema de Autenticación JWT Akira
Tipo: Core/Seguridad

Entradas:
- Credenciales de usuario
- Tokens JWT para validación
- Refresh tokens

Acciones:
- Genera tokens JWT seguros
- Valida tokens de acceso
- Gestiona refresh tokens
- Verifica permisos de usuario

Salidas:
- Tokens JWT firmados
- Validación de autenticación
- Información de usuario autenticado
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import secrets

from core import get_settings, get_logger
from core.exceptions import AkiraSecurityError

# Contexto de encriptación para passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenData(BaseModel):
    """Datos contenidos en el token"""
    username: Optional[str] = None
    user_id: Optional[str] = None
    scopes: list[str] = []
    exp: Optional[datetime] = None

class Token(BaseModel):
    """Respuesta de token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class User(BaseModel):
    """Modelo de usuario"""
    username: str
    user_id: str
    email: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False
    scopes: list[str] = []
    api_key: Optional[str] = None

class AuthManager:
    """Gestor de autenticación JWT"""

    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger()

        # Configuración JWT
        self.secret_key = getattr(self.settings, 'jwt_secret_key', self.settings.api_secret_key)
        self.algorithm = getattr(self.settings, 'jwt_algorithm', 'HS256')
        self.access_token_expire_minutes = getattr(self.settings, 'jwt_access_token_expire_minutes', 30)
        self.refresh_token_expire_days = getattr(self.settings, 'jwt_refresh_token_expire_days', 7)

        # Base de datos temporal de usuarios (en producción usar DB real)
        self._users_db: Dict[str, Dict[str, Any]] = {}
        self._revoked_tokens: set[str] = set()

    def hash_password(self, password: str) -> str:
        """Hashea una contraseña"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash"""
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crea un token JWT de acceso"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """Crea un token JWT de refresh"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> TokenData:
        """Verifica y decodifica un token JWT"""
        try:
            # Verificar si el token ha sido revocado
            if token in self._revoked_tokens:
                raise AkiraSecurityError("Token has been revoked")

            # Decodificar token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            username: str = payload.get("sub")
            user_id: str = payload.get("user_id")
            scopes: list = payload.get("scopes", [])
            exp: datetime = datetime.fromtimestamp(payload.get("exp"))

            if username is None:
                raise AkiraSecurityError("Invalid token: missing username")

            token_data = TokenData(
                username=username,
                user_id=user_id,
                scopes=scopes,
                exp=exp
            )

            return token_data

        except JWTError as e:
            raise AkiraSecurityError(f"Invalid token: {str(e)}")

    def revoke_token(self, token: str):
        """Revoca un token (logout)"""
        self._revoked_tokens.add(token)
        self.logger.info(f"Token revoked")

    def generate_api_key(self) -> str:
        """Genera una API key segura"""
        return f"ak_{secrets.token_urlsafe(32)}"

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autentica un usuario"""
        user_data = self._users_db.get(username)

        if not user_data:
            return None

        if not self.verify_password(password, user_data["hashed_password"]):
            return None

        return User(**user_data["user"])

    def create_user(self, username: str, password: str, email: str, is_admin: bool = False) -> User:
        """Crea un nuevo usuario"""
        if username in self._users_db:
            raise AkiraSecurityError(f"User {username} already exists")

        user_id = secrets.token_urlsafe(16)
        api_key = self.generate_api_key()
        hashed_password = self.hash_password(password)

        user = User(
            username=username,
            user_id=user_id,
            email=email,
            is_admin=is_admin,
            scopes=["scan:read", "scan:write"] + (["admin:all"] if is_admin else []),
            api_key=api_key
        )

        self._users_db[username] = {
            "user": user.dict(),
            "hashed_password": hashed_password
        }

        self.logger.info(f"User created: {username}")
        return user

    async def login(self, username: str, password: str) -> Token:
        """Login y genera tokens"""
        user = self.authenticate_user(username, password)

        if not user:
            raise AkiraSecurityError("Invalid username or password")

        if not user.is_active:
            raise AkiraSecurityError("User account is disabled")

        # Crear tokens
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)

        access_token = self.create_access_token(
            data={
                "sub": user.username,
                "user_id": user.user_id,
                "scopes": user.scopes
            },
            expires_delta=access_token_expires
        )

        refresh_token = self.create_refresh_token(
            data={
                "sub": user.username,
                "user_id": user.user_id
            }
        )

        await self.logger.log_activity(
            activity_type="user_login",
            details={
                "username": username,
                "user_id": user.user_id,
                "timestamp": datetime.utcnow().isoformat()
            },
            save_to_firebase=True
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.access_token_expire_minutes * 60
        )

    def refresh_access_token(self, refresh_token: str) -> Token:
        """Refresh token para obtener nuevo access token"""
        try:
            token_data = self.verify_token(refresh_token)

            # Crear nuevo access token
            access_token_expires = timedelta(minutes=self.access_token_expire_minutes)

            access_token = self.create_access_token(
                data={
                    "sub": token_data.username,
                    "user_id": token_data.user_id,
                    "scopes": token_data.scopes
                },
                expires_delta=access_token_expires
            )

            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=self.access_token_expire_minutes * 60
            )

        except Exception as e:
            raise AkiraSecurityError(f"Failed to refresh token: {str(e)}")

    def verify_api_key(self, api_key: str) -> Optional[User]:
        """Verifica una API key"""
        for user_data in self._users_db.values():
            user = User(**user_data["user"])
            if user.api_key == api_key:
                return user
        return None

    def has_permission(self, user: User, required_scope: str) -> bool:
        """Verifica si el usuario tiene un permiso específico"""
        if "admin:all" in user.scopes:
            return True
        return required_scope in user.scopes

# Instancia global del gestor de autenticación
_auth_manager = None

def get_auth_manager() -> AuthManager:
    """Obtiene la instancia del gestor de autenticación"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager
