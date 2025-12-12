from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.child import Child
from ..repository.child_repository import ChildRepository
from ..repository.user_repository import UserRepository
from ..schemas.child_schema import ChildCreate


def create_child(db: Session, payload: ChildCreate) -> Child:
    # Vérifie que le parent existe
    user_repo = UserRepository(db)
    parent = user_repo.get(payload.parent_id)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent user not found",
        )

    repo = ChildRepository(db)
    child = Child(
        name=payload.name,
        age=payload.age,
        handicap_id=payload.handicap_id,
        parent_id=payload.parent_id,
    )
    return repo.create(child)


def list_children(db: Session, skip: int = 0, limit: int = 100) -> list[Child]:
    repo = ChildRepository(db)
    return repo.list_latest(skip=skip, limit=limit)


def get_child_by_id(db: Session, child_id: int) -> Child:
    repo = ChildRepository(db)
    child = repo.get(child_id)
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found",
        )
    return child


def delete_child(db: Session, child_id: int) -> dict:
    repo = ChildRepository(db)
    child = get_child_by_id(db, child_id)
    repo.delete(child)
    return {"message": "Child deleted successfully"}