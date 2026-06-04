import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import close_db_pool, create_db_pool, get_db_session
from src.modules.auth.models.permission import Group, Permission, PermissionGroup
from src.modules.auth.permissions import GROUPS, PERMISSIONS


async def run(db: AsyncSession) -> None:
    """
    Script de configuración de roles y permisos. Este script se encarga de:
    1. Crear los permisos definidos en la lista `PERMISSIONS` si no existen.
    2. Crear los grupos definidos en la lista `GROUPS` si no existen.
    3. Asociar los permisos correspondientes a cada grupo según lo definido en `GROUPS`.
    4. Eliminar permisos de grupos que ya no estén definidos en la lista `GROUPS`.
    """

    # 1. Crear todos los permisos definidos en PERMISSIONS en la base de datos
    for perm_name in PERMISSIONS:
        perm_result = await db.execute(select(Permission).filter_by(name=perm_name))
        permission = perm_result.scalar_one_or_none()

        if not permission:
            permission = Permission(name=perm_name)
            db.add(permission)
            await db.flush()

    # 2. Configurar los grupos y sus respectivos permisos definidos en GROUPS
    for group_data in GROUPS:
        role_name = group_data["name"]

        group_result = await db.execute(select(Group).filter_by(name=role_name))
        group = group_result.scalar_one_or_none()

        if not group:
            group = Group(name=role_name)
            db.add(group)
            await db.flush()

        expected_permission_ids = set()

        for perm_name in group_data["permissions"]:
            perm_result = await db.execute(select(Permission).filter_by(name=perm_name))
            permission = perm_result.scalar_one_or_none()

            # Validación de integridad: Si el permiso no existe, se lanza una excepción
            if not permission:
                raise ValueError(
                    f"Permiso '{perm_name}' definido en GROUPS pero no encontrado en PERMISSIONS."
                )

            expected_permission_ids.add(permission.id)

            # Asociar Permiso al Grupo mediante PermissionGroup
            # fmt: off
            pg_result = await db.execute(
                select(PermissionGroup)
                .filter_by(group_id=group.id, permission_id=permission.id)
            )
            # fmt: on
            permission_group = pg_result.scalar_one_or_none()

            if not permission_group:
                permission_group = PermissionGroup(group_id=group.id, permission_id=permission.id)
                db.add(permission_group)
                await db.flush()

        # 3. Limpiar permisos antiguos que ya no corresponden al grupo
        pg_result = await db.execute(select(PermissionGroup).filter_by(group_id=group.id))
        current_permission_groups = pg_result.scalars().all()

        for pg in current_permission_groups:
            if pg.permission_id not in expected_permission_ids:
                await db.delete(pg)

        await db.flush()

    await db.commit()


async def main() -> None:

    # 1. Inicializar la conexión a la base de datos
    await create_db_pool()

    try:
        async for db in get_db_session():
            await run(db=db)
    except Exception as e:
        raise e
    finally:
        # 4. Cerrar la conexión de la base de datos
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())
