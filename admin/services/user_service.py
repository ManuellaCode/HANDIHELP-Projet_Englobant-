from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.user import User, UserRole  # ← direct import from user.py


def list_users(db: Session, skip: int = 0, limit: int = 100):
    """Lister tous les utilisateurs (non-admins)"""
    return db.query(User).filter(
        User.role.in_([UserRole.DONOR, UserRole.PARENT])
    ).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    """Récupérer un utilisateur par ID"""
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def delete_user(db: Session, user_id: int):
    """Supprimer un utilisateur"""
    user = get_user_by_id(db, user_id)

    # Empêcher suppression d'un admin
    if user.role == UserRole.ADMIN:  
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete admin users",
        )

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}