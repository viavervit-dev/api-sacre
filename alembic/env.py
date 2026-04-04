# ruff: noqa: F401

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection

import src.config.models
from src.config.database import Base
from src.config.parameters import settings

load_dotenv()
config = context.config

# Sobreescribe la URL del .ini con la URL real proveniente de las variables de entorno.
# Esto evita hardcodear credenciales en alembic.ini, que sí se sube al repositorio.
alembic_url = (
    os.getenv("ALEMBIC_DATABASE_URL")  # Usá esta si está definida
    or os.getenv("DATABASE_URL", "").replace(
        "+asyncpg", "+psycopg2"
    )  # Sino, transformá la async en sync
)
config.set_main_option("sqlalchemy.url", alembic_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de la Base declarativa. Alembic la compara contra el esquema real
# de la BD para determinar qué cambios generar con --autogenerate.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo **offline**."""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo **online**."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
