from fastapi import APIRouter

from src.modules.countries.routers.get_countries import countries_router
from src.modules.countries.routers.get_organization_country import organization_country_router

# Router raíz del módulo Countries
router = APIRouter()
router.include_router(router=organization_country_router)
router.include_router(router=countries_router)
