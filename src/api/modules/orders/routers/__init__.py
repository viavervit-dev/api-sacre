from fastapi import APIRouter

from src.api.modules.orders.routers.calculations import (
    add_percentage_router,
    get_tax_amount_router,
    multiply_router,
    sum_router,
)
from src.api.modules.orders.routers.purchase import (
    create_purchase_order_wholesaler_router,
    get_list_purchase_orders_router,
    get_purchase_order_router,
)

router = APIRouter()
router.include_router(router=create_purchase_order_wholesaler_router)
router.include_router(router=get_list_purchase_orders_router)
router.include_router(router=get_purchase_order_router)
router.include_router(router=add_percentage_router)
router.include_router(router=get_tax_amount_router)
router.include_router(router=multiply_router)
router.include_router(router=sum_router)
