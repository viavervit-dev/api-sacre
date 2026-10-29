from typing import TypedDict

from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.models.user import User
from src.api.modules.inventory.models.category import Category
from src.api.modules.inventory.models.product import Product
from src.api.modules.orders.models.shopping_order import ShoppingOrder
from src.api.modules.payments.models.payment import Payment
from src.api.modules.users.models.admin import Admin
from src.api.modules.users.models.customer import Customer
from src.api.modules.users.models.customer_wholesale import CustomerWholesale


class RoleGroupConfig(TypedDict):
    """
    Estructura de configuración para un grupo de roles. Define el nombre del grupo y los
    permisos asociados a ese grupo.
    """

    name: str
    permissions: list[str]


GROUPS: list[RoleGroupConfig] = [
    {
        "name": UserRoles.CUSTOMER.value,
        "permissions": [
            f"{User.__tablename__}.update_password",
            f"{User.__tablename__}.delete",
            f"{Customer.__tablename__}.read",
            f"{Customer.__tablename__}.update",
            f"{Customer.__tablename__}.delete",
            f"{Category.__tablename__}.read.public",
            f"{Product.__tablename__}.read.public",
            "authentication.jwt",
        ],
    },
    {
        "name": UserRoles.CUSTOMER_WHOLESALE.value,
        "permissions": [
            f"{Product.__tablename__}.read.public",
            f"{ShoppingOrder.__tablename__}.read",
            "authentication.jwt",
        ],
    },
    {
        "name": UserRoles.ADMINISTRATOR.value,
        "permissions": [
            f"{Admin.__tablename__}.read",
            f"{Category.__tablename__}.read.private",
            f"{Category.__tablename__}.create",
            f"{Category.__tablename__}.update",
            f"{Category.__tablename__}.delete",
            f"{Product.__tablename__}.read.private",
            f"{Product.__tablename__}.create",
            f"{Product.__tablename__}.update",
            f"{Product.__tablename__}.delete",
            f"{CustomerWholesale.__tablename__}.create",
            f"{CustomerWholesale.__tablename__}.read",
            f"{CustomerWholesale.__tablename__}.update",
            f"{CustomerWholesale.__tablename__}.delete",
            f"{ShoppingOrder.__tablename__}.read",
            f"{ShoppingOrder.__tablename__}.create",
            f"{Payment.__tablename__}.read",
            f"{Payment.__tablename__}.create",
            "authentication.jwt",
        ],
    },
]


PERMISSIONS = [
    # Permisos para los modelos del módulo auth
    f"{User.__tablename__}.update_password",
    f"{User.__tablename__}.delete",
    # Permisos para los modelos del módulo users
    f"{Customer.__tablename__}.read",
    f"{Customer.__tablename__}.update",
    f"{Customer.__tablename__}.delete",
    f"{Admin.__tablename__}.read",
    f"{CustomerWholesale.__tablename__}.create",
    f"{CustomerWholesale.__tablename__}.read",
    f"{CustomerWholesale.__tablename__}.update",
    f"{CustomerWholesale.__tablename__}.delete",
    # Permisos para los modelos del módulo inventory
    f"{Category.__tablename__}.read.public",
    f"{Category.__tablename__}.read.private",
    f"{Category.__tablename__}.create",
    f"{Category.__tablename__}.update",
    f"{Category.__tablename__}.delete",
    f"{Product.__tablename__}.read.public",
    f"{Product.__tablename__}.read.private",
    f"{Product.__tablename__}.create",
    f"{Product.__tablename__}.update",
    f"{Product.__tablename__}.delete",
    # Permisos para los modelos del módulo orders
    f"{ShoppingOrder.__tablename__}.read",
    f"{ShoppingOrder.__tablename__}.create",
    # Permisos para los modelos del módulo orders
    f"{Payment.__tablename__}.read",
    f"{Payment.__tablename__}.create",
    # Permisos generales
    "authentication.jwt",
]
