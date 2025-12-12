from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.child_schema import ChildCreate, ChildOut
from ..services.child_service import create_child, delete_child, get_child_by_id, list_children

router = APIRouter(prefix="/admin/children", tags=["Child Management"])


@router.post("/", response_model=ChildOut, status_code=status.HTTP_201_CREATED)
def create(payload: ChildCreate, db: Session = Depends(get_db)):
    return create_child(db, payload)


@router.get("/", response_model=list[ChildOut])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_children(db, skip=skip, limit=limit)


@router.get("/{child_id}", response_model=ChildOut)
def get_one(child_id: int, db: Session = Depends(get_db)):
    return get_child_by_id(db, child_id)


@router.delete("/{child_id}", status_code=status.HTTP_200_OK)
def remove(child_id: int, db: Session = Depends(get_db)):
    return delete_child(db, child_id)