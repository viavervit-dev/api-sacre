from fastapi import APIRouter

from src.api.modules.users.routers.customers.create import create_customer_router
from src.api.modules.users.routers.wholesaler.create import create_wholesaler_router
from src.api.modules.users.routers.wholesaler.get import get_wholesaler_router
from src.api.modules.users.routers.wholesaler.get_list import get_list_wholesaler_router
from src.api.modules.users.routers.wholesaler.update import update_wholesaler_router

router = APIRouter()
router.include_router(router=create_customer_router)
router.include_router(router=create_wholesaler_router)
router.include_router(router=update_wholesaler_router)
router.include_router(router=get_list_wholesaler_router)
router.include_router(router=get_wholesaler_router)
