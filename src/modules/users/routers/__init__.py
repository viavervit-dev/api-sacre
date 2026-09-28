from fastapi import APIRouter

from src.modules.users.routers.create_customer import create_customer_router

router = APIRouter()

router.include_router(router=create_customer_router)
