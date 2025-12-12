from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.user_schema import UserOut
from ..services.user_service import list_users, get_user_by_id, delete_user

router = APIRouter(prefix="/admin/users", tags=["User Management"])


@router.get("/", response_model=list[UserOut])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lister tous les utilisateurs"""
    return list_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par ID"""
    return get_user_by_id(db, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    """Supprimer un utilisateur"""
    return delete_user(db, user_id)