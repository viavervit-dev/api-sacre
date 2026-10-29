from fastapi import APIRouter

from src.api.modules.payments.routers.links.create import create_payment_link_router

router = APIRouter()
router.include_router(router=create_payment_link_router)
