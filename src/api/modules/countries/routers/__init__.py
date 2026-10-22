from fastapi import APIRouter

from src.api.modules.countries.routers.get_countries import countries_router
from src.api.modules.countries.routers.get_organization_country import organization_country_router

router = APIRouter()
router.include_router(router=organization_country_router)
router.include_router(router=countries_router)
