from fastapi import APIRouter

# Importación de routers de categorías
from src.modules.inventory.routers.categories.create_category import create_category_router
from src.modules.inventory.routers.categories.delete_category import delete_category_router
from src.modules.inventory.routers.categories.get_category import get_categories_router
from src.modules.inventory.routers.categories.update_category import update_category_router
from src.modules.inventory.routers.products.add_product_wholesaler import (
    add_product_wholesaler_router,
)

# Importación de routers de productos
from src.modules.inventory.routers.products.create_product import create_product_router
from src.modules.inventory.routers.products.delete_product import delete_product_router
from src.modules.inventory.routers.products.get_list_products import get_list_products_router
from src.modules.inventory.routers.products.get_products_wholesaler import (
    get_products_wholesaler_router,
)
from src.modules.inventory.routers.products.update_product import update_product_router

# Router raíz del módulo Inventory
router = APIRouter()

# Categorías
router.include_router(router=create_category_router)
router.include_router(router=get_categories_router)
router.include_router(router=update_category_router)
router.include_router(router=delete_category_router)

# Productos
router.include_router(router=create_product_router)
router.include_router(router=get_list_products_router)
router.include_router(router=get_products_wholesaler_router)
router.include_router(router=update_product_router)
router.include_router(router=delete_product_router)
router.include_router(router=add_product_wholesaler_router)
