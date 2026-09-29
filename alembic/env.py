# ruff: noqa: F401

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool, text
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


def get_all_model_schemas() -> set[str]:
    """Extrae dinámicamente todos los esquemas únicos definidos en los modelos."""

    return {table.schema for table in target_metadata.tables.values() if table.schema is not None}


def include_name(name: str | None, type_: str, parent_names: dict) -> bool:
    """
    Filtra los objetos para que Alembic no compare ni intente alterar
    esquemas internos propios de PostgreSQL (como pg_catalog, pg_toast, etc.).
    """

    if type_ == "schema":
        if name is None:
            return True

        # Ignorar esquemas internos de PostgreSQL
        if name.startswith("pg_") or name == "information_schema":
            return False

    return True


def cleanup_empty_schemas(connection: Connection) -> None:
    """Elimina automáticamente esquemas de la app que hayan quedado sin tablas ni objetos."""

    query = text("""
        SELECT n.nspname AS schema_name
        FROM pg_catalog.pg_namespace n
        WHERE n.nspname NOT LIKE 'pg_%'
            AND n.nspname NOT IN ('information_schema', 'public')
            AND NOT EXISTS (
                SELECT 1 FROM pg_catalog.pg_class c
                WHERE c.relnamespace = n.oid
            );
    """)

    empty_schemas = [row[0] for row in connection.execute(query).fetchall()]

    for schema in empty_schemas:
        connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" RESTRICT;'))


def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo **offline**."""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )

    with context.begin_transaction():
        for schema in get_all_model_schemas():
            context.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")

        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo **online**."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Aseguramos la existencia previa de los esquemas de los modelos
        for schema in get_all_model_schemas():
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

        connection.commit()

        # Configuramos el contexto con el filtro de esquemas del sistema
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
        )

        with context.begin_transaction():
            context.run_migrations()

        # Eliminamos esquemas que hayan quedado vacíos
        cleanup_empty_schemas(connection=connection)
        connection.commit()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
