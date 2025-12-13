import json
from pathlib import Path

from sqlalchemy import select

from ..core.database import Base, SessionLocal, engine
from ..models.handicap import Handicap
from ..models.solution import Solution


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "solutions_seed.json"


def main() -> None:
    # 1) Crée les tables si pas déjà fait (simple en dev)
    Base.metadata.create_all(bind=engine)

    # 2) Charge le JSON
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    handicaps = payload.get("handicaps", [])
    solutions = payload.get("solutions", [])

    with SessionLocal() as db:
        # 3) Seed handicaps (upsert simple par name)
        for h in handicaps:
            name = h["name"].strip()
            description = h.get("description")

            existing = db.execute(select(Handicap).where(Handicap.name == name)).scalar_one_or_none()
            if existing:
                if description is not None:
                    existing.description = description
            else:
                db.add(Handicap(name=name, description=description))

        db.commit()

        # 4) Construire un mapping name -> id
        rows = db.execute(select(Handicap)).scalars().all()
        handicap_by_name = {r.name: r.id for r in rows}

        # 5) Seed solutions (upsert simple par title)
        created = 0
        updated = 0

        for s in solutions:
            title = s["title"].strip()
            handicap_type = s.get("handicap_type")
            handicap_id = handicap_by_name.get(handicap_type) if handicap_type else None

            existing = db.execute(select(Solution).where(Solution.title == title)).scalar_one_or_none()
            if existing:
                existing.category = s["category"]
                existing.handicap_id = handicap_id
                existing.age_min = s.get("age_min")
                existing.age_max = s.get("age_max")
                existing.content = s["content"]
                existing.source_url = s.get("source_url")
                existing.tags = s.get("tags")
                existing.published = bool(s.get("published", False))
                updated += 1
            else:
                db.add(
                    Solution(
                        title=title,
                        category=s["category"],
                        handicap_id=handicap_id,
                        age_min=s.get("age_min"),
                        age_max=s.get("age_max"),
                        content=s["content"],
                        source_url=s.get("source_url"),
                        tags=s.get("tags"),
                        published=bool(s.get("published", False)),
                    )
                )
                created += 1

        db.commit()

    print(f"Seed terminé. Handicaps: {len(handicaps)} | Solutions créées: {created} | Solutions mises à jour: {updated}")


if __name__ == "__main__":
    main()