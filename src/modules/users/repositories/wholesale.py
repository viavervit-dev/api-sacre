from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.models.wholesale import Wholesale
from src.modules.users.repositories.interfaces import IWholesaleRepository


class WholesaleRepository(IWholesaleRepository):
    """
    Repositorio SQLAlchemy para la gestión de perfiles de mayorista `users.wholesale`.

    Implementa operaciones asíncronas para la creación y verificación de existencia
    de mayoristas registrados.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def create_wholesale(self, data: dict[str, Any]) -> Wholesale:

        instance = Wholesale(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def exists_wholesale(self, filters: dict[str, Any]) -> bool:

        stmt = select(Wholesale.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
