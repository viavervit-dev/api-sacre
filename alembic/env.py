# ruff: noqa: F401

import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path
from typing import Any

# Permite a Python encontrar módulos hermanos dentro de la carpeta alembic/
sys.path.insert(0, str(Path(__file__).resolve().parent))

import schemas  # noqa: E402
import sequences  # noqa: E402
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine, pool, text
from sqlalchemy.engine import Connection

import src.api.settings.models
from src.api.settings.database import ModelBase
from src.api.settings.parameters import api_parameters

config = context.config


if (
    config.config_file_name is not None
    and config.config_file_name.endswith(".ini")
    and os.path.exists(path=config.config_file_name)
):
    fileConfig(fname=config.config_file_name)

# Metadata de la Base declarativa. Alembic la compara contra el esquema real
# de la BD para determinar qué cambios generar con --autogenerate.
target_metadata = ModelBase.metadata


def include_name(name: str | None, type_: Any, parent_names: Any) -> bool:
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


def get_database_url() -> str:
    """Obtiene la URL de la base de datos para Alembic."""

    alembic_database_url = api_parameters.alembic_database_url

    if not alembic_database_url:
        raise ValueError(
            "La URL de la base de datos para Alembic no está configurada. "
            "Asegúrate de establecer 'ALEMBIC_DATABASE_URL' en el archivo "
            ".env o en las variables de entorno."
        )

    return alembic_database_url


def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo `offline`."""

    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo `online`."""

    connectable = create_engine(
        url=get_database_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Configuramos el contexto con el filtro de esquemas del sistema
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
