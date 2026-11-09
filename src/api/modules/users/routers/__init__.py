from fastapi import APIRouter

from src.api.modules.users.routers.customers import create_customer_router
from src.api.modules.users.routers.wholesaler import (
    create_wholesaler_router,
    get_list_wholesaler_router,
    get_wholesaler_router,
    update_wholesaler_router,
)

router = APIRouter()
router.include_router(router=create_customer_router)
router.include_router(router=create_wholesaler_router)
router.include_router(router=update_wholesaler_router)
router.include_router(router=get_list_wholesaler_router)
router.include_router(router=get_wholesaler_router)
