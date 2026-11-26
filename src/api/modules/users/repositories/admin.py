from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.users.models import Admin
from src.api.modules.users.repositories.interfaces import IAdminRepository
from src.api.settings.database import DBSessionDep


class AdminRepository(IAdminRepository):
    """Repositorio SQLAlchemy para la gestión de perfiles de administradores en `users.admins`."""

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


def admin_repository(db: DBSessionDep) -> AdminRepository:
    """
    Dependencia que provee el repositorio para gestionar la información de administradores
    en las base de datos.
    """

    return AdminRepository(db=db)


AdminRepositoryDep = Annotated[AdminRepository, Depends(admin_repository)]
