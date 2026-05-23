import asyncio
from typing import TypedDict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import close_db_pool, create_db_pool, get_db_session
from src.modules.admins.models.admin import Admin
from src.modules.auth.models.permission import Group, Permission, PermissionGroup
from src.modules.auth.models.user import User
from src.modules.customers.models.customer import Customer


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
            "authentication.jwt",
        ],
    },
    {
        "name": "admin",
        "permissions": [
            f"{User.__tablename__}.read",
            f"{Admin.__tablename__}.read",
            "authentication.jwt",
        ],
    },
]

PERMISSIONS = [
    # Permisos para el modelo User
    f"{User.__tablename__}.read",
    f"{User.__tablename__}.delete",
    f"{User.__tablename__}.update_password",
    # Permisos para el modelo Customer
    f"{Customer.__tablename__}.read",
    f"{Customer.__tablename__}.update",
    f"{Customer.__tablename__}.delete",
    # Permisos para el modelo Admin
    f"{Admin.__tablename__}.read",
    # Permisos generales
    "authentication.jwt",
]


async def run(session: AsyncSession) -> None:
    """
    Script de configuración de roles y permisos. Este script se encarga de:
    1. Crear los permisos definidos en la lista `PERMISSIONS` si no existen.
    2. Crear los grupos definidos en la lista `GROUPS` si no existen.
    3. Asociar los permisos correspondientes a cada grupo según lo definido en `GROUPS`.
    4. Eliminar permisos de grupos que ya no estén definidos en la lista `GROUPS`.
    """

    # 1. Crear todos los permisos definidos en PERMISSIONS en la base de datos
    for perm_name in PERMISSIONS:
        perm_result = await session.execute(select(Permission).filter_by(name=perm_name))
        permission = perm_result.scalar_one_or_none()

        if not permission:
            permission = Permission(name=perm_name)
            session.add(permission)
            await session.flush()

    # 2. Configurar los grupos y sus respectivos permisos definidos en GROUPS
    for group_data in GROUPS:
        role_name = group_data["name"]

        group_result = await session.execute(select(Group).filter_by(name=role_name))
        group = group_result.scalar_one_or_none()

        if not group:
            group = Group(name=role_name)
            session.add(group)
            await session.flush()

        expected_permission_ids = set()

        for perm_name in group_data["permissions"]:
            perm_result = await session.execute(select(Permission).filter_by(name=perm_name))
            permission = perm_result.scalar_one_or_none()

            # Validación de integridad: Si el permiso no existe, se lanza una excepción
            if not permission:
                raise ValueError(
                    f"Permiso '{perm_name}' definido en GROUPS pero no encontrado en PERMISSIONS."
                )

            expected_permission_ids.add(permission.id)

            # Asociar Permiso al Grupo mediante PermissionGroup
            pg_result = await session.execute(
                select(PermissionGroup).filter_by(group_id=group.id, permission_id=permission.id)
            )
            permission_group = pg_result.scalar_one_or_none()

            if not permission_group:
                permission_group = PermissionGroup(group_id=group.id, permission_id=permission.id)
                session.add(permission_group)
                await session.flush()

        # 3. Limpiar permisos antiguos que ya no corresponden al grupo
        pg_result = await session.execute(select(PermissionGroup).filter_by(group_id=group.id))
        current_permission_groups = pg_result.scalars().all()

        for pg in current_permission_groups:
            if pg.permission_id not in expected_permission_ids:
                await session.delete(pg)

        await session.flush()

    await session.commit()


async def main() -> None:

    # 1. Inicializar la conexión a la base de datos
    await create_db_pool()

    try:
        async for session in get_db_session():
            await run(session=session)
    except Exception as e:
        raise e
    finally:
        # 4. Cerrar la conexión de la base de datos
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())
