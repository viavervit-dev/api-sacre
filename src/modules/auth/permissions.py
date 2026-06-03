from typing import Annotated, Any, TypedDict

from fastapi import Depends

from src.common.exceptions import PermissionDenied
from src.modules.admins.models.admin import Admin
from src.modules.auth.jwt import get_user
from src.modules.auth.models.user import User
from src.modules.customers.models.customer import Customer
from src.modules.products.models.category import Category
from src.modules.products.models.product import Product


class RoleGroupConfig(TypedDict):
    """
    Estructura de configuración para un grupo de roles. Define el nombre del grupo y los
    permisos asociados a ese grupo.
    """

    name: str
    permissions: list[str]


GROUPS: list[RoleGroupConfig] = [
    {
        "name": "customer",
        "permissions": [
            f"{User.__tablename__}.read",
            f"{User.__tablename__}.update_password",
            f"{User.__tablename__}.delete",  # Si tiene el permiso, puede elimina los datos del rol
            f"{Customer.__tablename__}.read",
            f"{Customer.__tablename__}.update",
            f"{Category.__tablename__}.read",
            f"{Product.__tablename__}.read",
            "authentication.jwt",
        ],
    },
    {
        "name": "admin",
        "permissions": [
            f"{User.__tablename__}.read",
            f"{Admin.__tablename__}.read",
            f"{Category.__tablename__}.read",
            f"{Category.__tablename__}.create",
            f"{Category.__tablename__}.update",
            f"{Category.__tablename__}.delete",
            f"{Product.__tablename__}.read",
            f"{Product.__tablename__}.create",
            f"{Product.__tablename__}.update",
            f"{Product.__tablename__}.delete",
            "authentication.jwt",
        ],
    },
]


PERMISSIONS = [
    # Permisos para los modelos del módulo auth
    f"{User.__tablename__}.read",
    f"{User.__tablename__}.delete",
    f"{User.__tablename__}.update_password",
    # Permisos para los modelos del módulo customers
    f"{Customer.__tablename__}.read",
    f"{Customer.__tablename__}.update",
    f"{Customer.__tablename__}.delete",
    # Permisos para los modelos del módulo admins
    f"{Admin.__tablename__}.read",
    # Permisos para los modelos del módulo productos
    f"{Category.__tablename__}.read",
    f"{Category.__tablename__}.create",
    f"{Category.__tablename__}.update",
    f"{Category.__tablename__}.delete",
    f"{Product.__tablename__}.read",
    f"{Product.__tablename__}.create",
    f"{Product.__tablename__}.update",
    f"{Product.__tablename__}.delete",
    # Permisos generales
    "authentication.jwt",
]


class UserPermissionChecker:
    """Verifica si el usuario autenticado posee los permisos requeridos."""

    def __init__(self, allowed_role: str, permission: str) -> None:
        self.__allowed_role = allowed_role
        self.__permission = permission

    async def __call__(
        self, user: Annotated[tuple[User, Any], Depends(get_user)]
    ) -> tuple[User, Any]:
        """Extrae el usuario autenticado y verifica su rol."""

        user_account, user_profile = user

        # Verificamos si el rol del usuario es el permitido
        if user_account.role != self.__allowed_role:
            raise PermissionDenied()

        # Verificamos si el usuario tiene el permiso específico requerido
        if not user_account.has_permission(permission_name=self.__permission):
            raise PermissionDenied()

        return user_account, user_profile
