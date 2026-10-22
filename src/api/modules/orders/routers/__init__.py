from fastapi import APIRouter

from src.api.modules.orders.routers.calculations.add_percentage import add_percentage_router
from src.api.modules.orders.routers.calculations.get_tax_amount import get_tax_amount_router
from src.api.modules.orders.routers.calculations.sum import sum_router
from src.api.modules.orders.routers.create import create_order_customer_wholesale_router

router = APIRouter()
router.include_router(router=create_order_customer_wholesale_router)
router.include_router(router=add_percentage_router)
router.include_router(router=get_tax_amount_router)
router.include_router(router=sum_router)
