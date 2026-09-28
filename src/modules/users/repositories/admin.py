from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.models.admin import Admin
from src.modules.users.repositories.interfaces import IAdminRepository


class AdminRepository(IAdminRepository):
    """
    Repositorio SQLAlchemy para la gestión de perfiles de administradores en `admin.admins`.

    Implementa operaciones asíncronas para la creación y verificación de existencia
    de administradores vinculados a una cuenta de usuario.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def create_admin(self, user_id: UUID, data: dict[str, Any]) -> Admin:

        instance = Admin(user_id=user_id, **data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def exists_admin(self, filters: dict[str, Any]) -> bool:

        stmt = select(Admin.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
