import hashlib
import hmac
import os
from datetime import datetime, timedelta, UTC
from typing import Optional

try:
    import jwt  # PyJWT
except ImportError:
    jwt = None  # if you don't have it yet, create_access_token will raise


SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def get_password_hash(password: str) -> str:
    """
    Very simple hash using sha256.
    For production, use bcrypt/argon2.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Securely compare a plain password with its hash."""
    return hmac.compare_digest(get_password_hash(plain_password), hashed_password)


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
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt