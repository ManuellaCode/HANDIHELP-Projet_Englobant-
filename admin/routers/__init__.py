from fastapi import APIRouter

from .admin_routes import router as admin_routes_router
from .assistance_router import router as assistance_router
from .child_router import router as child_router
from .donation_router import router as donation_router
from .solutions import router as solutions_router
from .users_router import router as users_router

admin_api_router = APIRouter()
admin_api_router.include_router(admin_routes_router)
admin_api_router.include_router(users_router)
admin_api_router.include_router(donation_router)
admin_api_router.include_router(assistance_router)
admin_api_router.include_router(child_router)
admin_api_router.include_router(solutions_router)