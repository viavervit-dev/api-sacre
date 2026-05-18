from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.modules.authentication.constants import UserRoles
from src.modules.authentication.models.permission import Group, PermissionGroup
from src.modules.authentication.models.user import User
from src.modules.authentication.repositories.interfaces import IUserRepository


class UserRepository(IUserRepository):
    """
    Repositorio para usuarios. Esta clase proporciona métodos que realizan operaciones en la tabla
    `auth.users` de la base de datos, resuelve dinámicamente las consultas y relaciones dependiendo
    del rol del usuario.
    """

    @classmethod
    async def get_user(
        cls,
        session: AsyncSession,
        filters: dict[str, Any],
        role: str,
    ) -> tuple[User | None, Any]:

        # Construye la consulta base desempaquetando el diccionario de filtros
        query = select(User).filter_by(**filters)

        # Cargar proactivamente grupos
        query = query.options(
            selectinload(User.groups)
            .selectinload(Group.permission_groups)
            .selectinload(PermissionGroup.permission)
        )

        if role == UserRoles.CUSTOMER.value:
            query = query.options(selectinload(User.customer))
        elif role == UserRoles.ADMINISTRATOR.value:
            query = query.options(selectinload(User.admin))
        else:
            raise ValueError(f"El rol '{role}' no tiene una relación definida o no existe.")

        result = await session.execute(query)
        user_account = result.scalar_one_or_none()
        user_profile = None

        # Valida que el usuario tenga la relación correspondiente a su rol y construye el DTO
        if role == UserRoles.CUSTOMER.value:
            if user_account and not user_account.customer:
                raise ValueError(
                    f"El usuario '{user_account.id}' no existe en la tabla de su rol."
                )
            if user_account:
                user_profile = user_account.customer

            return user_account, user_profile
        if role == UserRoles.ADMINISTRATOR.value:
            if user_account and not user_account.admin:
                raise ValueError(
                    f"El usuario '{user_account.id}' no existe en la tabla de su rol."
                )
            if user_account:
                user_profile = user_account.admin

            return user_account, user_profile

        return user_account, user_profile
