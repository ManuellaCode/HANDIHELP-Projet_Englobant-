# admin/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from sqlalchemy.orm import Session
from .core.config import settings
from .core.database import get_db  # Nous avons besoin de la session DB
from .models.user import User  # Pour récupérer l'utilisateur et vérifier le rôle

# --- 1. Définir le schéma de sécurité OAuth2 ---
# Indique à FastAPI d'extraire le jeton de l'en-tête "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # Ajustez /login si nécessaire


# --- 2. Dépendance pour l'Admin ---
def get_current_admin(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 3. Décodage du Token (Utilise la fonction de PyJWT)
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            # On suppose que l'ID de l'utilisateur est stocké sous la clé "sub"
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # 4. Vérification dans la base de données (BONNE PRATIQUE)
    # Récupérer l'utilisateur à partir de la BDD pour vérifier son rôle actuel
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    # 5. Vérification du Rôle Admin
    if user.role != "admin":  # Assurez-vous que le rôle dans la BDD est bien "admin"
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation forbidden: Admin role required"
        )

    return user