from typing import TypedDict

from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.models import User
from src.api.modules.inventory.models import Category, Product, WholesalerProduct
from src.api.modules.orders.models import Order
from src.api.modules.users.models import Admin, Customer, Wholesaler


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
            f"{Category.__tablename__}.read",
            f"{Product.__tablename__}.read",
            "authentication.jwt",
        ],
    },
    {
        "name": UserRoles.WHOLESALER.value,
        "permissions": [
            f"{WholesalerProduct.__tablename__}.read",
            f"{Order.__tablename__}.read",
            "authentication.jwt",
        ],
    },
    {
        "name": UserRoles.ADMINISTRATOR.value,
        "permissions": [
            f"{Admin.__tablename__}.read",
            f"{Category.__tablename__}.read",
            f"{Category.__tablename__}.create",
            f"{Category.__tablename__}.update",
            f"{Category.__tablename__}.delete",
            f"{Product.__tablename__}.read",
            f"{Product.__tablename__}.create",
            f"{Product.__tablename__}.update",
            f"{Product.__tablename__}.delete",
            f"{WholesalerProduct.__tablename__}.read",
            f"{WholesalerProduct.__tablename__}.create",
            f"{WholesalerProduct.__tablename__}.update",
            f"{WholesalerProduct.__tablename__}.delete",
            f"{Wholesaler.__tablename__}.create",
            f"{Wholesaler.__tablename__}.read",
            f"{Wholesaler.__tablename__}.update",
            f"{Wholesaler.__tablename__}.delete",
            f"{Order.__tablename__}.read",
            f"{Order.__tablename__}.create",
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
    f"{Wholesaler.__tablename__}.create",
    f"{Wholesaler.__tablename__}.read",
    f"{Wholesaler.__tablename__}.update",
    f"{Wholesaler.__tablename__}.delete",
    # Permisos para los modelos del módulo inventory
    f"{Category.__tablename__}.read",
    f"{Category.__tablename__}.create",
    f"{Category.__tablename__}.update",
    f"{Category.__tablename__}.delete",
    f"{Product.__tablename__}.read",
    f"{Product.__tablename__}.create",
    f"{Product.__tablename__}.update",
    f"{Product.__tablename__}.delete",
    f"{WholesalerProduct.__tablename__}.read",
    f"{WholesalerProduct.__tablename__}.create",
    f"{WholesalerProduct.__tablename__}.update",
    f"{WholesalerProduct.__tablename__}.delete",
    # Permisos para los modelos del módulo orders
    f"{Order.__tablename__}.read",
    f"{Order.__tablename__}.create",
    # Permisos generales
    "authentication.jwt",
]
