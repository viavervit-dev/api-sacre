from fastapi import APIRouter

from src.modules.users.routers.customers.create_customer import create_customer_router
from src.modules.users.routers.customers_wholesale.create_wholesale import create_wholesale_router

router = APIRouter()

router.include_router(router=create_customer_router)
router.include_router(router=create_wholesale_router)
