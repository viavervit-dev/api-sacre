from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.modules.auth.constants import UserRoles
from src.modules.auth.models.permission import Group
from src.modules.auth.models.user import User
from src.modules.auth.repositories.interfaces import IUserRepository


class UserRepository(IUserRepository):
    """
    Repositorio SQLAlchemy para la gestión de usuarios y autenticación en `auth.users`.

    Implementa operaciones asíncronas para la consulta con carga dinámica de perfiles,
    registro de credenciales, verificación y control de sesiones.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_user(
        self,
        role: str,
        id: UUID | None = None,
        email: str | None = None,
        load_permissions: bool = True,
    ) -> User | None:

        profile_map = {
            UserRoles.CUSTOMER.value: User.customer,
            UserRoles.ADMINISTRATOR.value: User.admin,
        }

        if role not in profile_map:
            raise ValueError(f"El rol '{role}' no tiene una relación definida o no existe.")

        relation_field = profile_map[role]

        # Consulta por ID con joinedload de la relación según el rol
        filters = []
        if id is not None:
            filters.append(User.id == id)
        if email is not None:
            filters.append(User.email == email)

        if not filters:
            raise ValueError(
                "Se debe proporcionar al menos 'id' o 'email' para buscar el usuario."
            )

        stmt = select(User).where(*filters).options(joinedload(relation_field))

        # Carga inteligente de permisos
        if load_permissions:
            stmt = stmt.options(selectinload(User.groups).selectinload(Group.permissions))

        result = await self.__db.execute(stmt)
        instance = result.scalar_one_or_none()

        return instance

    async def create_user(
        self,
        email: str,
        password: str,
        role: str,
    ) -> User:

        # Cargar el grupo y sus permisos
        stmt_group = (
            select(Group).where(Group.name == role).options(selectinload(Group.permissions))
        )
        result_group = await self.__db.execute(stmt_group)
        role_group = result_group.scalar_one_or_none()

        if not role_group:
            raise ValueError(f"El rol/grupo '{role}' no existe en la base de datos.")

        # Crear usuario y encriptar contraseña
        instance = User(email=email, role=role, session_version=1)
        instance.set_password(password)
        instance.groups.append(role_group)

        # Guardar en base de datos
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def exists_user(self, filters: dict[str, Any]) -> bool:

        stmt = select(User.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)

    async def increment_session_versions(self, user_ids: Sequence[UUID]) -> None:

        stmt = (
            update(User)
            .where(User.id.in_(user_ids))
            .values(session_version=User.session_version + 1)
        )

        await self.__db.execute(stmt)
        await self.__db.commit()
