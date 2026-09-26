from fastapi import APIRouter

# Importación de routers de JWT
from src.modules.auth.routers.jwt.authenticate_admin import jwt_admin_router
from src.modules.auth.routers.jwt.get_current_user import jwt_me_router
from src.modules.auth.routers.jwt.logout import jwt_logout_router
from src.modules.auth.routers.jwt.refresh import jwt_refresh_router

router = APIRouter()

router.include_router(router=jwt_admin_router)
router.include_router(router=jwt_me_router)
router.include_router(router=jwt_logout_router)
router.include_router(router=jwt_refresh_router)
