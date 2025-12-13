from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..dependencies import get_current_admin
from ..models.user import User
from ..schemas.solution_schema import SolutionCreate, SolutionOut, SolutionUpdate
from ..services.solution_service import (
    create_solution,
    delete_solution,
    get_solution,
    list_solutions,
    update_solution,
)

router = APIRouter(prefix="/admin/solutions", tags=["Solution Management"])

@router.get("/solutions", response_model=List[SolutionOut]) # J'ai supposé SolutionOut
def read_solutions(
    db: Session = Depends(get_db),
    # AJOUT DES PARAMÈTRES DE FILTRAGE :
    handicap_type: Optional[str] = Query(
        None, description="Filtrer par type de handicap (ex: motor, visual, auditory)"
    ),
    published: Optional[bool] = Query(
        None, description="Filtrer par statut de publication (true/false)"
    ),
    # Les paramètres de pagination sont toujours là :
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
):
    # Appel du service en transmettant TOUS les paramètres
    solutions = list_solutions(
        db,
        skip=skip,
        limit=limit,
        handicap_type=handicap_type, # <-- TRANSMISSION
        published=published          # <-- TRANSMISSION
    )
    return solutions

@router.post("/", response_model=SolutionOut, status_code=status.HTTP_201_CREATED)
def create(payload: SolutionCreate, db: Session = Depends(get_db),
           current_admin: User = Depends(get_current_admin)):
    return create_solution(db, payload)


#@router.get("/", response_model=list[SolutionOut])
#def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    return list_solutions(db, skip=skip, limit=limit)


@router.get("/{solution_id}", response_model=SolutionOut)
def get_one(solution_id: int, db: Session = Depends(get_db)):
    return get_solution(db, solution_id)


@router.put("/{solution_id}", response_model=SolutionOut)
def update(solution_id: int, payload: SolutionUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return update_solution(db, solution_id, payload)


@router.delete("/{solution_id}", status_code=status.HTTP_200_OK)
def remove(solution_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return delete_solution(db, solution_id)