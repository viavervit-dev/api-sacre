import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import close_db_pool, create_db_pool, get_db_session
from src.modules.admins.models.admin import Admin
from src.modules.auth.constants import UserRoles
from src.modules.auth.models.permission import Group
from src.modules.auth.models.user import User, UserGroup

# Carga las variables de entorno
load_dotenv()


async def run(
    db: AsyncSession,
    email: str,
    password: str,
    first_names: str,
    last_names: str,
) -> None:
    """Crea un usuario administrador en la base de datos."""

    # Verificar si el usuario ya existe
    result = await db.execute(select(User).filter_by(email=email))
    user = result.scalar_one_or_none()

    if user:
        print(f"Error: Ya existe un usuario con el correo electrónico '{email}'.")
        return

    # Verificar si el grupo de permisos del administrador existe
    result = await db.execute(select(Group).filter_by(name=UserRoles.ADMINISTRATOR.value))
    permission_group = result.scalar_one_or_none()

    if not permission_group:
        print(f"Error: El grupo '{UserRoles.ADMINISTRATOR.value}' no existe.")
        return

    # Crear el Usuario
    user_account = User(
        role=UserRoles.ADMINISTRATOR.value,
        session_version=1,
        email=email,
    )
    user_account.set_password(password=password)
    db.add(user_account)

    await db.flush()

    # Asignar el Usuario al grupo de permisos del administrador
    admin_group = UserGroup(
        user_id=user_account.id,
        group_id=permission_group.id,
    )
    db.add(admin_group)

    # 5. Crear el perfil del Administrador
    user_profile = Admin(
        user_id=user_account.id,
        first_names=first_names,
        last_names=last_names,
    )
    db.add(user_profile)

    await db.commit()

    print("Administrador creado exitosamente")


async def main() -> None:
    await create_db_pool()

    try:
        async for db in get_db_session():
            await run(
                db=db,
                email=str(os.getenv(key="ADMIN_EMAIL")),
                password=str(os.getenv(key="ADMIN_PASSWORD")),
                first_names=str(os.getenv(key="ADMIN_FIRST_NAMES")),
                last_names=str(os.getenv(key="ADMIN_LAST_NAMES")),
            )
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())
