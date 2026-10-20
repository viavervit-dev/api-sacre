from fastapi import APIRouter

# Importación de routers de clientes
from src.api.modules.users.routers.customers.create import create_customer_router

# Importación de routers de clientes mayoristas
from src.api.modules.users.routers.customers_wholesale.create import (
    create_customer_wholesale_router,
)
from src.api.modules.users.routers.customers_wholesale.get_list import get_list_customers_wholesale
from src.api.modules.users.routers.customers_wholesale.update import (
    update_customer_wholesale_router,
)

router = APIRouter()

# Clientes
router.include_router(router=create_customer_router)

# Clientes mayoristas
router.include_router(router=create_customer_wholesale_router)
router.include_router(router=update_customer_wholesale_router)
router.include_router(router=get_list_customers_wholesale)
