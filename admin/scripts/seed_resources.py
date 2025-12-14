"""
Script pour importer des ressources depuis un fichier JSON.
Usage: python -m admin.scripts.seed_resources
"""
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..core.database import SessionLocal
from ..models.handicap import Handicap
from ..models.resource import Resource

# Chemin du fichier JSON
JSON_PATH = Path(__file__).resolve().parents[1] / "data" / "resources_seed.json"


def validate_json_structure(json_path: Path) -> tuple[bool, list]:
    """
    Valider que le JSON a la structure attendue.

    Returns:
        (is_valid, data)
    """
    required_fields = {'name', 'resource_type'}

    try:
        with json_path.open(encoding="utf-8") as f:
            data = json.load(f)

        # Vérifier que c'est une liste
        if not isinstance(data, list):
            print(f"❌ Le JSON doit être une liste d'objets")
            return False, []

        if len(data) == 0:
            print(f"⚠️ Le JSON est vide")
            return False, []

        # Vérifier la structure du premier élément
        first_item = data[0]
        fields = set(first_item.keys())

        print(f"\n📋 Champs trouvés : {fields}")

        missing = required_fields - fields
        if missing:
            print(f"❌ Champs manquants : {missing}")
            return False, []

        print(f"✅ Structure JSON valide ({len(data)} ressources)")
        return True, data

    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {json_path}")
        return False, []
    except json.JSONDecodeError as e:
        print(f"❌ JSON invalide : {e}")
        return False, []
    except Exception as e:
        print(f"❌ Erreur validation : {e}")
        return False, []


def main():
    """
    Fonction principale d'import des ressources depuis JSON.
    """
    print("=" * 70)
    print("🚀 IMPORT DES RESSOURCES (JSON)")
    print("=" * 70)
    print(f"📂 Fichier : {JSON_PATH}")

    # 1. Vérifier que le fichier existe
    if not JSON_PATH.exists():
        print(f"\n❌ ERREUR : Le fichier {JSON_PATH} n'existe pas !")
        print(f"\n💡 Créez le fichier avec cette structure :")
        print("""
[
  {
    "name": "APF France Handicap",
    "resource_type": "association",
    "description": "Association d'aide aux personnes handicapées",
    "handicap_type": "Mobilité réduite",
    "region": "Île-de-France",
    "city": "Paris",
    "phone": "0140786900",
    "email": "contact@apf.fr",
    "website": "https://www.apf-francehandicap.org"
  },
  {
    "name": "Unapei",
    "resource_type": "association",
    "description": "Union nationale des associations de parents",
    "handicap_type": "Handicap intellectuel",
    "region": "Île-de-France",
    "city": "Paris",
    "phone": "0144854350",
    "email": "contact@unapei.org",
    "website": "https://www.unapei.org"
  }
]
        """)
        return

    # 2. Valider et charger les données JSON
    is_valid, resources_data = validate_json_structure(JSON_PATH)
    if not is_valid:
        print("\n❌ Le JSON n'a pas la structure attendue. Arrêt.")
        return

    # 3. Traitement avec gestion d'erreur robuste
    inserted_count = 0
    skipped_count = 0
    error_count = 0

    try:
        with SessionLocal() as db:
            print(f"\n🔗 Connexion à la base de données...")

            # 4. Récupérer le mapping des handicaps
            print(f"📚 Chargement des types de handicap...")
            handicaps = {h.name: h.id for h in db.execute(select(Handicap)).scalars()}

            if handicaps:
                print(f"✅ {len(handicaps)} types de handicap : {list(handicaps.keys())}")
            else:
                print(f"⚠️ Aucun type de handicap en base.")

            # 5. Traiter chaque ressource
            print(f"\n📥 Traitement des ressources...\n")

            for i, item in enumerate(resources_data, start=1):
                try:
                    # Récupérer le nom (requis)
                    name = item.get("name", "").strip()
                    if not name:
                        print(f"⚠️ Ressource {i} : Nom vide, ignoré")
                        skipped_count += 1
                        continue

                    # Debug : Afficher la première ressource
                    if i == 1:
                        print(f"🔍 Première ressource (debug) :")
                        print(f"  {json.dumps(item, indent=2, ensure_ascii=False)}\n")

                    # Récupérer resource_type (requis)
                    resource_type = item.get("resource_type", "").strip()
                    if not resource_type:
                        print(f"⚠️ Ressource {i} ({name}) : Type manquant, ignoré")
                        skipped_count += 1
                        continue

                    # Gérer le handicap_id (optionnel)
                    handicap_type = item.get("handicap_type", "").strip()
                    handicap_id = None

                    if handicap_type:
                        handicap_id = handicaps.get(handicap_type)
                        if handicap_id is None:
                            print(f"⚠️ Ressource {i} ({name}) : Handicap '{handicap_type}' non trouvé")

                    # Vérifier doublon
                    existing = db.query(Resource).filter(
                        Resource.name == name
                    ).first()

                    if existing:
                        print(f"⏭️ Ressource {i} : '{name}' existe déjà, ignoré")
                        skipped_count += 1
                        continue

                    # Créer la ressource
                    resource = Resource(
                        name=name,
                        resource_type=resource_type,
                        description=item.get("description", "").strip() or None,
                        handicap_id=handicap_id,
                        region=item.get("region", "").strip() or None,
                        city=item.get("city", "").strip() or None,
                        phone=item.get("phone", "").strip() or None,
                        email=item.get("email", "").strip() or None,
                        website=item.get("website", "").strip() or None,
                        validated=True,
                    )

                    db.add(resource)
                    inserted_count += 1

                    # Afficher progression
                    if inserted_count % 10 == 0:
                        print(f"✅ {inserted_count} ressources ajoutées...")

                except KeyError as e:
                    error_count += 1
                    resource_name = item.get('name', 'INCONNU')
                    print(f"❌ Ressource {i} ({resource_name}) : Champ manquant {e}")
                    continue

                except Exception as e:
                    error_count += 1
                    resource_name = item.get('name', 'INCONNU')
                    print(f"❌ Ressource {i} ({resource_name}) : {type(e).__name__}: {e}")
                    continue

            # 6. Commit final
            if inserted_count > 0:
                print(f"\n💾 Enregistrement en base de données...")
                try:
                    db.commit()
                    print(f"✅ Commit réussi !")

                except IntegrityError as e:
                    db.rollback()
                    print(f"❌ ERREUR COMMIT : Violation contrainte")
                    print(f"Détails : {e}")
                    inserted_count = 0

                except Exception as e:
                    db.rollback()
                    print(f"❌ ERREUR COMMIT : {type(e).__name__}: {e}")
                    inserted_count = 0
            else:
                print(f"\n⚠️ Aucune ressource à insérer")

    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return

    # 7. Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DE L'IMPORT")
    print("=" * 70)
    print(f"✅ Ressources importées : {inserted_count}")
    print(f"⏭️ Ressources ignorées : {skipped_count}")
    print(f"❌ Erreurs : {error_count}")
    print(f"📈 Total traité : {inserted_count + skipped_count + error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()