from typing import Optional  # 1. AJOUTER L'IMPORT POUR LES TYPES OPTIONNELS
from sqlalchemy.orm import Session, joinedload

from ..models.solution import Solution
from ..models.handicap import Handicap  # 2. AJOUTER L'IMPORT DU MODÈLE HANDICAP
from .base import BaseRepository


class SolutionRepository(BaseRepository[Solution]):
    def __init__(self, db: Session):
        super().__init__(db, Solution)

    def list_latest(
            self,
            skip: int = 0,
            limit: int = 100,
            handicap_type: Optional[str] = None,  # 3. NOUVEAU PARAMÈTRE DE FILTRE
            published: Optional[bool] = None,  # 3. NOUVEAU PARAMÈTRE DE FILTRE
    ) -> list[Solution]:

        # Début de la construction de la requête avec l'Eager Loading
        query = self.db.query(Solution).options(joinedload(Solution.handicap))

        # Application du filtre "published"
        if published is not None:
            query = query.filter(Solution.published == published)

        # Application du filtre "handicap_type"
        if handicap_type:
            # On utilise .join() pour lier la table Solution à la table Handicap
            # puis on filtre sur le champ 'name' du modèle Handicap.
            query = query.join(Handicap).filter(Handicap.name == handicap_type)

        # Finalisation : Application de l'ordre et de la pagination
        return (
            query
            .order_by(Solution.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )