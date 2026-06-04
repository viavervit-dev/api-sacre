from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.modules.admins.models.admin import Admin
from src.modules.auth.constants import UserRoles
from src.modules.auth.models.permission import Group, PermissionGroup
from src.modules.auth.models.user import User, UserGroup
from src.modules.auth.repositories.interfaces import IUserRepository
from src.modules.customers.models.customer import Customer


class UserRepository(IUserRepository):
    """
    Repositorio para usuarios. Esta clase proporciona métodos que realizan operaciones en la tabla
    `auth.users` de la base de datos, resuelve dinámicamente las consultas y relaciones dependiendo
    del rol del usuario.
    """

    @classmethod
    async def get_user(
        cls,
        db: AsyncSession,
        filters: dict[str, Any],
        role: str,
    ) -> tuple[User, Any]:

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

        result = await db.execute(query)
        user_account = result.scalar_one()
        user_profile: Customer | Admin

        # Valida que el usuario tenga la relación correspondiente a su rol y construye el DTO
        if role == UserRoles.CUSTOMER.value:
            if user_account and not user_account.customer:
                raise ValueError(
                    f"El usuario '{user_account.id}' no existe en la tabla de su rol."
                )

            user_profile = user_account.customer

            return user_account, user_profile
        if role == UserRoles.ADMINISTRATOR.value:
            if user_account and not user_account.admin:
                raise ValueError(
                    f"El usuario '{user_account.id}' no existe en la tabla de su rol."
                )

            user_profile = user_account.admin

            return user_account, user_profile

        raise ValueError(f"El rol '{role}' no tiene una relación definida o no existe.")

    @classmethod
    async def create_user(
        cls,
        db: AsyncSession,
        user_data: dict[str, Any],
        profile_data: dict[str, Any],
        role: str,
    ) -> tuple[User, Any]:

        # Obtenemos el grupo correspondiente al rol para asignarlo al usuario
        result = await db.execute(select(Group).filter_by(name=role))
        role_instance = result.scalar_one_or_none()

        if not role_instance:
            raise ValueError(f"El rol '{role}' no existe en la base de datos.")

        # Determinamos el modelo relacionado según el rol
        RelatedModel: type[Customer] | type[Admin]

        if role == UserRoles.CUSTOMER.value:
            RelatedModel = Customer
        elif role == UserRoles.ADMINISTRATOR.value:
            RelatedModel = Admin
        else:
            raise ValueError(f"El rol '{role}' no tiene una relación definida o no existe.")

        # Creamos la instancia principal
        user_data["role"] = role
        password = user_data.pop("password")
        user_instance = User(**user_data)
        user_instance.set_password(password)

        # Creamos la instancia del perfil
        profile_instance = RelatedModel(user_id=user_instance.id, **profile_data)

        # Enlazamos las entidades según el rol
        if role == UserRoles.CUSTOMER.value:
            user_instance.customer = cast(Customer, profile_instance)
        elif role == UserRoles.ADMINISTRATOR.value:
            user_instance.admin = cast(Admin, profile_instance)

        db.add(user_instance)
        await db.flush()

        # Asignar el rol al nuevo usuario
        user_group = UserGroup(user_id=user_instance.id, group_id=role_instance.id)
        db.add(user_group)
        await db.flush()

        return user_instance, profile_instance

    @classmethod
    async def exists_user(cls, db: AsyncSession, filters: dict[str, Any], role: str) -> bool:

        query = select(User.id)

        # Determinar el modelo relacionado según el rol para construir la consulta con JOIN
        RelatedModel: type[Customer] | type[Admin] | None = None

        if role == UserRoles.CUSTOMER.value:
            RelatedModel = Customer
            query = query.join(User.customer)
        elif role == UserRoles.ADMINISTRATOR.value:
            RelatedModel = Admin
            query = query.join(User.admin)
        else:
            raise ValueError(f"El rol '{role}' no tiene una relación definida o no existe.")

        # Clasificar los filtros asumiendo prioridad al modelo User para campos comunes
        user_filters = []
        relation_filters = []

        for field, value in filters.items():
            if hasattr(User, field):
                user_filters.append(getattr(User, field) == value)
            elif hasattr(RelatedModel, field):
                relation_filters.append(getattr(RelatedModel, field) == value)
            else:
                raise ValueError(
                    f"La columna '{field}' no existe en User ni en {RelatedModel.__name__}."
                )

        # Agregar los filtros a la consulta
        if user_filters:
            query = query.where(*user_filters)
        if relation_filters:
            query = query.where(*relation_filters)

        exists_query = select(query.exists())
        result = await db.execute(exists_query)

        return result.scalar_one()
