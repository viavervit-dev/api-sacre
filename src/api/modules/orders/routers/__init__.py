from fastapi import APIRouter

from src.api.modules.orders.routers.create import create_order_customer_wholesale_router

router = APIRouter()
router.include_router(router=create_order_customer_wholesale_router)
