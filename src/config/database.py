import asyncio
from collections.abc import AsyncGenerator

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.config.parameters import settings


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM del proyecto."""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


# Instancia global del engine (inicializada en lifespan)
_engine: AsyncEngine | None = None
_async_session_factory: async_sessionmaker[AsyncSession] | None = None


async def create_db_pool() -> None:
    """
    Inicializa la piscina de conexiones a la base de datos, se llama durante el inicio de la
    aplicación via el gestor de `lifespan`.
    """

    global _engine, _async_session_factory
    db_url = str(settings.database_url)

    # Argumentos específicos para el driver asyncpg
    connect_args = {
        # Timeout para cualquier comando SQL individual
        "command_timeout": settings.db_command_timeout,
        "server_settings": {
            # Timeout a nivel de Postgres para matar queries colgadas tras 10 segundos
            "statement_timeout": settings.db_statement_timeout,
            # Desactiva JIT para reducir latencia en transacciones cortas OLTP
            "jit": settings.db_jit,
        },
    }

    _engine = create_async_engine(
        url=db_url,
        max_overflow=settings.db_pool_max_overflow,
        pool_timeout=settings.db_pool_timeout,
        pool_recycle=settings.db_pool_recycle,
        pool_size=settings.db_pool_size,
        connect_args=connect_args,
        echo=settings.db_echo,
        pool_pre_ping=True,
    )
    _async_session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


async def close_db_pool() -> None:
    """
    Cierra todas las conexiones a la base de datos de forma segura. Se llama durante el cierre de
    la aplicación via el gestor de `lifespan`.
    """

    global _engine, _async_session_factory

    if _engine is not None:
        await _engine.dispose()
        _async_session_factory = None
        _engine = None


async def check_db_connection() -> bool:
    """Verifica que la base de datos esté disponible ejecutando una consulta simple."""

    if _engine is None:
        return False

    try:
        # Timeout estricto de 2 segundos para no colgar las sondas de Kubernetes / Balanceador
        async with asyncio.timeout(2.0), _engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        return True
    except Exception:
        return False


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """
    Dependencia para obtener una sesión de base de datos.

    ### Ejemplo de uso:
    ```python
    @app.get("/users/{user_id}")
    async def get_user(
        user_id: int,
        session: Annotated[AsyncSession, Depends(get_db_session)], # Aquí se inyecta la sesión
    ):
        ...
    ```
    """

    if _async_session_factory is None:
        raise RuntimeError("Base de datos no inicializada. Llama a create_db_pool() primero.")

    async with _async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
