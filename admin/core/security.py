import hashlib
import hmac
from datetime import datetime, timedelta, UTC
from typing import Optional

try:
    import jwt  # PyJWT
    from jwt.exceptions import PyJWTError # AJOUT DE L'IMPORTATION DE L'EXCEPTION DE PYJWT
except ImportError:
    jwt = None

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db


# ==========================================
# PASSWORD HASHING
# ==========================================

def get_password_hash(password: str) -> str:
    """
    Very simple hash using sha256.
    For production, use bcrypt/argon2.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Securely compare a plain password with its hash."""
    return hmac.compare_digest(get_password_hash(plain_password), hashed_password)


# ==========================================
# JWT TOKEN
# ==========================================

def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.
    Requires PyJWT (`pip install PyJWT`).
    """
    if jwt is None:
        raise RuntimeError("PyJWT is not installed. Install it to use JWT tokens.")

    to_encode = data.copy()
    expire = datetime.now(UTC) + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT token.
    Returns the payload if valid, raises exception if not.
    """
    if jwt is None:
        raise RuntimeError("PyJWT is not installed.")

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ==========================================
# FASTAPI DEPENDENCIES
# ==========================================

# Security scheme pour extraire le token du header Authorization
security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    """
    Dépendance qui extrait et vérifie le token JWT.
    Retourne l'utilisateur connecté.

    Usage:
        @router.get("/protected")
        def protected_route(current_user = Depends(get_current_user)):
            return {"user": current_user.email}
    """
    # Import ici pour éviter circular import
    from ..models.user import User

    token = credentials.credentials

    # Décoder le token
    payload = decode_token(token)

    # Extraire l'email du payload
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    # Récupérer l'utilisateur depuis la DB
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def require_admin(
        current_user=Depends(get_current_user)
):
    """
    Dépendance qui vérifie que l'utilisateur est admin.

    Usage:
        @router.get("/admin/stats")
        def admin_stats(_: dict = Depends(require_admin)):
            return {"stats": "..."}
    """
    from ..models.user import UserRole

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user

def require_parent(
        current_user=Depends(get_current_user)
):
    """
    Dépendance qui vérifie que l'utilisateur est parent.

    Usage:
        @router.post("/children/")
        def create_child(child_data: ChildCreate, parent = Depends(require_parent)):
            return create_child_for_parent(parent, child_data)
    """
    # Import ici pour éviter circular import
    from ..models.user import UserRole

    if current_user.role != UserRole.PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Parent access required",
        )

    return current_user