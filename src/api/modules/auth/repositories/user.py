from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.models.permission import Group
from src.api.modules.auth.models.user import User
from src.api.modules.auth.repositories.interfaces import IUserRepository


class UserRepository(IUserRepository):
    """Repositorio SQLAlchemy para la gestión de usuarios y autenticación en `auth.users`."""

    __profile_map = {
        UserRoles.CUSTOMER.value: User.customer,
        UserRoles.CUSTOMER_WHOLESALE.value: User.customer_wholesale,
        UserRoles.ADMINISTRATOR.value: User.admin,
    }

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_user(
        self,
        filters: dict[str, Any],
        load_permissions: bool = True,
    ) -> User | None:

        if not filters:
            raise ValueError("Se debe proporcionar al menos un filtro para buscar el usuario.")

        # Validar que los campos existan en el modelo User
        valid_columns = set(User.__table__.columns.keys())
        invalid_keys = set(filters.keys()) - valid_columns

        if invalid_keys:
            invalid_list = ", ".join(sorted(invalid_keys))
            valid_list = ", ".join(sorted(valid_columns))

            raise ValueError(
                f"Campos no válidos para User: {invalid_list}. Campos permitidos: {valid_list}."
            )

        stmt = select(User).filter_by(**filters)

        # Carga del perfil según el rol especificado en los filtros
        role = filters.get("role")

        if role:
            if role not in self.__profile_map:
                raise ValueError(
                    f"El rol '{role}' no tiene una relación definida o no existe. "
                    f"Roles válidos: {', '.join(sorted(self.__profile_map.keys()))}."
                )

            relation_field = self.__profile_map[role]
            stmt = stmt.options(joinedload(relation_field))

        # Carga inteligente de permisos
        if load_permissions:
            stmt = stmt.options(selectinload(User.groups).selectinload(Group.permissions))

        result = await self.__db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_list_users(
        self,
        offset: int,
        limit: int,
        filters: dict[str, Any],
        load_permissions: bool = True,
    ) -> tuple[Sequence[User], int]:

        if not filters:
            raise ValueError("Se debe proporcionar al menos un filtro para buscar el usuario.")

        # Validar que los campos existan en el modelo User
        valid_columns = set(User.__table__.columns.keys())
        invalid_keys = set(filters.keys()) - valid_columns

        if invalid_keys:
            invalid_list = ", ".join(sorted(invalid_keys))
            valid_list = ", ".join(sorted(valid_columns))

            raise ValueError(f"Campos no válidos: {invalid_list}. Permitidos: {valid_list}.")

        role = filters.get("role")

        if role and role not in self.__profile_map:
            raise ValueError(
                f"El rol '{role}' no tiene una relación definida o no existe. "
                f"Roles válidos: {', '.join(sorted(self.__profile_map.keys()))}."
            )

        # Total para metadatos de paginación
        count_stmt = select(func.count(User.id))
        count_stmt = count_stmt.filter_by(**filters)
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Paginación y ordenamiento
        stmt = select(User).order_by(User.date_joined.desc()).offset(offset).limit(limit)
        stmt = stmt.filter_by(**filters)

        if role:
            stmt = stmt.options(joinedload(self.__profile_map[role]))
        if load_permissions:
            stmt = stmt.options(selectinload(User.groups).selectinload(Group.permissions))

        result = await self.__db.scalars(stmt)
        items = result.unique().all()

        return items, total_items

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
