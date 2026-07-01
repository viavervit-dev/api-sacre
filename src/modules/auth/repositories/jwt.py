from typing import Any

from sqlalchemy import exists, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.models.jwt import JWTBlacklist
from src.modules.auth.repositories.interfaces import IJWTBlacklistRepository


class JWTBlacklistRepository(IJWTBlacklistRepository):
    """
    Repositorio para la lista negra de tokens JWT. Esta clase proporciona métodos que realizan
    operaciones en la tabla `auth.json_web_token_blacklist` de la base de datos.
    """

    @classmethod
    async def add_to_list(cls, db: AsyncSession, data: dict[str, Any]) -> None:

        stmt = insert(JWTBlacklist).values(**data)

        await db.execute(stmt)
        await db.commit()

    @classmethod
    async def exists_token(cls, db: AsyncSession, jti: str) -> bool:

        stmt = select(exists().where(JWTBlacklist.jti == jti))
        result = await db.scalar(stmt)

        return bool(result)
