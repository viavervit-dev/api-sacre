from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.users.models import Wholesaler
from src.api.modules.users.repositories.interfaces import IWholesalerRepository


class WholesalerRepository(IWholesalerRepository):
    """
    Repositorio SQLAlchemy para la gestión de perfiles de clientes mayorista `users.wholesaler`.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def create_wholesaler(self, user_id: UUID, data: dict[str, Any]) -> Wholesaler:

        instance = Wholesaler(user_id=user_id, **data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def update_wholesaler(self, instance: Wholesaler, data: dict[str, Any]) -> Wholesaler:

        for key, value in data.items():
            setattr(instance, key, value)

        await self.__db.flush()

        return instance

    async def exists_wholesaler(self, filters: dict[str, Any]) -> bool:

        stmt = select(Wholesaler.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
