from fastapi import APIRouter

from src.api.modules.inventory.routers.categories import (
    create_category_router,
    delete_category_router,
    get_list_categories_router,
    update_category_router,
)
from src.api.modules.inventory.routers.products import (
    create_product_router,
    delete_product_router,
    get_list_products_router,
    get_product_router,
    update_product_router,
)
from src.api.modules.inventory.routers.products.wholesaler import (
    add_product_wholesaler_router,
    get_list_products_wholesaler_router,
    get_products_wholesaler_router,
    update_product_wholesaler_router,
)

router = APIRouter()
router.include_router(router=create_category_router)
router.include_router(router=get_list_categories_router)
router.include_router(router=update_category_router)
router.include_router(router=delete_category_router)
router.include_router(router=create_product_router)
router.include_router(router=get_list_products_router)
router.include_router(router=get_product_router)
router.include_router(router=get_products_wholesaler_router)
router.include_router(router=get_list_products_wholesaler_router)
router.include_router(router=update_product_router)
router.include_router(router=delete_product_router)
router.include_router(router=add_product_wholesaler_router)
router.include_router(router=update_product_wholesaler_router)
