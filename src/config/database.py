from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config.parameters import settings

# Instancia global del engine (inicializada en lifespan)
_engine: AsyncEngine | None = None
_async_session_factory: async_sessionmaker[AsyncSession] | None = None


async def create_db_pool() -> None:
    """
    Inicializa la piscina de conexiones a la base de datos, se llama durante el inicio de la
    aplicación via el gestor de `lifespan`.
    """

    global _engine, _async_session_factory

    _engine = create_async_engine(
        str(settings.database_url),
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_pool_max_overflow,
        pool_pre_ping=True,  # Verifica conexiones antes de usarlas
        echo=settings.debug,  # Registra sentencias SQL en modo debug
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


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependencia para obtener una sesión de base de datos.

    ```python
    @app.get("/users/{user_id}")
    async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_db_session), # Aquí se inyecta la sesión
    ):
        ...
    ```

    Yields:
        AsyncSession: Sesión de base de datos que hace `commit` automático en caso de éxito y
        `rollback` en caso de excepción.
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
