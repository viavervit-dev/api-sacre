from fastapi import APIRouter

from src.api.modules.auth.routers.jwt import (
    jwt_admin_router,
    jwt_logout_router,
    jwt_me_router,
    jwt_refresh_router,
)

router = APIRouter()
router.include_router(router=jwt_admin_router)
router.include_router(router=jwt_me_router)
router.include_router(router=jwt_logout_router)
router.include_router(router=jwt_refresh_router)
