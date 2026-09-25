from fastapi import APIRouter

from src.modules.customers.routers.create import create_customer_router

router = APIRouter()

router.include_router(router=create_customer_router)
