from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.handicap import Handicap
from ..models.solution import Solution
from ..repository.solution_repository import SolutionRepository
from ..schemas.solution_schema import SolutionCreate, SolutionUpdate


def _handicap_id_from_type(db: Session, handicap_type: str | None) -> int | None:
    if handicap_type is None:
        return None
    row = db.query(Handicap).filter_by(name=handicap_type).first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown handicap_type: {handicap_type}",
        )
    return row.id


def _fill_handicap_type(solution: Solution) -> None:
    # pour que SolutionOut puisse exposer handicap_type facilement
    if getattr(solution, "handicap", None) is not None:
        setattr(solution, "handicap_type", solution.handicap.name)
    else:
        setattr(solution, "handicap_type", None)


def create_solution(db: Session, payload: SolutionCreate) -> Solution:
    repo = SolutionRepository(db)

    handicap_id = _handicap_id_from_type(db, payload.handicap_type.value if payload.handicap_type else None)

    solution = Solution(
        title=payload.title,
        category=payload.category,
        handicap_id=handicap_id,
        age_min=payload.age_min,
        age_max=payload.age_max,
        content=payload.content,
        source_url=str(payload.source_url) if payload.source_url else None,
        tags=payload.tags,
        published=payload.published,
    )
    created = repo.create(solution)
    _fill_handicap_type(created)
    return created


def list_solutions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        handicap_type: Optional[str] = None,  # <-- NOUVEAU PARAMÈTRE
        published: Optional[bool] = None,  # <-- NOUVEAU PARAMÈTRE
) -> list[Solution]:
    repo = SolutionRepository(db)

    # On passe les filtres au Repository
    items = repo.list_latest(
        skip=skip,
        limit=limit,
        handicap_type=handicap_type,  # <-- TRANSMISSION
        published=published  # <-- TRANSMISSION
    )

    for s in items:
        _fill_handicap_type(s)
    return items

def get_solution(db: Session, solution_id: int) -> Solution:
    repo = SolutionRepository(db)
    solution = repo.get(solution_id)
    if not solution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solution not found")
    _fill_handicap_type(solution)
    return solution


def update_solution(db: Session, solution_id: int, payload: SolutionUpdate) -> Solution:
    repo = SolutionRepository(db)
    solution = get_solution(db, solution_id)

    if payload.handicap_type is not None:
        solution.handicap_id = _handicap_id_from_type(db, payload.handicap_type.value)

    for field in ("title", "category", "age_min", "age_max", "content", "tags", "published"):
        value = getattr(payload, field)
        if value is not None:
            setattr(solution, field, value)

    if payload.source_url is not None:
        solution.source_url = str(payload.source_url)

    db.commit()
    db.refresh(solution)
    _fill_handicap_type(solution)
    return solution


def delete_solution(db: Session, solution_id: int) -> dict:
    repo = SolutionRepository(db)
    solution = get_solution(db, solution_id)
    repo.delete(solution)
    return {"message": "Solution deleted successfully"}