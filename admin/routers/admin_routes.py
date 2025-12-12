from datetime import timedelta

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import create_access_token
from ..core.config import settings
from ..schemas.admin_schemas import AdminCreate, AdminOut, AdminLogin, Token
from ..services.admin_service import create_admin, authenticate_admin, list_admins

router = APIRouter(prefix="/admin", tags=["Admin Management"])


@router.post("/register", response_model=AdminOut, status_code=status.HTTP_201_CREATED)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """Créer un nouvel admin (super_admin only en prod)"""
    return create_admin(db, admin)


@router.post("/login", response_model=Token)
def login_admin(credentials: AdminLogin, db: Session = Depends(get_db)):
    """Connexion admin"""
    user = authenticate_admin(db, str(credentials.email), credentials.password)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/list", response_model=list[AdminOut])
def get_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lister tous les admins"""
    return list_admins(db, skip, limit)
