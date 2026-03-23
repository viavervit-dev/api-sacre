from collections.abc import AsyncGenerator

from sqlalchemy import text
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

    pass


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
    is_sqlite = db_url.startswith("sqlite")

    if is_sqlite:
        # SQLite no soporta pool_size ni max_overflow
        _engine = create_async_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=settings.debug,
        )
    else:
        _engine = create_async_engine(
            db_url,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_pool_max_overflow,
            pool_pre_ping=True,
            echo=settings.debug,
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

    global _engine

    if _engine is not None:
        await _engine.dispose()
        _engine = None


async def check_db_connection() -> bool:
    """Verifica que la base de datos esté disponible ejecutando una consulta simple."""

    if _engine is None:
        return False

    try:
        async with _engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        return True
    except Exception:
        return False


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependencia para obtener una sesión de base de datos.

    ### Ejemplo de uso:
    ```python
    @app.get("/users/{user_id}")
    async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_db_session), # Aquí se inyecta la sesión
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
