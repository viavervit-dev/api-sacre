# ruff: noqa: F401

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

import src.config.models
from src.config.database import Base
from src.config.parameters import settings

config = context.config

# Sobreescribe la URL del .ini con la URL real proveniente de las variables de entorno.
# Esto evita hardcodear credenciales en alembic.ini, que sí se sube al repositorio.
config.set_main_option("sqlalchemy.url", str(settings.database_url))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de la Base declarativa. Alembic la compara contra el esquema real
# de la BD para determinar qué cambios generar con --autogenerate.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Ejecuta las migraciones en modo *offline* (sin conexión activa a la BD).

    En este modo Alembic genera el SQL de las migraciones como texto plano sin
    necesitar conectarse a la base de datos. Útil para revisar los cambios antes
    de aplicarlos o para entornos donde no hay acceso directo a la BD.
    """

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Configura el contexto de Alembic con una conexión activa y ejecuta las migraciones.

    Esta función es un adaptador que permite pasar una conexión síncrona al contexto
    de Alembic desde un entorno async. Es invocada por `run_async_migrations` a través
    de `connection.run_sync()`, que ejecuta código síncrono dentro del event loop async.
    """

    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Crea un engine async y ejecuta las migraciones en modo *online*.

    Usa `NullPool` en lugar del pool estándar porque Alembic abre y cierra la
    conexión inmediatamente al terminar. Un pool persistente sería innecesario y
    podría dejar conexiones abiertas.
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Punto de entrada para ejecutar migraciones en modo *online* (conexión activa).

    Envuelve la corutina `run_async_migrations` con `asyncio.run()` para ejecutarla
    desde un contexto síncrono, que es como Alembic invoca este archivo.
    """

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
