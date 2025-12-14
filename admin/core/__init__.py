from .database import Base, engine

# ⚠️ IMPORTER TOUS LES MODÈLES ICI
from ..models.user import User
from ..models.handicap import Handicap
from ..models.resource import Resource
from ..models.solution import Solution
from ..models.don import Donation
from ..models.AssistanceRequest import AssistanceRequest
from ..models.child import Child

def init_db():
    print("⏳ Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
