from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from ..models.user import User, UserRole  
from ..schemas.admin_schemas import AdminCreate
from ..core.security import get_password_hash, verify_password


def create_admin(db: Session, admin: AdminCreate) -> User:
    """Créer un nouvel admin"""
    # Vérifier si l'email existe déjà
    existing_user = db.query(User).filter_by(email=admin.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Créer l'admin
    hashed_password = get_password_hash(admin.password)
    db_admin = User(
        email=admin.email,
        hashed_password=hashed_password,
        first_name=admin.first_name,
        last_name=admin.last_name,
        role=UserRole.ADMIN,
    )

    try:
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        return db_admin
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating admin",
        )


from typing import cast

def authenticate_admin(db: Session, email: str, password: str) -> User:
    """Authentifier un admin"""
    user = db.query(User).filter_by(email=email).first()

    if not user or user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or not an admin",
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return cast(User, user)


def list_admins(db: Session, skip: int = 0, limit: int = 100):
    """Lister tous les admins"""
    return (
        db.query(User)
        .filter_by(role=UserRole.ADMIN)
        .offset(skip)
        .limit(limit)
        .all()
    )
